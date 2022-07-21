import random

pieceScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

knightScore = [[1, 1, 1, 1, 1, 1, 1, 1],
              [1, 2, 2, 2, 2, 2, 2, 1],
              [1, 2, 3, 3, 3, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 3, 3, 3, 2, 1],
              [1, 2, 2, 2, 2, 2, 2, 1],
              [1, 1, 1, 1, 1, 1, 1, 1]] # finding best knight position

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
              [1, 2, 3, 3, 3, 1, 1, 1],
              [1, 4, 3, 3, 3, 2, 2, 1],
              [1, 2, 3, 3, 3, 2, 2, 1],
              [1, 2, 3, 3, 3, 2, 2, 1],
              [1, 4, 3, 3, 3, 2, 2, 1],
              [1, 1, 1, 3, 1, 1, 1, 1],
              [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
             [4, 4, 4, 4, 4, 4, 4, 4],
             [1, 1, 2, 3, 3, 2, 1, 1],
             [1, 2, 3, 4, 4, 3, 2, 1],
             [1, 2, 3, 4, 4, 3, 2, 1],
             [1, 1, 2, 2, 2, 2, 1, 1],
             [4, 4, 4, 4, 4, 4, 4, 4],
             [4, 3, 4, 4, 4, 4, 3, 4]]

whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8],
                  [5, 6, 6, 7, 7, 6, 6, 5],
                  [2, 3, 3, 4, 4, 3, 2 ,1],
                  [1, 2, 3, 4, 4, 3, 2, 1],
                  [1, 1, 2, 3, 3, 2, 1, 1],
                  [1, 1, 1, 0, 0, 1, 1, 1],
                  [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 1, 1, 0, 0, 1, 1, 1],
                  [1, 1, 2, 3, 3, 2, 1, 1],
                  [1, 2, 3, 4, 4, 3, 2, 1],
                  [2, 3, 3, 4, 4, 3, 2 ,1],
                  [5, 6, 6, 7, 7, 6, 6, 5],
                  [8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8]]

piecePositionScores = {"N": knightScore, "Q": queenScores, "B": bishopScores, "R": rookScores, "bp": blackPawnScores, "wp": whitePawnScores}


CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2

# picks and returns a random move
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


# basic minmax algorithm 
def findBestMoveMinMaxNoRecursion(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE # worst possible score for black
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves() 
                if gs.checkMate:
                    score = -turnMultiplier * CHECKMATE
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove


# helper method make first recursive call



def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    counter = 0
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter)
    return nextMove

  
# MinMax algorithm with recursion 
def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove, counter
    counter += 1
    if depth == 0: # at deepest I want to go
        return scoreMaterial(gs.board)

    if whiteToMove: 
        maxScore = -CHECKMATE  
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH: 
                    nextMove = move 
            gs.undoMove()
        return maxScore
            
    else:
        minScore = CHECKMATE 
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH: 
                    nextMove = move 
            gs.undoMove()
        return minScore
    
# negaMax algorithm with recursion
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    random.shuffle(validMoves)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
              
        gs.undoMove()
    return maxScore


# negaMax including alpha-beta pruning 
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    random.shuffle(validMoves)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
              
        gs.undoMove()
        if maxScore > alpha: # pruning happens
            alpha = maxScore
        if alpha >= beta:
            break 
          
    return maxScore
      

      
# a positive score is good for white, a negative score is good for black
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE # black wins
        else:
            return CHECKMATE # white wins 
    elif gs.staleMate:
        return STALEMATE 
  
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                # score it positionally
                piecePositionScore = 0
                if square[1] != 'K':
                    if square[1] == "p":
                        piecePositionScore = piecePositionScores[square][row][col]
                    else:
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                      
                if square[0] == 'w':
                    score += pieceScore[square[1]] + (piecePositionScore * 0.1)
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + (piecePositionScore * 0.1)
              
    return score

  

# score the board based on material
def scoreMaterial(board): 
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score