# Chinese Checkers Game

A simple Two-Player Chinese Checkers game built with Python and Pygame.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Change AI Algorithm](#change-ai-algorithm)
- [Project Structure](#project-structure)

## Introduction

This project is a basic implementation of the Chinese Checkers game using Python and Pygame. The game allows players to move their pieces across the board with the goal of reaching the opposite side.

## Features

- A two-player game
- Five AI algorithms: Stochastic Greedy, Stochastic Best Greedy, LookAhead, MiniMax, and MCTS, utilizing two different heuristic functions
- AI vs. AI mode
- AI vs. Human mode
- A simple and intuitive interface displaying game status

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/AntCay/Intro2AI/tree/chinese-checkers-gui
    ```

2. Navigate to the project directory:

    ```sh
    cd chinese-checkers-gui
    ```

3. Create a virtual environment (optional but recommended):

    Using `venv`:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

    Using `conda`:

    ```sh
    conda create --name <env-name>
    conda activate <env-name>
    ```

4. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

> **Note:** This project requires **Python 3.12+**.

## Usage

1. Using `run.sh` script:

    To run the game, use the `run.sh` script:

    ```sh
    ./run.sh
    ```

    Make sure to give execute permission to the run.sh script:

    ```sh
    chmod +x run.sh
    ```

2. Using `main.py`:

    To play the game, run the `main.py` file:

    ```sh
    cd src
    ```

    ```sh
    python main.py
    ```

## Change AI Algorithm

To change which AI algorithms will play, open the [`main.py`](src/main.py) file and change the `player1` and `player2` variables to the desired algorithm.

```sh
player1 = Player(1, COLORS[0], True, <Desired_Algorithm>(engine))
player2 = Player(2, COLORS[1], True, <Desired_Algorithm>(engine))
```

## Project Structure

```
chinese-checkers-gui/
├── images/
│   ├── game_play_UI.png      # A screenshot capturing the in-game interface during play.
│   ├── main_menu_UI.png      # Screenshot showing the main menu interface.
├── result/                   
│   ├── csv files             # CSV files with game and AI performance data
│   └── images/                  
│       ├── move_count_distribution_subplots.png  # Histogram of move count distribution.
│       └── win_distribution.png                     # Histogram of win distribution.
├── src/                      
│   ├── main.py               # The entry point of the game.
│   ├── settings.py           # Contains game settings and configurations.
│   ├── game.py               # Manages the GUI (converting matrix coordinates to screen coordinates) and handles Human player input.
│   ├── board.py              # Creates the game board and tracks game status.
│   ├── player.py             # Contains player attributes.
│   ├── utilities.py          # Provides utility functions used across the project.
│   ├── engine.py             # Implements the game engine logic (state management, move validation, goal checking).
│   ├── AI.py                 # Contains several classes implementing different AI algorithms.
│   └── analysis.py           # Analyzes results and plots histograms for game statistics.
├── .gitignore                # Specifies files and directories to be ignored by Git.
├── README.md                 # Contains information about the project.
├── requirements.txt          # Lists the dependencies required for the project.      
└── run.sh                    # Script to run the game.