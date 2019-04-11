#Theek Thaak Toe
import os
import random
import time
#Structure
box1=[['','',''],['','',''],['','','']]
box2=[['','',''],['','',''],['','','']]
box3=[['','',''],['','',''],['','','']]
box4=[['','',''],['','',''],['','','']]
box5=[['','',''],['','',''],['','','']]
box6=[['','',''],['','',''],['','','']]
box7=[['','',''],['','',''],['','','']]
box8=[['','',''],['','',''],['','','']]
box9=[['','',''],['','',''],['','','']]

matrix=[box1,box2,box3,box4,box5,box6,box7,box8,box9]
scoreCard={}

#Defining a function to display the matrix
def display():
    #clears the display after every turn
    os.system('cls')
    #Title
    print(' ╔╦╗┬ ┬┌─┐┌─┐┬┌─ ╔╦╗┬ ┬┌─┐┌─┐┬┌─ ╔╦╗┌─┐┌─┐')
    print('  ║ ├─┤├┤ ├┤ ├┴┐  ║ ├─┤├─┤├─┤├┴┐  ║ │ │├┤ ')
    print('  ╩ ┴ ┴└─┘└─┘┴ ┴  ╩ ┴ ┴┴ ┴┴ ┴┴ ┴  ╩ └─┘└─┘')
    
    
    print(21*'--')
    for i in range(0,8,3):
        for j in range (0,3):
            for m in range(0,3):
                print('|',end='')
                for k in range(0,3):
                    if matrix[i+m][j][k]=='':
                        print(matrix[i+m][j][k],end='  |')
                    else:
                        print(matrix[i+m][j][k],end=' |')
                print('\t',end='')
            if j<2:
                print()
                print(21*'- ')
        print()
        print(21*'--')
    print('X: ',list(scoreCard.values()).count('X'),end='\t')
    print('O: ',list(scoreCard.values()).count('O'))
    if num>6:
        box_activated=num-6
    elif num<4:
        box_activated=num+6
    else:
        box_activated=num
    print('Box active is ',box_activated)
    
    if turn_no%10==goodMove:
        print('Good move')
    
    
#Defining a function to check 3 chars in a row
def checkwin(box):
    if (box[0]+box[1]+box[2]).count(char)>=3:
        if box[0][0]==box[0][1]==box[0][2]!='':
            return True
        elif box[1][0]==box[1][1]==box[1][2]!='':
            return True
        elif box[2][0]==box[2][1]==box[2][2]!='':
            return True
        elif box[0][0]==box[1][0]==box[2][0]!='':
            return True
        elif box[0][1]==box[1][1]==box[2][1]!='':
            return True
        elif box[0][2]==box[1][2]==box[2][2]!='':
            return True
        elif box[0][0]==box[1][1]==box[2][2]!='':
            return True
        elif box[0][2]==box[1][1]==box[2][0]!='':
            return True
        else:
            return False
    else:
        return False
#Defining a function to switch between X and O
def oppChar(str):
    for i in ['X','O']:
        if i != str:
            return i
    
box_no=4
num=5
box_activated=0
turn_no=0
symbol=''
mode=2
goodMove=1
print('Hello','\n','Rules: To play press the key on your num pad corresponding to the box. Win more boxes to win. ')
print('To end the game at any moment press 0')   

while mode not in [0,1]:
    mode=int(input('Press (0) vs computer, (1) vs player: '))
while symbol not in ['X','O']:
    symbol=input('Enter Symbol (X/O): ').upper()
    
#Actual GAME

display()

while True:
    goodMove=random.randint(0,9)
    
    if turn_no%2==0:
        char=symbol
    else:
        char=oppChar(symbol)
    
    if mode==0 and turn_no%2 != 0:
        num=random.randint(1,9)
    else:
        try:
            num=int(input('Your chance: '))
        except ValueError:
            print('Input not valid ')
            print('Try Again')
            continue
            #will end the game if the input is not an integer
    if num == 0:
        print('Game Over')
        sc1,sc2=0,0
        l=list(scoreCard.values())
        sc1=l.count(char)
        sc2=l.count(oppChar(char))
        if sc1>sc2:
            print(char, 'won more boxes')
        elif sc1<sc2:
            print(oppChar(char), 'won more boxes')
        else:
            print('Draw!')
        time.sleep(3)
        break
    
    if num not in range(1,10):
        print('Number not within 1 and 9. Try Again')
        continue
    #to match with the numbering on numpad
    if num in (7,8,9):
        num-=6
    elif num in (1,2,3):
        num+=6

    if matrix[box_no][(num-1)//3][(num-1)%3] =='':
        matrix[box_no][(num-1)//3][(num-1)%3]=char
    elif '' not in matrix[box_no][0]+matrix[box_no][1]+matrix[box_no][2]:
        if list(scoreCard.values()).count(char)>len(list(scoreCard.values()))/2:
            print(char, 'Wins')
        elif list(scoreCard.values()).count(char)<len(list(scoreCard.values()))/2:
            print(oppChar(char), 'Wins')
        else:
            print('Draw!')
        time.sleep(3)
        break
    elif (turn_no%2==0 and mode==0) or mode==1:
        print('Box already occupied')
        continue
    else:
        continue
   
    display()
    if box_no+1 not in scoreCard and checkwin(matrix[box_no]):
        print(char,'Wins this box')
        scoreCard[box_no+1]=char
        if list(scoreCard.values()).count(char)==5:
            display()
            print(char,' Wins Congrats')
            time.sleep(3)
            break
    box_no=num-1
    turn_no+=1
