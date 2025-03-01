import warnings
import random
import numpy as np
import pandas as pd
import nashpy as nash
import itertools as it
from typing import List
from dataclasses import dataclass
from . import Player
from utils.GamePlotter import GamePlotter

warnings.filterwarnings("ignore")


@dataclass
class NashResult:
    payoff: tuple
    strategy_p1: str
    strategy_p2: str


class Game:
    strategies = ["T1/T2", "T1/T3", "T2/T3"]

    def __init__(self, player1: Player, player2: Player):
        self.p2_matrix = None
        self.p1_matrix = None
        self.payoff_matrix = None
        self.player1 = player1
        self.player2 = player2
        self.history = []

    def play(self, steps: int = 1, plot=True):
        for _ in range(steps):
            self.iter(plot=False)

        if plot:
            GamePlotter.plot_game_result(self.history)

        return self.history[-1]

    def iter(self, plot=False):
        self.payoff_matrix = self.generate_payoff_matrix()

        self.p1_matrix = [[payoff[0] for payoff in row] for row in self.payoff_matrix]
        self.p2_matrix = [[payoff[1] for payoff in row] for row in self.payoff_matrix]

        nash_equilibrium = self.find_nash_equilibrium()
        preferred_nash = self.decide_nash(nash_equilibrium)

        self.distribute_costs(preferred_nash)
        self.player1.result += preferred_nash.payoff[0]
        self.player2.result += preferred_nash.payoff[1]

        result = self.player1.result, self.player2.result

        self.history.append(result)

        if plot:
            self.display(nash_equilibrium)

        return result

    def decide_nash(self, nash_results: List[NashResult]):
        """ Selects a Nash equilibrium from the list of possible results. """
        return max(nash_results, key=lambda nash: sum(nash.payoff))

    def display(self, nash_equilibrium):
        pareto_optimal = self.find_pareto_optimal()
        all_outcomes = self.get_all_outcomes()

        self.display_payoff_matrix()
        print("Nash Equilibrium:", nash_equilibrium)
        print("Pareto Optimal Outcomes:", pareto_optimal)
        # GamePlotter.plot_game_outcomes(all_outcomes, pareto_optimal, nash_equilibrium)

    def check_debate(self, debate_slot: str):
        """ Determine the outcome of a debate based on the costs. """
        if self.player1.costs[debate_slot] > self.player2.costs[debate_slot]:
            return -1, 1
        elif self.player1.costs[debate_slot] < self.player2.costs[debate_slot]:
            return 1, -1
        return 0, 0

    def distribute_costs(self, nash_res: NashResult):
        """ Distributes the costs based on the Nash equilibrium strategies. """
        slots_p1 = nash_res.strategy_p1.split("/")
        slots_p2 = nash_res.strategy_p2.split("/")

        for slot in set(slots_p1) & set(slots_p2):
            change = self.check_debate(slot)
            self.player1.costs[slot] = max(self.player1.costs[slot] + change[0], 0)
            self.player2.costs[slot] = max(self.player2.costs[slot] + change[1], 0)

        for slot in set(slots_p1) - set(slots_p2):
            self.player1.costs[slot] = max(self.player1.costs[slot]-1, 0)

        for slot in set(slots_p2) - set(slots_p1):
            self.player2.costs[slot] = max(self.player2.costs[slot]-1, 0)

    def generate_payoff_matrix(self):
        """ Generates the payoff matrix based on players' strategies and costs. """
        return [[self.calculate_payoff(p1_choice.split('/'), p2_choice.split('/'))
                 for p2_choice in self.strategies]
                for p1_choice in self.strategies]

    def calculate_payoff(self, p1_choices: List[str], p2_choices: List[str]):
        """ Calculates the payoffs for each player based on their choices. """
        p1_payoff = self.player1.calculate_payoff(p1_choices)
        p2_payoff = self.player2.calculate_payoff(p2_choices)

        for choice in set(p1_choices) & set(p2_choices):
            cost1 = self.player1.costs[choice]
            cost2 = self.player2.costs[choice]
            total_cost = cost1 + cost2

            # Если общая стоимость равна 0, пропускаем
            if total_cost == 0:
                continue

            prob_p1 = cost2 / total_cost
            prob_p2 = cost1 / total_cost

            # Выбор игрока, который понесет убыток, на основе вероятностей
            if random.random() < prob_p1:
                p1_payoff -= cost1  # Игрок 1 теряет стоимость
            else:
                p2_payoff -= cost2  # Игрок 2 теряет стоимость

        return p1_payoff, p2_payoff

    def get_all_outcomes(self):
        """ Flattens the payoff matrix into a list of all outcomes. """
        return list(it.chain(*self.payoff_matrix))

    def display_payoff_matrix(self):
        """ Prints the payoff matrix as a DataFrame. """
        df = pd.DataFrame(self.payoff_matrix, index=self.strategies, columns=self.strategies)
        print(f"(Step: {len(self.history)}) Payoff Matrix:")
        print(df, '\n')

    def find_nash_equilibrium(self):
        """ Finds all Nash equilibrium using NashPy. """
        game = nash.Game(self.p1_matrix, self.p2_matrix)
        equilibrium = list(game.support_enumeration())

        return [
            NashResult(
                payoff=self.payoff_matrix[p1.argmax()][p2.argmax()],
                strategy_p1=self.strategies[p1.argmax()],
                strategy_p2=self.strategies[p2.argmax()]
            )
            for p1, p2 in equilibrium if p1.argmax() >= 0 and p2.argmax() >= 0
        ]

    def find_pareto_optimal(self):
        """ Identifies Pareto optimal outcomes from the payoff matrix. """
        outcomes = [((i, j), payoff) for i, row in enumerate(self.payoff_matrix) for j, payoff in enumerate(row)]
        pareto_optimal = []

        for ((i1, j1), (p1_payoff1, p2_payoff1)) in outcomes:
            if not any(
                    p1_payoff2 >= p1_payoff1 and p2_payoff2 >= p2_payoff1 and
                    (p1_payoff2 > p1_payoff1 or p2_payoff2 > p2_payoff1)
                    for ((i2, j2), (p1_payoff2, p2_payoff2)) in outcomes
            ):
                pareto_optimal.append((p1_payoff1, p2_payoff1))

        return pareto_optimal
