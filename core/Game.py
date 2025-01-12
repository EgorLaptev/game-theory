import nashpy as nash
import numpy as np
import pandas as pd
import itertools as it


class Game:
    def __init__(self, player1, player2, strategies):
        self.player1 = player1
        self.player2 = player2
        self.strategies = strategies
        self.payoff_matrix = self.generate_payoff_matrix()

        self.p1_matrix = [[payoff[0] for payoff in row] for row in self.payoff_matrix]
        self.p2_matrix = [[payoff[1] for payoff in row] for row in self.payoff_matrix]

        # nash game engine
        self.game = nash.Game(self.p1_matrix, self.p2_matrix)

    def generate_payoff_matrix(self):
        """
        Создаёт матрицу выплат на основе стратегий и затрат игроков.
        """
        matrix = []
        for p1_choice in self.strategies:
            row = []
            for p2_choice in self.strategies:
                p1_split = p1_choice.split('/')
                p2_split = p2_choice.split('/')
                payoffs = self.calculate_payoff(p1_split, p2_split)
                row.append(payoffs)
            matrix.append(row)
        return matrix

    def calculate_payoff(self, p1_choices, p2_choices):
        """
        Рассчитывает выплаты для каждого игрока.
        """
        p1_payoff = self.player1.calculate_payoff(p1_choices)
        p2_payoff = self.player2.calculate_payoff(p2_choices)

        # Adjust payoffs for overlapping choices
        for choice in set(p1_choices) & set(p2_choices):
            if self.player1.costs[choice] > self.player2.costs[choice]:
                p2_payoff -= self.player2.costs[choice]
            else:
                p1_payoff -= self.player1.costs[choice]

        return p1_payoff, p2_payoff

    def max_payoff(self):
        pairs = it.combinations(self.player1.costs.items(), 2)
        max_pair = max(pairs, key=lambda pair: pair[0][1] + pair[1][1])
        return max_pair[0][1] + max_pair[1][1]

    def get_all_outcomes(self):
        return list(it.chain(*self.payoff_matrix))

    def display_payoff_matrix(self):
        """
        Печатает матрицу выплат в виде DataFrame.
        """
        df = pd.DataFrame(
            [[payoff for payoff in row] for row in self.payoff_matrix],
            index=self.strategies,
            columns=self.strategies,
        )
        print("Матрица выплат:")
        print(df)

    def find_nash_equilibrium(self):
        nash_equilibrium = list(self.game.support_enumeration())
        nash_payoffs = []
        for p1, p2 in nash_equilibrium:
            x = np.argmax(p1)
            y = np.argmax(p2)
            nash_payoffs.append(self.payoff_matrix[x][y])

        return nash_payoffs

    def find_pareto_optimal(self):
        """
        Находит парето-оптимальные исходы.
        """
        outcomes = [
            ((i, j), payoff)
            for i, row in enumerate(self.payoff_matrix)
            for j, payoff in enumerate(row)
        ]

        pareto_optimal = []

        for ((i1, j1), (p1_payoff1, p2_payoff1)) in outcomes:
            dominated = False
            for ((i2, j2), (p1_payoff2, p2_payoff2)) in outcomes:
                if (
                    p1_payoff2 >= p1_payoff1
                    and p2_payoff2 >= p2_payoff1
                    and (p1_payoff2 > p1_payoff1 or p2_payoff2 > p2_payoff1)
                ):
                    dominated = True
                    break
            if not dominated:
                # pareto_optimal.append(((self.strategies[i1], self.strategies[j1]), (p1_payoff1, p2_payoff1)))
                pareto_optimal.append((p1_payoff1, p2_payoff1))
        return pareto_optimal
