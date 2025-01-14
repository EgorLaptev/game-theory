from core.Player import Player
from core.Game import Game

# Players interests
P1_costs = {"T1": 5, "T2": 10, "T3": 2}
P2_costs = {"T1": 2, "T2": 5, "T3": 10}

# Initialize players
P1 = Player("Player 1", P1_costs)
P2 = Player("Player 2", P2_costs)

# Create the game
game = Game(P1, P2)

game.play(steps=100)
