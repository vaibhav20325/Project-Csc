# -*- coding: utf-8 -*-
"""
Welcome to the Matrix

Created on Wed Jan  9 21:20:37 2019

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
  for i in x:
    finalx.append(i)
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

'''
def plus(m2,yx):
  final=[yx]
  t3=copy.deepcopy(final)
  while len(t3)!=0:
    g=crosslist(m2,t3)
    for k in g:
      if k not in final:
        final.append(k)
    t3=newblanks(g,t3)
    for k in t3:
      if m2[k[0]][k[1]]!=0:
        t3.remove(k)
  
  return final
'''
#------------------------------------------------------------------------------
# INPUTS + FORMATION OF DISPLAY STRUCTURE
#------------------------------------------------------------------------------

xVal=yVal=0

while((xVal*yVal)<6):
  xVal=int(input("No. of columns:"))
  yVal=int(input("No. of rows:"))
  if(xVal*yVal<6):
    print("Grid too small")

dispStruct=[]

for i in range(yVal):
  dispStruct.append([])
  for j in range(xVal):
    dispStruct[i].append(0)

realStruct=copy.deepcopy(dispStruct)

#------------------------------------------------------------------------------
# BOMBS + CHECKERS + FORMATION OF REAL STRUCTURE + BLANK GROUPING
#------------------------------------------------------------------------------

bDone=[]
nBomb=(xVal*yVal)//6

while(len(bDone)!=nBomb):
  xBomb=random.randint(0,xVal-1)
  yBomb=random.randint(0,yVal-1)
  realStruct[yBomb][xBomb]="*"
  tBombCurrent=(yBomb,xBomb)
  if(tBombCurrent not in bDone):
    bDone.append(tBombCurrent)
    realStruct=check(realStruct,tBombCurrent)

groupBlanks=[]
blanksOpen=[]
for i in range(yVal):
  for j in range(xVal):
    if (i,j) not in blanksOpen and value(realStruct,i,j)==0:
      origin=[(i,j)]
      loopList=[(i,j)]
      loopExit=False
      while(not loopExit):
        crossed=crosslist(realStruct,origin)
        checker=copy.deepcopy(origin)
        origin=newblanks(crossed,origin)
        loopList.extend(origin)
        for k in origin:
          d=value(realStruct,k[0],k[1])
          if d!=0 or d in loopList or d in blanksOpen:
            origin.remove(k)
        if origin==checker:
          loopExit=True
      groupBlanks.append(loopList)
      blanksOpen.extend(loopList)

matprint(realStruct)
print(groupBlanks)
#------------------------------------------------------------------------------
# DISPLAY + INTERFACE
#------------------------------------------------------------------------------
'''
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

gameDisp=pygame.display.set_mode((gWidth,gHeight))
pygame.display.set_caption("M'sweeper")
clock=pygame.time.Clock()

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
grey=(130,130,130)

def cursor(x,y):
  gameDisp.blit(cursorImg,(x,y))

def text_objects(text,font):
  textSurface=font.render(text,True,black)
  return textSurface, textSurface.get_rect()

def message_display(text):
  largeText=pygame.font.Font('freesansbold.ttf',115)
  TextSurf, TextRect = text_objects(text,largeText)
  TextRect.center = ((gWidth/2),(gHeight/2))
  gameDisp.blit(TextSurf,TextRect)
  
  pygame.display.update()

def cellx():
  mouse=pygame.mouse.get_pos()
  mouse_x=mouse[0]
  xTile=math.floor((mouse_x-(thickness/2))/(cellSide+thickness))
  if xTile+1>xVal:
    xTile=xVal-1
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

def gameintro():
  pass

def gameloop():
  
  gameExit=False
  
  cursor_x=0
  cursor_y=80
  
  while(not gameExit):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
   
    cursor_x=(cellx())*(cellSide+thickness)
    cursor_y=((celly())*(cellSide+thickness))+spaceTop
    
    gameDisp.fill(black)
    gameDisp.blit(logoImg,(((gWidth-logoWidth)/2),0))
    
    pygame.draw.rect(gameDisp,white,[0,spaceTop,gWidth,gHeight])
    for i in range(xVal):
      xBox=(thickness*(i+1))+(cellSide*i)
      for j in range(yVal):
        yBox=(thickness*(j+1))+(cellSide*j)+spaceTop
        
        pygame.draw.rect(gameDisp,black,[xBox,yBox,cellSide,cellSide])
    
    cursor(cursor_x,cursor_y)
    
    pygame.display.update()
    clock.tick(60)

gameloop()
pygame.quit()
quit()
'''
