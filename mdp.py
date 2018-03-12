"""AI Assignment 2."""
import sys, copy

class MDP:
    def __init__(self, board, end_states, walls, start_state, step_reward, policy):
        "Initializing the MDP."
        self.board = board;
        self.old_board = copy.deepcopy(self.board);
        self.end_states = end_states;
        self.walls = walls;
        self.start_state = start_state;
        self.step_reward = step_reward;
        self.policy = policy
        self.probability = {
        'target' : 0.8,
        'alt':     0.1,
        }
        self.delta = 0.01
        self.init_board()
        self.init_policy()
        self.value_iteration()
        self.policy()

    def init_board(self):
        """Initializing the board with the walls. Replacing walls with NaN."""
        for i in range(len(self.walls)):
            x, y = self.walls[i]
            self.board[x][y] = "NaN"

    def init_policy(self):
        """Initializing policy for the board."""
        for i in range(len(self.end_states)):
            x, y = self.end_states[i]
            if self.board[x][y] > 0:
                self.policy[x][y] = "Goal"
            else:
                self.policy[x][y] = "Bad"

    def value_iteration(self):
        """Applying value iteration algorithm on the board."""
        while True:
            changed_pairs = []
            for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if (i, j) not in self.walls and (i, j) not in self.end_states:
                            # print('Iteration %d' % int(i + 1))
                            # print('Estimating S(%d,%d)' % (i, j))
                            self.board[i][j] = self.update((i, j))
                            changed_pairs.append((self.board[i][j]-self.old_board[i][j])/self.old_board[i][j])

            # Adding code to check if change is less than delta and then terminate
            if max(list) <= self.delta:
                return

    def update(self, state):
        """Bellman update step."""

        # curVal represents the current utility of the state
        curVal = self.old_board[state[0]][state[1]]

        # Initializing value array for neighbours
        val = [0 for i in range(4)]
        # Value of neighbour above
        val.append(self.get_state_utility(curVal, tuple((state[0], state[1]+1))))
        # Value of neighbour below
        val.append(self.get_state_utility(curVal, tuple((state[0], state[1]-1))))
        # Value of neighbour on the left
        val.append(self.get_state_utility(curVal, tuple((state[0]-1, state[1]))))
        # Value of neighbour on the right
        val.append(self.get_state_utility(curVal, tuple((state[0]+1, state[1]))))

        val[0] = val[0]*self.probability['target'] + (val[2]+val[3])*self.probability['alt']
        val[1] = val[1]*self.probability['target'] + (val[2]+val[3])*self.probability['alt']
        val[2] = val[2]*self.probability['target'] + (val[0]+val[1])*self.probability['alt']
        val[3] = val[3]*self.probability['target'] + (val[0]+val[1])*self.probability['alt']

        # Discount factor is taken as 1 in this step.
        return self.step_reward + max(val)

    def get_state_utility(self, curVal, state):
        """Get utility of a state from old board after checking if state is valid."""
        x, y = state
        if x < 0 or y < 0 or x>len(self.old_board) or y>len(self.old_board[0]) or self.board[x][y]==0:
            # Hit the edge of the board, return value of initial state from which
            # function was called.
            return float(curVal)
        return float(self.old_board[x][y])

    def get_state_policy(self, curVal, state):
        """Get policy of a state from old board after checking if state is valid."""
        x, y = state
        if x < 0 or y < 0 or x>len(self.old_board) or y>len(self.old_board[0]) or self.board[x][y]==0:
            # Hit the edge of the board, return value of initial state from which
            # function was called.
            return float(curVal)

        return float(self.board[x][y])

    def policy(self):
        """Setting the policy after completion of value iteration."""

        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                if tuple(i, j) not in self.walls and tuple(i, j) not in self.end_states:

                    # curVal represents the current policy of the state
                    curVal = self.board[i][j]

                    # Initializing value array for neighbours
                    val = [0 for k in range(4)]
                    # Value of neighbour above
                    val.append(self.get_state_policy(curVal, tuple((i, j+1))))
                    # Value of neighbour below
                    val.append(self.get_state_policy(curVal, tuple((i, j-1))))
                    # Value of neighbour on the left
                    val.append(self.get_state_policy(curVal, tuple((i-1, j))))
                    # Value of neighbour on the right
                    val.append(self.get_state_policy(curVal, tuple((i+1, j))))

                    val[0] = val[0]*self.probability['target'] + (val[2]+val[3])*self.probability['alt']
                    val[1] = val[1]*self.probability['target'] + (val[2]+val[3])*self.probability['alt']
                    val[2] = val[2]*self.probability['target'] + (val[0]+val[1])*self.probability['alt']
                    val[3] = val[3]*self.probability['target'] + (val[0]+val[1])*self.probability['alt']

                    maxIndex = -1
                    for k in range(4):
                        if max(val) == val[k]:
                            maxIndex = k

                    self.policy[i][j] = k+1
                    self.print_policy()

    def print_policy(self):
        for i in range(len(self.policy)):
            for j in range(len(self.policy[i])):
                sys.stdout.write(self.policy[i][j])
            print


if __name__ == '__main__':

    # Taking input for size of board
    inp = raw_input()
    inp = inp.split()
    n = int(inp[0])
    m = int(inp[1])

    # Initializing board with 0
    board = [[0 for i in range(m)] for j in range(n)]

    # Initializing policy
    policy = [["NaN" for i in range(m)] for j in range(n)]

    # Taking row wise input
    for i in range(n):
        rows = raw_input()
        rows = rows.split()
        for j in range(m):
            board[i][j] = rows[j]

    # Taking input for e and w, number of end states and number of walls
    inp = raw_input()
    inp = inp.split()
    e = int(inp[0])
    w = int(inp[1])

    # Initializing end states and walls arrays
    end_states = []
    walls = []

    # Taking input for all end states
    for i in range(e):
        inp = raw_input()
        inp = inp.split()
        end_states.append(tuple((int(inp[0]), int(inp[1]))))

    # Taking input for all walls
    for i in range(w):
        inp = raw_input()
        inp = inp.split()
        walls.append(tuple((int(inp[0]), int(inp[1]))))

    # Taking input for start state
    inp = raw_input()
    inp = inp.split()

    start = tuple((inp[0], inp[1]))

    # Taking input for unit step reward
    unit_step_reward = float(raw_input())

    m = MDP(board, end_states, walls, start, unit_step_reward, policy)
