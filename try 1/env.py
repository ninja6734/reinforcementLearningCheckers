class Environment:
    def __init__(self):
        self.reward = 0
        self.board = []
        for columns in range(8):
            column = []
            for row in range(8):
                if(row % 2 == columns % 2):
                    if(columns < 5 and columns > 2):
                        column.append(0)
                    else:
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
        self.reward += 2 * enPiecesDestroyed + 4 * int(Promotion) + 50 * int(Won)
    
    def makeAction(self,acts,piece):
        X = []
        Y = []
        for act in range(int(len(acts)/2)):
            X.append(acts[act * 2 + 1])
            Y.append(acts[act * 2])

        res = self.changeEnv([X,Y],piece)
        self.sendReward(res[0], res[1], res[2])
        return self.reward
    
    def getActionsOfPiece(self, pieceCoor, piece):
        actions = []
        posX = [pieceCoor[1]]  # List to track x-coordinates
        visPos = ()
        posY = [pieceCoor[0]]  # List to track y-coordinates
        visitedPositions = [pieceCoor]
        
        if(piece == 1):
            directions = [(1, 1), (-1, 1)]
        else:
            directions = [(1,-1),(-1,-1)]
        first = True
        while posX:
            currentX = posX.pop(0)  # Get the current x-coordinate and remove it from the list
            currentY = posY.pop(0)  # Get the current y-coordinate and remove it from the list
            
            for dirX, dirY in directions:
                nextX = currentX + dirX
                nextY = currentY + dirY
                
                if 0 <= nextX < len(self.board[0]) and 0 <= nextY < len(self.board):
                    testingSpot = self.board[nextY][nextX]
                    
                    if testingSpot != piece:
                        if testingSpot == 0 and first:
                            actions.append(pieceCoor + (nextY, nextX))  # Valid move
                        elif testingSpot == -piece:
                            position = (nextY + dirY, nextX + dirX)
                            if (0 <= position[1] < len(self.board[0]) and
                                0 <= position[0] < len(self.board) and not position in visitedPositions):
                                actions.append(pieceCoor + visPos + (position[0] - dirY ,position[1] - dirX) + position)  # Capture move
                                visPos = visPos + (position[0] - dirY ,position[1] - dirX) + position
                                first = False
                                posX.append(position[1])
                                posY.append(position[0])
                                visitedPositions.append(position)

        
        return actions

    
    def getActions(self,piece):
        availablePieces = []
        actions = []
        for columnCnt, row in enumerate(self.board):
            for rowCnt, curPiece in enumerate(row):
                if curPiece == piece:
                    availablePieces.append((columnCnt, rowCnt))
        for availablePiece in availablePieces:
            actions.append(self.getActionsOfPiece(availablePiece,piece))
        
        actions = [item for sub_list in actions for item in sub_list]
        return actions
    
    def boardToTuple(self):
        return tuple([item for sub_list in self.board for item in sub_list])
    