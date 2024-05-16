import random
import cv2
import cvzone 
import math

class Game : 
    def __init__ (self):
        # initialize 
        self.points = []            #  all points the number 8 of hand passed from
        self.Lenght = []
        self.currentHead = 0,0     #  current Point 
        self.previosHead = 0,0 
        self.currentLenght = 0
        self.MaxLenght = 100
        self.Counter = 0
    def update (self , image , currentPoint) :   # function will get the frame and current Point
        px , py = self.previosHead      #  current Point from to dimention (x , y)
        cx , cy = currentPoint      #  current Point from to dimention (x , y)
        distance = math.hypot(cx-px , cy-py)
        self.points.append ([cx ,cy])   
        self.Lenght.append (distance)
        self.currentLenght += distance
        self.previosHead  = cx , cy
        if (self.currentLenght > self.MaxLenght ) :   #  when lenght of array bigger then 10  
                for i , Lenght in enumerate (self.Lenght) :
                        self.currentLenght -= Lenght
                        self.points.pop(i)    
                        self.Lenght.pop(i)    
                        if (self.currentLenght < self.MaxLenght ) : 
                                break
        if self.points : 
         
            for i , points in enumerate (self.points) :    

                if  i != 0 :  
                    cv2.line(image ,self.points[i-1] , self.points[i] ,(255, 102, 102) ,10 )
                #    bgr
        return image

    def update_sweet_posision (self) :

        x1 = random.random()
        y1 = random.random()

        x = (int(x1 * 1200)  + 100)
        y = (int(y1 * 600)  + 100)

        return x , y     

# ********************************************************

game = Game()


from cvzone.HandTrackingModule import HandDetector

sweet = cv2.imread( "sweet.png" , cv2.IMREAD_UNCHANGED)
sweet = cv2.resize (sweet , (50 , 50))
sweetx , sweety = game.update_sweet_posision()  # get first randomly point for cake

cap = cv2.VideoCapture(0)
detect = HandDetector(detectionCon=0.5 , maxHands=1)


#this mothode is responsible for detecting the hand when the module catches half the featruser of the hand

while (cap.isOpened()) :        # if camera is oppening
        
    ref , img = cap.read()  #  get frame for camera video continuously

    if (ref == True):       # if getting frame is success

        imgResize = cv2.resize(img, (1600,900)) # resize the frame
        img = cv2.flip(imgResize , 1)           # flip up the frame

        cv2.circle(img , (51,51) ,50 , (255, 102, 102) , 3 ) # drow circle in corner to display the score

        hands , img = detect.findHands(img , flipType=False)  # fined hands

        if hands:       # if detect hand
            lmList = hands[0]["lmList"]  #  get first hand and applay lmList system to detect points of hand
            cx , cy = lmList[8][0:2]  # get x and y dimention for point number 8 
            cvzone.overlayPNG(img , sweet , ( sweetx , sweety )  ) # drow cake on screen on randownly posision  sweetx , sweety 
            cv2.putText(img , f"{game.Counter}" , (40 , 60) , 2 , 1 ,(255, 102, 102) )  # write score inside the circel then in corner 

            if   sweetx  < cx  < sweetx + 50  and  sweety  < cy  < sweety + 50  : # when point 8 in the hand crash the cake

                game.Counter += 1          # increse counter
                game.MaxLenght += 25
                sweetx , sweety = game.update_sweet_posision() # update cake posision

            img = game.update(img , (cx , cy)) # update the line that behind the finger
        else : 
            game = Game()
        
        cv2.imshow("video" , img)

        if  (cv2.waitKey(1) & 0xFF == ord('q')) :
            break
         