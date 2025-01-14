class Player:
    def __init__(self, name, costs):
        super().__init__()
        self.name = name
        self.costs = costs
        self.result = 0

    def calculate_payoff(self, choices):
        return sum(self.costs[choice] for choice in choices)
