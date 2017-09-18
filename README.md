# Reversi Game

### ABOUT THE CODE

Reversi game is implemented using MiniMax algorithm optimized with Alpha-Beta pruning. Positional weight evaluation functions are used to determine the next best move. 

To play the game, the intial state must be specified in the input file.

Start the game by running main.py. 

This in turn calls Reversi.py, which upon considering all possible moves in a given state, using minimax, predicts the next best move and returns the next state. 

### SYSTEM REQUIREMENTS

Operating System : Windows / Mac OS X

Programming Language: Python 2.7

### FILE DESCRIPTIONS

main.py - Allows you to start the game, initialize state and predicts next best move 

reversi.py - Reversi game and its functionalities

Pawn.py - class representing position of Pawn 

constants.py - contains constant values used in the game

properties.py - contains external properties like file intput and output path

Sample input output - folder containing test input and output files to test code
