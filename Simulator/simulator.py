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
        self.gamma_val = gamma_value
        self.q_array = [] # array of q values, length 10369 
        
        # Your Code Goes Here
    
    def f_function(self):
        '''
        Choose action based on an epsilon greedy approach
        :return action selected
        '''
        action_selected = None
        
        # Your Code Goes Here!
        
        return action_selected

    def train_agent(self):
        '''
        Train the agent over a certain number of games.
        '''
        # Your Code Goes Here!
        pass
    
    def play_game(self):
        '''
        Simulate an actual game till the agent loses.
        '''
        game = MDP(ball_x=0.5,ball_y=0.5,velocity_x=0.03,velocity_y=0.01,paddle_y=0.4)
        while not game.miss: # while paddle has not missed
            
        pass