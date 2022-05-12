# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 17:31:38 2021

@author: merem
"""
import math
class Kmeans:
    
    def calculate_centroids(self,x,y):
        self.centroidsx = [0.1, 0.45, 0.6, 0.9]   # los componentes de centroids estan guardados
        self.centroidsy = [0.1, 0.2, 0.6, 0.9]
        #self.centroidsx = [0.1, 0.4, 0.45, 0.7]   # los componentes de centroids estan guardados
        #self.centroidsy = [0.05, 0.3, 0.40, 0.6]
        k=4
        #Declaración de variables
        disteucl = []
        iterations = 200
        n=0
        
        ##Creamos matrices vacias
        for i in range(len(x)):
            disteucl.append([])
            for j in range(len(self.centroidsx)):
                    disteucl[i].append(0)
                    
        while n<iterations:
            cluster0 = []
            cluster1 = []
            cluster2 = []
            cluster3 = []
            cluster0_x = []
            cluster1_x = []
            cluster2_x = []
            cluster3_x = []
            cluster0_y = []
            cluster1_y = []
            cluster2_y = []
            cluster3_y = []
            count0 = 0
            count1 = 0
            count2 = 0
            count3 = 0
            min_distance = []
            position = []
            
            for i in range(len(x)): #Aca tomo la distancia entre cada punto y cada centroide y los guardo en una matriz.
                for j in range(len(self.centroidsx)): #x e y son los vectores de mean_rgb_data y mhus_data
                    disteucl[i][j] = math.sqrt((x[i]-self.centroidsx[j])**2+(y[i]-self.centroidsy[j])**2)
                    disteucl[i][j] = "{:.4f}".format(disteucl[i][j]) #La matriz es de 4 columnas por n filas (n depende de la cantidad de elementos dato)
                min_distance.append(min(disteucl[i])) #Aca analizo por fila. Busco el minimo por fila. Es decir para un punto de train, cual es el centroide que tene mas cerca.
                position.append(disteucl[i].index(min_distance[i])) #Aca analizo si ese centroide mas cercano esta en el indice 1,2,3 o 4
            i=0
            
            for j in range(len(position)): #Aca formo los clusters. Es decir, voy agregando a cada. Cluster 1 es de bananas, 2 de limones, 3 de naranjas y 4 de tomates.
                if position[j]==0: #Si la posicion donde estaba la minima distancia era la 0, entonces agrego al cluster 0 ese elemendo DATO x,y
                    cluster0.append([0,0]) 
                    cluster0[count0] = [x[i],y[i]] #Aca le agrego elementos al cluster 0
                    cluster0_x.append(x[i])
                    cluster0_y.append(y[i])
                    count0 = count0 +1
                if position[j]==1: #Si la posicion donde estaba la minima distancia era la 1, entonces agrego al cluster 1 ese elemendo DATO x,y
                    cluster1.append([0,0])
                    cluster1[count1] = [x[i],y[i]] ##Aca le agrego elementos al cluster 1
                    cluster1_x.append(x[i])
                    cluster1_y.append(y[i])
                    count1 = count1 +1
                if position[j]==2:
                    cluster2.append([0,0])
                    cluster2[count2] = [x[i],y[i]]
                    cluster2_x.append(x[i])
                    cluster2_y.append(y[i])
                    count2 = count2 +1
                if position[j]==3:
                    cluster3.append([0,0])
                    cluster3[count3] = [x[i],y[i]]
                    cluster3_x.append(x[i])
                    cluster3_y.append(y[i])
                    count3 = count3 +1
                i+=1
            
            
            for i in range(2): #Aca recalculamos los centroides de cada cluster, considerando promedios en x y en y.
                if len(cluster0) != 0:
                    if i == 0:
                        c0 = sum(cluster0_x)/len(cluster0_x)
                    else:
                        c0 = sum(cluster0_y)/len(cluster0_y)
                    #c0 = sum(cluster0[i])/len(cluster0[i])
                    
                if len(cluster1) != 0:
                    if i == 0:
                        c1 = sum(cluster1_x)/len(cluster1_x)
                    else:
                        c1 = sum(cluster1_y)/len(cluster1_y)
                
                if len(cluster2) != 0:
                    if i == 0:
                        c2 = sum(cluster2_x)/len(cluster2_x)
                    else:
                        c2 = sum(cluster2_y)/len(cluster2_y)
                
                if len(cluster3) != 0:
                    if i == 0:
                        c3 = sum(cluster3_x)/len(cluster3_x)
                    else:
                        c3 = sum(cluster3_y)/len(cluster3_y)
                    
                if i==0:
                    self.centroidsx = [c0,c1,c2,c3]
                if i==1:
                    self.centroidsy = [c0,c1,c2,c3]
            n = n + 1 #iteramos muchas veces 
            
        
    
    def CalculateClass(self,x,y,x_test,y_test,srcTest):
        self.calculate_centroids(x,y)
        distance = []
        min_distance = []
        position = []
        for i in range(len(x_test)):
                distance.append([])
                for j in range(len(self.centroidsx)):
                    distance[i].append(0)
                    
        for i in range(len(x_test)): #Aca ya con los centroides formados, verificamos para cada punto de test cual es su centroide mas cercano.
            for j in range(len(self.centroidsx)):
                distance[i][j] = math.sqrt((x_test[i]-self.centroidsx[j])**2+(y_test[i]-self.centroidsy[j])**2)
                distance[i][j]="{:.4f}".format(distance[i][j])
            min_distance.append(min(distance[i]))
            position.append(distance[i].index(min_distance[i]))
        
        n=0
        count=0
        for i in position:
            print('Fruta real: '+str(srcTest[n]))
            if i == 0:
                print("Fruta detectada: Limon")
                if "limon" in srcTest[n]:count+=1
            if i == 1:
                print("Fruta detectada: Banana")
                if "banana" in srcTest[n]:count+=1
            if i == 2:
                print("Fruta detectada: Naranja")
                if "naranja" in srcTest[n]:count+=1
            if i == 3:
                print("Fruta detectada: Tomate")
                if "tomate" in srcTest[n]:count+=1
            n+=1
            
        print("\n Acuracy K-MEANS: "+str(count*100/n)+"%")
        
        #print(position)
        #print("-Cluster 1:Banana \n-Cluster 2:Limon \n-Cluster 3:Tomate \n-Cluster 4:Naranjas ")
        
        
        
        