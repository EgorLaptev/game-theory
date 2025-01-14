import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.ticker import MaxNLocator


class GamePlotter:
    max_payoff = 10
    all_outcomes_color = 'blue'
    impossible_max_color = 'red'
    pareto_color = 'green'
    nash_color = 'purple'
    impossible_marker_size = 100
    marker_size = 50
    nash_marker_size = 60
    x_label = 'X-axis Label'
    y_label = 'Y-axis Label'
    title = 'Game Outcomes Plot'

    @staticmethod
    def _setup_axes():
        ax = plt.figure().gca()
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    @staticmethod
    def plot_all_outcomes(all_outcomes):
        all_outcomes_flag = True
        for outcome in all_outcomes:
            plt.scatter(outcome[0], outcome[1], color=GamePlotter.all_outcomes_color,
                        label='All outcomes' if all_outcomes_flag else "")
            all_outcomes_flag = False

    @staticmethod
    def plot_pareto_outcomes(pareto_outcomes):
        sorted_pareto_outcomes = sorted(pareto_outcomes, key=lambda x: x[0])
        for i in range(len(sorted_pareto_outcomes) - 1):
            point1, point2 = sorted_pareto_outcomes[i], sorted_pareto_outcomes[i + 1]
            plt.plot([point1[0], point2[0]], [point1[1], point2[1]], linestyle='--',
                     color=GamePlotter.pareto_color, linewidth=1)

        for outcome in pareto_outcomes:
            plt.scatter(outcome[0], outcome[1], color=GamePlotter.pareto_color, s=GamePlotter.marker_size,
                        label='Pareto efficiency' if outcome is pareto_outcomes[0] else "")

    @staticmethod
    def plot_nash_outcomes(nash_outcomes, pareto_outcomes):
        U = (GamePlotter.max_payoff, GamePlotter.max_payoff)
        for outcome in nash_outcomes:
            plt.scatter(outcome[0], outcome[1], color=GamePlotter.nash_color, s=GamePlotter.nash_marker_size,
                        label='Nash equilibrium' if outcome is nash_outcomes[0] else "")
            if outcome in pareto_outcomes:
                plt.scatter(outcome[0], outcome[1], s=GamePlotter.nash_marker_size, c=GamePlotter.pareto_color,
                            marker=MarkerStyle("o", fillstyle="right"))
                plt.scatter(outcome[0], outcome[1], s=GamePlotter.nash_marker_size, c=GamePlotter.nash_color,
                            marker=MarkerStyle("o", fillstyle="left"))
            plt.plot([U[0], outcome[0]], [U[1], outcome[1]], linestyle='--', color=GamePlotter.impossible_max_color,
                     linewidth=1)

    @staticmethod
    def plot_game_outcomes(all_outcomes, pareto_outcomes, nash_outcomes):
        GamePlotter._setup_axes()
        GamePlotter.plot_all_outcomes(all_outcomes)
        GamePlotter.plot_pareto_outcomes(pareto_outcomes)
        GamePlotter.plot_nash_outcomes(nash_outcomes, pareto_outcomes)

        plt.xticks(range(0, GamePlotter.max_payoff+1))
        plt.yticks(range(0, GamePlotter.max_payoff+1))
        plt.xlim(-0.5, GamePlotter.max_payoff+0.5)
        plt.ylim(-0.5, GamePlotter.max_payoff+0.5)
        plt.xlabel(GamePlotter.x_label)
        plt.ylabel(GamePlotter.y_label)
        plt.title(GamePlotter.title)
        plt.grid(True)
        plt.legend()

        plt.show()

    @staticmethod
    def plot_game_result(history):
        GamePlotter._setup_axes()

        x = [i+1 for i in range(len(history))]
        y1 = [step[0] for step in history]
        y2 = [step[1] for step in history]

        plt.plot(x, y1, label='player 1')
        plt.plot(x, y2, label='player 2')

        plt.xlabel('Steps')
        plt.ylabel('Winning')
        plt.title('Winnings from the number of games')
        plt.grid(True)
        plt.legend()

        plt.show()
