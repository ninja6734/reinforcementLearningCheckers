import random

class agent:
    def __init__(self,pID):
        self.qTable = {}
        self.alpha = 0.1
        self.epsilon = 0.1
        self.gamma = 0.99
        self.pID = pID
    
    def getQValue(self,state, action) -> float:
        if state in self.qTable:
            if action in self.qTable[state]:
                return self.qTable[state][action]
            else:
                return 0.0
        else:
            return 0.0
    
    def setQValue(self,state,action,value) -> None:
        if state not in self.qTable:
            self.qTable[state] = {}
        self.qTable[state][action] = value

    def chooseAction(self,state,availableActions,epsilon = None):
        if epsilon != None:
            if random.random() < epsilon:
                return [random.choice(availableActions), 1.0]
            else:
                actions = [action for action in availableActions]
                q_values= [self.getQValue(state,action) for action in availableActions]
                return [actions[q_values.index(max(q_values))], max(q_values)]
        else:
            if random.random() < self.epsilon:
                return [random.choice(availableActions), 1.0]
            else:
                actions = [action for action in availableActions]
                q_values= [self.getQValue(state,action) for action in availableActions]
                print(q_values)
                return [actions[q_values.index(max(q_values))], max(q_values)]
        
    def updateQTable(self,state,action,reward,nextState,nextAvailableActions):
        bestNextAction = self.chooseAction(nextState,nextAvailableActions,0)
        tdTarget = reward + self.gamma * self.getQValue(nextState,bestNextAction[0])
        tdError = tdTarget - self.getQValue(state,action)
        self.setQValue(state,action,self.getQValue(state,action) + self.alpha * tdError)