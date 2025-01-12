from core.Player import Player
from core.Game import Game
from utils.plotter import game_plot

# Players interests
P1_costs = {"T1": 1, "T2": 3, "T3": 2}
P2_costs = {"T1": 3, "T2": 2, "T3": 1}

# Possible choices
choices = ["T1/T2", "T1/T3", "T2/T3"]


# Initialize players
P1 = Player("Player 1", P1_costs)
P2 = Player("Player 2", P2_costs)

# Create the game
game = Game(P1, P2, choices)

# display the payoff table
game.display_payoff_matrix()

# Find Nash equilibrium
nash_equilibrium = game.find_nash_equilibrium()
print("Nash Equilibria:", nash_equilibrium)

# Find Pareto optimal outcomes
pareto_optimal = game.find_pareto_optimal()
print("Pareto Optimal Outcomes:", pareto_optimal)

all_outcomes = game.get_all_outcomes()

game_plot(all_outcomes, pareto_optimal, nash_equilibrium)
