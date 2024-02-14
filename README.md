# Tic-Tac-Toe-Bot
An automatic Tic-Tac-Toe Solver. Features different modes, such as Min-Max and Alpha-Beta Pruning

# How to Run

Simply run on command line "python gameBot.py <SearchMode> <First> <PlayerMode>" (Do not include <>) 
<SearchMode> is the search type. Possible values are {1:Min-Max Algorithm ,2: Alpha-Beta Pruning}
<First> is which side goes first. Possible values are {"X": X, who is always the player, goes first, "O": The bot, who is always O, goes first}
<PlayerMode> determines if it is either Player vs CPU or CPU vs CPU. {1: Player vs Player, 2: Player vs CPU}

The program will also show how many nodes were generated for the used algorithm.
