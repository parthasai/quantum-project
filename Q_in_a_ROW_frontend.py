import numpy as np
import pygame
import sys
import math
import pygame_menu
import button
import requests
import os

from tkinter import *
from tkinter import messagebox
Tk().wm_withdraw()

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
LIGHT_RED = (255,153,153)
LIGHT_YELLOW = (255,255,153)
GREEN = (0,255,0)
WHITE = (255,255,255)

ROW_COUNT = 6
COLUMN_COUNT = 7

REDPLAYER = "Player 1"
YELLOWPLAYER = "Player 2"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board, Pairs):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, (r+1)*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int((r+1)*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 3: 
				pygame.draw.circle(screen, LIGHT_RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), 3*RADIUS/4)
			elif board[r][c] == 4: 
				pygame.draw.circle(screen, LIGHT_YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), 3*RADIUS/4)
	
	buttonFont = pygame.font.SysFont("monospace", 20, True)

	for i, pair in enumerate(Pairs):
		for SCoin in pair:
			label_pair = buttonFont.render(str(i+1), 1, BLACK)
			if i+1 < 10:
				screen.blit(label_pair, (int(SCoin[1]*SQUARESIZE+SQUARESIZE/2)-5,height-int(SCoin[0]*SQUARESIZE+SQUARESIZE/2)-10))
			else:
				screen.blit(label_pair, (int(SCoin[1]*SQUARESIZE+SQUARESIZE/2)-10,height-int(SCoin[0]*SQUARESIZE+SQUARESIZE/2)-10))

	pygame.display.update()


pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+2) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)

pygame.display.set_caption('Q in a ROW')
Icon = pygame.image.load(resource_path('logo.png'))
pygame.display.set_icon(Icon)

menu = pygame_menu.Menu('Q in a ROW', width, height, theme=pygame_menu.themes.THEME_DARK)


