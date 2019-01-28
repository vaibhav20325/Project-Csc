"""
Welcome to M'Sweeper
Created on Wed Jan 9 21:20:37 2019
@author: Aman Thukral
"""
#------------------------------------------------------------------------------
# DEFINITION OF FUNCTIONS + IMPORTING MODULES
#------------------------------------------------------------------------------

import copy
import random
import pygame
import time
import math

def matprint(m):
  for i in range(len(m)):
    print(m[i])

def value(m,y,x):
  return(m[y][x])

add=[(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]

def check(m1,yx):  
  for i in range(len(add)):
    try:
      if(((yx[0]+add[i][0])>=0) and ((yx[1]+add[i][1])>=0)):                     # DUAL ERROR HANDLING
        m1[yx[0]+add[i][0]][yx[1]+add[i][1]]+=1
    except:
      pass
  return(m1)

def newblanks(l1,l2):
  result=[]
  for i in l1:
    if i not in l2:
      result.append(i)
  
  return result

def crosslist(m1,x):
  finalx=[]
  for q in x:
    finalx.append(q)
  for i in x:
     for j in add[0:4]:
       try:
         if i[0]+j[0]>=0 and i[1]+j[1]>=0:
           currentTuple=((i[0]+j[0]),(i[1]+j[1]))
           currentTupleValue=m1[currentTuple[0]][currentTuple[1]]
           if (currentTupleValue>=0) and (currentTuple not in finalx):
             finalx.append(currentTuple)
       except:
         pass
  
  return finalx

#------------------------------------------------------------------------------
# INPUTS + FORMATION OF DISPLAY STRUCTURE
#------------------------------------------------------------------------------

xVal=yVal=0

inputBounds=True
while inputBounds:
  xVal=int(input("No. of columns:"))
  yVal=int(input("No. of rows:"))
  if xVal<3 or yVal<3:
    print("Grid too small")
  elif xVal>11 or yVal>11:
    print("Grid too big")
  else:
    inputBounds=False

bombDividend=6
mode=input("Difficulty - Easy[E] or Hard[H]?:").upper()
if mode=='H':
  bombDividend=5

dispStruct=[]
realStruct=[]
for i in range(yVal):
  dispStruct.append([])
  realStruct.append([])
  for j in range(xVal):
    dispStruct[i].append('untouched')
    realStruct[i].append(0)

#------------------------------------------------------------------------------
# BOMBS + CHECKERS + FORMATION OF REAL STRUCTURE + BLANK GROUPING
#------------------------------------------------------------------------------

bDone=[]
nBomb=(xVal*yVal)//bombDividend

while(len(bDone)!=nBomb):
  xBomb=random.randint(0,xVal-1)
  yBomb=random.randint(0,yVal-1)
  realStruct[yBomb][xBomb]="*"
  tBombCurrent=(yBomb,xBomb)
  if(tBombCurrent not in bDone):
    bDone.append(tBombCurrent)
    realStruct=check(realStruct,tBombCurrent)

blanks=[]
for i in range(yVal):
  for j in range(xVal):
    if value(realStruct,i,j)==0:
      crossed=crosslist(realStruct,[(i,j)])
      for k in blanks:
        if (i,j) in k:
          k.extend(newblanks(crossed,k))
          break
        else:
          continue
      else:
        blanks.append(crossed)

#------------------------------------------------------------------------------
# DISPLAY + INTERFACE
#------------------------------------------------------------------------------

pygame.init()
spaceTop=80
thickness=10
cellSide=70

logoWidth=240
logoImg=pygame.image.load('logo.png')

gWidth=(xVal*(cellSide+thickness))+thickness
gHeight=(yVal*(cellSide+thickness))+spaceTop+thickness

cursorImg=pygame.image.load('cursor.png')
cursorWidth=80

greyImg=pygame.image.load('grey.png')
oneImg=pygame.image.load('one.png')
twoImg=pygame.image.load('two.png')
threeImg=pygame.image.load('three.png')
fourImg=pygame.image.load('four.png')
fiveImg=pygame.image.load('five.png')
sixImg=pygame.image.load('six.png')
sevenImg=pygame.image.load('seven.png')
eightImg=pygame.image.load('eight.png')

bombImg=pygame.image.load('bomb.png')
flagImg=pygame.image.load('flag.png')

imgDict={0:greyImg,1:oneImg,2:twoImg,3:threeImg,4:fourImg,5:fiveImg,6:sixImg,7:sevenImg,8:eightImg,'*':bombImg,'F':flagImg}

gameDisp=pygame.display.set_mode((gWidth,gHeight))
pygame.display.set_caption("M'sweeper")
clock=pygame.time.Clock()

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
grey=(130,130,130)

def coordx(x):
  return x*(cellSide+thickness)

def coordy(y):
  return y*(cellSide+thickness)+spaceTop

def cursor(x,y):
  gameDisp.blit(cursorImg,(x,y))

def text_objects(text,font):
  textSurface=font.render(text,True,white)
  return textSurface, textSurface.get_rect()

def message_display(text,f):
  largeText=pygame.font.Font(f,60)
  TextSurf, TextRect = text_objects(text,largeText)
  TextRect.center = ((gWidth/2),40)
  gameDisp.blit(TextSurf,TextRect)
  
  pygame.display.update()

def cellx():
  mouse=pygame.mouse.get_pos()
  mouse_x=mouse[0]
  xTile=math.floor((mouse_x-(thickness/2))/(cellSide+thickness))
  if xTile+1>xVal:
    xTile=xVal-1
  elif xTile+1<1:
    xTile=0
  return xTile

def celly():
  mouse=pygame.mouse.get_pos()
  mouse_y=mouse[1]-spaceTop
  yTile=math.floor((mouse_y-(thickness/2))/(cellSide+thickness))
  if yTile+1>yVal:
    yTile=yVal-1
  elif yTile+1<1:
    yTile=0
  return yTile

def bomb():
  pygame.draw.rect(gameDisp,black,[0,0,gWidth,spaceTop])
  message_display("BOOM!",'BeforeCollapse.ttf')
  time.sleep(3)
  
  pygame.quit()
  quit()

def gameWin():
  pygame.draw.rect(gameDisp,black,[0,0,gWidth,spaceTop])
  message_display("YOU WON!",'BradyBunch.ttf')
  time.sleep(3)
  
  pygame.quit()
  quit()

def gameloop():
  
  gameExit=False
  
  dispStruct1=copy.deepcopy(dispStruct)
  
  cursor_x=0
  cursor_y=80
  
  while(not gameExit):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      
      if event.type == pygame.MOUSEBUTTONDOWN:
        
        dispValue=value(dispStruct1,celly(),cellx())
        
        if pygame.mouse.get_pressed()[0]:
          
          if dispValue=='untouched':
            dispStruct1[celly()][cellx()]=realStruct[celly()][cellx()]
            
            if value(realStruct,celly(),cellx())==0:
              blankGroup=[(celly(),cellx())]
              for i in blanks:
                if (celly(),cellx()) in i:
                  blankGroup=i
                  break
              for j in blankGroup:
                dispStruct1[(j[0])][(j[1])]=value(realStruct,j[0],j[1])
            
            if value(realStruct,celly(),cellx())=='*':
              gameDisp.blit(bombImg,(coordx(cellx()),coordy(celly())))
              bomb()
        
        elif pygame.mouse.get_pressed()[2]:
          
          if dispValue=='untouched':
            dispStruct1[celly()][cellx()]='F'
          
          elif dispValue=='F':
            dispStruct1[celly()][cellx()]='untouched'
    
    cursor_x=coordx(cellx())
    cursor_y=coordy(celly())
    
    gameDisp.fill(black)
    gameDisp.blit(logoImg,(((gWidth-logoWidth)/2),0))
    
    pygame.draw.rect(gameDisp,white,[0,spaceTop,gWidth,gHeight])
    
    for i in range(xVal):
      xBox=(thickness*(i+1))+(cellSide*i)
      for j in range(yVal):
        yBox=(thickness*(j+1))+(cellSide*j)+spaceTop
        
        pygame.draw.rect(gameDisp,grey,[xBox,yBox,cellSide,cellSide])
    
    counter=0
    
    for i in range(xVal):
      xBox=(thickness*(i+1))+(cellSide*i)
      for j in range(yVal):
        yBox=(thickness*(j+1))+(cellSide*j)+spaceTop
        
        if value(dispStruct1,j,i)!='untouched':
          currentImg=imgDict[value(dispStruct1,j,i)]
          gameDisp.blit(currentImg,(coordx(i),coordy(j)))
        
        else:        
          pygame.draw.rect(gameDisp,grey,[xBox,yBox,cellSide,cellSide])
        
        if value(dispStruct1,j,i)=='F':
          if value(realStruct,j,i)=='*':
            counter+=1
            if counter==nBomb:
              dispStruct1=realStruct
              gameWin()
          else:
            counter=0
    
    cursor(cursor_x,cursor_y)
    
    pygame.display.update()
    clock.tick(60)

gameloop()
pygame.quit()
quit()
