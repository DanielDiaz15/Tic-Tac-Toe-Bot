import math
import sys

class game:
    def __init__(self):
        #setup
        self.state = [ [' ',' ',' '],
                       [' ',' ',' '],
                       [' ',' ',' ']
                                      ] # [row][column]

                        #[ [1, 2, 3]
                        #  [4, 5, 6]
                        #  [7, 8, 9] ]


        self.turn = 1 # 1 is X and 0 is O
        self.recentMove = None

        self.viableMoves = [1,2,3,4,5,6,7,8,9]  # changed form set to list because apparently it can be random for loops


    def genNext(self):
        returnList = []
        for i in self.viableMoves:
            gameNode = self.placeCopy(self.turn, i)
            returnList.append(gameNode)
        return returnList

    def place(self, player, spot):  # player denoted by 1 or 0
        if spot == 0:
            exit()
        if spot not in self.viableMoves:  # should be caught before
            return

        # find row,column,symbol
        s = 'X' if player == 1 else 'O'
        r = math.floor((spot - 1)/3)
        c = ((spot -1) % 3)

        # alter game and change turn
        self.state[r][c] = s
        self.viableMoves.remove(spot)
        self.turn = (1 ^ player)
        self.recentMove = spot

        return self

    def placeCopy(self, player, spot):  # player denoted by 1 or 2

        # must make a deep copy
        # copying a list of lists will only copy outside list
        newState = self.state.copy()
        for i in range (0,3):
            newState[i] = self.state[i].copy()
        newViable = self.viableMoves.copy()
        if spot not in newViable:
            return

        # find row and column as well as symbol
        s = 'X' if player == 1 else 'O'
        r = math.floor((spot - 1)/3)
        c = ((spot -1) % 3)

        # alter game
        newGame = game()
        newGame.state = newState
        newGame.viableMoves = newViable
        newGame.place(player, spot)


        return newGame


    def returnWinner(self):

        # Rows, will
        for row in self.state:
            if row[0] == row[1] == row[2]:
                if row[0] != ' ':
                    return row[0]  # need to return so it doesn't move onto next
                    #print(row)
        # Columns
        for i in range (0,3):  # r is exclusive
            if self.state[0][i] == self.state[1][i] == self.state[2][i]:
                if self.state[0][i] != ' ':
                    return self.state[0][i]  # need to return so it doesn't move onto next
                    # print("column win")

        # Diagonals
        if self.state[0][0] == self.state[1][1] == self.state[2][2]:
            if self.state[0][0] != ' ':
                return self.state[0][0]
                # print("diagonal 1 win")

        if self.state[2][0] == self.state[1][1] == self.state[0][2]:
            if self.state[2][0] != ' ':
                return self.state[2][0]

        #tie
        if len(self.viableMoves) == 0:
            return 't' #tie

        return 'n'  # neither a winner

    def display(self):
        return " " + self.state[0][0] + " | " + self.state[0][1] + " | " + self.state[0][2] + "\n" + \
               "---+---+---\n" + \
               " " + self.state[1][0] + " | " + self.state[1][1] + " | " + self.state[1][2] + "\n" + \
               "---+---+---\n" + \
               " " + self.state[2][0] + " | " + self.state[2][1] + " | " + self.state[2][2] + "\n"

    def isOver(self):
        winner = self.returnWinner()
        return winner == 't' or winner == 'X' or winner == 'O'

