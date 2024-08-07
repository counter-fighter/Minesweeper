# Minesweeper
## Python Minesweeper Project
#### Team Name: Minesweeper Variance
#### Goal: To code a minesweeper in python with an extra rules/game mode.

## How to Run the Program
To run the program, go to the root directory of the project and run `python main.py` in a terminal.

## Summary
Minesweeper is a classic computer puzzle game that involves a grid of covered squares. 
The main goal of Minesweeper is to uncover all the squares on the grid that do not contain mines. 
If you uncover a square that contains a mine, you lose the game. When you click on a square without a mine, it will reveal a number. 
This number indicates how many mines are in the 8 adjacent squares. 
If you suspect a square contains a mine, you can right-click to place a flag on it, which will help you remember where you think mines are located. 
To win the game, you have to uncover all of the square that does not contain a mine.

## Main Menu
When we run the code, the main menu should pop up, allowing the user to select the size of the board, difficulty of the game (% of mine/non-mine), different game mode, continue playing from the previous session, or start the new session. 
Once the user finishes selecting the configuration and press the play button, the main menu window should close, and a new minesweeper window should pop up. 

## Features
- The minesweeper window should have the minesweeper grid, timer, current mine count and the help button that will pop up the explanation of the extra rules of the current game mode that the user currently selected. 
- If the program is closed before the board is solved or the user click the mine, the program should write the current state of the board into a text file so that the user can continue the current board from the main menu. 
- The user can interact with the minesweeper grid by either left-click to reveal a tile or right-click to flag that tile as a mine. 
- If the user left-click the non-mine tile, the tile is revealed, and the game will continue. 
- If the user left-click the mine, the new window will pop up with the text you hit a mine along with the choice to continue or not. 
- If the user presses yes, their previous move is undone, and the game continues. Otherwise, another window will pop up and ask the user to start the new board or return to the main menu. During the main menu option, the minesweeper window should also reveal all the mine on the current board. 
- If the user press a new game, a new board with the same setting as the current board is generated and replace the current minesweeper window. 
- If the user select the main menu button, the pop up is close and the minesweeper window is replaced with the main menu window.
- The user can resume a lost game by selecting the continue button in the main menu and the mine that triggered the loss will be revealed when the user continues to play.

## Game Modes
In the main menu, if the user select any game mode and presses play, the game should generate the board with an extra rule according to the selected option. 
Some examples of the extra rule are:
- Instead of the number giving clue to the surrounding tile, they give a clue vertically and horizontally 2 tiles away from the number.
- The number of the clue will always overshoot or undershoot the true value. Eg. If the clue say 2, the actual number of surrounding mine could be either 1 or 3.
