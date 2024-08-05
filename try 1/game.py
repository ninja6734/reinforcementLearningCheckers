from agent import Agent
from env import Environment
import tkinter as tk
import pickle


player1 = Agent(64,32,100,1)
player2 = Agent(64,32,100,-1)

f = open("qTable.pkl","rb")
data = pickle.load(f)
player1.load(data)
player2.load(data)

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
    
def moveOfPlayer(playerObject):
    state = envi.boardToTuple().reshape(1, -1)  # Current state as a flattened array
    available_actions = envi.getActions(playerObject.pID)  # Get available actions for the current state
    if(not available_actions):
        return 0,0
    else:
        action = playerObject.choose_action(state, available_actions)  # Choose an action
        reward,won = envi.makeAction(action,playerObject.pID)
        if(won):
            return 2,action
        else:
            next_state = envi.boardToTuple().reshape(1, -1)  # Get the next state
            next_available_actions = envi.getActions(playerObject.pID)  # Get available actions for the next state
            if(next_available_actions):
                # Update the agent based on the transition
                playerObject.update(state, action, reward, next_state, available_actions, next_available_actions)

            return 1,action


def game(show = False):
    envi.resetBoard()
    moments = 1000
    moment = 0
    winner = "no one"
    while moment < moments:
        win,action = moveOfPlayer(player1)
        if(0 == win):
            winner = "p2"
            break
        elif(2 == win):
            winner = "p1"
            break
        if(show):
            showBoard(action)

        win,action = moveOfPlayer(player2)
        if(0 == win):
            winner = "p2"
            break
        elif(2 == win):
            winner = "p1"
            break
        if(show):
            showBoard(action)

        moment += 1

    return winner

def main(learn = False, rate = 4000):
    out = "y"
    if(learn):
    
        for gme in range(rate):
            winner = game()
            print(gme)
        if(winner == "p1"):
            data = player1.model
        else:
            data = player2.model
        f = open("qTable.pkl","wb")
        pickle.dump(data, f)
    else:
        print(out)
        while out == "y":
            print(f"winner: {game(show = True)}")
            input("continue? y/n")
main()