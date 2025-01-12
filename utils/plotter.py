import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from config.plot import *


def game_plot(all_outcomes, pareto_outcomes, nash_outcomes):
    U = (5, 5)

    plt.figure(figsize=(8, 8))

    for outcome in all_outcomes:
        plt.scatter(outcome[0], outcome[1], color=all_outcomes_color, label='All outcomes' if outcome is all_outcomes[0] else "")

    plt.scatter(U[0], U[1], color=impossible_max_color, label='Impossible maximum', s=impossible_marker_size)

    for outcome in pareto_outcomes:
        plt.scatter(outcome[0], outcome[1], color=pareto_color, s=marker_size, label='Pareto efficiency' if outcome is pareto_outcomes[0] else "")

    for outcome in nash_outcomes:
        plt.scatter(outcome[0], outcome[1], color=nash_color, s=nash_marker_size, label='Nash equilibrium' if outcome is nash_outcomes[0] else "")

        if outcome in pareto_outcomes:
            plt.scatter(outcome[0], outcome[1], s=nash_marker_size, c=pareto_color, marker=MarkerStyle("o", fillstyle="right"))
            plt.scatter(outcome[0], outcome[1], s=nash_marker_size, c=nash_color, marker=MarkerStyle("o", fillstyle="left"))


    plt.xticks(x_ticks)
    plt.yticks(y_ticks)
    plt.xlim(x_limit)
    plt.ylim(y_limit)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.legend()

    plt.show()
