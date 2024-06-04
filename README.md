# Monopoly Game

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Game Description](#game-description)
- [Instructions](#instructions)
- [Team Contributions](#team-contributions)
- [License](#license)

## Introduction
This is a Monopoly-themed board game developed in Python with a graphical user interface (GUI) using Tkinter. Players can choose different characters and start the game. The game includes sound effects and animations, adding more fun and interactivity.

## Installation
1. Ensure you have Python 3.x installed.
2. Install the required Python libraries:
    ```bash
    pip install pillow pygame
    ```
3. Clone the project to your local machine:
    ```bash
    git clone https://github.com/yourusername/monopoly-game.git
    cd monopoly-game
    ```

## Game Description
This game is a multiplayer game where players can choose to play with 2 to 4 players. Each player selects a character and is assigned an initial amount of money. The game includes a variety of images and sound effects to make the gameplay more engaging and lively.

## Instructions
1. Run the main program to start the game:
    ```bash
    python main.py
    ```
2. On the main screen, click the "Start Game" button to enter the player selection screen.
3. Select the number of players and initial funds, then click "Continue" to proceed to the character selection screen.
4. Each player chooses their character by clicking on the desired character and confirming their selection.
5. Once all players have selected their characters, click the "Start Game" button to begin the game.
6. Follow the on-screen instructions to play the game.

### Gameplay Mechanics
1. **Rolling the Dice**: Click the "Roll Dice" button to roll the dice and move your character.
2. **Buying Properties**: If you land on an unowned property, you have the option to buy it.
3. **Paying Rent**: If you land on a property owned by another player, you must pay rent.
4. **Chance and Fate Cards**: Landing on a Chance or Fate space will trigger a card draw, which can have positive or negative effects.
5. **Magic Cards and Special Spaces**: Special spaces like Jail, Hospital, and Magic Card spaces have unique effects.

### Store
- Access the store to buy special cards that provide various advantages in the game. Use the store button to enter the store and buy cards with your in-game money.

### Game Over
- The game ends when a player goes bankrupt. The remaining player with the most money wins.

## Team Contributions
- **黃禹辰**: Player selection interface and File I/O and map settings and game flow
- **羅鈺婷**: Gacha store and game flow 
- **葉珈妤**: Presentation and map settings and game flow
- **劉亮萱**: Presentation and map settings and game flow
- **呂沛珍**: Chance or Fate settings and soud effect and game flow

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
