import copy

utility_values = [[99, -8, 8, 6, 6, 8, -8, 99], [-8, -24, -4, -3, -3, -4, -24, -8], [8, -4, 7, 4, 4, 7, -4, 8],
                  [6, -3, 4, 0, 0, 4, -3, 6], [6, -3, 4, 0, 0, 4, -3, 6], [8, -4, 7, 4, 4, 7, -4, 8],
                  [-8, -24, -4, -3, -3, -4, -24, -8], [99, -8, 8, 6, 6, 8, -8, 99]]
rowColumnNeighbours = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
rows = 8
columns = 8


class Pawn:
    row = -1
    column = -1

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __repr__(self):
        return '[{},{}]'.format(self.row, self.column)


class Game:
    moves_made = []
    state = [[]]
    moves = ""
    moves_list = []

    def __init__(self, intialstate, startplayer, maxdepth):
        self.state = intialstate
        self.maxdepth = maxdepth
        self.startplayer = startplayer
        if self.startplayer == 'X':
            self.opponent = 'O'
        else:
            self.opponent = 'X'

    def addmoves(self, str):
        self.moves += "\n"
        self.moves += str

    def evaluate(self, state_of_board):
        blackWeight = 0
        whiteWeight = 0
        for row in range(0, 8, 1):
            for column in range(0, 8, 1):
                if state_of_board[row][column] == self.startplayer:
                    blackWeight += utility_values[row][column]
                elif state_of_board[row][column] == self.opponent:
                    whiteWeight += utility_values[row][column]
        return blackWeight - whiteWeight

    def outofrange(self, row, column):
        rowColumnRange = range(0, 8)
        if row in rowColumnRange and column in rowColumnRange:
            return 1
        return -1

    def result(self, state, action, current):
        resultstate = copy.deepcopy(state)

        if current == 'X':
            opponentpawn = 'O'
        else:
            opponentpawn = 'X'

        neighbourRow = action.row
        neighbourColumn = action.column

        resultstate[neighbourRow][neighbourColumn] = current

        for rowDirection, columnDirection in rowColumnNeighbours:
            # check in the direction of every neighbouring node
            neighbourRow = action.row
            neighbourColumn = action.column

            neighbourRow += rowDirection
            neighbourColumn += columnDirection

            if self.outofrange(neighbourRow, neighbourColumn) == -1 or resultstate[neighbourRow][
                neighbourColumn] == current:
                continue

            # move in the direction as long as you keep encountering the opponents pawn
            # stop when you encounter anything else or out of range
            while self.outofrange(neighbourRow, neighbourColumn) == 1 and resultstate[neighbourRow][
                neighbourColumn] == opponentpawn:
                neighbourRow += rowDirection
                neighbourColumn += columnDirection

            if self.outofrange(neighbourRow, neighbourColumn) == 1 and resultstate[neighbourRow][
                neighbourColumn] == current:
                neighbourRow -= rowDirection
                neighbourColumn -= columnDirection

                while resultstate[neighbourRow][neighbourColumn] == opponentpawn:
                    # update state
                    resultstate[neighbourRow][neighbourColumn] = current
                    # update pawns
                    # iterate
                    neighbourRow -= rowDirection
                    neighbourColumn -= columnDirection

        return resultstate

    # state does not get altered by this method
    def getPossibleActions(self, state, currentplayer):

        actions = []
        if currentplayer == 'X':
            opponentpawn = 'O'
        else:
            opponentpawn = 'X'
        for row in range(0, 8, 1):
            for column in range(0, 8, 1):
                if state[row][column] == currentplayer:
                    for rowDirection, columnDirection in rowColumnNeighbours:
                        neighbourRow = copy.copy(row)
                        neighbourColumn = copy.copy(column)
                        neighbourRow += rowDirection
                        neighbourColumn += columnDirection
                        if (self.outofrange(neighbourRow, neighbourColumn) == -1 or state[neighbourRow][
                            neighbourColumn] != opponentpawn):
                            continue

                        if state[neighbourRow][neighbourColumn] == opponentpawn:
                            self.no_opponant = False
                        # move in the direction as long as you keep encountering the opponant's pawn and stop when you encounter anything else or out of range
                        while self.outofrange(neighbourRow, neighbourColumn) == 1 and state[neighbourRow][
                            neighbourColumn] == opponentpawn:
                            neighbourRow += rowDirection
                            neighbourColumn += columnDirection
                        duplicate = False
                        if self.outofrange(neighbourRow, neighbourColumn) == 1 and state[neighbourRow][
                            neighbourColumn] == '*':
                            for action in actions:
                                if action.row == neighbourRow and action.column == neighbourColumn:
                                    duplicate = True
                            if duplicate != True:
                                actions.append(Pawn(neighbourRow, neighbourColumn))
                                # if it is on board all pawns encountered till now must be changed
        return actions

    def cutoff_test(self, state, depth, currentplayer):
        if (depth == self.maxdepth):
            return -1
        return self.getPossibleActions(state, currentplayer)

    def node(self, nodevalue):
        if nodevalue == "root":
            return "root"
        elif nodevalue == "pass":
            return "pass"
        else:
            start = ord('a') - 1
            return chr(start + nodevalue.column + 1) + str(nodevalue.row + 1)

    def max_value(self, max_state, max_alpha, max_beta, max_depth, max_current_player, pass_turn):
        if max_current_player == 'X':
            min_opponent_player = 'O'
        else:
            min_opponent_player = 'X'

        validActions = self.cutoff_test(max_state, max_depth, max_current_player)
        terminal_node = self.moves_made[-1]

        v = float('-inf')

        # When depth==maxdepth
        if validActions == -1:
            self.print_move(self.node(terminal_node), max_depth, str(self.evaluate(max_state)),
                            max_alpha, max_beta)
            return self.evaluate(max_state)


        # When there are no possible actions in current state
        elif len(validActions) == 0:

            # When the previous turn was a pass too, terminate the game
            if pass_turn == True:

                self.print_move(self.node(terminal_node), max_depth, v, max_alpha, max_beta)

                v = self.evaluate(max_state)
                terminal_node = self.moves_made[-1]

                self.print_move(self.node(terminal_node), max_depth + 1, v, max_alpha, max_beta)

                if (v >= max_beta):
                    self.print_move(self.node(terminal_node), max_depth, v, max_alpha, max_beta)
                    return v

                max_alpha = max(max_alpha, v)
                self.print_move(self.node(terminal_node), max_depth, v, max_alpha, max_beta)
                return v

            # PASS MOVE
            self.print_move(self.node(terminal_node), max_depth, v, max_alpha, max_beta)

            self.moves_made.append("pass")
            v = self.min_value(max_state, max_alpha, max_beta, max_depth + 1, min_opponent_player, True)
            self.moves_made.pop()

            if (v >= max_beta):
                self.print_move(self.node(self.moves_made[-1]), max_depth, v, max_alpha, max_beta)
                return v

            max_alpha = max(max_alpha, v)
            self.print_move(self.node(self.moves_made[-1]), max_depth, v, max_alpha, max_beta)
            return v

        self.print_move(self.node(terminal_node), max_depth, v, max_alpha, max_beta)
        validActions = sorted(validActions, key=lambda a: (a.row, a.column))

        # When there are valid actions
        for action in validActions:

            self.moves_made.append(action)
            v = max(v, self.min_value(self.result(max_state, action, max_current_player),
                                      max_alpha, max_beta, max_depth + 1, min_opponent_player, False))
            self.moves_made.pop()

            if (v >= max_beta):
                self.print_move(self.node(self.moves_made[-1]), max_depth, v, max_alpha, max_beta)
                return v

            max_alpha = max(max_alpha, v)
            self.print_move(self.node(self.moves_made[-1]), max_depth, v, max_alpha, max_beta)

        return v

    def min_value(self, min_state, min_alpha, min_beta, min_depth, min_current_player, pass_turn):
        if min_current_player == 'X':
            max_opponent_player = 'O'
        else:
            max_opponent_player = 'X'

        self.no_opponant = False
        validActions = self.cutoff_test(min_state, min_depth, min_current_player)

        v = float('inf')
        terminal_node = self.moves_made[-1]

        # When depth==maxdepth
        if validActions == -1:
            self.print_move(self.node(terminal_node), min_depth, str(self.evaluate(min_state)), min_alpha,
                            min_beta)
            return self.evaluate(min_state)


        # When there are no valid moves
        elif len(validActions) == 0:

            # When the previous turn was a pass too, terminate the game
            if pass_turn == True:
                self.print_move(self.node(terminal_node), min_depth, v, min_alpha, min_beta)

                v = self.evaluate(min_state)
                terminal_node = self.moves_made[-1]
                self.print_move(self.node(terminal_node), min_depth + 1, v, min_alpha, min_beta)

                if (v <= min_alpha):
                    self.print_move(self.node(terminal_node), min_depth, v, min_alpha, min_beta)
                    return v

                min_beta = min(min_beta, v)
                self.print_move(self.node(terminal_node), min_depth, v, min_alpha, min_beta)
                return v

            # PASS MOVE
            self.print_move(self.node(terminal_node), min_depth, v, min_alpha, min_beta)

            self.moves_made.append("pass")
            v = self.max_value(min_state, min_alpha, min_beta, min_depth + 1, max_opponent_player, True)
            self.moves_made.pop()

            if (v <= min_alpha):
                self.print_move(self.node(self.moves_made[-1]), min_depth, v, min_alpha, min_beta)
                return v

            min_beta = min(min_beta, v)
            self.print_move(self.node(self.moves_made[-1]), min_depth, v, min_alpha, min_beta)

            return v

        # When there are valid actions
        self.print_move(self.node(terminal_node), min_depth, v, min_alpha, min_beta)
        validActions = sorted(validActions, key=lambda a: (a.row, a.column))
        for action in validActions:

            self.moves_made.append(action)
            v = min(v, self.max_value(self.result(min_state, action, min_current_player), min_alpha, min_beta,
                                      min_depth + 1, max_opponent_player, False))
            self.moves_made.pop()

            if (v <= min_alpha):
                self.print_move(self.node(self.moves_made[-1]), min_depth, v, min_alpha, min_beta)
                return v

            min_beta = min(min_beta, v)
            self.print_move(self.node(self.moves_made[-1]), min_depth, v, min_alpha, min_beta)

        return v

    def alpha_beta_search_next_move(self, state, max_alpha, max_beta, currentplayer):
        # Initialze start states

        depth = 0
        if currentplayer == 'X':
            min_opponent_player = 'O'
        else:
            min_opponent_player = 'X'
        self.moves_made.append("root")
        nextmove = None
        validActions = self.cutoff_test(state, depth, currentplayer)
        terminal_node = self.moves_made[-1]
        v = float('-inf')

        if validActions == -1:
            self.print_move(self.node(terminal_node), depth, str(self.evaluate(state)), max_alpha,
                            max_beta)
            return
        # When there are no valid moves
        if len(validActions) == 0:
            self.print_move(self.node(terminal_node), depth, v, max_alpha, max_beta)

            self.moves_made.append("pass")
            v = self.min_value(state, max_alpha, max_beta, depth + 1, min_opponent_player, True)
            self.moves_made.pop()

            if (v >= max_beta):
                self.print_move(self.node(self.moves_made[-1]), depth, v, max_alpha, max_beta)
                return

            max_alpha = max(max_alpha, v)
            self.print_move(self.node(self.moves_made[-1]), depth, v, max_alpha, max_beta)
            return

        self.print_move(self.node(terminal_node), depth, v, max_alpha, max_beta)
        validActions = sorted(validActions, key=lambda a: (a.row, a.column))
        possibleActions = self.getPossibleActions(state, currentplayer)

        v = float('-inf')
        possibleActions = sorted(possibleActions, key=lambda a: (a.row, a.column))
        for action in possibleActions:

            self.moves_made.append(action)
            value = self.min_value(self.result(state, action, currentplayer),
                                   max_alpha, max_beta, depth + 1, min_opponent_player, False)
            self.moves_made.pop()

            if v < value:
                v = value
                nextmove = action

            # Returns move in order of preference when there are multiple valid moves of same value
            elif v == value:
                if nextmove.row > action.row:
                    nextmove = action
                elif nextmove.row == action.row:
                    if nextmove.column > action.column:
                        nextmove = action

            # if (v >= max_beta):
            #     self.print_move(self.node(self.moves_made[-1]), depth, v, max_alpha, max_beta)
            #     return

            max_alpha = max(max_alpha, v)
            self.print_move(self.node(self.moves_made[-1]), depth, v, max_alpha, max_beta)

        return nextmove

    def output_results(self, resultant_state):
        result = ""
        for row in range(0, 8):
            for column in range(0, 8):
                result += resultant_state[row][column]
            result += "\n"
        return result

    def print_move(self, move, depth, v, alpha, beta):
        printmove = ""
        printmove += move + "," + str(depth) + "," + self.replace_inf_string(v) + "," + self.replace_inf_string(
            alpha) + "," + self.replace_inf_string(beta)
        self.moves_list.append(printmove)

    def replace_inf_string(self, val):
        if val == float('-inf'):
            return "-Infinity"
        elif val == float('inf'):
            return "Infinity"
        else:
            return str(val)

def main():
    # Read input
    rawinput = open('C:/aitest/input.txt', 'r')
    lines = rawinput.read().splitlines()
    currentplayer = lines[0]
    # depth = int(lines[1])
    maxdepth = int(lines[1])

    # Initialize state
    state = []
    for counter in range(2, rows + 2, 1):
        state.append(list(lines[counter]))

    # Start game
    game = Game(state, currentplayer, maxdepth)

    alpha = float('-inf')
    beta = float('inf')
    pawn = game.alpha_beta_search_next_move(state, alpha, beta, currentplayer)

    # Print Output
    f = open('output.txt', 'w')
    moves_pattern = "Node,Depth,Value,Alpha,Beta"
    if pawn == None:
        for ele in game.moves_list:
            game.addmoves(ele)
        print  game.output_results(state), moves_pattern, game.moves
        print >> f, game.output_results(state), moves_pattern, game.moves
    else:
        resultant_state = game.result(state, pawn, currentplayer)
        game.output_results(resultant_state)
        for ele in game.moves_list:
            game.addmoves(ele)
        print game.output_results(resultant_state), moves_pattern, game.moves
        print >> f, game.output_results(resultant_state), moves_pattern, game.moves


if __name__ == "__main__":
    main()
