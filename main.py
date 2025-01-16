from core.Player import Player
from core.Game import Game

# Players interests
P1_costs = {"T1": 1, "T2": 2, "T3": 3}
P2_costs = {"T1": 3, "T2": 1, "T3": 2}

# Initialize players
P1 = Player("Player 1", P1_costs)
P2 = Player("Player 2", P2_costs)

# Create the game
game = Game(P1, P2)

game.play(steps=10, plot=True)
