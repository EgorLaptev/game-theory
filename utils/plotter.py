import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
import numpy as np
from config.plot import *
from matplotlib.ticker import MaxNLocator

ax = plt.figure().gca()

ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_locator(MaxNLocator(integer=True))


def game_plot(all_outcomes, pareto_outcomes, nash_outcomes, max_payoff):
    U = (max_payoff, max_payoff)

    plt.figure(figsize=(8, 8))

    all_outcomes_flag = True

    for outcome in all_outcomes:
        plt.scatter(outcome[0], outcome[1], color=all_outcomes_color, label='All outcomes' if all_outcomes_flag else "")
        all_outcomes_flag = False

    plt.scatter(U[0], U[1], color=impossible_max_color, label='Impossible maximum', s=impossible_marker_size)

    # Сортируем точки Парето по X (или по Y, в зависимости от того, как хотите)
    sorted_pareto_outcomes = sorted(pareto_outcomes, key=lambda x: x[0])

    # Строим цепочку между точками Парето
    for i in range(len(sorted_pareto_outcomes) - 1):
        point1 = sorted_pareto_outcomes[i]
        point2 = sorted_pareto_outcomes[i + 1]
        plt.plot([point1[0], point2[0]], [point1[1], point2[1]], linestyle='--', color=pareto_color, linewidth=1)

    for outcome in pareto_outcomes:
        plt.scatter(outcome[0], outcome[1], color=pareto_color, s=marker_size, label='Pareto efficiency' if outcome is pareto_outcomes[0] else "")

    for outcome in nash_outcomes:
        plt.scatter(outcome[0], outcome[1], color=nash_color, s=nash_marker_size, label='Nash equilibrium' if outcome is nash_outcomes[0] else "")

        if outcome in pareto_outcomes:
            plt.scatter(outcome[0], outcome[1], s=nash_marker_size, c=pareto_color, marker=MarkerStyle("o", fillstyle="right"))
            plt.scatter(outcome[0], outcome[1], s=nash_marker_size, c=nash_color, marker=MarkerStyle("o", fillstyle="left"))

        # Провести линии от невозможного максимума (U) до каждой точки Нэша
        plt.plot([U[0], outcome[0]], [U[1], outcome[1]], linestyle='--', color=impossible_max_color, linewidth=1)

    plt.xticks(range(0, max_payoff+1))
    plt.yticks(range(0, max_payoff+1))
    plt.xlim(-0.5, max_payoff+0.5)
    plt.ylim(-0.5, max_payoff+0.5)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.legend()

    plt.show()


def game_result(history):
    # Разделим массив на отдельные оси X и Y
    x = [i+1 for i in range(len(history))]  # Индексы для оси X
    y1 = [step[0] for step in history]  # Значения для оси Y (берем второй элемент каждого подмассива)
    y2 = [step[1] for step in history]  # Значения для оси Y (берем второй элемент каждого подмассива)

    # Построим график
    plt.plot(x, y1, label='player 1')
    plt.plot(x, y2, label='player 2')

    # plt.xticks(range(0, len(history)))
    # plt.yticks(range(0, max(y1+y2)))
    plt.xlabel('Steps')
    plt.ylabel('Winning')
    plt.title('winnings from the number of games')
    plt.grid(True)
    plt.legend()

    plt.show()
