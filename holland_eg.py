from pybrain3.rl.environments.environment import Environment
from scipy import zeros, clip, asarray
from pybrain3.rl.environments.task import Task
from numpy import *
from pybrain3.rl.learners.valuebased import ActionValueTable
from pybrain3.rl.agents import LearningAgent
from pybrain3.rl.learners import Q
from pybrain3.rl.experiments import Experiment
from pybrain3.rl.explorers import EpsilonGreedyExplorer


class SnakeEnv(Environment):
    """ A (terribly simplified) Blackjack game implementation of an environment. """

    # the number of action values the environment accepts
    indim = 4

    # the number of sensor values the environment produces
    outdim = 6

    def getSensors(self):
        """ the currently visible state of the world (the    observation may be stochastic - repeated calls returning different values)
            :rtype: by default, this is assumed to be a numpy array of doubles
        """
        hand_value = int(input("Enter hand value: ")) - 1
        return [float(hand_value), ]

    def performAction(self, action):
        """ perform an action on the world that changes it's internal state (maybe stochastically).
            :key action: an action that should be executed in the Environment.
            :type action: by default, this is assumed to be a numpy array of doubles
        """
        print("Action performed: ", action)

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

    def performAction(self, action):
        """ A filtered mapping towards performAction of the underlying environment. """
        self.env.performAction(action)

    def getObservation(self):
        """ A filtered mapping to getSample of the underlying environment. """
        sensors = self.env.getSensors()
        return sensors

    def getReward(self):
        """ Compute and return the current reward (i.e. corresponding to the last action performed) """
        reward = input("Enter reward: ")

        # retrieve last reward, and save current given reward
        cur_reward = self.lastreward
        self.lastreward = reward

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

av_table = ActionValueTable(21, 2)
av_table.initialize(0.)

# define Q-learning agent
learner = Q(0.5, 0.0)
learner._setExplorer(EpsilonGreedyExplorer(0.0))
agent = LearningAgent(av_table, learner)

# define the environment
env = BlackjackEnv()

# define the task
task = BlackjackTask(env)

# finally, define experiment
experiment = Experiment(task, agent)

# ready to go, start the process
while True:
    experiment.doInteractions(1)
    agent.learn()
    print(av_table.params.reshape(21, 2))
    agent.reset()