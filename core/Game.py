import nashpy as nash
import numpy as np
import pandas as pd
import itertools as it
from utils.plotter import game_plot
import warnings
from dataclasses import dataclass
from typing import List
from . import Player

warnings.filterwarnings("ignore")

@dataclass
class NashResult:
    payoff: tuple
    strategy_p1: str
    strategy_p2: str

class Game:
    strategies = ["T1/T2", "T1/T3", "T2/T3"]

    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2

    def play(self, steps: int = 1):
        print(f"Playing {steps} steps")
        for _ in range(steps):
            res = self.iter()

        return res

    def iter(self):
        self.payoff_matrix = self.generate_payoff_matrix()

        self.p1_matrix = [[payoff[0] for payoff in row] for row in self.payoff_matrix]
        self.p2_matrix = [[payoff[1] for payoff in row] for row in self.payoff_matrix]

        nash_equilibrium = self.find_nash_equilibrium()
        pareto_optimal = self.find_pareto_optimal()
        all_outcomes = self.get_all_outcomes()
        max_payoff = self.max_payoff()

        # self.display_payoff_matrix()

        # print("nash: ", nash_equilibrium)
        # print("pareto: ", pareto_optimal)

        preferred_nash = self.decide_nash(nash_equilibrium)

        # print(f"Preferred nash: {preferred_nash}")

        self.distribute_costs(preferred_nash)
        self.player1.result += preferred_nash.payoff[0]
        self.player2.result += preferred_nash.payoff[1]

        # print("Player1 costs:")
        # print(self.player1.costs)
        # print("Player2 costs:")
        # print(self.player2.costs)

        # print(f"Player1 payoff: {self.player1.result}")
        # print(f"Player2 payoff: {self.player2.result}")
        
        return self.player1.result, self.player2.result

    def decide_nash(self, nash_results: list):
        pass
        return nash_results[0]

    def display(self):
        nash_equilibrium = self.find_nash_equilibrium()
        pareto_optimal = self.find_pareto_optimal()
        all_outcomes = self.get_all_outcomes()
        max_payoff = self.max_payoff()

        self.display_payoff_matrix()

        print("nash: ", nash_equilibrium)
        print("pareto: ", pareto_optimal)

        # game_plot(
        #     all_outcomes,
        #     pareto_optimal,
        #     nash_equilibrium,
        #     max_payoff
        # )

    def check_debate(self, debate_slot: str):
        if self.player1.costs[debate_slot] > self.player2.costs[debate_slot]:
            return (-1, 1)
        return (1, -1)

    def distribute_costs(self, nash_res: NashResult):
        slots_p1 = nash_res.strategy_p1.split("/")
        slots_p2 = nash_res.strategy_p2.split("/")

        if slots_p1[0] in slots_p2 and slots_p1[1] not in slots_p2:
            debate_strategy = slots_p1[0]
            change = self.check_debate(debate_strategy)
            self.player1.costs[debate_strategy] += change[0]
            self.player2.costs[debate_strategy] += change[1]

            self.player1.costs[slots_p1[1]] -= 1
            self.player2.costs[list(set(slots_p2)-set([debate_strategy]))[0]] -= 1

        elif slots_p1[1] in slots_p2 and slots_p1[0] not in slots_p2:
            debate_strategy = slots_p1[1]
            change = self.check_debate(debate_strategy)
            self.player1.costs[debate_strategy] += change[0]
            self.player2.costs[debate_strategy] += change[1]

            self.player1.costs[slots_p1[0]] -= 1
            self.player2.costs[list(set(slots_p2)-set([debate_strategy]))[0]] -= 1
        elif slots_p1[0] in slots_p2 and slots_p1[1] in slots_p2:
            debate_strategy_1 = slots_p1[0]
            change = self.check_debate(debate_strategy_1)
            self.player1.costs[debate_strategy_1] += change[0]
            self.player2.costs[debate_strategy_1] += change[1]

            debate_strategy_2 = slots_p1[1]
            change = self.check_debate(debate_strategy_2)
            self.player1.costs[debate_strategy_2] += change[0]
            self.player2.costs[debate_strategy_2] += change[1]
        else:
            print("КАК ТЫ ТАКУЮ СИТУАЦИЮ ПОЛУЧИЛ ЭТО ЖЕ, *****, НЕВОЗМОЖНО???")

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
        # nash game engine
        game = nash.Game(self.p1_matrix, self.p2_matrix)

        nash_equilibrium = list(game.support_enumeration())
        nash_payoffs = []
        for p1, p2 in nash_equilibrium:
            x = self.find_index(p1, 1)
            y = self.find_index(p2, 1)

            if x < 0 or y < 0:
                continue

            nash_payoffs.append(
                NashResult(
                    payoff=self.payoff_matrix[x][y],
                    strategy_p1=self.strategies[x],
                    strategy_p2=self.strategies[y]
                )
            )

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
