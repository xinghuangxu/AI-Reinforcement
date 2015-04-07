# qlearningAgents.py
# ------------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random, util, math
from lib2to3.tests.pytree_idempotency import diff

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        self.qvalues = {}
        "*** YOUR CODE HERE ***"

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        if state not in self.qvalues:
            return 0
        if action not in self.qvalues[state]:
            return 0
        return self.qvalues[state][action]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
            return 0
        maxValue = -999999
        if state in self.qvalues:
            for laction in legalActions:
                qvalue = self.getQValue(state, laction)
                if qvalue > maxValue:
                    maxValue = qvalue
        return maxValue
            

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0:
            return None
        maxValue = -99999
        maxAction = list(legalActions)
#         print "Actions:",maxAction
        if state in self.qvalues:
            for laction in legalActions:
                qvalue = self.getQValue(state, laction)
                if qvalue > maxValue:
                    maxValue = qvalue
                    maxAction = [laction]
#                     print "Actions:",maxAction
                elif qvalue == maxValue:
#                     print "Actions Before Append:",maxAction
                    maxAction.append(laction)
        return random.choice(maxAction)

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        if(len(legalActions) == 0):return None
        if(util.flipCoin(self.epsilon)):return random.choice(legalActions)
        return self.computeActionFromQValues(state)


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
#         print "Q Value Before:", self.qvalues
#         print "State:", state
#         print "Reward:", reward
#         print "Action:", action
#         print "Next State:", nextState
        
        if nextState not in self.qvalues:
            self.qvalues[nextState] = {}
            legalActions = self.getLegalActions(nextState)
            for key in legalActions:
                self.qvalues[nextState][key] = 0

        maxQValue = -9999999
        actionValuePairs = self.qvalues[nextState]
        for key in actionValuePairs:
            if(actionValuePairs[key] > maxQValue):
                maxQValue = actionValuePairs[key]
        if maxQValue < -999999: maxQValue = 0
#         print "Max Next State QValue:",maxQValue
        sample = reward + self.discount * maxQValue
        if state not in self.qvalues:
            self.qvalues[state] = {}
            legalActions = self.getLegalActions(state)
            for key in legalActions:
                self.qvalues[state][key] = 0
        self.qvalues[state][action] = (1 - self.alpha) * self.qvalues[state][action] + self.alpha * sample
#         print "Q Value After:", self.qvalues
#         print "\n"

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self, state)
        self.doAction(state, action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        qvalue=0
        features=self.featExtractor.getFeatures(state,action)
        for key in features:
            qvalue = qvalue + features[key]*self.weights[key]
#         print "Features:",features
#         print "Weights:",self.weights
#         print "qValue:",qvalue
        return qvalue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        maxQValue=-999999
        legalActions=self.getLegalActions(nextState)
        for laction in legalActions:
            qValue=self.getQValue(nextState, laction)
            if qValue>maxQValue:
                maxQValue=qValue
        if(len(legalActions)==0):maxQValue=0
        difference=(reward+self.discount*maxQValue)-self.getQValue(state, action)
        features=self.featExtractor.getFeatures(state,action)
        for fkey in features:
            self.weights[fkey]=self.weights[fkey]+self.alpha*difference*features[fkey]
            

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
