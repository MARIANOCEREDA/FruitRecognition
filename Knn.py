# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 19:14:56 2020

@author: merem
"""
import math
#from cv2 import data

class Knn:
    
    def __init__(self,k):
        self.k_nearest = []
        self.index = []
        self.k = k
        self.accuracy_counter = 0
    
    def CalculateDistEucl(self,means_RGB,mhus_sum31,test_RGB,test_mhu):
        'Calcula la distancia euclideana entre el punto de test que recibe y todos cada punto del train'
        
        ran1 = len(means_RGB)
        euclDist = []
        for i in range(ran1):
            euclDist.append(math.sqrt((means_RGB[i]-test_RGB)**2 + (mhus_sum31[i]-test_mhu)**2))    
        sortedDist = sorted(euclDist)
        self.k_nearest = sortedDist[0:self.k] #Tomo los puntos mas cercanos
        
        self.index = []
        for i in range(len(self.k_nearest)):
            self.index.append(euclDist.index(self.k_nearest[i]))
        
        return self.k_nearest,self.index #index contiene los indices de los 4 puntos mas cercanos encontrados al punto de test.
    
    def CalculateClass(self,length,n,show_percent,srcTest):
        #lenht es un vector de 4 componentes que tiene en cada elemento la lonitud de elementos de train de cada fruta
        'Segun los k_nearest encontrados, clasifica los datos'
        
        count = [0,0,0,0]
        percentage = [0,0,0,0]
        for j in range(len(self.index)): 
            i = self.index[j]
            if i in range(0,length[0]): #Si el elemento index esta entre 0 y 11, es una banana, entonces sumo 1 a ese elemento.
                count[0] +=1
            elif i in range(length[0],sum(length[0:2])): #Si esta entre 11 y 20 será limon, etc.
                count[1] +=1
            elif i in range(sum(length[0:2]),sum(length[0:3])):
                count[2] +=1
            elif i in range(sum(length[0:3]),sum(length[0:4])):
                count[3] +=1
                
        for i in range(len(count)):
            percentage[i]=count[i]/len(self.index)*100 #Aca evaluamos que tan "banana" o "naranja" o "limon", etc . Es la fruta analizada.
        
        maximo = max(percentage)
        index_max = percentage.index(maximo)
        
        
        if index_max == 0: 
            print("Fruta detectada:Banana")
            if "banana" in srcTest[n]:self.accuracy_counter+=1
        if index_max == 1: 
            print("Fruta detectada:Limon")
            if "limon" in srcTest[n]:self.accuracy_counter+=1
        if index_max == 2: 
            print("Fruta detectada:Naranja")
            if "naranja" in srcTest[n]:self.accuracy_counter+=1
        if index_max == 3: 
            print("Fruta detectada:Tomate")
            if "tomate" in srcTest[n]:self.accuracy_counter+=1
        
        if show_percent:
            print("La fruta "+str(n)+" es Banana en un : "+str(percentage[0])+"%")
            print("La fruta "+str(n)+" es Limon en un : "+str(percentage[1])+"%")
            print("La fruta "+str(n)+" es Naranja en un : "+str(percentage[2])+"%")
            print("La fruta "+str(n)+" es Tomate en un : "+str(percentage[3])+"%")
    
    
                
                
                
                
                
                