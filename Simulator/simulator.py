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
        self.q_succ = [ [[0.0,0] for tile in range(10369)]  for action in range(3)] # 2d array of successors
        
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
        max_bounces = 0
        games =0
        for x in range(self.num_games):
            bounce = self.play_game()
            games+=1
            if bounce >max_bounces:
                max_bounces=bounce
                if max_bounces >10:
                    break
        self.epsilon_value=0
        bounce = self.play_game()
        if bounce >max_bounces:
            max_bounces=bounce
        print max_bounces
        pass

    def update_q(self, state_log):
        '''
        Update value of q given game state
        '''
        successor_state = 10368
        successor_reward = -1
        while len(state_log) > 0: # while states remain
            current_entry = state_log.pop() # type tuple (state number, action, reward)
            #print current_entry
            # compute average of rewards as a result of this state
            self.q_succ[ current_entry[1] ][ current_entry[0] ][0]=(successor_reward + self.q_succ[ current_entry[1] ][ current_entry[0] ][0] * self.q_succ[ current_entry[1] ][ current_entry[0] ][1]) / (self.q_succ[ current_entry[1] ][ current_entry[0] ][1]+1)
            self.q_succ[ current_entry[1] ][ current_entry[0] ][1]+=1

            max_successor = max(self.q_succ[0][current_entry[0]][0], self.q_succ[1][ current_entry[0] ][0], self.q_succ[2][current_entry[0]][0])
            #if self.epsilon_value==0:
            #    print self.q_array[0][current_entry[0]]
            #    print self.q_array[1][current_entry[0]]
            #    print self.q_array[2][current_entry[0]]
            #    print current_entry
            #    print ""
            value = current_entry[2] + self.gamma_value*max_successor - self.q_array[ current_entry[1] ][ current_entry[0] ]
            self.q_array[ current_entry[1] ][ current_entry[0] ] = self.q_array[ current_entry[1] ][ current_entry[0] ] + self.alpha_value * value
            successor_state = current_entry[0]
            successor_reward = self.q_array[ current_entry[1] ][ current_entry[0] ] # store current state as successor of predecessor

    def play_game(self):
        '''
        Simulate an actual game till the agent loses.
        '''
        #apply rewards and stuff
        state_log = []
        bounces = 0
        game = MDP(ball_x=0.5,ball_y=0.5,velocity_x=0.03,velocity_y=0.01,paddle_y=0.4) #MDP(ball_x=random.uniform(0,1),ball_y=random.uniform(0,1),velocity_x=random.uniform(-0.2,0.2),velocity_y=random.uniform(-0.2,0.2),paddle_y=random.uniform(0,0.8))
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
        return bounces
        pass