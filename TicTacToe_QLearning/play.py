from agent import QLearningAgent
from tic_tac_toe import TicTacToe
import random
import json

def getMove(board, moves, player, random_rate):
    board_state = board.repr()
    q_table = player.q_table
    if random.random() < random_rate or board_state not in q_table:
        move = random.choices(moves)[0]
    else:
        # get best move
        action_map = q_table[board.repr()]
        move = -1
        best_val = -999
        # check all moves
        for m in moves:
            if m not in action_map:
                continue
            
            if action_map[m] > best_val:
                move = m
                best_val = action_map[m]

        if move == -1:
            move = random.choices(moves)[0]

    return move

playerOneAgent = QLearningAgent()
playerTwoAgent = QLearningAgent()
playerOneAgent.load('playerOneData_500k.pkl')
playerTwoAgent.load('playerTwoData_500k.pkl')

playerOneAgent.q_table

# with open('playerOneData_500k.json', 'w') as f:
#     json.dump(playerOneAgent.q_table, f)

# with open('playerTwoData_500k.json', 'w') as f:
#     json.dump(playerTwoAgent.q_table, f)

board = TicTacToe()
while not board.isDone() and len(board.getMoves()) != 0:
    moves = board.getMoves()
    move = getMove(board, moves, playerOneAgent, 0)
    board.move(move + 1)
    print(board)

    if board.isDone() or len(board.getMoves()) == 0:
        break

    moves = board.getMoves()
    move = int(input("move: "))
    board.move(move)
    print(board)

board = TicTacToe()
while not board.isDone() and len(board.getMoves()) != 0:
    print(board)
    moves = board.getMoves()
    move = int(input("move: "))
    board.move(move)
    print(board)

    if board.isDone() or len(board.getMoves()) == 0:
        break

    moves = board.getMoves()
    move = getMove(board, moves, playerTwoAgent, 0)
    board.move(move + 1)
    print(board)