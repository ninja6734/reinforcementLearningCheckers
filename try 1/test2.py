board = [[1, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, -1, 0, 0, 0, 1], [1, 0, -1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 1, 0, -1], [2, 0, 0, 0, -1, 0, -1, 0], [0, 0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, -1, 0, 0]]
def obtainSingleActionOfPiece(pieceID, lastPositions, actions, First=True):
    print(actions)
    _actions = actions
    _lastPositions = lastPositions
    _fixed = False
    if(_lastPositions):
        print(_lastPositions)
        if(type(_lastPositions[0][-1]) == type([])):
            directions = _lastPositions[0][-1]
            _fixed = True
        else:
            directions = [(1,1),(1,-1),(-1,-1),(-1,1)]
            if(pieceID == 1):
                directions = directions[:2]
            elif(pieceID == -1):
                directions = directions[2:]
        pos = _lastPositions.pop(0)
        for dirX,dirY in directions:
            nextX = pos[-1] + dirX
            nextY = pos[-2] + dirY
            if(0 <= nextX <= 8):
                if(0 <= nextY <= 8):
                    testingSpace = board[nextY][nextX]
                    if(testingSpace == 0):
                        if(abs(pieceID) == 2):
                            #promoted and no take
                            positions = pos + [nextY,nextX]
                            _lastPositions.append(positions.append([dirX,dirY]))
                            if(_fixed):
                                _actions.append(positions[:-1])
                                return obtainSingleActionOfPiece(pieceID, _lastPositions[:-1], _actions)
                            else:
                                _actions.append(positions)
                                return obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
                        elif(First):
                            #not promoted and no take
                            positions = pos + [nextY,nextX]
                            _actions.append(positions)
                            return obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
                    elif(not testingSpace/abs(testingSpace) == pieceID/abs(pieceID)):
                        testingSpace = board[nextY+dirY][nextX+dirX]
                        if(abs(pieceID) == 2):
                            #promoted and a take
                            if(testingSpace == 0):
                                positions = pos + [nextY, nextX,nextY + dirY, nextX+ dirX]
                                _lastPositions.append(positions)
                                _actions.append(positions)
                                return obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
                        else:
                            #not promoteed and a take
                            if(testingSpace == 0):
                                positions = pos + [nextY, nextX , (nextY + dirY), (nextX+ dirX)]
                                print(pos)
                                _lastPositions.append(positions)
                                _actions.append(positions)
                                return obtainSingleActionOfPiece(pieceID, _lastPositions, _actions, First=False)
                    else:
                        return obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
                return obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
            return obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)


    else:
        
        return _actions

    
def getActionsOfPiece(pieceID,coor):
    return obtainSingleActionOfPiece(pieceID, [coor], [])


def getActions(piece):
    actions = []
    for colCnt,col in enumerate(board):
        for rowCnt, row in enumerate(col):
            if row * piece > 0:
                e = getActionsOfPiece(row,[colCnt,rowCnt])
                actions.extend(e)
    
    return actions

print(getActions(-1))