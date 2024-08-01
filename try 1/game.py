from agent import agent
from env import Environment

player1 = agent(1)
player2 = agent(-1)
envi = Environment()
"""
moments = 1000
moment = 0

while moment < moments:
    player1.chooseAction(envi.board,envi.getActions(player1.pID))
    moment += 1
"""
print(envi.board)
print(envi.getActionsOfPiece((2,0),1))