def start_the_game():
	board = create_board()
	print_board(board)
	game_over = False
	turn = 0
	superposition = False
	collapse = False
	SPPairs = []
	Ele1=[]
	Ele2=[]
	SCoin = 0

	back_img = pygame.image.load(resource_path('back_btn.png')).convert_alpha()
	back_button = button.Button(width - 40, 20, back_img,back_img, 1)

	super_img_off = pygame.image.load(resource_path('super_off_btn.png')).convert_alpha()
	super_img_on = pygame.image.load(resource_path('super_on_btn.png')).convert_alpha()

	super_button = button.Button(20, 20, super_img_off,super_img_on, 1)

	collapse_img_off = pygame.image.load(resource_path('collapse_off_btn.png')).convert_alpha()
	collapse_img_on = pygame.image.load(resource_path('collapse_on_btn.png')).convert_alpha()

	collapse_button = button.Button(width - 210, 20, collapse_img_off,collapse_img_on, 1)

	myfont = pygame.font.SysFont("monospace", 75)
	Exitfont = pygame.font.SysFont("monospace", 50)
	buttonFont = pygame.font.SysFont("monospace", 20, True)

	REDPLAYER=red.get_value()
	YELLOWPLAYER=yellow.get_value()

	pygame.draw.rect(screen, BLACK, (0,0, width, 2*SQUARESIZE))

	label_turn = buttonFont.render(REDPLAYER+"'s Turn", 1, WHITE)
	screen.blit(label_turn, (width/2-90,20))

	back_button.draw(screen, False)
	super_button.draw(screen, superposition)
	collapse_button.draw(screen, collapse)
	draw_board(board, SPPairs)

	while not game_over:
		mouse = pygame.mouse.get_pos()
		if back_button.draw(screen,False):
			return

		if super_button.draw(screen, superposition):
			if SCoin == 0:
				superposition = not superposition
			else:
				messagebox.showinfo("Alert !!","You can't change to Classical in middle of Quantum Turn.")		

		if collapse_button.draw(screen, collapse):
			collapse_button.draw(screen, True)
			label_collapse = buttonFont.render("Computing ...", 1, WHITE)
			screen.blit(label_collapse, (width/2-80,60))

			if len(SPPairs)>0:
				x = requests.get('http://smartatwork.in:5000/collapse', params = {"pairs": len(SPPairs)})
				#SPString = board_collapse(len(SPPairs))
				SPString = x.text
				print(SPString)
				for i,char in enumerate(SPString):
				#char = 1
				#for i, pair in enumerate(SPPairs):
					if char == "0":
						if SPPairs[i][0][2] == 3:
							board[SPPairs[i][0][0]][SPPairs[i][0][1]]=1
						else:
							board[SPPairs[i][0][0]][SPPairs[i][0][1]]=2
						board[SPPairs[i][1][0]][SPPairs[i][1][1]]=0
					else:
						if SPPairs[i][1][2] == 3:
							board[SPPairs[i][1][0]][SPPairs[i][1][1]]=1
						else:
							board[SPPairs[i][1][0]][SPPairs[i][1][1]]=2
						board[SPPairs[i][0][0]][SPPairs[i][0][1]]=0
					draw_board(board, SPPairs)
					pygame.time.wait(1000)
				SPPairs.clear()
				columnList = []
				for column in range(0,7):
					for row in board:
						if row[column] > 0:
							columnList.append(row[column])
					for i in range(0,6):
						try:
							board[i][column] = columnList[i]
						except Exception as e:
							board[i][column] = 0
					columnList=[]
					pygame.time.wait(200)
					draw_board(board, SPPairs)
				win1 = winning_move(board, 1)
				win2 = winning_move(board, 2)
				if win1 and win2:
					label = myfont.render("Draw Match !!", 1, WHITE)
					screen.blit(label, (20,SQUARESIZE+10))
					game_over = True
				elif win1:
					label = myfont.render(REDPLAYER+" Wins!!", 1, RED)
					screen.blit(label, (20,SQUARESIZE+10))
					game_over = True
				elif win2:
					label = myfont.render(YELLOWPLAYER+" Wins!!", 1, YELLOW)
					screen.blit(label, (20,SQUARESIZE+10))
					game_over = True
				else:
					if turn==0:
						turn = 1
					else:
						turn = 0
			else:
				messagebox.showinfo('Alert !!','No Quantum Pairs to Collapse')

			pygame.draw.rect(screen, BLACK, (width/2-80,60, 200, 25))
			collapse_button.draw(screen, False)
			pygame.draw.rect(screen, BLACK, (width/2-90,20, 200, 25))
			if turn == 0:
				label_turn = buttonFont.render(REDPLAYER+"'s Turn", 1, WHITE)
				screen.blit(label_turn, (width/2-90,20))
			else: 
				label_turn = buttonFont.render(YELLOWPLAYER+"'s Turn", 1, WHITE)
				screen.blit(label_turn, (width/2-90,20))
			print_board(board)
			draw_board(board, SPPairs)
			if game_over:
				messagebox.showinfo('Game Over !!','Click OK to Quit.')
				pygame.time.wait(1000)

			pygame.event.clear()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen, BLACK, (0,SQUARESIZE, width, SQUARESIZE))
				posx = event.pos[0]
				if turn == 0:
					if superposition:
						pygame.draw.circle(screen, LIGHT_RED, (posx, int(3*SQUARESIZE/2)), 3*RADIUS/4)
					else:
						pygame.draw.circle(screen, RED, (posx, int(3*SQUARESIZE/2)), RADIUS)
				else: 
					if superposition:
						pygame.draw.circle(screen, LIGHT_YELLOW, (posx, int(3*SQUARESIZE/2)), 3*RADIUS/4)
					else:
						pygame.draw.circle(screen, YELLOW, (posx, int(3*SQUARESIZE/2)), RADIUS)
			pygame.display.update()

			if event.type == pygame.MOUSEBUTTONDOWN:
				pygame.draw.rect(screen, BLACK, (0,SQUARESIZE, width, SQUARESIZE))

				if 20 <= mouse[0] <= 230 and 20 <= mouse[1] <= 80:
					pass

				elif width-210 <= mouse[0] <= width and 20 <= mouse[1] <= 80:
					pass
					
				else:
					#print(event.pos)
					# Ask for Player 1 Input
					if turn == 0:
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))

						if superposition:
							if is_valid_location(board, col):
								row = get_next_open_row(board, col)
								drop_piece(board, row, col, 3)
								if SCoin==0:
									SCoin+=1
									turn = 0
									Ele1=[row,col,3]
								else:
									SCoin=0
									superposition=False
									turn = 1
									Ele2=[row,col,3]
									SPPairs.append([Ele1,Ele2])
								if winning_move(board, 1):
									label = myfont.render(REDPLAYER+" Wins!!", 1, RED)
									screen.blit(label, (20,SQUARESIZE+10))
									game_over = True
							else:
								turn=0       
								messagebox.showinfo('Alert !!','This Column is full, try another or Click on Collapse.')
						else:
							if is_valid_location(board, col):
								row = get_next_open_row(board, col)
								drop_piece(board, row, col, 1)
								turn = 1

								if winning_move(board, 1):
									label = myfont.render(REDPLAYER+" Wins!!", 1, RED)
									screen.blit(label, (20,SQUARESIZE+10))
									game_over = True
							else:
								turn=0
								messagebox.showinfo('Alert !!','This Column is full, try another or Click on Collapse.')

					# # Ask for Player 2 Input
					else:
						posx = event.pos[0]
						col = int(math.floor(posx/SQUARESIZE))

						if superposition:
							if is_valid_location(board, col):
								row = get_next_open_row(board, col)
								drop_piece(board, row, col, 4)
								if SCoin==0:
									SCoin+=1
									turn = 1
									Ele1=[row,col,4]
								else:
									SCoin=0
									superposition=False
									turn = 0
									Ele2=[row,col,4]
									SPPairs.append([Ele1,Ele2])
								if winning_move(board, 2):
									label = myfont.render(YELLOWPLAYER+" Wins!!", 1, YELLOW)
									screen.blit(label, (20,SQUARESIZE+10))
									game_over = True
							else:
								turn=1
								messagebox.showinfo('Alert !!','This Column is full, try another or Click on Collapse.')
								
						else:
							if is_valid_location(board, col):
								row = get_next_open_row(board, col)
								drop_piece(board, row, col, 2)
								turn = 0

								if winning_move(board, 2):
									label = myfont.render(YELLOWPLAYER+" Wins!!", 1, YELLOW)
									screen.blit(label, (20,SQUARESIZE+10))
									game_over = True
							else:
								turn=1
								messagebox.showinfo('Alert !!','This Column is full, try another or Click on Collapse.')
				pygame.draw.rect(screen, BLACK, (width/2-90,20, 200, 25))
				if turn == 0:
					label_turn = buttonFont.render(REDPLAYER+"'s Turn", 1, WHITE)
					screen.blit(label_turn, (width/2-90,20))
				else: 
					label_turn = buttonFont.render(YELLOWPLAYER+"'s Turn", 1, WHITE)
					screen.blit(label_turn, (width/2-90,20))
				print_board(board)
				draw_board(board, SPPairs)
				if game_over:
					messagebox.showinfo('Game Over !!','Click OK to Quit.')
					pygame.time.wait(1000)


