import random
import pickle

class QLearningAgent:
    def __init__(self):
        self.q_table = {}
        self.alpha = .05
        self.l = .9
        pass

    def learn(self, state, move, reward, future_reward):
        if state not in self.q_table:
            self.q_table[state] = {}
        
        if move not in self.q_table[state]:
            self.q_table[state][move] = 0.0

        self.q_table[state][move] = (1 - self.alpha) * self.q_table[state][move] + self.alpha * (reward + self.l * future_reward)
        pass

    def bestMove(self, state, moves, multiplier = 1):
        max_future = None
        best_move = None
        for m in moves:
            if state not in self.q_table:
                break
            if m in self.q_table[state] and (max_future == None or (self.q_table[state][m] * multiplier) > max_future):
                max_future = self.q_table[state][m] * multiplier
                best_move = m

        if best_move == None:
            max_future = 0
            best_move = random.choice(moves)

        return (max_future, best_move)

    def save(self, file_name):
        pickle.dump(self.q_table, open(file_name, "wb" ))

    def load(self, file_name):
        self.q_table = pickle.load(open(file_name, "rb" ))
