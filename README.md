### README: Тренировочный симулятор с использованием теории игр

## Описание проекта

Этот проект моделирует игру между двумя игроками, каждый из которых принимает стратегические решения на основе различных групп мышц. Игроки используют свои предпочтения (стоимость тренировки для каждой группы) для принятия решений в каждом раунде. В проекте применяются концепции **Нэшевого равновесия** и **Парето-оптимальности** для анализа результатов. Игра моделируется с использованием библиотеки **NashPy** для нахождения равновесий и **Matplotlib** для визуализации.

### Основные компоненты:
- **Игроки (Player)**: Каждый игрок имеет набор стратегий с различной стоимостью для каждой группы.
- **Игра (Game)**: Моделирует несколько шагов игры, генерирует матрицу выплат, находит Нэшевые равновесия и парето-оптимальные результаты.
- **Визуализация (GamePlotter)**: Визуализирует результаты игры, отображая Нэшевы равновесия, парето-оптимальные и другие исходы.

## Структура проекта

```text
project-directory/
│
├── core/
│   ├── Game.py             # Логика игры, вычисление равновесий и выплат
│   └── Player.py           # Класс игрока, хранение стратегий и расчет выплат
│
├── utils/
│   └── GamePlotter.py      # Визуализация результатов игры
│
├── config/
│   └── plot.py             # Конфигурация параметров для визуализации
│
├── main.py                 # Точка входа, запуск игры
└── README.md               # Документация
```

### Описание файлов

#### 1. **`core/Game.py`**

Этот файл содержит основную логику игры, включая вычисления выплат, нахождение Нэшевых равновесий и парето-оптимальных исходов.

**Классы и методы:**
- **`Game`**: Основной класс игры, который управляет процессом игры между двумя игроками.
  - **`play(steps)`**: Запускает игру на указанное количество шагов.
  - **`iter()`**: Осуществляет один шаг игры, генерирует матрицу выплат и обновляет состояния игроков.
  - **`generate_payoff_matrix()`**: Генерирует матрицу выплат на основе выбранных стратегий игроков.
  - **`find_nash_equilibrium()`**: Находит Нэшевы равновесия с использованием библиотеки NashPy.
  - **`find_pareto_optimal()`**: Находит парето-оптимальные исходы.
  - **`display()`**: Отображает матрицу выплат и результаты игры.

#### 2. **`core/Player.py`**

Этот файл описывает класс игрока, его стратегии и метод расчета выплат.

**Классы и методы:**
- **`Player`**: Класс игрока, который хранит информацию о стратегиях и расчет выплат.
  - **`calculate_payoff(choices)`**: Метод для расчета выплат на основе выбранных стратегий.

#### 3. **`utils/GamePlotter.py`**

Этот файл отвечает за визуализацию результатов игры. Он использует Matplotlib для создания графиков.

**Методы:**
- **`plot_game_outcomes()`**: Визуализирует все исходы игры, включая Нэшевы равновесия и парето-оптимальные исходы.
- **`plot_game_result()`**: Строит график результатов игры по шагам (выигрыши игроков на каждом шаге).
- **`plot_pareto_outcomes()`**: Отображает парето-оптимальные исходы.
- **`plot_nash_outcomes()`**: Отображает Нэшевы равновесия.

#### 4. **`config/plot.py`**

Конфигурационный файл для визуализации, который задает параметры отображения графиков, такие как цвета, метки осей и размеры маркеров.

#### 5. **`main.py`**

Главный файл, который запускает игру. Здесь создаются игроки, настраиваются их стратегии, и начинается симуляция игры.

**Пример использования:**
```python
from core.Player import Player
from core.Game import Game

# Стоимости для игроков
P1_costs = {"T1": 5, "T2": 10, "T3": 2}
P2_costs = {"T1": 2, "T2": 5, "T3": 10}

# Инициализация игроков
P1 = Player("Player 1", P1_costs)
P2 = Player("Player 2", P2_costs)

# Создание игры
game = Game(P1, P2)

# Игровой процесс
game.play(steps=100)
```

## Установка и запуск

### Требования:
- Python 3.x или выше
- Установленные библиотеки:
  - `numpy`
  - `pandas`
  - `nashpy`
  - `matplotlib`

### Установка зависимостей:

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/EgorLaptev/game-theory.git
   ```

2. Перейдите в директорию проекта:
   ```bash
   cd game-theory
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

### Запуск проекта:

1. Запустите игру с помощью следующей команды:
   ```bash
   python main.py
   ```

2. После выполнения игры, вы увидите графики с результатами.

