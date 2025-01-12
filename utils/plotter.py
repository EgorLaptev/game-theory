import matplotlib.pyplot as plt


def game_plot(all_outcomes, pareto_outcomes, nash_outcomes):
    U = (5, 5)

    plt.figure(figsize=(8, 8))

    # Все исходы
    for outcome in all_outcomes:
        plt.scatter(outcome[0], outcome[1], color='gray', label='All outcomes' if outcome is all_outcomes[0] else "")

    # Парето-оптимальные исходы
    for outcome in pareto_outcomes:
        plt.scatter(outcome[0], outcome[1], color='#1A64B8', s=50, label='Pareto efficiency' if outcome is pareto_outcomes[0] else "")

    # Равновесия по Нэшу
    for outcome in nash_outcomes:
        plt.scatter(outcome[0], outcome[1], color='#408040', s=75, label='Nash equilibria' if outcome is nash_outcomes[0] else "")

    # Невозможный максимум
    plt.scatter(U[0], U[1], color='#DB3838', label='Impossible maximum', s=100)

    plt.xticks(range(0, 6))
    plt.yticks(range(0, 6))
    plt.xlim(0, 5.5)
    plt.ylim(0, 5.5)
    plt.xlabel('P1 payoff')
    plt.ylabel('P2 payoff')
    plt.title('Game Outcomes')
    plt.grid(True)
    plt.legend()

    # Показываем график
    plt.show()
