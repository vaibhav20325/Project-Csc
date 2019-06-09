#GAME OF LIFE
import copy

import pygame

#Display
BLACK = (0, 0, 0)
GREY=(50,50,50)
WHITE = (255, 255, 255)
WIDTH = 10
HEIGHT = 10
MARGIN = 1

pygame.init()
WINDOW_SIZE = [551, 551]

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("GameOfLife")
clock = pygame.time.Clock()

def display():
    screen.fill(GREY)
    #pygame.draw.rect(screen,(140,140,140),[MARGIN,MARGIN,551-MARGIN,2*HEIGHT+MARGIN])
    for row in range(0,n):
        for column in range(n):
            color = BLACK
            if m[row][column] == 1:
                color = WHITE
            pygame.draw.rect(screen,color,[(MARGIN + WIDTH) * column + MARGIN,(MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])
    clock.tick(5) 
    pygame.display.flip()

m=[]
newm=[]
n=50
for n_rows in range(n):
    row_temp=[]
    for n_col in range(n):
        row_temp.append(0)
    m.append(row_temp)

#Testing
'''
m[9][11]=1
m[10][10]=1
m[10][11]=1
m[10][12]=1
'''
display()
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key== pygame.K_ESCAPE:
                running=False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            m[row][column] = 1
            display()
def check_n(x,y):
    global m
    global new_m
    sum_n=0
    try:
        sum_n=m[x-1][y]+m[(x+1)%n][y]+m[x][(y+1)%n]+m[x][y-1]+m[x-1][y-1]+m[x-1][(y+1)%n]+m[(x+1)%n][y-1]+m[(x+1)%n][(y+1)%n]
    except:
        sum_n=0

    if sum_n<2:
        new_m[x][y]=0
    elif sum_n==2 and m[x][y]:
        pass
    elif sum_n==3:
        new_m[x][y]=1
    elif sum_n>3:
        new_m[x][y]=0


for i in range(120):
        new_m=copy.deepcopy(m)
        for i in range(n):
            for j in range(n):
                check_n(i,j)
        m=new_m
        display()
'''
        Try Glider
            $$$
            $
             $
'''
