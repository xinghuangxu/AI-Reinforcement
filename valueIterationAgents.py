# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        newValues = util.Counter()
        # Write value iteration code here
        states = self.mdp.getStates()
        for x in range(iterations):
            for state in states:
                maxActionVal=-9999999
                actions=self.mdp.getPossibleActions(state)
                for action in self.mdp.getPossibleActions(state):
                    qvalue=self.computeQValueFromValues(state,action)
                    if(qvalue>maxActionVal):
                        maxActionVal=qvalue
                if(len(actions)>0):
                    newValues[state]=maxActionVal
                else:
                    newValues[state]=0
            for key in newValues.keys():
                self.values[key]=newValues[key]


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
  
#           self.values[state] = self.oldValues[state]
        qvalue = 0;
#         print "iteration:", self.iterations
#             possibleActions=self.mdp.getPossibleActions(state)
#         print "Action:", action
#         if action not in possibleActions: return 0
        transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
#         print "Transition States And Probabilities:", transitionStatesAndProbs
        for (nextState, prob) in transitionStatesAndProbs:
            qvalue += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState])
#         print "Q-Value:", qvalue
        return qvalue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
#         keys= self.oldValues.sortedKeys()
#         for key in keys:
#             self.values[key]=self.oldValues[key]
        if(self.mdp.isTerminal(state)):
            return None;
        legalActions=self.mdp.getPossibleActions(state)
        bestAction=None
        bestActionValue=-999999
        for action in legalActions:
            transitionStatesAndProbs = self.mdp.getTransitionStatesAndProbs(state, action)
            value=0
            for (nextState, prob) in transitionStatesAndProbs:
                value+=prob*self.values[nextState]
            if(value>bestActionValue):
                bestAction=action
                bestActionValue=value
        return bestAction
#         self.values[state] = self.oldValues[state]
#         print "Action Value:", state, self.values.argMax()
#         return self.values.argMax();
#         posibleActions = self.mdp.getPossibleActions(state)
#         bestQValue=-999999
#         bestAction=None
#         for action in posibleActions:
#             qValue=self.computeQValueFromValues(state, action)
#             if(qValue>bestQValue):
#                 bestQValue=qValue
#                 bestAction=action
#         self.values[state]=bestQValue;
#         return bestAction

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
