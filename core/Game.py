import nashpy as nash
import numpy as np
import pandas as pd
import itertools as it
from utils.plotter import game_plot
import warnings

warnings.filterwarnings("ignore")


class Game:
    strategies = ["T1/T2", "T1/T3", "T2/T3"]

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.payoff_matrix = self.generate_payoff_matrix()

        self.p1_matrix = [[payoff[0] for payoff in row] for row in self.payoff_matrix]
        self.p2_matrix = [[payoff[1] for payoff in row] for row in self.payoff_matrix]

        # nash game engine
        self.game = nash.Game(self.p1_matrix, self.p2_matrix)

    def iter(self):
        pass

    def display(self):
        nash_equilibrium = self.find_nash_equilibrium()
        pareto_optimal = self.find_pareto_optimal()
        all_outcomes = self.get_all_outcomes()
        max_payoff = self.max_payoff()

        self.display_payoff_matrix()

        print("nash: ", nash_equilibrium)
        print("pareto: ", pareto_optimal)

        game_plot(
            all_outcomes,
            pareto_optimal,
            nash_equilibrium,
            max_payoff
        )

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
                # if p1_choice == p2_choice:
                #     row.append((0, 0))
                # else:
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
                # p1_payoff -= self.player1.costs[choice]
            else:
                # p2_payoff -= self.player2.costs[choice]
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

    def find_index(self, arr, target):
        arr = list(arr)

        try:
            return arr.index(target)  # Ищем индекс числа
        except ValueError:
            return -1  # Если числа нет в массиве, возвращаем -1

    def find_nash_equilibrium(self):
        nash_equilibrium = list(self.game.support_enumeration())
        nash_payoffs = []
        for p1, p2 in nash_equilibrium:
            x = self.find_index(p1, 1)
            y = self.find_index(p2, 1)

            if x < 0 or y < 0:
                continue

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
