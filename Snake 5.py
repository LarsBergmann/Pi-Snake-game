# Sense HAT imports
from sense_hat import SenseHat

from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import time
from time import sleep
from signal import pause
from random import randint
import array as arr

#one time initializations
sense = SenseHat()

#Constants setting
BackgroundColour=(0,0,0)
SnakeHeadColour=(255,0,0)
SnakeBodyColour=(0,255,0)
CandyColour=(0,0,255)

MaxSnakeBodySize=10 # Try changing this to make the game easier or harder (or very hard (e.g.25))
SnakeMovementSpeed=3 #1=Slow, 3=Normal, 5=Fast
HardDisplayBoundaries=False #True:Difficult game. False=Easier game.

SnakeBodyX=[0 for i in range(MaxSnakeBodySize+1)]
SnakeBodyY=[0 for i in range(MaxSnakeBodySize+1)]

#-Functions-------------------------------------------------------
def init():    
    #Variables declaration
    global SnakeBodyLength
    global TravelDirectionX
    global TravelDirectionY
    global CandyVisible
    global CandyPositionX
    global CandyPositionY
    
    sense.clear(BackgroundColour) #Clear Sense HAT display

    for i in range(MaxSnakeBodySize+1): #Initialize the SnakeBody array to save the pixel locations
        SnakeBodyX[i]=0
        SnakeBodyY[i]=0
            
    SnakeBodyX[0]=randint(2,6) #Starting point X (Not too close to the edges in case "HardDisplayBoundaries=True")
    SnakeBodyY[0]=randint(2,6) #Starting point Y (Not too close to the edges in case "HardDisplayBoundaries=True")
    SnakeBodyLength=0 #Starting as a baby snake
    
    TravelDirectionX=randint(-1,1) #Random direction of travel
    if TravelDirectionX!=0:
        TravelDirectionY=0
    else:
        if randint(0,1)==1:
            TravelDirectionY=1
        else:
            TravelDirectionY=-1

    CandyVisible=False
   
#---------------------
def GameOver(Result):
    flash =[0 for i in range(64)] #Initialize
    

    pixel_list = sense.get_pixels() #Store current pixel map

    if Result=='Win':
        print("Game over - You WON")
        for i in range(64): #Colourfull display to celebrate the win
            flash[i] = [randint(0,255),randint(0,255),randint(0,255)]
    else:
        print("Game over - You lost") # White display to indicate the loss
        O = [255, 255, 255]  # White
        flash = [
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, O
        ]
    for i in range(5): #Flash the display a couple of times
        sense.set_pixels(flash)     
        sleep(0.2)
        sense.set_pixels(pixel_list)
        sleep(0.2)

    Wait=True   
    while Wait: #Await joystich middle press for restart a game
        for event in sense.stick.get_events():
        #print("The joystick was {} {}".format(event.action, event.direction))
            if event.action == "released" and event.direction == "middle":
                Wait=False
                init() #Restart game and return to main loop again

#------------------------------------------------------
#Main loop

init()

