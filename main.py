from core.Player import Player
from core.Game import Game

for _ in range(10):
    while True:
        P1_costs = {"T1": 2, "T2": 2, "T3": 3}
        P2_costs = {"T1": 2, "T2": 3, "T3": 2}

        P1 = Player("Player 1", P1_costs)
        P2 = Player("Player 2", P2_costs)

        game = Game(P1, P2)

        try:
            result = game.play(steps=100, plot=True)
        except:
            continue
        else:
            break