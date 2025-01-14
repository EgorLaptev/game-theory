from core.Player import Player
from core.Game import Game

# Players interests
P1_costs = {"T1": 1, "T2": 2, "T3": 3}
P2_costs = {"T1": 2, "T2": 3, "T3": 1}

# Initialize players
P1 = Player("Player 1", P1_costs)
P2 = Player("Player 2", P2_costs)

# Create the game
game = Game(P1, P2)

print(game.play(steps=7))

# # day 1
# game.iter()
# # game.display()

# # # day 2
# game.iter()
# # game.display()
