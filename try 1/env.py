class Environment:
    def __init__(self):
        self.reward = 0
        self.board = []
        for columns in range(8):
            column = []
            for row in range(8):
                if(row % 2 == columns % 2):
                    column.append(int(columns < 4)*2-1)
                else:
                    column.append(0)
            self.board.append(column)

    def changeEnv(self,acts,piece):
        self.board[acts[1][0]][acts[0][0]] = 0
        destroyedPieces = 0
        for act in acts[1:-1]:
            if (self.board[act[1]][act[0]] != 0):
                destroyedPieces += 1
            self.board[act[1]][act[0]] = 0
        Promotion = False
        if(piece == 1):
            Promotion = acts[-1][1] == 7
            self.board[acts[1][-1]][acts[0][-1]] = (int(Promotion) +1)
        else:
            Promotion = acts[-1][1] == 0
            self.board[acts[1][-1]][acts[0][-1]] = (-(int(Promotion)) -1)

        won = True
        for row in self.board:
            if(-piece in row):
                won = False

        return [destroyedPieces, Promotion, won]


    def sendReward(self,enPiecesDestroyed: int, Promotion: bool, Won: bool):
        print(enPiecesDestroyed, Promotion, Won)
        self.reward += 2 * enPiecesDestroyed + 4 * int(Promotion) + 50 * int(Won)
    
    def makeAction(self,acts,piece):
        X,Y= [[],[]]
        for act in acts:
            X.append(act % 8)
            Y.append(act // 8)

        res = self.changeEnv([X,Y],piece)
        self.sendReward(res[0], res[1], res[2])
        return self.reward

env = Environment()
print(env.makeAction([1,2],1))