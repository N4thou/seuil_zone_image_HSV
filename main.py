#-------le programme a été calibrée pour la vidéo FLIR1497-------------
#Programme réaliser par Nathanael Thevenard


import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


os.chdir("D:/Stockage/Programation/Python_Worspace/seuillage_image")#chemin pour la source et l'enregistrement du fichier de sortie

#chois de la vidéo source
cap = cv2.VideoCapture("FLIR1497.mp4")

fourcc=cv2.VideoWriter_fourcc(*'XVID')

out=cv2.VideoWriter('output.avi',fourcc,20.0,(320,240))

#note: dimenssion de la vidéo: 320*240 => centre 160 120

print(cap.isOpened())

#coordonée de la zone a seuiller
#note: si la zone a seuiller se retrouve avec une partie a forte exposition, le seuillage perdras de son efficacité proportionnellement a la surface sur exposée
zone=[[150,230],[110,180]]#XX YY

#initilalisation des valeur min et max

#Définition de H:  0<H<360 définie de degrés
Hmax=0
Hmin=360

#Définition de S:  0<H<360
Smax=0
Smin=100

#Définition de V:  0<H<360
Vmax=0
Vmin=100

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:

        #print(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) #donne la largeur de l'image
        #print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) #donne la longueur de l'image

        hsvframe = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)#conversion HSV

        h,s,v=cv2.split(hsvframe)#decomposition de l'image

        for i in range(zone[1][0],zone[1][1]):
            for j in range(zone[0][0],zone[0][1]):
                if h[i][j]>=Hmax:
                    Hmax=h[i][j]
                if h[i][j]<=Hmin:
                    Hmin=h[i][j]
                if s[i][j]>=Smax:
                    Smax=s[i][j]
                if s[i][j]<=Smin:
                    Smin=s[i][j]
                if v[i][j]>=Vmax:
                    Vmax=v[i][j]
                if v[i][j]<=Vmin:
                    Vmin=v[i][j]


        for i in range(zone[1][0],zone[1][1]):
            for j in range(zone[0][0],zone[0][1]):
                h[i][j]=round((h[i][j]/(Hmax-Hmin)),0)*360
                s[i][j]=round((s[i][j]/(Smax-Smin)),0)*100
                v[i][j]=round((v[i][j]/(Vmax-Vmin)),0)*100

        hsvframe=cv2.merge((h,s,v))



        out.write(hsvframe)

        cv2.imshow('frame' ,frame) #affiche l'image avant la conversion en HSV
        cv2.imshow('hsvframe',hsvframe) #affiche l'image après la convertion en HSV


        plt.imshow(hsvframe) #affiche une frame de l'imag pour choisir les coordonée
        #plt.show() #cette ligne est complémentaire avec la précédente elle permet d'afficher la frame a décomenter pour choisir une zone


        if cv2.waitKey(1) & 0xFF == ord("q"): #si une touche est appuyer et que c'est q on sort de la boucle
            break
    else:
        break


print(Hmax,Hmin)
cap.release()
out.release()
cv2.destroyAllWindows()