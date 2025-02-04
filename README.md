# Halma Minimax AI

This project implements an AI agent to play the game of Halma using the Minimax algorithm with Alpha-Beta pruning. The AI is designed to evaluate the game board and determine the optimal move up to a specified depth.

## Table of Contents

- [Introduction](#introduction)
- [Game Rules](#game-rules)
- [Features](#features)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Input and Output Formats](#input-and-output-formats)
- [Algorithm Details](#algorithm-details)
- [File Structure](#file-structure)
- [Contributors](#contributors)
- [License](#license)

## Introduction

Halma is a strategic board game played on a 16x16 checkered board. Each player starts with 19 pieces positioned in diagonally opposite corners. The objective is to move all pieces from the starting corner to the opponent's corner. This project focuses on creating an AI agent capable of playing Halma efficiently against human players or other AI agents.

## Game Rules

- **Objective**: Transfer all your pieces from your starting corner to the opponent's starting corner.
- **Moves**:
  - **Single Step Move**: Move a piece to any adjacent empty square.
  - **Jump Move**: Jump over any adjacent piece (of any color) into an empty square directly opposite. Multiple jumps can be chained in a single move, provided each jump is over a different piece and lands in an unoccupied space.
- **Restrictions**:
  - Players cannot move a piece that starts outside their own camp and ends up back in their own camp.
  - If a player has pieces remaining in their camp, they must prioritize moving those pieces out.

For a detailed explanation of the rules, refer to [this resource](http://www.cyningstan.com/post/922/unspoiling-halma).

## Features

- **AI Opponent**: Utilizes the Minimax algorithm with Alpha-Beta pruning to determine optimal moves.
- **Configurable Depth**: Allows setting the depth of the Minimax search to balance between performance and decision quality.
- **Time Management**: The AI can be configured to operate within a specified time limit for making decisions.

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/CatalinMoldova/Halma_Minimax.git
   cd Halma_Minimax
2. **Install Dependencies**:
   ```bash
   Ensure you have Python 3.x installed. Install any required packages using pip:
   pip install -r requirements.txt
## Usage

To run the AI agent
```bash
python halma.py
```
The program reads from an input.txt file and writes the chosen move(s) to an output.txt file.



## Input and Output Formats

**Input (input.txt)**

**First Line**: SINGLE or GAME indicating whether the AI is making a single move or playing a full game.

**Second Line**: BLACK or WHITE indicating the AI's color.

**Third Line**: A positive floating-point number representing the total play time remaining for the AI.

**Next 16 Lines**: The game board representation:

W for a cell occupied by a white piece.

B for a cell occupied by a black piece.

. for an empty cell.

Example:

SINGLE
WHITE
100.0
BBBBB...........
BBBBB...........
BBBB............
BBB.............
BB..............
................
................
................
................
................
................
..............WW
.............WWW
............WWWW
...........WWWWW
...........WWWWW

Output (output.txt)

Each line represents a move in one of the following formats:

Single Step Move: E FROM_X,FROM_Y TO_X,TO_Y

Jump Move: J FROM_X,FROM_Y TO_X,TO_Y

Example:

J 14,13 12,11

Algorithm Details

The AI employs the Minimax algorithm with Alpha-Beta pruning to evaluate potential moves up to a specified depth. The evaluation function considers factors such as:

Distance of pieces from the target corner.

Number of pieces in the opponent's starting zone.

Penalties for pieces remaining in their own starting zone.

This approach ensures the AI makes strategic decisions aimed at winning the game efficiently.

File Structure

📂 Halma_Minimax
│── 📄 halma.py              # Main script to run the AI agent
│── 📄 input.txt             # Input file containing the current game state
│── 📄 output.txt            # Output file where the AI writes its move(s)
│── 📄 README.md             # Project documentation
│── 📄 requirements.txt      # List of required Python packages
│── 📂 docs                  # Documentation files (if any)

Contributors

CatalinMoldova

License

This project is licensed under the MIT License. See the LICENSE file for details.


