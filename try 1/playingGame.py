from agent import agent
from env import Environment
import tkinter as tk
import pickle
import ast
import random

#bad_setup: [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 1, 0, -2], [-1, 0, 0, 0, 0, 0, -1, 0], [0, -1, 0, 2, 0, -1, 0, -1]]

player1 = agent(1)
with open("qTable.pkl", "rb") as pickle_file:
    data = pickle.load(pickle_file)
player1.load(data)
envi = Environment()
window = tk.Tk()
window.geometry("600x600")
canvas = tk.Canvas(window,width=400,height=400)
canvas.pack()
text = tk.Label(window)
text.pack()
button = tk.Button(window,text="Next", command=lambda: window.quit())
button.pack()
textbox = tk.Text(window, width=100,height=30)
textbox.pack()

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
        if(move):
            for act in range(int(len(move) / 2)-1):
                x1,y1,x2,y2 = [getFieldX(move[act * 2 + 1]),getFieldY(move[act * 2]),getFieldX(move[act * 2 + 3]),getFieldY(move[act * 2+2])]
                canvas.create_line(x1,y1,x2,y2,width=3)

def showBoard(move=None):
    if(move):
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
        print(f"reward: {reward} expected reward: {expectedReward}")
        if(won == True):
            winner = "p1"
            break
        next_state = envi.boardToTuple()
        next_action = envi.getActions(player1.pID)
        if(next_action):
            player1.updateQTable(state,choice,reward,next_state,next_action)
        showBoard(choice)
        
        availableActions = envi.getActions(-1)
        if(availableActions):
            text.config(text="Enter next move: ")
        else:
            winner = "p1"
            break
        move = None
        while not move in availableActions:
            showBoard()
            move = textbox.get(1.0,100.0)
            move = ast.literal_eval(move)
            if(move == ()):
                move = random.choice(availableActions)
        
        _,won = envi.makeAction(move,-1)
        if(won == True):
            winner = "p2"
            break



        moment += 1

    return winner

print(game())