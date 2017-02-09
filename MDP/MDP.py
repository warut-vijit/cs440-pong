class MDP:
    
    def __init__(self, 
                 ball_x=None,
                 ball_y=None,
                 velocity_x=None,
                 velocity_y=None,
                 paddle_y=None):
        '''
        Setup MDP with the initial values provided.
        '''
        self.create_state(
            ball_x=ball_x,
            ball_y=ball_y,
            velocity_x=velocity_x,
            velocity_y=velocity_y,
            paddle_y=paddle_y
        )
        
        # the agent can choose between 3 actions - stay, up or down respectively.
        self.actions = [0, 0.04, -0.04]
        
    
    def create_state(self,
              ball_x=None,
              ball_y=None,
              velocity_x=None,
              velocity_y=None,
              paddle_y=None):
        '''
        Helper function for the initializer. Initialize member variables with provided or default values.
        '''
        self.paddle_height = paddle_height if paddle_height != None else 0.2
        self.ball_x = ball_x if ball_x != None else 0.5
        self.ball_y = ball_y if ball_y != None else 0.5
        self.velocity_x = velocity_x if velocity_x != None else 0.03
        self.velocity_y = velocity_y if velocity_y != None else 0.01
        self.paddle_y = 0.5
    
    def simulate_one_time_step(self, action_selected):
        '''
        :param action_selected - Current action to execute.
        Perform the action on the current continuous state.
        '''
        action_performed = self.actions[action_selected]
        self.paddle_y = min(1.0, max(0.0, self.paddle_y + action_performed))
        self.ball_x = min(1.0, max(0.0, self.ball_x + self.velocity_x))
        self.ball_y = min(1.0, max(0.0, self.ball_y + self.velocity_y))
        self.velocity_x *= -1 if self.ball_x == 0.0 else 1
        self.velocity_y *= -1 if self.ball_y == 1.0 or self.ball_y == 0.0 else 1
        self.velocity_x *= -1 if abs(self.ball_y-self.paddle_y)<paddle_height/2 and self.else 1
        
        pass
    
    def discretize_state(self):
        '''
        Convert the current continuous state to a discrete state.
        '''
        # Your Code Goes Here!
        pass