"""
Mini-project for Principles of Computing Part 1. A machine Tic-Tac-Toe player by Monte Carlo simulation.
Written on: 18/09/2015
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 30         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
def mc_trial(board, player):
    """
    Function that takes a current board and the next player to move.
    Play a game by making random moves. Return the modified state of board
    """
    game_in_progress = True
    while game_in_progress:
        empty_squares = board.get_empty_squares()
        square = empty_squares[random.randrange(len(empty_squares))]
        board.move(square[0],square[1],player)
        game_in_progress = not board.check_win()
        player = provided.switch_player(player)
        
def mc_update_scores(scores, board, player):
    """
    Function that takes a grid of scores with the same dimensions as
    the TTT board, a board from a completed game, and which player the
    machine player is. Score the completed board and update the score grid
    """
    # Find the winner of the current game.
    winner = board.check_win()

    # The scoring logic:  
    # If the current player won the game, each square that matches
    # the current player should get a positive score (corresponding to
    # SCORE_CURRENT) and each square that matches the other player should
    # get a negative score (corresponding to -SCORE_OTHER).
    # Conversely, if the current player lost the game, each square that matches
    # the current player should get a negative score (-SCORE_CURRENT) and
    # each square that matches the other player should get a positive score
    #(SCORE_OTHER). All empty squares should get a score of 0.
    # If the game is a DRAW, all squares get a score of 0
    current_player = provided.switch_player(player)
    if winner == current_player:
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                square_occupant = board.square(row,col)
                if square_occupant == current_player:
                    scores[row][col] += SCORE_CURRENT
                elif square_occupant == player:
                    scores[row][col] -= SCORE_OTHER
    elif winner == player:   
        for row in range(board.get_dim()):
            for col in range(board.get_dim()):
                square_occupant = board.square(row,col)
                if square_occupant == current_player:
                    scores[row][col] -= SCORE_CURRENT
                elif square_occupant == player:
                    scores[row][col] += SCORE_OTHER 

def get_best_move(board, scores):
    """
    Takes a current board and a grid of scores. Find all the empty squares with
    the maximum score and randomly return one of them as (row, column) tuple.
    It is an error to call this function if the board has no empty squares
    """
    # Find the list of all empty squares
    empty_squares = board.get_empty_squares()
    # Get the maximum score over all empty squares and store the square index
    ix_maxscore = []
    maxscore = -50
    for square_ix in empty_squares:
        current_score = scores[square_ix[0]][square_ix[1]]
        if current_score > maxscore:
            maxscore = current_score
            ix_maxscore = []                # Discard all stored squares so far
            ix_maxscore.append(square_ix)   # Then store the square of current max
        elif current_score == maxscore:
            ix_maxscore.append(square_ix)   # maxscore hasn't changed. Just append another square
    
    # Return one of the squares with maxscore
    return ix_maxscore[random.randrange(len(ix_maxscore))]

def mc_move(board, player, trials):
    """
    Takes a current board, which player the machine player is, and the number
    of trials to run. Use Monte Carlo simulation to return a move for the machine
    player. Returns a (row, column) tuple
    """
    
    # Initialize the score board
    scores = [[0] * board.get_dim() for dummy in range(board.get_dim())]
    
    # Generate trial and update scores
    for dummy_trial in range(trials):
        board_copy = board.clone()                   # Make a copy of the original board 
        mc_trial(board_copy, player)                 # Play a trial 
        mc_update_scores(scores, board_copy, player)  # Then update the score board

    return get_best_move(board, scores)    

# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
