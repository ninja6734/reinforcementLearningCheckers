import numpy as np

class Environment:
    def __init__(self):
        self.reward = 0
        self.board = []
        self.resetBoard()

    def resetBoard(self):
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
        promoted = abs(self.board[acts[0][0]][acts[0][1]]) == 2
        self.board[acts[0][0]][acts[0][1]] = 0
        destroyedPieces = 0
        for act in acts[1:-1]:
            if (self.board[act[0]][act[1]] != 0):
                destroyedPieces += 1
            self.board[act[0]][act[1]] = 0
        Promotion = False
        if(promoted):
            self.board[acts[-1][0]][acts[-1][1]] = piece * 2
        else:
            if(piece == 1):
                Promotion = acts[-1][0] == 7
                self.board[acts[-1][0]][acts[-1][1]] = (int(Promotion) +1)
            else:
                Promotion = acts[-1][0] == 0
                self.board[acts[-1][0]][acts[-1][1]] = (-(int(Promotion)) -1)

        won = True
        for row in self.board:
            if(-piece in row or -2 * piece in row):
                won = False

        return [destroyedPieces, Promotion, won]


    def sendReward(self,enPiecesDestroyed: int, Promotion: bool, Won: bool):
        self.reward = -20 + 30 * enPiecesDestroyed + 20 * int(Promotion) + 200 * int(Won)
    
    def makeAction(self,acts,piece):
        actsList = []
        for act in range(int(len(acts)/2)):
            actsList.append([acts[act*2],acts[act*2+1]])

        res = self.changeEnv(actsList,piece)
        self.sendReward(res[0], res[1], res[2])
        return self.reward,res[2]
    
    def isInActionList(self,actionList,act):
        _actionList = []
        for index in range(len(actionList)//2):
              _actionList.append([actionList[index*2],actionList[index*2+1]])
        return act in _actionList
    def obtainSingleActionOfPiece(self,pieceID, lastPositions, actions, First=True):
        _actions = actions
        _lastPositions = lastPositions
        
        if _lastPositions:
            if type(_lastPositions[0][-1]) == type([]):
                directions = _lastPositions[0].pop(-1)
                
            else:
                directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
                if pieceID == 1:
                    directions = directions[:2]
                elif pieceID == -1:
                    directions = directions[2:]

            pos = _lastPositions.pop(0)
            for dirY, dirX in directions:
                nextX = pos[-1] + dirX
                nextY = pos[-2] + dirY
                if 0 <= nextX < 8 and 0 <= nextY < 8:
                    testingSpace = self.board[nextY][nextX]
                    if testingSpace == 0:
                        if abs(pieceID) == 2:
                            # promoted and no take
                            positions = pos + [nextY, nextX]
                            positions.append([[dirX, dirY]])
                            if(not self.isInActionList(positions, [nextY, nextX])):
                                _lastPositions.append(positions)
                            
                            _actions.append(positions)
                            self.obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
                        elif First:
                            # not promoted and no take
                            positions = pos + [nextY, nextX]
                            _actions.append(positions)
                            self.obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
                    elif not testingSpace / abs(testingSpace) == pieceID / abs(pieceID):
                        if 0 <= (nextX + dirX) < 8 and 0 <= (nextY + dirY) < 8:
                            testingSpace = self.board[nextY + dirY][nextX + dirX]
                            if abs(pieceID) == 2:
                                # promoted and a take
                                if testingSpace == 0:
                                    positions = pos + [nextY, nextX, nextY + dirY, nextX + dirX]
                                    
                                    if(not self.isInActionList(positions, [nextY, nextX])):
                                        _lastPositions.append(positions)
                                    _actions.append(positions)
                                    self.obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
                            else:
                                # not promoted and a take
                                if testingSpace == 0:
                                    positions = pos + [nextY, nextX, nextY + dirY, nextX + dirX]
                                    if(not self.isInActionList(positions, [nextY, nextX])):
                                        _lastPositions.append(positions)
                                    _actions.append(positions)
                                    self.obtainSingleActionOfPiece(pieceID, _lastPositions, _actions, First=False)
            # After the loop completes
            return _actions
        else:
            return _actions


    
    def getActionsOfPiece(self,pieceID,coor):
        actions = self.obtainSingleActionOfPiece(pieceID, [coor], [])
        
        return actions


    def getActions(self,piece):
        actions = []
        for colCnt,col in enumerate(self.board):
            for rowCnt, row in enumerate(col):
                if row * piece > 0:
                    e = self.getActionsOfPiece(row,[colCnt,rowCnt])
                    actions.extend(e)
        
        return actions
        
    def boardToTuple(self):
        return np.array([item for sub_list in self.board for item in sub_list])
        