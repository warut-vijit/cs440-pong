import random
from MDP.MDP import MDP


class Simulator:
    
    def __init__(self, num_games=0, alpha_value=0, gamma_value=0, epsilon_value=0, granularity=0):
        '''
        Setup the Simulator with the provided values.
        :param num_games - number of games to be trained on.
        :param alpha_value - 1/alpha_value is the decay constant.
        :param gamma_value - Discount Factor.
        :param epsilon_value - Probability value for the epsilon-greedy approach.
        '''
        self.num_games = num_games       
        self.epsilon_value = epsilon_value       
        self.alpha_value = alpha_value       
        self.gamma_value = gamma_value
        self.q_array = [[0.0] * 10369 for action in range(3)] # 2d array of q values, length 10369, with 3 actions 
        self.q_succ = [ [[] for tile in range(10369)]  for action in range(3)] # 2d array of successors
        
        self.train_agent()
    
    def f_function(self, state, q):
        '''
        Choose action based on an epsilon greedy approach
        :return action selected
        '''
        action_selected = 0
        if random.random()<=self.epsilon_value or (q[0][state] == q[1][state] and q[0][state] == q[2][state]): # exploring
            action_selected = random.randint(0,2)
        else: 
            if q[0][state]>q[1][state] and q[0][state]>q[2][state]:
                action_selected = 0
            elif q[1][state]>q[2][state]:
                action_selected = 1
            else:
                action_selected = 2
        return action_selected

    def train_agent(self):
        '''
        Train the agent over a certain number of games.
        '''
        for x in range(self.num_games):
            self.play_game()
        self.epsilon_value=0
        sum = 0
        for i in xrange(5):
            sum += self.play_game()
        print sum
        pos = 0
        neg = 0
        for x in self.q_array:
            for y in x:
                if y>0:
                    pos+=1
                elif y<0:
                    neg+=1
        print str(pos)+" -- "+str(neg)+" -- "+str(10368*3-pos-neg)
        #for action in range(3):
        #    for x in range(11*864,11*864+863):
        #        if self.q_array[action][x]>0:
        #            print self.q_array[action][x]
        pass

    def update_q(self, state_log):
        '''
        Update value of q given game state
        '''
        successor_state = 10368
        while len(state_log) > 0: # while states remain
            current_entry = state_log.pop() # type tuple (state number, action, reward)
            action = current_entry[1]
            state = current_entry[0]
            reward = current_entry[2]
            #print current_entry
            # compute average of rewards as a result of this state and action
            if successor_state not in self.q_succ[action][state]:
                self.q_succ[action][state].append(successor_state) # mark this next state as a possible successor

            # compute simple (later weighted?) average of successors
            sum_still = sum([ self.q_array[0][next_state] for next_state in self.q_succ[0][state] ])/len(self.q_succ[0][state]) if len(self.q_succ[0][state])>0 else 0  # assumes for simplicity that next action will be same as this one
            sum_up = sum([ self.q_array[1][next_state] for next_state in self.q_succ[1][state] ])/len(self.q_succ[1][state]) if len(self.q_succ[1][state])>0 else 0
            sum_down = sum([ self.q_array[2][next_state] for next_state in self.q_succ[2][state] ])/len(self.q_succ[2][state]) if len(self.q_succ[2][state])>0 else 0
            max_successor = max(sum_still, sum_up, sum_down)
            #if self.epsilon_value==0:
            #    print self.q_array[0][current_entry[0]]
            #    print self.q_array[1][current_entry[0]]
            #    print self.q_array[2][current_entry[0]]
            #    print current_entry
            #    print ""
            value = reward + self.gamma_value*max_successor - self.q_array[action][state]
            self.q_array[action][state] = self.q_array[action][state] + self.alpha_value * value
            successor_state = state # store current state as successor of predecessor

    def play_game(self):
        '''
        Simulate an actual game till the agent loses.
        '''
        #apply rewards and stuff
        state_log = []
        bounces = 0
        game = MDP(ball_x=0.5,ball_y=0.5,velocity_x=0.03,velocity_y=0.01,paddle_y=0.4)
        #if self.epsilon_value == 0:
        #    game = MDP(ball_x=0.5,ball_y=0.5,velocity_x=0.03,velocity_y=0.01,paddle_y=0.4)
        #else:
        #    game = MDP(ball_x=random.uniform(0,1),ball_y=random.uniform(0,1),velocity_x=random.uniform(-0.2,0.2),velocity_y=random.uniform(-0.2,0.2),paddle_y=random.uniform(0,0.8))
        while True: # while paddle has not missed
            action = self.f_function(game.discretize_state(), self.q_array) # get action given current state, q array
            game.simulate_one_time_step(action) # advance one step
            if game.bounce: # if paddle bounced
                state_log.append( (game.discretize_state(), action, 1) )
                game.bounce = False
                bounces+=1
            elif not game.discretize_state()==10368: # neutral state
                state_log.append( (game.discretize_state(), action, 0) )
            else: # loss
                state_log.append( (game.discretize_state(), action, -1) )
                break
        self.update_q(state_log)
        if self.epsilon_value == 0:
            return bounces
        return