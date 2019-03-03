_board_template_ = ''' %d | %d | %d \n''' + \
                   '''---+---+---\n''' + \
                   ''' %d | %d | %d \n''' + \
                   '''---+---+---\n''' + \
                   ''' %d | %d | %d \n'''

class Player:
    def __init__(self,name):
        self.name = name
        self.wins = 0

    def print_player(self):
        print('%s has %d wins!' % (self.name,self.wins))

class Square:
    def __init__(self):
        self.state = 0

    def is_blank(self):
        return not self.state

    def reset(self):
        self.state = 0

    def mark(self,player):
        self.state = player

    def get_mark(self):
        return self.state

class Board:
    def __init__(self):
        self.squares = [Square() for ii in range(9)]
        self.winning_combos = []
        self.winning_combos.extend(
            [[self.squares[ii],self.squares[ii+1],self.squares[ii+2]]
             for ii in [0,3,6]])
        self.winning_combos.extend(
            [[self.squares[ii],self.squares[ii+3],self.squares[ii+6]]
             for ii in [0,1,2]])
        self.winning_combos.extend(
            [[self.squares[0],self.squares[4],self.squares[8]],
             [self.squares[2],self.squares[4],self.squares[6]]])

    def reset(self):
        for square in self.squares:
            square.reset()

    def get_marks(self):
        marks = [square.get_mark() for square in self.squares]
        return tuple(marks)

    def display_board(self):
        print(_board_template_ % self.get_marks())

    def did_someone_win(self):
        for combo in self.winning_combos:
            if all(square.get_mark() == 1 for square in combo):
                return 1
            if all(square.get_mark() == 2 for square in combo):
                return 2
        return 0

    def is_board_full(self):
        return all([not square.is_blank() for square in self.squares])

class TicTacToeController:
    def __init__(self):
        self.board = Board()
        self.players = [[],[],[]]
        self.players[1] = Player(input('Welcome player #1! What is your name? '))
        self.players[2] = Player(input('Welcome player #2! What is your name? '))
        self.print_instructions()
        self.start_game()

    def print_instructions(self):
        print('On your turn, enter a square number 0-8, corresponding to this grid')
        print(_board_template_ % tuple(range(9)))
        print('Press <ctrl>-C to quit')
        print()

    def start_game(self):
        Player(input('Press <enter> to play a new game!'))
        self.whose_turn = 1
        self.board.reset()
        self.next_move()

    def prompt_for_move(self):
        self.board.display_board()
        while True:
            move = input('%s, please enter your move: ' %
                         (self.players[self.whose_turn].name))
            try:
                move = int(move)
                if move < 0 or move > 8:
                    raise ValueError('Move must be between 0 and 8!')
                if not self.board.squares[move].is_blank():
                    raise ValueError('This square is already full!')
                return move
            except ValueError as e:
                print('Invalid move: %s' % e)
                print('Please try again...')

    def print_wins(self):
        [player.print_player() for player in self.players[1:]]

    def handle_win(self):
        print('Congrats to %s!' % self.players[self.whose_turn].name)
        self.players[self.whose_turn].wins += 1
        self.print_wins()
        self.start_game()

    def handle_draw(self):
        print('Cat game!')
        self.print_wins()
        self.start_game()

    def next_move(self):
        move = self.prompt_for_move()
        self.board.squares[move].mark(self.whose_turn)
        if self.board.did_someone_win():
            self.handle_win()
        elif self.board.is_board_full():
            self.handle_draw()
        else:
            self.whose_turn = (self.whose_turn%2) + 1
            self.next_move()
        

if __name__ == '__main__':
    try:
        TicTacToeController()
    except KeyboardInterrupt:
        pass
