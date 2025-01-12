class Player:
    def __init__(self, name, costs):
        self.name = name
        self.costs = costs

    def calculate_payoff(self, choices):
        return sum(self.costs[choice] for choice in choices)
