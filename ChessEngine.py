"""
This class is responsible for storing all of the info about the current state of the chess game.
It will also be responsible for determining the valid moves at the current state.
It will also keep a move log
"""

class GameState():
    def __init__(self):
        # board is 8x8 2D list, each element has 2 characters
        # first letter is b or w (color)
        # second letter represents the type of piece (K - king, n - Knight)
        # string -- represents empty space with no piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        '''self.board = [
            ["bR", "--", "bB", "--", "--", "--", "bK", "--"],
            ["--", "--", "--", "--", "--", "--", "bp", "--"],
            ["wp", "--", "bN", "--", "bp", "bR", "--", "bp"],
            ["bQ", "--", "bp", "--", "--", "--", "--", "--"],
            ["--", "bB", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "wN", "wp", "--", "wN", "--", "--"],
            ["wp", "wp", "--", "wQ", "wB", "wp", "wp", "wp"],
            ["wR", "--", "--", "--", "wK", "--", "--", "wR"]]'''


      
        self.moveFunctions ={'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 
                            'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves} # mapping each piece to a function
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4) 
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () # co ords for the square where en passant capture is possible
        self.enPassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.wqs, self.currentCastlingRights.bks, self.currentCastlingRights.bqs,)]
        



      
    # takes move as a parameter and executes it, will not work for casteling, pawn promotion and en-passant
    def makeMove(self, move):
      self.board[move.startRow][move.startCol] = "--"
      self.board[move.endRow][move.endCol] = move.pieceMoved
      self.moveLog.append(move) #logs the move so we can undo it
      self.whiteToMove = not self.whiteToMove # switch turns
      # update location if king moved
      if move.pieceMoved == 'wK':
          self.whiteKingLocation = (move.endRow, move.endCol)
      elif move.pieceMoved == 'bK':
          self.blackKingLocation = (move.endRow, move.endCol)
        
      # pawn promotion - auto queen
      if move.isPawnPromotion:
          self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

      # en passant move
      if move.isEnpassantMove:
        self.board[move.startRow][move.endCol] = '--' # capturing the pawn

      # update enpassantPossible variable
      if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: # only on 2 sqr pawn advances
          self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
      else:
          self.enpassantPossible = ()
      # castle move
      if move.isCastleMove:
          if move.endCol - move.startCol == 2: #king side castle
              self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] # moves the rook
              self.board[move.endRow][move.endCol+1] = '--' # erase old rook
          else: # queen side castle
                  self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] # moves the rook
                  self.board[move.endRow][move.endCol-2] = '--' # erase old rook

      self.enPassantPossibleLog.append(self.enpassantPossible) 
      # update castling rights - whenever it is a rook or a king move
      self.updateCastleRights(move)
      self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks,       self.currentCastlingRights.wqs, self.currentCastlingRights.bks, self.currentCastlingRights.bqs,))

      
        
    #this will undo the last move
    def undoMove(self):
        if len(self.moveLog) != 0: #make sure there is a move to undo
            move = self.moveLog.pop() # gives us the move and removes it from the moveLog
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # switches turn back
            # updating kings position
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            # undo en passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' # leave square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                
            self.enPassantPossibleLog.pop() 
            self.enPassantPossibleLog[-1]

            # undo castling rights
            self.castleRightsLog.pop() # get rid of new castle rights from the move we are undoing
            self.currentCastlingRights = self.castleRightsLog[-1] # setting the castle rights to the previous moves ones
            # undo the castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: # kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'
            self.checkMate = False
            self.staleMate = False 


              

    # updating castling rights - whenever a rook or king moves
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: # left rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: # left rook
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7: # right rook
                    self.currentCastlingRights.bks = False
        # if a rook is captured
        if move.pieceCaptured =='wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured =='bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False
                


                  
    # all moves considering checks
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs) # copies current castling rights
        # 1. get all possible moves
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        # 2. for each move, make the move
        for i in range(len(moves)-1, -1, -1): # when removing from a list go backwards
            self.makeMove(moves[i])
            # 3. generate all opponents moves
            # 4. for each of the opponents moves, see if they attack the king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                # 5. if they do attack king, not a valid move  
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: # either checkmate or stalemate
          if self. inCheck():
              self.checkMate = True
          else: 
              self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tempEnpassantPossible 
        self.currentCastlingRights = tempCastleRights
        return moves

    # determine if current player is in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    # determine if they can attack the square
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switch to opponents pov
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove # switch turn back
        for move in oppMoves:
          if move.endRow == r and move.endCol == c: # square is under attack
              return True
        return False
    
    # all moves without considering checks
    def getAllPossibleMoves(self): 
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
              # takes first letter in piece name
                    piece = self.board[r][c][1] # takes second letter in piece name
                    self.moveFunctions[piece](r, c, moves) # calls the appropriate move function
        return moves

      
    # get all pawn moves at row col and then add these moves to the list
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: # white pawn moves
            if self.board[r-1][c] == "--": # one square pawn advance
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: # don't go over the board
                if self.board[r-1][c-1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board)) # to the left
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7: # don't go over the board
                if self.board[r-1][c+1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board)) # to the right      
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))

        else: # black pawn moves          
            if self.board[r+1][c] == "--": # one square pawn advance
                moves.append(Move((r,c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0: # don't go over the board
                if self.board[r+1][c-1][0] == 'w': # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board)) # to the left
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7: # don't go over the board
                if self.board[r+1][c+1][0] == 'b': # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board)) # to the right   
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))

                  
          
    # get all rook moves at row col and then add these moves to the list
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c +d[1] * i 
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: # off board
                    break

  
    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves: 
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece - empty or enemy piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))
      
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c +d[1] * i 
                if 0 <= endRow < 8 and 0 <= endCol < 8: # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # empty space valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # enemy piece valid
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: # off board
                    break
      
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
      
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1),)
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8): 
            
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: # not an ally piece - empty or enemy piece
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    
                  


    # generate all valid castle moves for the king at (r, c) and add them to list moves
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
          return # cannot castle while in check
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
          self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
          self.getQueensideCastleMoves(r, c, moves)

          
    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))
          

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))
          


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():

    # maps keys to values
    # key : values
    # ranks are rows = numbered 1 to 8 going up the board
    # files are col going from a to h
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()} # reverses dictionary
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()} # reverses dictionary
    

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol] # empty string if no piece is there
        # pawn promotion below
        self.isPawnPromotion = False
        self.isPawnPromotion = ((self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7))
        # en passant below
        self.isEnpassantMove = isEnpassantMove
        #self.castle = castle
        if self.isEnpassantMove == True:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
        # castle move
        self.isCastleMove = isCastleMove
        self.isCapture = self.pieceCaptured != '--'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow *10 + self.endCol

    # over riding the equals method
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

  

    def getChessNotation(self):
      # can later make this real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __str__(self): # overriding the str function
        #castle move
        if self.isCastleMove:
            return '0-0' if self.endCol == 6 else '0-0-0'
        endSquare = self.getRankFile(self.endRow, self.endCol)
        # pawn moves 
        if self.pieceMoved[1] == 'p':
            if self.isCapture:
                  return self.colsToFiles[self.startCol] + 'x' + endSquare 
            else:
                  return endSquare
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare