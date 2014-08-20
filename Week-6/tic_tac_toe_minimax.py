"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def min_move(board, player):
    """
    To simulate PLAYERO's action in this game. Select the position with minimal score.  
    """
    best_score = 0
    best_pos = (-1, -1)
    empty_squares = board.get_empty_squares()
    for position in empty_squares:
        cur_board = board.clone()
        row, col = position
        cur_board.move(row, col, player)
        if player == cur_board.check_win():
            return SCORES[player], (row, col)
        elif provided.DRAW == cur_board.check_win():
            return SCORES[provided.DRAW], (row, col)
        else:
            score, dummy_pos = mm_move(cur_board, provided.switch_player(player))
            if best_pos == (-1, -1) or score <= best_score:
                best_score = score
                best_pos = position
    return best_score, best_pos

def max_move(board, player):
    """
    To simulate PLAYERX's action in this game. Select the position with maximal score. 
    """
    best_score = 0
    best_pos = (-1, -1)
    empty_squares = board.get_empty_squares()
    for position in empty_squares:
        cur_board = board.clone()
        row, col = position
        cur_board.move(row, col, player)
        if player == cur_board.check_win():
            return SCORES[player], (row, col)
        elif provided.DRAW == cur_board.check_win():
            return SCORES[provided.DRAW], (row, col)
        else:
            score, dummy_pos = min_move(cur_board, provided.switch_player(player))
            if best_pos == (-1, -1) or score >= best_score:
                best_score = score
                best_pos = position
    return best_score, best_pos

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    if player == provided.PLAYERX:
        best_score, best_pos = max_move(board, player)
    else:
        best_score, best_pos = min_move(board, player)
    return best_score, best_pos

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
