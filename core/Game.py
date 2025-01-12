import pandas as pd


class Game:
    def __init__(self, player1, player2, choices):
        self.player1 = player1
        self.player2 = player2
        self.choices = choices
        self.payoff_table = {}

    def calculate_payoff(self, P1_choice, P2_choice):
        P1_payoff = self.player1.calculate_payoff(P1_choice)
        P2_payoff = self.player2.calculate_payoff(P2_choice)

        # Adjust payoffs for overlapping choices
        if P1_choice[0] in P2_choice and self.player1.costs[P1_choice[0]] < self.player2.costs[P1_choice[0]]:
            P2_payoff -= self.player2.costs[P1_choice[0]]
        elif P1_choice[0] in P2_choice:
            P1_payoff -= self.player1.costs[P1_choice[0]]

        if P1_choice[1] in P2_choice and self.player1.costs[P1_choice[1]] < self.player2.costs[P1_choice[1]]:
            P2_payoff -= self.player2.costs[P1_choice[1]]
        elif P1_choice[1] in P2_choice:
            P1_payoff -= self.player1.costs[P1_choice[1]]

        return (P1_payoff, P2_payoff)

    def generate_payoff_table(self):
        for P1_choice in self.choices:
            for P2_choice in self.choices:
                P1_split = P1_choice.split('/')
                P2_split = P2_choice.split('/')
                self.payoff_table[(P1_choice, P2_choice)] = self.calculate_payoff(P1_split, P2_split)

    def display_payoff_table(self):
        df = self.get_dataframe()
        for (P1_choice, P2_choice), payoff in self.payoff_table.items():
            df.loc[P1_choice, P2_choice] = str(payoff)
        print(df)

    def get_dataframe(self):
        return pd.DataFrame(index=self.choices, columns=self.choices)

    def get_all_outcomes(self):
        return [(P1_choice, P2_choice, self.payoff_table[(P1_choice, P2_choice)])
                for P1_choice in self.choices
                for P2_choice in self.choices]

    def find_nash_equilibria(self):
        nash_equilibria = []
        df = self.get_dataframe()
        for P1_choice in self.choices:
            for P2_choice in self.choices:
                P1_payoff, P2_payoff = self.payoff_table[(P1_choice, P2_choice)]

                # Проверяем, является ли это лучшим ответом для P1
                P1_best_response = all(P1_payoff >= self.payoff_table[(P1_choice, other)][0] for other in df.columns)

                # Проверяем, является ли это лучшим ответом для P2
                P2_best_response = all(P2_payoff >= self.payoff_table[(other, P2_choice)][1] for other in df.index)

                if P1_best_response and P2_best_response:
                    # Добавляем не только ходы, но и их выплаты
                    nash_equilibria.append(((P1_choice, P2_choice), (P1_payoff, P2_payoff)))
        return nash_equilibria

    def find_pareto_optimal(self):
        pareto_optimal = []
        all_outcomes = self.get_all_outcomes()

        for (P1_choice, P2_choice, (P1_payoff, P2_payoff)) in all_outcomes:
            is_dominated = False
            for (other_P1_choice, other_P2_choice, (other_P1_payoff, other_P2_payoff)) in all_outcomes:
                if (other_P1_payoff >= P1_payoff and other_P2_payoff >= P2_payoff) and (other_P1_payoff > P1_payoff or other_P2_payoff > P2_payoff):
                    is_dominated = True
                    break
            if not is_dominated:
                # Добавляем не только ходы, но и их выплаты
                pareto_optimal.append(((P1_choice, P2_choice), (P1_payoff, P2_payoff)))
        return pareto_optimal
