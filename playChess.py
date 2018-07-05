import pygame

from board import chessBoard
from board.move import Move
from player.minimax import Minimax

pygame.init()
gameDisplay = pygame.display.set_mode((360, 360))
pygame.display.set_caption("Ajedrez")
clock = pygame.time.Clock()

firstBoard = chessBoard.Board()
firstBoard.createBoard()

allTiles = []
allPieces = []
currentPlayer = firstBoard.currentPlayer

def createSqParams():
    allSqRanges = []
    xMin = 0
    xMax = 45
    yMin = 0
    yMax = 45
    for _ in range(8):
        for _ in range(8):
            allSqRanges.append([xMin, xMax, yMin, yMax])
            xMin += 45
            xMax += 45
        xMin = 0
        xMax = 45
        yMin += 45
        yMax += 45
    return allSqRanges

def squares(x, y, w, h, color):
    pygame.draw.rect(gameDisplay, color, [x, y, w, h])
    allTiles.append([color, [x, y, w, h]])

def drawChessPieces():
    xpos = 0
    ypos = 0
    color = 0
    width = 100
    height = 100
    black = (120, 120, 120)
    white = (255, 228, 196)
    number = 0
    for _ in range(8):
        for _ in range(8):
            if color % 2 == 0:
                squares(xpos, ypos, width, height, white)
                if not firstBoard.gameTiles[number].pieceOnTile.toString() == "-":
                    img = pygame.image.load("./imag/" + firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() + firstBoard.gameTiles[
                        number].pieceOnTile.toString().upper() + ".png")
                    allPieces.append([img, [xpos, ypos], firstBoard.gameTiles[number].pieceOnTile])
                xpos += 45
            else:
                squares(xpos, ypos, width, height, black)
                if not firstBoard.gameTiles[number].pieceOnTile.toString() == "-":
                    img = pygame.image.load("./imag/" + firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() + firstBoard.gameTiles[
                        number].pieceOnTile.toString().upper() + ".png")
                    allPieces.append([img, [xpos, ypos], firstBoard.gameTiles[number].pieceOnTile])
                xpos += 45

            color += 1
            number += 1
        color += 1
        xpos = 0
        ypos += 45



def updateChessPieces():

    xpos = 0
    ypos = 0
    number = 0
    newPieces = []

    for _ in range(8):
        for _ in range(8):
            if not firstBoard.gameTiles[number].pieceOnTile.toString() == "-":

                img = pygame.image.load(
                    "./imag/" + firstBoard.gameTiles[number].pieceOnTile.alliance[0].upper() + firstBoard.gameTiles[
                        number].pieceOnTile.toString().upper() + ".png")

                newPieces.append([img, [xpos, ypos], firstBoard.gameTiles[number].pieceOnTile])
            xpos += 45
            number += 1
        xpos = 0
        ypos += 45

    return newPieces


allSqParams = createSqParams()
drawChessPieces()


selectedImage = None
selectedLegals = None
resetColors = []
quitGame = False
mx, my = pygame.mouse.get_pos()
prevx, prevy = [0,0]
while not quitGame:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            quitGame = True
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            if selectedImage == None:
                mx, my = pygame.mouse.get_pos()
                for piece in range(len(allPieces)):

                    if allPieces[piece][2].alliance == currentPlayer:

                        if allPieces[piece][1][0] < mx < allPieces[piece][1][0]+45:
                            if allPieces[piece][1][1] < my < allPieces[piece][1][1] + 45:
                                selectedImage = piece
                                prevx = allPieces[piece][1][0]
                                prevy = allPieces[piece][1][1]

                                selectedLegals = allPieces[selectedImage][2].calculateLegalMoves(firstBoard)
                                for legals in selectedLegals:
                                    resetColors.append([legals, allTiles[legals][0]])


                                    if allTiles[legals][0] == (66,134,244):
                                        allTiles[legals][0] = (135, 46, 40)
                                    else:
                                        allTiles[legals][0] = (183, 65, 56)


        if event.type == pygame.MOUSEMOTION and not selectedImage == None:

            mx, my = pygame.mouse.get_pos()
            allPieces[selectedImage][1][0] = mx-50
            allPieces[selectedImage][1][1] = my-50

        if event.type == pygame.MOUSEBUTTONUP:

            for resets in resetColors:
                allTiles[resets[0]][0] = resets[1]

            try:



                pieceMoves = allPieces[selectedImage][2].calculateLegalMoves(firstBoard)
                legal = False
                theMove = 0
                for moveDes in pieceMoves:
                    if allSqParams[moveDes][0] < allPieces[selectedImage][1][0]+50 < allSqParams[moveDes][1]:
                        if allSqParams[moveDes][2] < allPieces[selectedImage][1][1]+50 < allSqParams[moveDes][3]:
                            legal = True
                            theMove = moveDes
                if legal == False:
                    allPieces[selectedImage][1][0] = prevx
                    allPieces[selectedImage][1][1] = prevy
                else:
                    allPieces[selectedImage][1][0] = allSqParams[theMove][0]
                    allPieces[selectedImage][1][1] = allSqParams[theMove][2]

                    thisMove = Move(firstBoard, allPieces[selectedImage][2], theMove)
                    newBoard = thisMove.createNewBoard()
                    if not newBoard == False:
                        firstBoard = newBoard

                    newP = updateChessPieces()
                    allPieces = newP

                    currentPlayer = newBoard.currentPlayer

                    if currentPlayer == "Black":
                        aiBoard = True
                        minimax = Minimax(firstBoard, 1)
                        aiBoard = minimax.getMove()
                        firstBoard = aiBoard

                        newP = updateChessPieces()
                        allPieces = newP
                        currentPlayer = aiBoard.currentPlayer

            except:
                pass

            prevy = 0
            prevx = 0
            selectedImage = None

    gameDisplay.fill((255, 255, 255))

    for info in allTiles:
        pygame.draw.rect(gameDisplay, info[0], info[1])

    for img in allPieces:
        gameDisplay.blit(img[0], img[1])



    pygame.display.update()
    clock.tick(60)



