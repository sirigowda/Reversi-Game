import constants
import properties
import Reversi

def main():
    # Read input
    rawinput = open(properties.INPUT_FILE_PATH, 'r')
    lines = rawinput.read().splitlines()
    currentplayer = lines[0]
    maxdepth = int(lines[1])

    # Initialize state
    state = []
    for counter in range(2, constants.ROWS + 2, 1):
        state.append(list(lines[counter]))

    # Start game
    game = Reversi.Reversi(state, currentplayer, maxdepth)

    alpha = float('-inf')
    beta = float('inf')
    pawn = game.alpha_beta_search_next_move(state, alpha, beta, currentplayer)

    # Print Output
    f = open(properties.OUTPUT_FILE_PATH, 'w')
    moves_pattern = "Node,Depth,Value,Alpha,Beta"
    if pawn == None:
        for ele in game.moves_list:
            game.add_moves(ele)
        print  game.output_results(state), moves_pattern, game.moves
        print >> f, game.output_results(state), moves_pattern, game.moves
    else:
        resultant_state = game.result(state, pawn, currentplayer)
        game.output_results(resultant_state)
        for ele in game.moves_list:
            game.add_moves(ele)
        print game.output_results(resultant_state), moves_pattern, game.moves
        print >> f, game.output_results(resultant_state), moves_pattern, game.moves

if __name__ == "__main__":
    main()