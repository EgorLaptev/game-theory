from numpy.random import pareto

from core.Player import Player
from core.Game import Game
from utils.plotter import game_plot


# Define the costs for each muscle group for both players
P1_costs = {"T1": 1, "T2": 2, "T3": 3}
P2_costs = {"T1": 2, "T2": 3, "T3": 1}

# Define the possible combinations of choices
choices = ["T1/T2", "T1/T3", "T2/T3"]

# Initialize players
P1 = Player("Player 1", P1_costs)
P2 = Player("Player 2", P2_costs)

# Create the game
game = Game(P1, P2, choices)

# Generate and display the payoff table
game.generate_payoff_table()
game.display_payoff_table()


# Find Nash equilibria
nash_equilibria = game.find_nash_equilibria()
print("Nash Equilibria:", nash_equilibria)

# Find Pareto optimal outcomes
pareto_optimal = game.find_pareto_optimal()
print("Pareto Optimal Outcomes:", pareto_optimal)

df = game.get_dataframe()


all_outcomes = [all_outcome[2] for all_outcome in game.get_all_outcomes()]
pareto_outcomes = [pareto[1] for pareto in pareto_optimal]
nash_outcomes = [nash[1] for nash in nash_equilibria]

game_plot(all_outcomes, pareto_outcomes, nash_outcomes)