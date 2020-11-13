import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
os.chdir("D:/Stockage/Programation/Python_Worspace/traitement_image")

cap = cv2.VideoCapture("FLIR1497.mp4")

fourcc=cv2.VideoWriter_fourcc(*'XVID')

out=cv2.VideoWriter('output.avi',fourcc,20.0,(320,240))

#note: dimenssion de la vidéo: 320*240 => centre 160 120

print(cap.isOpened())
zone=[[160,230],[120,170]]#XX YY

Hmax=0
Hmin=360

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:

        #print(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) #donne la largeur de l'image
        #print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) #donne la longueur de l'image

        hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#conversion HSV

        h,s,v=cv2.split(hsvframe)

        for i in range(zone[1][0],zone[1][1]):
            for j in range(zone[0][0],zone[0][1]):
                if h[i][j]>=Hmax:
                    Hmax=h[i][j]
                if h[i][j]<=Hmin:
                    Hmin=h[i][j]
                #s[i][j]=50

        for i in range(zone[1][0],zone[1][1]):
            for j in range(zone[0][0],zone[0][1]):
                h[i][j]=round((h[i][j]/(Hmax-Hmin)),0)*360
                a=1
        hsvframe=cv2.merge((h,s,v))



        out.write(hsvframe)
        cv2.imshow('frame' ,frame)
        cv2.imshow('hsvframe',hsvframe)
        plt.imshow(hsvframe)
        #plt.show()
        if cv2.waitKey(1) & 0xFF == ord("q"): #si une touche est appuyer et que c'est q on sort de la boucle
            break
    else:
        break
print(Hmax,Hmin)
cap.release()
out.release()
cv2.destroyAllWindows()