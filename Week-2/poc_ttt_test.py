"""
Test suite for Tic-Tac-Toe.
"""

from poc_simpletest import TestSuite
import poc_ttt_template as tic_tac_toe
import poc_ttt_provided as provided

def run_test():
    """
    Run the test suite of Tic-Tac-Toe.
    """

    suite = TestSuite()

    board = provided.TTTBoard(3)
    scores = [[0 for dummy_col in range(3)] for dummy_row in range(3)]

    mc_trial = tic_tac_toe.mc_trial
    mc_update_scores = tic_tac_toe.mc_update_scores
    get_best_move = tic_tac_toe.get_best_move
    mc_move = tic_tac_toe.mc_move

    for dummy in range(3):
        board_clone = board.clone()
        mc_trial(board_clone, provided.PLAYERX)
        suite.run_test(board_clone.check_win() != None, True, \
            "Test #1: mc_trial")
        print board_clone

        mc_update_scores(scores, board_clone, provided.PLAYERX)
        print scores

    best_move = get_best_move(board, scores)
    print best_move

    move = mc_move(board, provided.PLAYERX, 3)
    print move

    board = provided.TTTBoard(3, False, \
        [[provided.PLAYERX, provided.EMPTY, provided.EMPTY], \
        [provided.PLAYERO, provided.PLAYERO, provided.EMPTY], \
        [provided.EMPTY, provided.PLAYERX, provided.EMPTY]])
    print board
    print mc_move(board, provided.PLAYERX, tic_tac_toe.NTRIALS)

    suite.report_results()

run_test()
