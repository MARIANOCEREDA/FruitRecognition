import matplotlib.pyplot as plot
import cv2
from ProcImg import Procesamiento_img
from PreprosImg import Preprocesamiento_img
from Knn import Knn
from Kmeans import Kmeans

def normalize_data(total_dict):
    'Normaliza los datos, entre 0 y 1'
    
    #Encontramos el máximo y mínimo en la lista completa para normalizar
    total_list = total_dict['train'] + total_dict['test']
    x_max = max(total_list)
    x_min = min(total_list)

    #Normalizamos la data de train y el test por separado
    norm_data = list()
    norm_test = list()
    
    for key,x in total_dict.items():
        for i in x:
            if key == 'train':
                norm_data.append((i-x_min)/(x_max-x_min))
            if key == 'test':
                norm_test.append((i-x_min)/(x_max-x_min))

    return norm_data,norm_test

def plot_clusters(condition,x_plot,y_plot):
    if condition:
        plot.scatter(x_plot,y_plot, c=fruit_type)
        plot.xlabel(["Media RGB"])
        plot.ylabel(["Suma momentos hu 3 + 1"])
        plot.show()
        

if __name__ == "__main__":
    # Instanciamos objetos
    preprocImg = Preprocesamiento_img()
    img = Procesamiento_img()
    #fileProp = open("Propiedades.txt","w")

    #Leemos los archivos que contienen las frutas de data y de test
    (srcTotal,srcBanana,srcLimon,srcNaranja,srcTomate,srcTest,fruit_type) = preprocImg.ChargeImage()
    srcs = {'banana':srcBanana,'limon':srcLimon,'naranja':srcNaranja,'tomate':srcTomate}
    DATA_LENGTH = [len(srcBanana),len(srcLimon),len(srcNaranja),len(srcTomate)]

    #Inicializamos algunas variables
    n = 0 
    mhus_sum31_data = []
    means_RGB_data = [] #contendrá la media de los rgb para todas las imagenes
    fig, ax = plot.subplots()
    
    #IMAGENES DE TRAIN O DATA
    while n<len(srcTotal):
        #PREPROCESAMIENTO de imágenes - devuelve la imágen en gris , la original y la imagen con un filtro edge preserving
        (imGrey,imOriginal,imEp)=preprocImg.Convert(srcTotal[n],n)
        
        # COMIENZA EL PROCESAMIENTO 

        ##Aplicacion de filtro gaussian blur y binarización de la imagen
        imGauss = img.GaussianFilter(imGrey) #Aplica filtro gausiano. "Emborrona" la imagen y elimina ruido.Promedio ponerado de toda la imagen.
        imBinaria = img.BinarizarImagen(imGauss) #Binariza la imagen, blanco y negro
        
        ##Separación de la fruta y el fondo
        (imBinary,cnts,imMask,imFruit)=img.SeparateBackground(imGauss,imEp, n) #Separa el fondo de la fruta
        
        #Normalizado de la imagen
        imNorm = img.NormalizeImage(imBinary,n) #Aumenta la intensidad de los pixeles.Aumenta el contraste, permitiendo extraer info mas facil.
        
        #Extracción de capas e histogramas
        red_image = img.GenerarCapas("rojo",imFruit)
        green_image = img.GenerarCapas('verde',imFruit)
        blue_image = img.GenerarCapas('azul',imFruit)
        (hist,meanRGB) = img.CalculateHistogram(imFruit,n)
        means_RGB_data.append(meanRGB)
        
        # Calculo de momentos hu
        (sum31,mhu3,mhu1,mhuActual)= img.HUmoments(imNorm)
        mhus_sum31_data.append(sum31)
        
        
        #Realización de operaciones morfologicas (va antes de im norm)
        #imClose = img.OpMorfo(imBinary,cv2.MORPH_CLOSE)      ##CIERRE
        #imGradiente = img.OpMorfo(imBinaria,cv2.MORPH_GRADIENT)   ##GRADIENTE
        
        ## PROPIEDADES GEOMÉTRICAS EXTRA
        #props = img.Properties(cnts)
        n +=1
            
    #IMAGENES DE TEST
    n = 0
    mhus_sum31_test = []
    means_RGB_test = []
    while n<len(srcTest):

        #PREPROCESAMIENTO de imagenes de TEST
        (imGrey,imOriginal,imEp)=preprocImg.Convert(srcTest[n],100+n)
        
        #PROCESAMIENTO  de imagenes de test.
        imGauss = img.GaussianFilter(imGrey)
        imBinaria = img.BinarizarImagen(imGauss)
        
        (imBinary_test,cnts_test,imMask_test,imFruit_test)=img.SeparateBackground(imGauss,imEp,100+n)
        
        (hist_test,meanRGB_test) = img.CalculateHistogram(imFruit_test,100+n)
        means_RGB_test.append(meanRGB_test)
        
        imNorm_test = img.NormalizeImage(imBinary_test,100+n)
        
        (sum31_test,mhu3_test,mhu1_test,mhuActual_test)= img.HUmoments(imNorm_test)
        mhus_sum31_test.append(sum31_test)
        
        #props = img.Properties(cnts)
        n +=1
    
    total_elements_to_test = n
        
    #Combinamos el vector de entrenamiento con el de testeo en un diccionario
    means_RGB_total = {'train':means_RGB_data,'test':means_RGB_test}
    mhus_sum31_total = {'train':mhus_sum31_data,'test':mhus_sum31_test}

    #Normalizamos los vectores que contienen la información (mhus y rgb)
    norm_RGB_data,norm_RGB_test = normalize_data(means_RGB_total)
    norm_mhus_data,norm_mhus_test = normalize_data(mhus_sum31_total)

    #Ploteamos los datos
    x_plot = norm_RGB_data+norm_RGB_test
    y_plot = norm_mhus_data+norm_RGB_test
    plot_clusters(True,x_plot,y_plot)

    #ALGORITMO DE Knn
    print("\n RESULTADOS SEGÚN KNN: \n")
    knn = Knn(4)
    for i in range(len(srcTest)): #Analizo cada elemento de test y veo cuales son los puntos mas cercanos.
        print("Fruta real: ",srcTest[i])
        (knearest,index) = knn.CalculateDistEucl(norm_RGB_data,norm_mhus_data,norm_RGB_test[i],norm_mhus_test[i])
        knn.CalculateClass(DATA_LENGTH,i,False,srcTest) #DATA LENGTH contiene el tamaño del vector de datos
    print("\n Acuracy KNN: "+str(knn.accuracy_counter*100/len(srcTest))+"%")
        
    #ALGORITMO DE Kmeans
    print("\nRESULTADOS SEGÚN KMEANS: \n")
    kmeans =  Kmeans()
    kmeans.CalculateClass(norm_RGB_data,norm_mhus_data,norm_RGB_test,norm_mhus_test,srcTest)
    
    #Cantidad de frutas testeadas
    print("\n Cantidad de frutas testeadas: "+str(total_elements_to_test))


