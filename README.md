# Chinese Checkers Game

A simple Chinese Checkers game built with Python and Pygame.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project is a basic implementation of the Chinese Checkers game using Python and Pygame. The game allows players to move their pieces across the board with the goal of reaching the opposite side.

## Features

- Single-player mode
- Simple and intuitive interface
- Automatic detection of valid moves

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/ChineseCheckers-GUI.git
    ```

2. Navigate to the project directory:

    ```sh
    cd chinese-checkers
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

ChineseCheckers-GUI/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── settings.py
│   ├── game.py
│   ├── board.py
│   ├── pieces.py
│   ├── player.py
│   ├── utilities.py
│   ├── engine.py
│   └── AI.py
├── .gitignore
├── README.md
├── requirements.txt
├── run.sh
└── sample.png

src/: Contains the source code of the game.
    main.py: The entry point of the game.
    settings.py: Contains game settings and configurations.
    game.py: Contains the main game logic.
    board.py: Contains the board logic.
    pieces.py: Contains the pieces logic.
    player.py: Contains the player logic.
    utilities.py: Contains utility functions.
    engine.py: Contains the game engine logic.
    AI.py: Contains the AI logic.
.gitignore: Specifies files and directories to be ignored by Git.
README.md: Contains information about the project.
requirements.txt: Lists the dependencies required for the project.
run.sh: Script to run the game.
sample.png: sample image of the GUI.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please create an issue or submit a pull request.

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.