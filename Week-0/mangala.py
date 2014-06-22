lass SolitaireMancala:

    def __init__(self):
        self.board = [0]

    def set_board(self, configuration):
        self.board = list(configuration)
        return self

    def get_num_seeds(self, house_num):
        return self.board[house_num]

    def is_legal_move(self, house_num):
        if house_num == 0:
            return False
        return self.board[house_num] == house_num

    def apply_move(self, house_num):
        if not self.is_legal_move(house_num):
            return self
        for i in range(house_num):
            self.board[i] += 1
        self.board[house_num] = 0
        return self

    def choose_move(self):
        for house_num in range(len(self.board)):
            if self.is_legal_move(house_num):
                return house_num
        return 0

    def is_game_won(self):
        return sum(self.board[1:]) == 0

    def plan_moves(self):
        moves = []
        backup_board = list(self.board)
        while True:
            house_num = self.choose_move()
            if house_num == 0:
                break
            else:
                moves.append(house_num)
                self.apply_move(house_num)
        self.set_board(backup_board)
        return moves

    def __str__(self):
        reversed_board = [self.board[i] for i in range(len(self.board)-1, -1, -1)]
        return str(reversed_board)

# import poc_mancala_testsuite
# poc_mancala_testsuite.run_test(SolitaireMancala)

# import poc_mancala_gui
# poc_mancala_gui.run_gui(SolitaireMancala())
