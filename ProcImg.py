# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 09:18:33 2020

@author: merem
"""

import math
import cv2
import mahotas
import numpy as np
import matplotlib.pyplot as plot 
import skimage.measure

class Procesamiento_img:
    
    def GaussianFilter(slef,imGrey):
        imGauss= cv2.GaussianBlur(imGrey,(9,9),15)
        return imGauss

    def BinarizarImagen(self,imagen):
        ret,imBinaria = cv2.threshold(imagen,230,255,cv2.THRESH_BINARY) #Convierte la imagen a blanco y negro.
        return imBinaria 
    
    def NormalizeImage(self,image,index):
        height, width = image.shape
        normalizedImg = np.zeros((height, width),dtype=np.double)
        imNorm = cv2.normalize(image, normalizedImg, 0, 255, cv2.NORM_MINMAX)
        route = 'Imagenes/Modificadas/'+str(index)+'_imNorm.jpg'
        cv2.imwrite(route,imNorm)   
        return imNorm
    
    def SeparateBackground(self,imGauss,imSty,index):
        #Threshold Normal
        T = mahotas.thresholding.otsu(imGauss) 
        (_,imThresh)=cv2.threshold(imGauss,T,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU) #Los valores menores al threshold se les asigna el 0
        route = 'Imagenes/Modificadas/'+str(index)+'_imThresh.jpg'
        cv2.imwrite(route,imThresh)#Luego al aplicar los filtros, eliminamos algunos huecos ya que imMorph y imThresh son casi similares.   
        
        #Operación de cierre (erosionado + dilatación)   
        #https://docs.opencv.org/master/d9/d61/tutorial_py_morphological_ops.html
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)) #Aplica un kernel eliptico de 3 x3 a la imagen. 
        imMorph = cv2.morphologyEx(imThresh,cv2.MORPH_CLOSE,kernel,iterations = 1) #Al utilizar morphclose realiza una erosion y luego una dilatacion de la imagen.
        imMorph = cv2.morphologyEx(imThresh, cv2.MORPH_CLOSE,kernel,iterations = 1) #La imMorph Es en blanco y negro para separar las diferentes partes de la imagen.
        route = 'Imagenes/Modificadas/'+str(index)+'_imMorph.jpg'
        cv2.imwrite(route,imMorph)    
        
        #Detección de los contornos
        #https://docs.opencv.org/master/d4/d73/tutorial_py_contours_begin.html
        #https://omes-va.com/operadores-bitwise/
        c,d = cv2.findContours(imMorph,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #Encuentra los contornos de la imagen. Debe encontrar objetos blancos con fondo negro.
        cnts = sorted(c,key=cv2.contourArea)[-1]
        
        #Dibujamos los contornos
        mask= cv2.drawContours(imMorph, cnts, 0, (0, 255, 0), 0) #Dibuja los contornos encontrados en una nueva imagen, que sera la mascara.
        imMask = cv2.bitwise_and(imSty, imSty, mask=mask) #Ahora juntamos la imagen stylizada con los contornos encontrados. Dibujamos una sobre la otra.
        route = 'Imagenes/Modificadas/'+str(index)+'_imMascara.jpg'
        cv2.imwrite(route,imMask)
        
        #Rectangulo aproximado alrededor de la imagen
        #Usamos bounding rect para dibujar un rectángulo aproximado alrededor de la imagen binaria
        x, y, w, h = cv2.boundingRect(cnts) #y:coordy , x:coordx, h:alto, w:ancho. 
        imFruit = imMask[y: y + h, x: x + w] #Hasta aca importa ya que obtengo imFruit e imMorph que son las importantes.
        
        imFruitGrey= cv2.cvtColor(imFruit, cv2.COLOR_BGR2GRAY) #Pasamos la imagen a gris
        _, alpha = cv2.threshold(imFruitGrey, 0, 255, cv2.THRESH_BINARY_INV) #Binarizamos
        #Obtenemos todos los canales de la imagen objeto, que es la que contiene separada foto y fondo
        b, g, r = cv2.split(imFruit) 
        route = 'Imagenes/Modificadas/'+str(index)+'_imObjetoGris.jpg'
        cv2.imwrite(route,imFruitGrey) 
    
        #rgba = [r, g, b, alpha]
        #imFruit = cv2.merge(rgba, 4) ##Unimos el conjunto de canales separados previamente (ES DECIR, LA PARTE DE COLOR CON EL FONDO NEGRO)
        #imFruit = cv2.cvtColor(imFruit,cv2.COLOR_BGR2RGB)
               
        route = 'Imagenes/Modificadas/'+str(index)+'_imObjeto.jpg'
        cv2.imwrite(route, imFruit)
        
        return imMorph,cnts,mask,imFruit
    
    
    def GenerarCapas(self,color,imObjeto):
        color_img = imObjeto.copy()
        if color == 'rojo':
            color_img[:,:,1] = 0
            color_img[:,:,2] = 0
        if color == 'verde':
            color_img[:,:,0] = 0
            color_img[:,:,2] = 0
        if color == 'azul':
            color_img[:,:,0] = 0
            color_img[:,:,1] = 0
        return color_img
       
    def CalculateHistogram(self,imFruit,index):
        color = ["b","g","r"]
        for i, c in enumerate(color):
            hist = cv2.calcHist([imFruit],[i], None, [255], [10, 250])
        meanRGB = np.mean(hist)
        return hist,meanRGB
        
    def PlotImgs(self,listPlots,titles,subplot):
        rango = len(listPlots)
        if subplot == 'sp':
            fig1, axs = plot.subplots(2, 2)
            for i in range(rango):
                if i == 0:
                    plot.subplot(2,2,i+1),plot.imshow(cv2.cvtColor(listPlots[i],cv2.COLOR_GRAY2RGB))
                    plot.title(titles[i])
                else:
                    plot.subplot(2,2,i+1),plot.imshow(listPlots[i])
                    plot.title(titles[i])
        if subplot == 'nosp':
            fig1, axs = plot.subplots(1, 1)
            for i in range(rango):
                plot.imshow(listPlots[i])
                plot.title(titles[i])
    
            
    def HUmoments(self,imBinary):
        mu = skimage.measure.moments_central(imBinary)
        nu = skimage.measure.moments_normalized(mu)
        mhu =  skimage.measure.moments_hu(nu)
        for i in range(len(mhu)):
            mhu[i] = -1*np.sign(mhu[i])*np.log10(np.abs(mhu[i]))
        mhuActual = mhu.tolist()
        mhu1=mhu[0]
        mhu3=mhu[2]
        sum31 = mhu1 + mhu3
        #sumTot = sum(mhu)
        return sum31,mhu3,mhu1,mhuActual
    
    def Properties(self,cnts):
        area = cv2.contourArea(cnts)
        perimeter = cv2.arcLength(cnts,True)
        roundness = 4*math.pi*(area/perimeter**2)
        listProps = [perimeter,area,roundness] 
        return listProps
    
    
    

        
        
        
        
        
        
        
        
        
        
        
        