board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]


def isInActionList(actionList,act):
        _actionList = []
        for index in range(len(actionList)//2-1):
            _actionList.append([actionList[index*2],actionList[index*2+1]])
        return act in _actionList
def obtainSingleActionOfPiece(pieceID, lastPositions, actions, First=True):
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
            print(f"position: {_lastPositions}")
            pos = _lastPositions.pop(0)
            for dirY, dirX in directions:
                nextX = pos[-1] + dirX
                nextY = pos[-2] + dirY
                print(f"directions: {directions}")
                print(f"nextX: {nextX} nextY: {nextY}")
                if 0 <= nextX < 8 and 0 <= nextY < 8:
                    testingSpace = board[nextY][nextX]
                    if testingSpace == 0:
                        if abs(pieceID) == 2:
                            # promoted and no take
                            positions = pos + [nextY, nextX]
                            positions.append([[dirY, dirX]])
                            if(not isInActionList(positions, [nextY, nextX])):
                                _lastPositions.append(positions)
                                print(_lastPositions)
                            
                            _actions.append(positions)
                            obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
                        elif First:
                            # not promoted and no take
                            positions = pos + [nextY, nextX]
                            _actions.append(positions)
                            obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
                    elif not testingSpace / abs(testingSpace) == pieceID / abs(pieceID):
                        if 0 <= (nextX + dirX) < 8 and 0 <= (nextY + dirY) < 8:
                            testingSpace = board[nextY + dirY][nextX + dirX]
                            if abs(pieceID) == 2:
                                # promoted and a take
                                if testingSpace == 0:
                                    positions = pos + [nextY, nextX, nextY + dirY, nextX + dirX]
                                    
                                    if(not isInActionList(positions, [nextY, nextX])):
                                        _lastPositions.append(positions)
                                    _actions.append(positions)
                                    obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
                            else:
                                # not promoted and a take
                                if testingSpace == 0:
                                    positions = pos + [nextY, nextX, nextY + dirY, nextX + dirX]
                                    if(not isInActionList(positions, [nextY, nextX])):
                                        _lastPositions.append(positions)
                                    _actions.append(positions)
                                    obtainSingleActionOfPiece(pieceID, _lastPositions, _actions, First=False)
            # After the loop completes
            return _actions
        else:
            return _actions


    
def getActionsOfPiece(pieceID,coor):
        actions = obtainSingleActionOfPiece(pieceID, [coor], [])
        
        return actions


def getActions(piece):
        actions = []
        for colCnt,col in enumerate(board):
            for rowCnt, row in enumerate(col):
                if row * piece > 0:
                    e = getActionsOfPiece(row,[colCnt,rowCnt])
                    actions.extend(e)
        
        return actions

print(getActions(1))