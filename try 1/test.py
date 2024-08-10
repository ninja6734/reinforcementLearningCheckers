import env
import tkinter as tk

window = tk.Tk()
window.geometry("600x600")
canvas = tk.Canvas(window,width=400,height=400)
canvas.pack()
text = tk.Label(window)
text.pack()
button = tk.Button(window,text="Next", command=lambda: window.quit())
button.pack()
Entry = tk.Text(window, width=100, height=1)
Entry.pack()

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

def showBoard(move, fake = True):
    text.config(text=move)

    if (fake):
        showField(canvas,move)

    window.mainloop()

envi = env.Environment()
envi.board = [[2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

actions = envi.getActions(1)
for act in actions:
    showBoard(act)