from agent import agent
from env import Environment
import tkinter as tk

player1 = agent(1)
player2 = agent(-1)
envi = Environment()
moments = 1000
moment = 0

def getFieldX(rowNum):
    return 50+rowNum * 40
def getFieldY(colNum):
    return 330 - colNum * 40

def showField(canvas,move):
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
    
        print(len(move))
        for act in range(int(len(move) / 2)-1):
            print("line")
            x1,y1,x2,y2 = [getFieldX(move[act * 2 + 1]),getFieldY(move[act * 2]),getFieldX(move[act * 2 + 3]),getFieldY(move[act * 2+2])]
            print(x1,y1,x2,y2)
            canvas.create_line(x1,y1,x2,y2,width=10)

def showBoard(move):
    window = tk.Tk()
    window.geometry("600x600")
    canvas = tk.Canvas(window,width=400,height=400)
    canvas.pack()
    text = tk.Label(window, text=move)
    text.pack()

    showField(canvas,move)

    tk.mainloop()

while moment < moments:
    state = envi.boardToTuple()
    choice,expectedReward = player1.chooseAction(state,envi.getActions(player1.pID))
    print("player1 chose")
    reward = envi.makeAction(choice,player1.pID)
    next_state = envi.boardToTuple()
    next_action = envi.getActions(player1.pID)
    player1.updateQTable(state,choice,reward,next_state,next_action)
    print("player1 done")

    showBoard(choice)

    
    state = envi.boardToTuple()
    choice, expectedReward = player2.chooseAction(state,envi.getActions(player2.pID))
    print("player2 chose")
    reward = envi.makeAction(choice,player2.pID)
    next_state = envi.boardToTuple()
    next_action = envi.getActions(player2.pID)
    player2.updateQTable(state,choice,reward,next_state,next_action)
    print("player2 done")

    showBoard(choice)


    moment += 1
    print(moment)


