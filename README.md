# checkers
This repository is where I keep all the files for my checkers engine. The goal is to create a program that can play checkers and win every time against any human.

## General Plan of Attack:

- [x] represent the relevant board information as an ordered list of bitmaps

- [x] create a move finder for each of the following types of moves:
    - [x] **simple move:** a move from one square to an empty neighboring square which is immediately diagonal to the starting square
    - [x] **jump move:** a move from one square to another square that is two diagonal squares in the same direction away from the initial square; the first diagonal square in the path must contain an opposite colored piece (which is then captured), and the destination square must be empty; jumps can also occur in chains (and they must continue jumping if possible), meaning if another jump is possible after an initial jump, then the jumping piece must continue jumping in that direction

- [x] create a UI for a playable 2-player human game

- [ ] create a player input method that will alow a person to play a game of checkers against the engine (using random moves at first)

- [ ] create an evaluation function to evaluate any board position and find the best move from a list of all possible moves in that position (up to a reasonable depth)

## Regarding the UI:

The empty board looks like the following (where the equals sign represents a square that cannot be accessed by pieces):

|=| |=| |=| |=| |
| |=| |=| |=| |=|
|=| |=| |=| |=| |
| |=| |=| |=| |=|
|=| |=| |=| |=| |
| |=| |=| |=| |=|
|=| |=| |=| |=| |
| |=| |=| |=| |=|

The starting position looks like the following (where an "o" is a black piece and an "x" is a red piece):

|=|o|=|o|=|o|=|o|
|o|=|o|=|o|=|o|=|
|=|o|=|o|=|o|=|o|
| |=| |=| |=| |=|
|=| |=| |=| |=| |
|x|=|x|=|x|=|x|=|
|=|x|=|x|=|x|=|x|
|x|=|x|=|x|=|x|=|

When a piece gets to the back rank, it is promoted to a king (denoted by a capital letter: either "O" or "X").

Additionally, each accessible square is represented by a coordinate from 1 to 32, going from the top left to the bottom right (the same way you are reading this sentence). The following image demonstrates this nicely: https://commons.wikimedia.org/wiki/File:Draughts_Notation.svg#/media/File:Draughts_Notation.svg

---

> **Note:** I am attempting to do as much of the problem solving on my own in terms of best practices for coding the ideal checkers engine. However, I will obviously turn to the internet for help if I hit a wall.