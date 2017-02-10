import random
import math

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
        self.paddle_height = 0.2
        self.ball_x = ball_x if ball_x != None else 0.5
        self.ball_y = ball_y if ball_y != None else 0.5
        self.velocity_x = velocity_x if velocity_x != None else 0.03
        self.velocity_y = velocity_y if velocity_y != None else 0.01
        self.paddle_y = paddle_y if paddle_y != None else 0.5

        # boolean flags to generate rewards
        self.bounce = False
        self.miss = False
    
    def simulate_one_time_step(self, action_selected):
        '''
        :param action_selected - Current action to execute.
        Perform the action on the current continuous state.
        '''
        action_performed = self.actions[action_selected]
        self.paddle_y = min(1.0, max(0.0, self.paddle_y + action_performed))
        self.ball_x += self.velocity_x
        self.ball_y += self.velocity_y
        if self.ball_y<0:
            self.ball_y *= -1
            self.velocity_y *= -1
        elif self.ball_y>1:
            self.ball_y = 2-self.ball_y
            self.velocity_y *= -1
        if self.ball_x<0:
            self.ball_x *= -1
            self.velocity_x *= -1
        if self.ball_x>1:
            if self.ball_y>=self.paddle_y and self.ball_y<=self.paddle_y+self.paddle_height:
                self.velocity_x = -1*self.velocity_x+random.uniform(-0.015,0.015)
                self.velocity_y = self.velocity_y+random.uniform(-0.03,0.03)
                if abs(self.velocity_x)<0.3:
                    self.velocity_x = -0.3 if self.velocity_x<0 else 0.3
                if abs(self.velocity_x)>1:
                    self.velocity.x = -1 if self.velocity.x<0 else 1
                if abs(self.velocity_y)>1:
                    self.velocity.y = -1 if self.velocity.y<0 else 1
                self.bounce = True
            self.miss = True
        pass
    
    def discretize_state(self):
        '''
        Convert the current continuous state to a discrete state.
        '''
        #ball passed paddle
        if self.ball_x >1:
            return 10368

        ball_x = math.floor(self.ball_x*12)
        ball_y = math.floor(self.ball_y*12)
        vel_y = 1

        if self.velocity_y > 0.015:
            vel_y = 2
        elif self.velocity_y < -0.015:
            vel_y = 0

        vel_x = 1
        if self.velocity_x < 0:
            vel_x = 0

        paddle = math.floor(12*self.paddle_y/(1-self.paddle_height))

        index = 864*ball_x + 72*ball_y + 36*vel_x + 12*vel_y + paddle
        return int(index)