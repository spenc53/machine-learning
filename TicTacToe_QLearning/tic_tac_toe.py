PLAYER_ONE = 1
PLAYER_TWO = -1

class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [0 for _ in range(9)]
        self.currPlayer = PLAYER_ONE
        self.lastMove = -1

    def move(self, move):
        # assume that a move is 1 based
        move -= 1
        self.board[move] = self.currPlayer
        self.currPlayer = PLAYER_TWO if self.currPlayer == PLAYER_ONE else PLAYER_ONE
        self.lastMove = move

    def getMoves(self):
        validMoves = []
        for move in range(9):
            if self.board[move] == 0:
                validMoves.append(move)
        return validMoves

    def undoMove(self):
        self.board[self.lastMove] = 0
        self.currPlayer = PLAYER_TWO if self.currPlayer == PLAYER_ONE else PLAYER_ONE
        self.lastMove = -1

    def isDone(self):
        # check rows
        for y in range(3):
            total = 0
            for x in range(3):
                total += self.board[3 * y + x]
            
            if abs(total) == 3:
                if total > 0:
                    return PLAYER_ONE
                else:
                    return PLAYER_TWO
 
        # check columns
        for x in range(3):
            total = 0
            for y in range(3):
                total += self.board[3 * y + x]
            
            if abs(total) == 3:
                if total > 0:
                    return PLAYER_ONE
                else:
                    return PLAYER_TWO

        # 0, 4, 8
        # 3, 5, 7
        total = self.board[0] + self.board[4] + self.board[8]
        if abs(total) == 3:
                if total > 0:
                    return PLAYER_ONE
                else:
                    return PLAYER_TWO

        total = self.board[2] + self.board[4] + self.board[6]
        if abs(total) == 3:
                if total > 0:
                    return PLAYER_ONE
                else:
                    return PLAYER_TWO
        return 0

    def __str__(self):
        b = ""
        for y in range(3):
            for x in range(3):
                t = self.board[3 * y + x]
                b += "x" if t == PLAYER_ONE else "o" if t == PLAYER_TWO else str(3 * y + x + 1) if False else " "
                if x != 2:
                    b += "|"

            if y != 2:
                b += "\n"
                b += "-----"
                b += "\n"
        return b

    def repr(self):
        return ''.join(map(str, self.board))