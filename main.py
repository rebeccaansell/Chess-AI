"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object
"""

import pygame as p
import ChessEngine, chessAI

p.init()
BOARD_WIDTH = BOARD_HEIGHT = 280
MOVE_LOG_PANEL_WIDTH = 125
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8  # chess board dimensions 8x8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15  # for animations later on
IMAGES = {}
'''
Initialize a global dictionary of images. This will be called exactly once in the main
'''
backgroundColor = 255,  0,  0
screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))


def main():
    
   # p.init() 
    p.display.init()
    # screen = p.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    # screen.fill(p.Color("white"))
    screen.fill(backgroundColor) 
    p.display.flip()
    moveLogFont = p.font.SysFont("Arial", 10, False, False)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves() # list of all valid moves
    moveMade = False # flag var for when a move is made - list will only be regenerated after the user makes a move
    
    print(gs.board)
    animate = False # flag var for when we should animate
    loadImages()  # only do this once
    running = True
    sqSelected = () # no square is selected initially, keep track of last click of the user
    playerClicks = [] # keep track of player clicks (two tuples:[(6, 4), (4, 4)])
    gameOver = False
    playerOne = True # if a human if playing white, this will be true, if an AI is playing then false
    playerTwo = False # same as above but for black 
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN: 
                if (gameOver == False) and (humanTurn == True):
                    location = p.mouse.get_pos() #(x, y) position of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col) or col >= 8: # user clicked some square twice
                        sqSelected = () # deselect
                        playerClicks = [] #clear player clicks
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) # append for both first and second click
                    if len(playerClicks) == 2: # after second click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)   
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () # reset user clicks 
                                playerClicks = [] 
                        if not moveMade:
                            playerClicks = [sqSelected]

                          
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove() 
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r: # resets the game when r is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected =()
                    playerClicks =[]
                    moveMade = False
                    animate = False
                    gameOver = False 

        # AI move finder
        if not gameOver and not humanTurn:
            AIMove = chessAI.findBestMove(gs, validMoves)
            if AIMove is None: # no best move found
                AIMove = chessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True 
      
        if moveMade:
              if animate == True:
                  animateMove(gs.moveLog[-1], screen, gs.board, clock)
              validMoves = gs.getValidMoves()
              moveMade = False
              animate = False
          
        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkMate or gs.checkMate:
            gameOver = True
            if gs.staleMate:
                text = 'Stalemate'
            else: 
                text = 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate'
        
            drawEndGameText(screen, text)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
Responsible for all the graphics within current game state
"""

def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares
    drawMoveLog(screen, gs, moveLogFont)

'''
Draw the squares on the board
Top left square is always white
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

# highlight square selected and moves for piece selected
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # sqSelected is a piece that can be moved
            #highlight the selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparancy value, 0 completely see through; 255 solid
            s.fill(p.Color('pink'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol ==c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))


"""
Responsible for all the graphics within current game state
"""

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # note we can now access an image using the dictionary by saying something like IMAGES['wp']


'''Draw the pieces on the board using the current GameState.board'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect((c*SQ_SIZE), (r*SQ_SIZE), SQ_SIZE, SQ_SIZE))

              
#draws the move log 
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("light blue"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + '. ' + str(moveLog[i]) + ' '
        if i + 1 < len(moveLog): # makes sure black has made a move
            moveString += str(moveLog[i+1])
        moveTexts.append(moveString)
    padding = 5
    textY = padding
    for i in range(len(moveTexts)):
        text = moveTexts[i]
        textObject = font.render(text, True, p.Color('black'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height()
    

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount+1):
        r, c = ((move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        # erase the piece moved from ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece back
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = (move.endRow+1) if move.pieceCaptured[0] == 'b' else move.endRow -1
                endSquare = p.Rect(move.endCol*SQ_SIZE, enPassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
  

def drawEndGameText(screen, text):
    font = p.font.SysFont("Helvitca", 20, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))


main()

if __name__ == "__name_":
    main()

