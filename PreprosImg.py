# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 21:43:41 2020

@author: merem
"""
import os
import cv2

class Preprocesamiento_img:
    def __init__(self):
        self.srcBanana = []
        self.srcLimon = []
        self.srcTomate = []
        self.srcNaranja = []
        self.srcTotal = []
        self.srcData = []
    
    def ChargeImage(self):
        'Cargamos los archivos de las imágenes'
        
        self.srcBanana = os.listdir('Imagenes/Propias/Banana')
        self.srcLimon = os.listdir('Imagenes/Propias/Limon')
        self.srcNaranja = os.listdir('Imagenes/Propias/Naranja')
        self.srcTomate = os.listdir('Imagenes/Propias/Tomate')
        fruit_type = list()
        for i in range(len(self.srcBanana)):
            self.srcBanana[i] = "Imagenes/Propias/Banana/"+self.srcBanana[i]
            fruit_type.append(9) #9

        for i in range(len(self.srcLimon)):
            self.srcLimon[i] = "Imagenes/Propias/Limon/"+self.srcLimon[i]
            fruit_type.append(1) #1

        for i in range(len(self.srcNaranja)):
            self.srcNaranja[i] = "Imagenes/Propias/Naranja/"+self.srcNaranja[i]
            fruit_type.append(5) #5

        for i in range(len(self.srcTomate)):
            self.srcTomate[i] = "Imagenes/Propias/Tomate/"+self.srcTomate[i]
            fruit_type.append(3) #3

        self.srcTotal = self.srcBanana + self.srcLimon + self.srcNaranja + self.srcTomate
        self.srcData = os.listdir('Imagenes/Test/')
        for i in range(len(self.srcData)):
            self.srcData[i] = 'Imagenes/Test/'+self.srcData[i]
            fruit_type.append(7)
        print(self.srcData)
        return self.srcTotal,self.srcBanana,self.srcLimon,self.srcNaranja,self.srcTomate,self.srcData,fruit_type
    
    def Convert(self,src,n):
        'Hace un pequeño preprocesamiento para luego procesar directamente estas imagenes'
        
        ###############LECTURA DE LA IMAGEN ORIGINAL########################
        imOriginal = cv2.imread(src,1)
        ratio= 100/imOriginal.shape[1]                                       # new ratio    
        dim = (100,int(imOriginal.shape[0]*ratio))                            # new dimension to preserve the image
        imOriginal = cv2.resize(imOriginal,dim,interpolation=cv2.INTER_AREA)
        
        ################ESTILIZAMOS LA IMÁGEN ##############################
        imSty = cv2.stylization(imOriginal, sigma_s=30, sigma_r=0.8) #Suaviza la imagen, permitiendo reconocer mejor los bordes
        src_sty = "Imagenes/Estilizadas/Img_"+str(n)+"_sty.jpg"
        cv2.imwrite(src_sty,imSty)
        imEp = cv2.edgePreservingFilter(imSty, flags=1, sigma_s=30, sigma_r=0.8) #Suaviza la imagen aun mas.
        imEp = cv2.resize(imEp,(100,100),interpolation=cv2.INTER_AREA)
        src_ep = "Imagenes/Estilizadas/Img_"+str(n)+"_ep.jpg"
        cv2.imwrite(src_ep,imEp)
        
        
        #################CONVERTIMOS A ESCALA DE GRISES####################
        imGris = cv2.imread(src,0) #El 0 es para que sea leida en escala de grises
        imGris = cv2.resize(imGris,(100,100),interpolation=cv2.INTER_AREA)
        
        return imGris,imOriginal,imEp
    
    
    
    
    
    
    