# Chinese Checkers Game

A simple Two-Player Chinese Checkers game built with Python and Pygame.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Introduction

This project is a basic implementation of the Chinese Checkers game using Python and Pygame. The game allows players to move their pieces across the board with the goal of reaching the opposite side.

## Features

- Two-player mode
- AI vs AI mode
- AI vs Human mode
- Simple and intuitive interface with game status

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

## Usage

To run the game, use the `run.sh` script:

```sh
./run.sh
```

Make sure to give execute permission to the run.sh script:

```sh
chmod +x run.sh
```

## Project Structure

```
chinese-checkers-gui/
├── images/
│   ├── game_play_UI.png      # A screenshot capturing the in-game interface during play.
│   ├── main_menu_UI.png      # Screenshot showing the main menu interface.
├── src/
│   ├── main.py               # The entry point of the game.
│   ├── settings.py           # Contains game settings and configurations.
│   ├── game.py               # Responsible for manipulating the GUI (converting matrix coordinates into GUI coordinates) and handling input for the Human player.
│   ├── board.py              # Responsible for creating the game board and tracking the game status.
│   ├── player.py             # Contains the player attributes.
│   ├── utilities.py          # Contains utility functions.
│   ├── engine.py             # Contains the game engine logic, responsible for storing the game state, determining possible movements of pieces, updating game state, and checking goal state.
│   └── AI.py                 # Contains several classes implementing different AI algorithms.
├── .gitignore                # Specifies files and directories to be ignored by Git.
├── README.md                 # Contains information about the project.
├── requirements.txt          # Lists the dependencies required for the project.      
└── run.sh                # Script to run the game.
```
