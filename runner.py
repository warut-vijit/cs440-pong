from Simulator.simulator import Simulator
import sys

if __name__ == "__main__":
    '''
    Runner code to start the training and game play.
    '''
    alpha_value = float(sys.argv[1]) #0.4
    gamma_value = float(sys.argv[2]) #0.95
    epsilon_value = float(sys.argv[3]) # 0.04
    num_games = 100000
    Simulator(num_games, alpha_value, gamma_value, epsilon_value)