class gameHandler:

    def __init__(self, searchType, versus, firstPlay):
        self.g = game()
        self.numNode = 1  # number of generated nodes, 1 since root is included
        self.totalNode = 0
        self.searchMode = searchType
        self.vsMode = versus
        if firstPlay == 'O':
            self.g.turn = 0


    def util(self, gameS):
        winner = gameS.returnWinner()
        #something wrong here, seen in result, games not actually won
        if winner == 'X':
            # if len(gameS.viableMoves) != 0:
            #     print(gameS.display())
            #     print("util value given: 1")
            return 1
        elif winner == 'O':
            # if len(gameS.viableMoves) != 0:
            #     print(gameS.display())
            #     print("util value given: -1")
            return -1
        elif winner == 't':
            # if len(gameS.viableMoves) != 0:
            #     print(gameS.display())
            #     print("util value given: 0")
            return 0
        else:
            return None

    def abSearch(self, gameRoot):  # alpha beta search, returns best move

        if gameRoot.turn == 1:
            (value, move) = self.findMaxAB(gameRoot, -100, 100)  # max a util will ever be is 1 or -1 so this is fine
        if gameRoot.turn == 0:
            (value, move) = self.findMinAB(gameRoot, -100, 100)
        return move.recentMove

    def findMaxAB(self, gameN, a, b):  # returns a tuple of (value, game)
        possibleUtil = self.util(gameN)
        v = -100
        nGame = None
        alpha = a
        if possibleUtil is not None:  # is terminal operation
            return (possibleUtil, gameN)

        newNodes = gameN.genNext()

        for act in newNodes:
            (val, nextGame) = self.findMinAB(act, alpha, b)
            self.numNode += 1
            if val > v:
                v = val
                nGame = act
                alpha = max(alpha, v)
            if v >= b:
                return (v, nGame)
        return (v, nGame)

    def findMinAB(self, gameN, a, b):  # returns a tuple of (value, game)
        possibleUtil = self.util(gameN)
        v = 100
        nGame = None
        beta = b
        if possibleUtil is not None:  # is terminal operation
            return (possibleUtil, gameN)

        newNodes = gameN.genNext()
        # DEBUG: Alternate Counting Method
        # self.numNode += len(newNodes)

        for act in newNodes:
            (val, nextGame) = self.findMaxAB(act, a, beta)
            self.numNode += 1
            if val < v:
                v = val
                nGame = act
                beta = min(beta, v)
            if v <= a:
                return (v, nGame)
        return (v, nGame)

    def MinMax(self, gameRoot):
        if gameRoot.turn == 1:
            (value, move) = self.findMax(gameRoot)  # max a util will ever be is 1 or -1 so this is fine
        if gameRoot.turn == 0:
            (value, move) = self.findMin(gameRoot)
        # DEBUG: print("move value: ", value)
        return move.recentMove  # move is actually a game object

    def findMax(self, gameN):
        possibleUtil = self.util(gameN)
        v = -100
        nGame = None
        if possibleUtil is not None:  # is terminal operation
            return (possibleUtil, gameN)

        newNodes = gameN.genNext()
        # DEBUG: Alternative counting method
        # self.numNode += len(newNodes)

        for act in newNodes:
            (val, nextGame) = self.findMin(act)
            self.numNode += 1
            if val > v:
                v = val
                nGame = act
        return (v, nGame)

    def findMin(self, gameN):
        possibleUtil = self.util(gameN)
        v = 100
        nGame = None

        if possibleUtil is not None:  # is terminal operation
            return (possibleUtil, gameN)

        newNodes = gameN.genNext()
        self.numNode += len(newNodes)

        for act in newNodes:
            (val, nextGame) = self.findMax(act)
            if val < v:
                v = val
                nGame = act
        return (v, nGame)


    def search(self):
        if self.searchMode == 1:
            return self.MinMax(self.g)
        else:
            return self.abSearch(self.g)

    def runGame(self):

        # should check mode that either 1 or 2 at arg level
        modeStr = "human versus computer" if self.vsMode == 1 else "computer versus computer"
        algText = "Minimax" if self.searchMode == 1 else "Minimax with alpha-beta pruning"
        turnSymbol = "X" if self.g.turn == 1 else "O"

        print("Diaz, Daniel, A20480127 solution: \n",
              "Algorithm: ", algText, "\n",
              "First: ", self.g.turn, "\n",
              "Mode: ", modeStr, "\n")

        print(self.g.display())
        if self.g.turn == 1:
            self.humanMove()
        else:
            self.computerMove()

    def humanMove(self):
        print("X's move")  # human is always X if human versus computer
        invalid = True
        possible = str(self.g.viableMoves)

        # move checking
        while invalid:
            choice = (input("What is your move (possible moves at the moment are: " + possible +
                            " | enter 0 to exit the game)?? "))
            if choice.isdigit():
                if int(choice) == 0:
                    exit()
                if int(choice) in self.g.viableMoves:
                    invalid = False

        # handle placement and hand off
        self.g.place(self.g.turn, int(choice))
        print(self.g.display())
        self.tryWinner()
        self.computerMove()

    def computerMove(self):
        turnSymbol = 'X' if self.g.turn == 1 else 'O'

        # decides what search will be used
        searchMove = self.search()
        print(turnSymbol, "'s selected move: ", searchMove)
        print("Number of search tree nodes generated: ", self.numNode)
        self.totalNode += self.numNode
        # Need to reset num nodes because each search new tree
        # This means it decrease as possible moves/trees get smaller
        self.numNode = 1
        self.g.place(self.g.turn, searchMove)
        print(self.g.display())
        self.tryWinner()


        # depends on human or computer opponent
        if self.vsMode == 1:
            self.humanMove()
        else:
            self.computerMove()

    def tryWinner(self):
        # see if a winner exists. If so, end game
        winner = self.g.returnWinner()
        triggered = False
        if winner == 'X' or winner == 'O':
            print(winner, " WON")
            triggered = True
        if winner == 't':
            print("TIE")
            triggered = True
        if triggered:
            print("Total number of nodes", self.totalNode)
            exit()


def triggerFail():
    # argument failure
    print("ERROR: Not enough/too many/illegal input arguments.")
    exit()


# main program running from here on out
if len(sys.argv) != 4:  # 4 because file technically is 1st (the 0th index)
    triggerFail()

# check if args 1 and 3 are digits, else fail
if not sys.argv[1].isdigit() or not sys.argv[3].isdigit():
    triggerFail()

# check if 1st and 3rd args are 1 or 2
if int(sys.argv[1]) not in range(1,3) or int(sys.argv[3]) not in range(1,3):
    triggerFail()

# check if 2nd argument is not X or O
if sys.argv[2] != "X" and sys.argv[2] != "O":
    triggerFail()

ticGame = gameHandler(int(sys.argv[1]), int(sys.argv[3]), sys.argv[2])
ticGame.runGame()

