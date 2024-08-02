from agent import agent
from env import Environment
import tkinter as tk
import pickle

#bad_setup: [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, -2], [-1, 0, 0, 0, 0, 0, -1, 0], [0, -1, 0, 2, 0, -1, 0, -1]]

player1 = agent(1)
player2 = agent(-1)
envi = Environment()
window = tk.Tk()
window.geometry("600x600")
canvas = tk.Canvas(window,width=400,height=400)
canvas.pack()
text = tk.Label(window)
text.pack()
button = tk.Button(window,text="Next", command=lambda: window.quit())
button.pack()

def getFieldX(rowNum):
    return 50+rowNum * 40
def getFieldY(colNum):
    return 330 - colNum * 40

def showField(canvas,move):
        canvas.delete("all")
        for colNum,col in enumerate(envi.board):
            for rowNum,row in enumerate(col):
                if(colNum % 2 == 0):
                    if(rowNum % 2 != 0):
                        canvas.create_rectangle(30+rowNum * 40,350 - colNum * 40,70 + rowNum * 40,310 - colNum * 40,fill="green")
                else:
                    if(rowNum % 2 == 0):
                        canvas.create_rectangle(30+rowNum * 40,350 - colNum * 40,70 + rowNum * 40,310 - colNum * 40,fill="green")
                if(row == 1):
                    canvas.create_oval(30+rowNum * 40,350 - colNum * 40,70 + rowNum * 40,310 - colNum * 40,fill="blue")
                elif(row == -1):
                    canvas.create_oval(30+rowNum * 40,350 - colNum * 40,70 + rowNum * 40,310 - colNum * 40,fill="violet")
                elif(row == 2):
                    canvas.create_oval(30+rowNum * 40,350 - colNum * 40,70 + rowNum * 40,310 - colNum * 40,fill="cyan")
                elif(row==-2):
                    canvas.create_oval(30+rowNum * 40,350 - colNum * 40,70 + rowNum * 40,310 - colNum * 40,fill="purple")
    
        for act in range(int(len(move) / 2)-1):
            x1,y1,x2,y2 = [getFieldX(move[act * 2 + 1]),getFieldY(move[act * 2]),getFieldX(move[act * 2 + 3]),getFieldY(move[act * 2+2])]
            canvas.create_line(x1,y1,x2,y2,width=3)

def showBoard(move):
    text.config(text=move)

    showField(canvas,move)

    window.mainloop()
    
def game():
    envi.resetBoard()
    moments = 1000
    moment = 0
    while moment < moments:
        state = envi.boardToTuple()
        availableActions = envi.getActions(player1.pID)
        if(availableActions):
            choice, expectedReward = player1.chooseAction(state,availableActions)
        else:
            winner = "p2"
            break
        reward,won = envi.makeAction(choice,player1.pID)
        if(won == True):
            winner = "p1"
            break
        next_state = envi.boardToTuple()
        next_action = envi.getActions(player1.pID)
        if(next_action):
            player1.updateQTable(state,choice,reward,next_state,next_action)
        
        state = envi.boardToTuple()
        availableActions = envi.getActions(player2.pID)
        if(availableActions):
            choice, expectedReward = player2.chooseAction(state,availableActions)
        else:
            winner = "p1"
            break
        reward,won = envi.makeAction(choice,player2.pID)
        if(won == True):
            winner = "p2"
            break
        next_state = envi.boardToTuple()
        next_action = envi.getActions(player2.pID)
        if(next_action):
            player2.updateQTable(state,choice,reward,next_state,next_action)



        moment += 1

    return winner

for gme in range(1000):
    winner = game()
    print(gme)
if(winner == "p1"):
    dict = player1.qTable
else:
    dict = player2.qTable

f = open("qTable.pkl","wb")
pickle.dump(dict, f)
