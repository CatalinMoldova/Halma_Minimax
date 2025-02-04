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
python halma.py

