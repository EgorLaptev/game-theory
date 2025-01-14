# Training Simulator Using Game Theory

## Short Description

This project is a simulator where two athletes make decisions on which muscle groups to train, based on their preferences and the cost of each training session. The game uses game theory to find Nash equilibria and Pareto-optimal outcomes. Training results are visualized using **Matplotlib**.

The simulation models two players (athletes) who choose one of three available muscle groups to train. Players may conflict if both choose the same muscle group. In this case, the player with the lower training cost wins. The game proceeds over three rounds, and players can adapt their strategies after each round.

---

## Project Description

This project simulates a game between two players, where each player makes strategic decisions based on the cost of training different muscle groups. The game uses **Nash Equilibrium** and **Pareto Optimality** to analyze the outcomes and provides visual representations of the results.

The athletes have the option to train different muscle groups, and the cost associated with training these groups differs between the two players. The game proceeds in 3 rounds, where players can each train two muscle groups per round. If both players choose the same muscle group, the player with the lower training cost gains the points for that training. The players' muscle group weights decrease with each subsequent training day.

### Key Components:
- **Players (Player)**: Each player has a set of strategies with varying costs for each muscle group.
- **Game (Game)**: Simulates the steps of the game, generates the payoff matrix, finds Nash equilibria, and determines Pareto-optimal outcomes.
- **Visualization (GamePlotter)**: Visualizes the game's results, displaying Nash equilibria, Pareto-optimal outcomes, and other relevant data.

## Project Structure

```text
project-directory/
│
├── core/
│   ├── Game.py             # Game logic, calculating equilibria and payoffs
│   └── Player.py           # Player class, storing strategies and calculating payoffs
│
├── utils/
│   └── GamePlotter.py      # Visualizing game results
│
├── config/
│   └── plot.py             # Configuration for visualization settings
│
├── main.py                 # Entry point to run the game
└── README.md               # Documentation
```

### File Descriptions

#### 1. **`core/Game.py`**

This file contains the core game logic, including the calculation of payoffs, finding Nash equilibria, and identifying Pareto-optimal outcomes.

**Classes and Methods:**
- **`Game`**: The main class for the game, which manages the game flow between two players.
  - **`play(steps)`**: Starts the game for the given number of steps.
  - **`iter()`**: Performs one step of the game, generates the payoff matrix, and updates the players' scores.
  - **`generate_payoff_matrix()`**: Generates the payoff matrix based on the players' selected strategies.
  - **`find_nash_equilibrium()`**: Finds all Nash equilibria using NashPy.
  - **`find_pareto_optimal()`**: Identifies Pareto-optimal outcomes.
  - **`display()`**: Displays the payoff matrix and results of the game.

#### 2. **`core/Player.py`**

This file defines the Player class, which stores the player’s strategies and calculates their payoffs based on chosen strategies.

**Classes and Methods:**
- **`Player`**: The player class that stores strategies and computes the payoffs.
  - **`calculate_payoff(choices)`**: Computes the payoff based on the selected strategies.

#### 3. **`utils/GamePlotter.py`**

This file handles the visualization of the game’s results using Matplotlib.

**Methods:**
- **`plot_game_outcomes()`**: Visualizes all game outcomes, including Nash equilibria and Pareto-optimal outcomes.
- **`plot_game_result()`**: Plots the players' results over time (winnings per step).
- **`plot_pareto_outcomes()`**: Visualizes Pareto-optimal outcomes.
- **`plot_nash_outcomes()`**: Visualizes Nash equilibrium outcomes.

#### 4. **`config/plot.py`**

Configuration file for visualization, where you set up parameters such as colors, axis labels, and marker sizes.

#### 5. **`main.py`**

The main entry point of the project that runs the game. Players are initialized with their costs, and the game is simulated.

**Example Usage:**
```python
from core.Player import Player
from core.Game import Game

# Players' costs for each muscle group
P1_costs = {"T1": 5, "T2": 10, "T3": 2}
P2_costs = {"T1": 2, "T2": 5, "T3": 10}

# Initialize players
P1 = Player("Player 1", P1_costs)
P2 = Player("Player 2", P2_costs)

# Create the game
game = Game(P1, P2)

# Run the game for 100 steps
game.play(steps=100)
```

## Installation and Running the Project

### Requirements:
- Python 3.x or higher
- Required libraries:
  - `numpy`
  - `pandas`
  - `nashpy`
  - `matplotlib`

### Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/EgorLaptev/game-theory.git
   ```

2. Navigate to the project directory:
   ```bash
   cd game-theory
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project:

1. Run the game using the following command:
   ```bash
   python main.py
   ```

2. After the game finishes, you will see visualizations of the results.
