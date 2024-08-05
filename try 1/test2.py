board = [[1, 0, 1, 0, 0, 0, 1, 0], [0, 0, 0, -1, 0, 0, 0, 1], [1, 0, -1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 1, 0, -1], [2, 0, 0, 0, -1, 0, -1, 0], [0, 0, 0, 0, 0, -1, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, -1, 0, 0]]


def obtainSingleActionOfPiece(pieceID, lastPositions, actions, First=True):
    _actions = actions
    _lastPositions = lastPositions
    _fixed = False

    if _lastPositions:
        if type(_lastPositions[0][-1]) == type([]):
            directions = _lastPositions[0].pop(-1)
            _fixed = True
        else:
            directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
            if pieceID == 1:
                directions = directions[:2]
            elif pieceID == -1:
                directions = directions[2:]
        print(directions)

        pos = _lastPositions.pop(0)
        for dirY, dirX in directions:
            nextX = pos[-1] + dirX
            nextY = pos[-2] + dirY
            if 0 <= nextX < 8 and 0 <= nextY < 8:
                testingSpace = board[nextY][nextX]
                if testingSpace == 0:
                    if abs(pieceID) == 2:
                        # promoted and no take
                        positions = pos + [nextY, nextX]
                        positions.append([[dirX, dirY]])
                        _lastPositions.append(positions)
                        if _fixed:
                            _actions.append(positions[:-1])
                            obtainSingleActionOfPiece(pieceID, _lastPositions[:-1], _actions)
                        else:
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
                                _lastPositions.append(positions)
                                _actions.append(positions)
                                obtainSingleActionOfPiece(pieceID, _lastPositions, _actions)
                        else:
                            # not promoted and a take
                            if testingSpace == 0:
                                positions = pos + [nextY, nextX, nextY + dirY, nextX + dirX]
                                _lastPositions.append(positions)
                                _actions.append(positions)
                                obtainSingleActionOfPiece(pieceID, _lastPositions, _actions, First=False)
        # After the loop completes
        return _actions
    else:
        return _actions


    
def getActionsOfPiece(pieceID,coor):
    actions = obtainSingleActionOfPiece(pieceID, [coor], [])
    print(f"actions outer: {coor} for {actions}")
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