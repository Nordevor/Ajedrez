import pygame
import sys
import math
pygame.init()

cuadradoA, cuadradoH = 45, 45
altura = cuadradoA * 8
ancho = cuadradoH * 8

sbarw = 40
tamano = [ancho, altura+sbarw]

pygame.display.set_caption("Ajedrez")

pantalla = pygame.display.set_mode(tamano)

selected = False
pieces = []
movimientosB, movimientosN = [], []
moves = [movimientosB, movimientosN]
playerIsWhite = True

highlightimg = pygame.image.load("imagenes/mover.png")
attackimg = pygame.image.load("imagenes/comer.png")
imagenes = {}
imagenes["BPeon"] = pygame.image.load("imagenes/peon.png")
imagenes["BTorre"] = pygame.image.load("imagenes/torre.png")
imagenes["BCaballo"] = pygame.image.load("imagenes/caballo.png")
imagenes["BAlfil"] = pygame.image.load("imagenes/alfil.png")
imagenes["BReina"] = pygame.image.load("imagenes/reina.png")
imagenes["BRey"] = pygame.image.load("imagenes/rey.png")

imagenes["NPeon"] = pygame.image.load("imagenes/peon negro.png")
imagenes["NTorre"] = pygame.image.load("imagenes/torre negra.png")
imagenes["NCaballo"] = pygame.image.load("imagenes/caballo negro.png")
imagenes["NAlfil"] = pygame.image.load("imagenes/alfil negro.png")
imagenes["NReina"] = pygame.image.load("imagenes/reina negra.png")
imagenes["NRey"] = pygame.image.load("imagenes/rey negro.png")

class Piece():
	def __init__(self,nombre,color,startpos):
		global pieces
		self.nombre = nombre
		self.color = color
		self.pos = startpos
		self.image = imagenes[color+nombre]
		self.hasMoved = False
		self.beingAttacked = False
		tablero[startpos[0]][startpos[1]] = self
		pieces.append(self)
	def move(self,pos):
		global selected
		global moves
		if playerIsWhite:
			moves[1].append((self.nombre, (self.pos, pos)))
		else:
			moves[0].append((self.nombre, (self.pos, pos)))
		tablero[self.pos[0]][self.pos[1]] = EMPTY
		self.pos = pos
		tablero[self.pos[0]][self.pos[1]] = self
		self.hasMoved = True
	def select(self):
		global selected
		selected = self.pos

pieceLogic = {}
whiteInCheck = False
blackInCheck = False
EMPTY = 0

tablero = [
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0],
]

def isFree(pos):
	row, col = pos[0], pos[1]
	if ((row < 0) or (col < 0) or (row > len(tablero)-1) or (col > len(tablero)-1)): return
	return tablero[row][col] == EMPTY
def checkLogic(piece, newpos):
	return True
def colLogic(piece, newpos):
	squareamountx = abs(piece.pos[0]-newpos[0])
	squareamounty = abs(piece.pos[1]-newpos[1])
	if piece.nombre == 'Caballo' or piece.nombre == 'Rey':
		return True
	elif squareamountx == 0:
		for i in range(1, squareamounty):
			mod = -i if (piece.pos[1] > newpos[1]) else i
			testpos = (piece.pos[0], piece.pos[1]+mod)
			if not isFree(testpos):
				return False
	elif squareamounty == 0:
		for i in range(1, squareamountx):
			mod = -i if (piece.pos[0] > newpos[0]) else i
			testpos = (piece.pos[0]+mod, piece.pos[1])
			if not isFree(testpos):
				return False
	else:
		squareamount = abs(piece.pos[0]-newpos[0])
		for i in range(1, squareamount):
			mod = -i if (piece.pos[0] > newpos[0]) else i
			mod2 = -i if (piece.pos[1] > newpos[1]) else i
			testpos = (piece.pos[0]+mod, piece.pos[1]+mod2)
			if not isFree(testpos):
				return False
		return True
	return True

def torre(piece, newpos):
	return ((piece.pos[0] == newpos[0]) or (piece.pos[1] == newpos[1]))
pieceLogic['Torre']=torre

def caballo(piece, newpos):
	diffx = abs(piece.pos[0]-newpos[0])
	diffy = abs(piece.pos[1]-newpos[1])
	return (diffx <= 2 and diffy <= 2 and diffx != 0 and diffy != 0 and diffx != diffy)
pieceLogic['Caballo']=caballo

def alfil(piece, newpos):
	return (abs(piece.pos[1]-newpos[1]) == abs(piece.pos[0]-newpos[0]))
pieceLogic['Alfil']=alfil

def reina(piece, newpos):
	return (torre(piece, newpos) or alfil(piece, newpos))
pieceLogic['Reina']=reina

def rey(piece, newpos):
	if (piece.pos[1]-newpos[1] == 0 and (abs(piece.pos[0]-newpos[0])>1 and abs(piece.pos[0]-newpos[0]<4)) and piece.hasMoved == False):
		xdir = True if piece.pos[0]-newpos[0] > 0  else False
		castlerook = tablero[0][piece.pos[1]] if xdir == True else tablero[7][piece.pos[1]]
		if xdir == True and castlerook != 0 and (abs(piece.pos[0]-newpos[0]) == 2 and castlerook.hasMoved == False):
			if rc:
				castlerook.move((3, piece.pos[1]))
			return True
		elif xdir == False and castlerook != 0 and (abs(piece.pos[0]-newpos[0]) == 2 and castlerook.hasMoved == False):
			if rc:
				castlerook.move((5, piece.pos[1]))
			return True
	else:
		return (reina(piece, newpos) and (abs(piece.pos[0]-newpos[0]) <= 1 and abs(piece.pos[1]-newpos[1]) <= 1))