while True:      
    for i in range(SnakeBodyLength,-1,-1): #Counting downwards to copy snake pixel positions from the back
        SnakeBodyX[i+1]=SnakeBodyX[i]
        SnakeBodyY[i+1]=SnakeBodyY[i]
        if i==0:
            sense.set_pixel(SnakeBodyX[0], SnakeBodyY[0], SnakeHeadColour)
        else:
            sense.set_pixel(SnakeBodyX[i], SnakeBodyY[i], SnakeBodyColour)
            
    if SnakeBodyLength<3:
        SnakeBodyLength+=1 #Increase length of the snake until it is 3 pixels. Larger than that requires Candy
    else: # >=3  -  When the snake has grown to be 3 pixels long, things start to happen
        # clear the last snake pixel when moving forward. Now it can only grow when eating candy
        sense.set_pixel(SnakeBodyX[SnakeBodyLength+1], SnakeBodyY[SnakeBodyLength+1], BackgroundColour)

        #Create a yummi Candy      
        if CandyVisible==False : #Need to take care NOT to place the yummi candy on top of the snake body
            SnakeBodyCollisionFound=False
            SnakeBodyCollisionChecked=False
            while SnakeBodyCollisionChecked==False:
                CandyPositionX=randint(0,7) #First attempt of where to place the candy
                CandyPositionY=randint(0,7) #First attempt of where to place the candy
                for i in range(SnakeBodyLength,0,-1):
                    if CandyPositionX==SnakeBodyX[i] and CandyPositionY==SnakeBodyY[i]: #Check if the Candy will hit an occupied pixel
                        SnakeBodyCollisionFound=True
                if SnakeBodyCollisionFound==True: #Collision found. Try again
                    SnakeBodyCollisionFound=False
                else:
                    SnakeBodyCollisionChecked=True
            sense.set_pixel(CandyPositionX, CandyPositionY, CandyColour)
            CandyVisible=True        
        else: #if CandyVisible==True
            if SnakeBodyX[0]==CandyPositionX and SnakeBodyY[0]==CandyPositionY: #Check if the Snake eats the Candy
                print('Yummi: Candy!')
                if SnakeBodyLength<MaxSnakeBodySize:
                    SnakeBodyLength+=1 #Increase length of the snake
                    if SnakeBodyLength==MaxSnakeBodySize:
                        GameOver('Win')
                CandyVisible=False   

    # Sense joystick events          
    for event in sense.stick.get_events():
        #print("The joystick was {} {}".format(event.action, event.direction))
        if event.action == "released" :      
            if event.direction == "right" and TravelDirectionX!=-1 :
                TravelDirectionX=1
                TravelDirectionY=0
            elif event.direction == "left" and TravelDirectionX!=1 :
                TravelDirectionX=-1
                TravelDirectionY=0
            elif event.direction == "down" and TravelDirectionY!=-1 :
                TravelDirectionX=0
                TravelDirectionY=1
            elif event.direction == "up" and TravelDirectionY!=1 :
                TravelDirectionX=0
                TravelDirectionY=-1
            #print('TravelDirectionX:', TravelDirectionX, 'TravelDirectionY:', TravelDirectionY)
                
    if TravelDirectionX==1 : SnakeBodyX[0]=SnakeBodyX[0]+1
    elif TravelDirectionX==-1 : SnakeBodyX[0]=SnakeBodyX[0]-1
    elif TravelDirectionY==1 : SnakeBodyY[0]=SnakeBodyY[0]+1
    elif TravelDirectionY==-1 : SnakeBodyY[0]=SnakeBodyY[0]-1
    
    #If hitting the boundaries the Game is over           
    if HardDisplayBoundaries==True:
        if SnakeBodyX[0]==8 or SnakeBodyX[0]==-1 or SnakeBodyY[0]==8 or SnakeBodyY[0]==-1 :
            print('Snake hit the wall')
            GameOver('Lose')
    else: #wrap around the display edges
        if SnakeBodyX[0]==8:SnakeBodyX[0]=0
        elif SnakeBodyX[0]==-1:SnakeBodyX[0]=7
        if SnakeBodyY[0]==8:SnakeBodyY[0]=0
        elif SnakeBodyY[0]==-1:SnakeBodyY[0]=7

    #Check if the snake has hit itself
    for i in range(SnakeBodyLength,1,-1):
        #print('i:',i,' Snake head:',SnakeBodyX[0], SnakeBodyY[0], 'vs Snake:',SnakeBodyX[i],SnakeBodyY[i])
        if SnakeBodyX[0]==SnakeBodyX[i] and SnakeBodyY[0]==SnakeBodyY[i]: #Check if the Snake Head is in an occupied pixel pixel
            print('Snake collision: ', CandyPositionX, CandyPositionY)
            GameOver('Lose')
            
    #Make the candy pixel flash to look even more tempting
    sleep(1/SnakeMovementSpeed) #0,3
    if CandyVisible==True:sense.set_pixel(CandyPositionX, CandyPositionY, BackgroundColour)
    sleep(1/SnakeMovementSpeed)  #0,4
    if CandyVisible==True:sense.set_pixel(CandyPositionX, CandyPositionY, CandyColour)

# End of main loop

