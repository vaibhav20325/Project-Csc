'''
Stack1e - The Ultimate Stacking Game
'''

import pygame
import os
from pygame.locals import *
from math import sin

boardsize = boardwidth, boardheight = 12, 20
screensize = screenwidth, screenheight = 240, 400
tilewidth = screenwidth/boardwidth
tileheight = screenheight/boardheight
tilesize = tilewidth, tileheight

tilecolor = (232, 130, 6)
tilecolor2 = (6, 232, 134)

black = (0,0,0)

levelspd = (80, 80, 75, 75, 70, 70, 65, 65, 60, 55, 50, 45, 40, 35, 30)
maxwidth = (3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3)

colorchangey = 10
winlevel = 15

current_speed = 50 #in milliseconds
board = []
lose_tiles = []
current_direction = 1
current_x, current_y, current_width = 0, boardheight - 1, 3
current_level = 0

intro = 0
playing = 1
lose = 2
win = 3

game_state = intro

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, 'data'))

def filepath(filename):
    #Determine the path to a file in the data directory.
    return os.path.join(data_dir, filename)

def load_image(filename):
    return pygame.image.load(os.path.join(data_dir, filename))

bg_images = (load_image("intro.png"), load_image("game.png"), load_image("lose.png"), load_image("win.png"))

bg_images[win].set_colorkey(black)
bg_images[lose].set_colorkey(black)

running = True
pygame.init()
pygame.display.set_caption('Stack1e')

def main():
	global game_state, current_x, current_y, current_speed, running, current_width, current_level


	screen = pygame.display.set_mode(screensize)

	reset_game()

	while(running):
		update_movement()
		update_board_info()
		update_screen(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == KEYDOWN:
				if event.key == K_SPACE:
					key_hit()
				elif event.key == K_ESCAPE:
					if game_state == intro:
						running = False
					else:
						reset_game()
				elif event.key == K_LCTRL: #for cheater scum
					current_x -= 1
					if (current_x < 0): current_x = 0
					current_width += 1
					if (current_width >= boardwidth): current_width = boardwidth - 1

	pygame.display.quit()

def reset_game():
	global game_state, current_x, current_y, current_speed, running, current_width, current_level, lose_tiles

	clear_board()
	lose_tiles = []

	running = True

	game_state = intro

	current_x = 0
	current_y = boardheight - 1
	current_level = 0
	current_speed = levelspd[current_level]
	current_width = maxwidth[current_level]

def key_hit():
	global running, game_state, current_x, current_y, current_width, current_speed, current_level, lose_tiles

	if game_state == playing:
		if current_y < boardheight - 1:
			for x in range(current_x, current_x + current_width):
				if board[x][current_y + 1] == 0: # Collision check
					current_width -= 1 #Give one less block next time
					board[x][current_y] = 0 # Remove extra blocks
					lose_tiles.append((x, current_y, pygame.time.get_ticks())) #Block falling animation

		current_level += 1
		check_win_lose()
		current_y -= 1
	elif game_state == intro:
		game_state = playing
	elif (game_state == lose) or (game_state == win):
		reset_game()
		game_state = intro
	else:
		running = False

def check_win_lose():
	global game_state, current_width, current_level, current_speed, running, tilecolor

	if current_width == 0:
		game_state = lose
	elif current_level == winlevel:
		current_speed = 100
		game_state = win
	else:
		current_speed = levelspd[current_level]
		if current_width > maxwidth[current_level]:
			current_width = maxwidth[current_level]

last_time = 0
def update_movement():
	global game_state, last_time, current_x, current_y, current_width, current_speed, current_direction

	current_time = pygame.time.get_ticks()
	if (last_time + current_speed <= current_time):
		if game_state == playing:
			new_x = current_x + current_direction

			if (new_x < 0) or (new_x + current_width > boardwidth):
				current_direction = -current_direction

			current_x += current_direction

		last_time = current_time

def update_screen(screen):
	global game_state

	if game_state == playing:
		draw_background(screen)
		draw_board(screen)
	elif game_state == intro:
		draw_background(screen)
		pass
	elif (game_state == lose) or (game_state == win):
		screen.fill(black)
		draw_board(screen)
		draw_background(screen)

	pygame.display.flip()

def draw_background(screen):
	global game_state
	screen.blit(bg_images[game_state], (0,0,screenwidth,screenheight),	(0,0,screenwidth,screenheight))


def update_board_info():
	global game_state

	if game_state == playing:
		clear_row(current_y)
		fill_current_row()

def draw_board(screen):
	for x in range(boardwidth):
		for y in range(boardheight):
			if board[x][y] == 1:
				draw_tile(screen, x, y)

	draw_lose_tiles(screen)

def draw_tile(screen, x, y):
	xoffset = 0 #Win animation
	col = tilecolor
	if (y < colorchangey):
		col = tilecolor2

	if game_state == win:
		xoffset = sin(pygame.time.get_ticks() * 0.004 + y * 0.5) * (screenwidth / 4)

	pygame.draw.rect(screen, col, (x * tilewidth + xoffset, y * tileheight, tilewidth, tileheight))
	pygame.draw.rect(screen, black, (x * tilewidth + xoffset, y * tileheight, tilewidth, tileheight), 2)

#Block falling animation
def draw_lose_tiles(screen):
	for lt in lose_tiles:
		falltime = (pygame.time.get_ticks() - lt[2]) * 0.008 #Time falling
		x = lt[0] * tilewidth
		y = lt[1] * tileheight + falltime * falltime

		col = tilecolor
		if (lt[1] < colorchangey):
			col = tilecolor2

		if (y > screenheight):
			lose_tiles.remove(lt)
		else:
			pygame.draw.rect(screen, col, (x+2, y+2, tilewidth-3, tileheight-3))

def clear_board():
	global board

	board = []
	for x in range(boardwidth):
		board.append([])
		for y in range (boardheight):
			board[x].append(0)

def clear_row(y):
	for x in range(boardwidth):
		board[x][y] = 0

def fill_current_row():
	global current_x, current_y, current_width
	for x in range(current_x, current_x + current_width):
		board[x][current_y] = 1
main()