pieceLogic['Rey']=rey

def peon(piece, newpos):
	squaresallowed = piece.hasMoved and 1 or 2
	movedh = (piece.pos[0] - newpos[0]) if piece.color == 'B' else (newpos[0] - piece.pos[0])
	movedv = (piece.pos[1] - newpos[1]) if piece.color == 'B' else (newpos[1] - piece.pos[1])
	if tablero[newpos[0]][newpos[1]] != 0 and (alfil(piece, newpos) and (abs(movedh) == 1 and movedv == 1)):
		return True
	elif tablero[newpos[0]][newpos[1]] != 0 and movedh == 0:
		return False
	return ((piece.pos[0] == newpos[0]) and (movedv <= squaresallowed) and (movedv > 0))
pieceLogic['Peon']=peon

def pieceCanMove(piece, newpos, realcall):
	global rc
	rc = realcall
	for key in pieceLogic:
		if piece.nombre == key:
			return (pieceLogic[key](piece, newpos) and colLogic(piece, newpos) and checkLogic(piece, newpos))
	return True

for i in range(0, 8):
	Piece('Peon', 'B', (i, 6))
	Piece('Peon', 'N', (i, 1))

Piece('Torre',   'B', (0, 7))
Piece('Torre',   'B', (7, 7))
Piece('Caballo', 'B', (1, 7))
Piece('Caballo', 'B', (6, 7))
Piece('Alfil', 'B', (2, 7))
Piece('Alfil', 'B', (5, 7))
Piece('Reina',  'B', (3, 7))
Piece('Rey',   'B', (4, 7))
Piece('Torre',   'N', (0, 0))
Piece('Torre',   'N', (7, 0))
Piece('Caballo', 'N', (1, 0))
Piece('Caballo', 'N', (6, 0))
Piece('Alfil', 'N', (2, 0))
Piece('Alfil', 'N', (5, 0))
Piece('Reina',  'N', (3, 0))
Piece('Rey',   'N', (4, 0))

font = pygame.font.SysFont("monospace", 20)
def updateText():
	global turno, jaquemate
	turno = font.render("Turno: "+("blanco" if playerIsWhite == True else "negro  "), True, (139, 125, 107), (0, 0, 0, 0))
updateText()

def contains(pos):
	boardpos = tablero[pos[0]][pos[1]]
	if boardpos == 0:
		return 0
	if playerIsWhite == True:
		return 1 if boardpos.color == 'B' else 2
	else:
		return 1 if boardpos.color == 'N' else 2

def pixelpos(pos): return (pos[0] * cuadradoA, pos[1] * cuadradoH)

def drawPieces():
	global selected
	for i in range(len(tablero)):
		row = tablero[i]
		for i2 in range(len(row)):
			piece = row[i2]

			if selected != False:
				if pieceCanMove(tablero[selected[0]][selected[1]], (i, i2), False) and selected != (i, i2) and contains((i, i2)) != 1:
					pantalla.blit(highlightimg, pixelpos((i, i2)))

					(mouseX, mouseY) = pygame.mouse.get_pos()
					curRow = int(math.ceil(mouseX/cuadradoA) - 1)
					curCol = int(math.ceil(mouseY/cuadradoH) - 1)
					if contains((i, i2)) == 2:
						pantalla.blit(attackimg, pixelpos((i, i2)))
				else:
					pass
			if piece != EMPTY:
				pantalla.blit(piece.image, (i*45, i2*45))

def getAttacks():
	for piece in pieces:
		piece.beingAttacked = False
		for piece2 in pieces:
			enemyname = "N" if piece.color == 'B' else "B"
			if piece2 != piece and piece2.color == enemyname and pieceCanMove(piece2, piece.pos, False):
				piece.beingAttacked = True

clock = pygame.time.Clock()

darktan = (120, 120, 120)
lighttan = (255, 228, 196)
while True:
	clock.tick(30)
	pygame.draw.rect(pantalla, darktan, [0, 0, ancho, altura])
	for row in range(4):
		for col in range(4):
			pygame.draw.rect(pantalla, lighttan, [row*90, col*90, cuadradoA, cuadradoH])
			pygame.draw.rect(pantalla, lighttan, [row*90+cuadradoA, col*90+cuadradoH, cuadradoA, cuadradoH])

	drawPieces()

	pantalla.blit(turno, (0, altura+10))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.event.post(pygame.event.Event(pygame.QUIT))
			elif event.key == pygame.K_r:
				pass
		elif event.type == pygame.MOUSEBUTTONUP and pygame.mouse.get_pos()[1] <= altura:
			(mouseX, mouseY) = pygame.mouse.get_pos()
			curCol = int(math.ceil(mouseY/cuadradoA) - 1)
			curRow = int(math.ceil(mouseX/cuadradoH) - 1)

			if selected == False:
				if contains((curRow, curCol)) == 1:
					tablero[curRow][curCol].select()
			else:
				if contains((curRow, curCol)) != 1:
					if pieceCanMove(tablero[selected[0]][selected[1]], (curRow, curCol), True):
						playerIsWhite = not playerIsWhite
						updateText()
						tablero[selected[0]][selected[1]].move((curRow, curCol))
						selected = False
						getAttacks()
				else:
					tablero[curRow][curCol].select()

	pygame.display.update()
