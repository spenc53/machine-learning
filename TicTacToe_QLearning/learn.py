from agent import QLearningAgent
from tic_tac_toe import TicTacToe
import random
from tqdm import tqdm

playerOneAgent = QLearningAgent()
playerTwoAgent = QLearningAgent()

# helper funciton to get a move from a player
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

# initial random move rate
random_move_rate = 1

for i in tqdm(range(0, 500000)):

    # update how frequently random moves are chosen based on how many games have been played
    if i == 5000:
        random_move_rate = .5
    if i == 10000:
        random_move_rate = .1
    if i == 400000:
        random_move_rate = .01

    # create a new game
    board = TicTacToe()

    # Player 1 learning loop
    while not board.isDone() and len(board.getMoves()) != 0:

        # Get player 1's move and play it
        moves = board.getMoves()
        move = getMove(board, moves, playerOneAgent, random_move_rate)
        
        old_board_state = board.repr()
        board.move(move + 1)

        # player 2 needs to make a move if the game is not over
        if not board.isDone() and not len(board.getMoves()) == 0:
            opp_move = getMove(board, board.getMoves(), playerTwoAgent, random_move_rate)
            board.move(opp_move + 1)

        # get the board's reward
        reward = board.isDone()

        # if the game is done, there are no future moves and thus the future reward is 0
        if board.isDone() or len(board.getMoves()) == 0:
            future_reward = 0
        else:
            future_reward = playerOneAgent.bestMove(board.repr(), board.getMoves())[0]

        # Give the player one agent the information that it needs to udpate it's q-value table
        playerOneAgent.learn(old_board_state, move, reward, future_reward)

    
    # create a new game for player 2 to learn
    board = TicTacToe()

    # since player 2 plays second, the initial board they get need to have player 1 played already
    opp_move = getMove(board, board.getMoves(), playerOneAgent, random_move_rate)
    board.move(opp_move + 1)

    # Player 2 learning loop
    while not board.isDone() and len(board.getMoves()) != 0:
        # Get player 2's move
        moves = board.getMoves()
        move = getMove(board, moves, playerTwoAgent, random_move_rate)
        
        old_board_state = board.repr()
        board.move(move + 1)

        # if the game isn't over, let player 1 play
        if not board.isDone() and not len(board.getMoves()) == 0:
            opp_move = getMove(board, board.getMoves(), playerOneAgent, random_move_rate)
            board.move(opp_move + 1)

        # we inverse the reward for player 2 because -1 means player 2 won
        reward = board.isDone() * -1

        # if the game is over, the max future reward is 0 since there are no future games
        if board.isDone() or len(board.getMoves()) == 0:
            future_reward = 0
        else:
            future_reward = playerTwoAgent.bestMove(board.repr(), board.getMoves())[0]

        # give player 2 the information it needs to learn
        playerTwoAgent.learn(old_board_state, move, reward, future_reward)

# Save the player information
playerOneAgent.save("playerOneData_500k.pkl")
playerTwoAgent.save("playerTwoData_500k.pkl")

# See player 1 play player 2
board = TicTacToe()
while not board.isDone() and len(board.getMoves()) != 0:
    moves = board.getMoves()
    move = getMove(board, moves, playerOneAgent, 0)
    board.move(move + 1)
    print(board)

    if board.isDone() or len(board.getMoves()) == 0:
        break

    moves = board.getMoves()
    move = getMove(board, moves, playerTwoAgent, 0)
    board.move(move + 1)
    print(board)

print(board)

# After done training, you can play against player 1.
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