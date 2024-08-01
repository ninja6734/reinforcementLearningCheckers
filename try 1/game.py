from agent import agent
from env import Environment
import tkinter as tk

player1 = agent(1)
player2 = agent(-1)
envi = Environment()
moments = 1000
moment = 0

while moment < moments:
    state = envi.boardToTuple()
    choice,expectedReward = player1.chooseAction(state,envi.getActions(player1.pID))
    print("player1 chose")
    reward = envi.makeAction(choice,player1.pID)
    next_state = envi.boardToTuple()
    next_action = envi.getActions(player1.pID)
    player1.updateQTable(state,choice,reward,next_state,next_action)
    print("player1 done")

    
    state = envi.boardToTuple()
    choice, expectedReward = player2.chooseAction(state,envi.getActions(player2.pID))
    print("player2 chose")
    reward = envi.makeAction(choice,player2.pID)
    next_state = envi.boardToTuple()
    next_action = envi.getActions(player2.pID)
    player2.updateQTable(state,choice,reward,next_state,next_action)
    print("player2 done")


    moment += 1
    print(moment)

def showField():
        canvas.delete("all")
        print(envi.board)
        for colNum,col in enumerate(envi.board):
            print(col)
            for rowNum,row in enumerate(col):
                print(row)
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


window = tk.Tk()
window.geometry("600x600")
canvas = tk.Canvas(window)
canvas.pack()

showField()

tk.mainloop()