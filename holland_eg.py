from pybrain3.rl.environments.environment import Environment
from pybrain3.rl.environments.task import Task
from numpy import *
from pybrain3.rl.learners.valuebased import ActionValueTable
from pybrain3.rl.agents import LearningAgent
from pybrain3.rl.learners import Q
from pybrain3.rl.experiments import Experiment
from pybrain3.rl.explorers import EpsilonGreedyExplorer
from snake import Game
import pygame
from random import random, choice


class SnakeEnv(Environment):
    """ A (terribly simplified) Blackjack game implementation of an environment. """

    def __init__(self, indim, outdim):
        super().__init__()
        """ All tasks are coupled to an environment. """
        # the number of action values the environment accepts
        self.indim = indim

        # the number of sensor values the environment produces
        self.outdim = outdim

        self.game = None

        self.running = True
        self.numActions = 4
        self.allActions = [
            pygame.K_UP,
            pygame.K_DOWN,
            pygame.K_RIGHT,
            pygame.K_LEFT
        ]

        self.stochAction = 0.

        self.apple_distance = 0.
        self.apple_change = 0.

    def init_game(self, snake_size):
        self.game = Game()
        self.game.init_game(snake_size)
        self.running = True

    def getSensors(self):
        """ the currently visible state of the world (the    observation may be stochastic - repeated calls returning different values)
            :rtype: by default, this is assumed to be a numpy array of doubles
        """
        self.apple_distance = self.game.get_apple_distance()
        state = self.game.get_current_state()
        print(state)
        index = 9 * state["left"] + 3 * state["forward"] + state["right"]
        print(index)
        return [float(index), ]

    def performAction(self, action):
        """ perform an action on the world that changes it's internal state (maybe stochastically).
            :key action: an action that should be executed in the Environment.
            :type action: by default, this is assumed to be a numpy array of doubles
        """
        action = int(action[0])
        if self.stochAction > 0:
            if random() < self.stochAction:
                print(random())
                action = choice(list(range(len(self.allActions))))
        keydown = self.allActions[action]

        self.game.update_frame(keydown)
        if self.game.info["done"]:
            self.running = False
            return self.running

        self.apple_change = self.apple_distance - self.game.get_apple_distance()

        self.game.render()

        if action == 0:
            print("up")
        if action == 1:
            print("down")
        if action == 2:
            print("right")
        if action == 3:
            print("left")

    def reset(self):
        """ Most environments will implement this optional method that allows for reinitialization.
        """


class BlackjackTask(Task):
    """ A task is associating a purpose with an environment. It decides how to evaluate the observations, potentially returning reinforcement rewards or fitness values.
    Furthermore it is a filter for what should be visible to the agent.
    Also, it can potentially act as a filter on how actions are transmitted to the environment. """

    def __init__(self, environment):
        super().__init__(environment)
        """ All tasks are coupled to an environment. """
        self.env = environment
        # we will store the last reward given, remember that "r" in the Q learning formula is the one from the last interaction, not the one given for the current interaction!
        self.lastreward = 0
        self.no_apple = 0

    def performAction(self, action):
        """ A filtered mapping towards performAction of the underlying environment. """
        self.env.performAction(action)

    def getObservation(self):
        """ A filtered mapping to getSample of the underlying environment. """
        sensors = self.env.getSensors()
        return sensors

    def getReward(self):
        """ Compute and return the current reward (i.e. corresponding to the last action performed) """
        #if self.no_apple > 100:
        #    self.env.running = False

        if not self.env.running:
            reward = -1.
            self.no_apple = 0
        elif self.env.game.snake_ate_apple:
            reward = 1
            self.no_apple = 0
        else:
            reward = 1 - (self.env.apple_distance / 1064) - (0.01 * self.no_apple)
            self.no_apple += 1

        # retrieve last reward, and save current given reward
        cur_reward = self.lastreward
        self.lastreward = reward

        print(reward)

        return cur_reward

    @property
    def indim(self):
        return self.env.indim

    @property
    def outdim(self):
        return self.env.outdim



# define action-value table
# number of states is:
#
#    current value: 1-21
#
# number of actions:
#
#    Stand=0, Hit=1

av_table = ActionValueTable(27, 4)
av_table.initialize(2.)

game = Game()

# define Q-learning agent
learner = Q(0.5, 0.2)
learner._setExplorer(EpsilonGreedyExplorer(0.0))
agent = LearningAgent(av_table, learner)

# define the environment
env = SnakeEnv(4, 27)
env.init_game(15)

# define the task
task = BlackjackTask(env)

# finally, define experiment
experiment = Experiment(task, agent)

# ready to go, start the process
while True:
    print(av_table.params.reshape(27, 4))
    if not env.running:
        print("not running")
        env.init_game(15)
    experiment.doInteractions(1)
    agent.learn()
    agent.reset()