ABOUT = ['Q in a ROW v0.1\n',
         'Authors: Partha Sai & Sathya Narayana',
         'Emails: sparthasai@gmail.com, \n              sathyanarayanans135@gmail.com',
		 '\n\nDescription: \nQ in a ROW is our Quantum take on 4 in a Row game.\nThis game was created as part of our project submission \nfor Certification in Quantum Computing & Machine \nLearning (CQCML-01)']

WINDOW_SIZE = (width, height)

about_theme = pygame_menu.themes.THEME_DARK
about_theme.widget_margin = (0, 0)

about_menu = pygame_menu.Menu(
	height=WINDOW_SIZE[1] * 0.8,
	theme=about_theme,
	title='About',
	width=WINDOW_SIZE[0] * 0.8
)

for m in ABOUT:
	about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
about_menu.add.vertical_margin(30)
about_menu.add.button('Return to Menu', pygame_menu.events.BACK)


RULES = ['Players take turns placing colored pieces into columns.',
'To create a quantum superposition, players',
'can click the "SUPERPOSITION" button and place',
'two lighter-shaded pieces in different locations,',
'which each have a 50% chance of appearing in either',
'spot upon clicking "COLLAPSE".',
'',
'Using quantum pieces also denies certain squares',
'to opponents. The game continues until one player',
'gets four of their classical pieces in a row ',
'horizontally, vertically, or diagonally.',
'',
'If the board fills up with classical pieces ',
'before either player can achieve WIN, the game',
'ends in a DRAW.',
'Additionally, if both players form winning combinations ',
'simultaneously when the superpositions collapse,',
'it is also a DRAW.',
'',
'Things to note:',
'- Player looses a turn on Clicking "COLLAPSE"',
'- Player cant change to Classical after ',
'  dropping a Quantum piece',
'- Player can trigger Collapse only if there',
'  is at least one Quantum Pair on the board'
]

rules_theme = pygame_menu.themes.THEME_DARK
rules_theme.widget_margin = (0, 0)

rules_menu = pygame_menu.Menu(
	height=WINDOW_SIZE[1] * 0.8,
	theme=rules_theme,
	title='RULES',
	width=WINDOW_SIZE[0] * 0.8
)

for m in RULES:
	rules_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
rules_menu.add.vertical_margin(30)
rules_menu.add.button('Return to Menu', pygame_menu.events.BACK)

def switch():
	a = red.get_value()
	red.set_value(yellow.get_value())
	yellow.set_value(a)

menu.add.image(resource_path('logo.png'))
menu.add.label("")
red = menu.add.text_input('Red Player : ', default='Player 1',selection_color=RED,font_color=RED)
yellow = menu.add.text_input('Yellow Player : ', default='Player 2',selection_color=YELLOW,font_color=YELLOW)
menu.add.button('Play Game', start_the_game,selection_color=GREEN)
menu.add.button('Switch Turns', switch,selection_color=GREEN)
menu.add.button('Rules', rules_menu,selection_color=GREEN)
menu.add.button('About', about_menu,selection_color=GREEN)
menu.add.button('Quit', pygame_menu.events.EXIT,selection_color=GREEN)
menu.mainloop(screen)
