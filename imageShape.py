# Taller 2 -- imageShape.py
# Leidy Carolina Pulido Feo
# Procesamiento de Imágenes y visión

#Librerías
import numpy as np
import cv2
import random
import math

class imageShape:   # Creación de la clase imageShape

    def __init__(self, width, height):    # Constructor -- Recibe parámetros de ancho y alto
        self.width = width  #Ancho
        self.height = height    #Alto

    def generateShape(self):   # Método generateShape
        #Creación de imagen con fondo negro donde se va a integrar la figura
        size = (self.height, self.width, 3)     #Tamaño de la ventana
        self.img = np.zeros(size, np.uint8)     #Creación de imagen con fondo negro
        self.center_x = int(self.width / 2)     #Cálculo de coordenada x del centro
        self.center_y = int(self.height / 2)    #Cálculo de coordenada y del centro
        self.center = (self.center_x, self.center_y)    #Coordenada centro de la imagen
        self.aleatorio = random.randint(0, 3)    #Número aleatorio entre 0 y 3

        if self.aleatorio == 0: #Trángulo
            lado = int(min(self.width, self.height) / 2)    #Valor cada lado del triángulo equilatero
            h = int(lado * (math.sin(60*(math.pi/180))))    #Cálculo de la altura del triángulo equilátero
            #Coordenadas para los tres puntos del triángulo
            p1y = int(self.center_y - (h/2))     #Coordenada y del punto 1
            p2x = int(self.center_x + (lado/2))  #Coordenada x del punto 2
            p2y = int(self.center_y + (h/2))     #Coordenada y del punto 2
            p3x = int(self.center_x - (lado/2))  #Coordenada x del punto 3
            p3y = int(self.center_y + (h/2))     #Coordenada y del punto 3
            #Puntos-coordenadas para formar el triángulo
            pt1 = (self.center_x, p1y)   #Punto 1 de triángulo (Punta Superior)
            pt2 = (p2x, p2y)        #Punto 2 de triángulo (Punta Inferior Derecha)
            pt3 = (p3x, p3y)        #Punto 3 de triángulo (Punta Inferior Izquierda)
            triangle = np.array([pt1, pt2, pt3])    #Arreglo que unifica los tres puntos-cordenadas
            self.shape = cv2.drawContours(self.img, [triangle], 0, (255, 255, 0), -1)   #Función de dibuja el triángulo y lo rellena de color cyan

        elif self.aleatorio == 1:   #Cuadrado
            lado = int(min(self.width, self.height)/2)  #Valor cada lado del cuadrado
            x1 = (self.center_x - int(lado / 2))    #Coordenada x del vértice del cuadrado
            y1 = (self.center_y - int(lado / 2))    #Coordenada y del vértice del cuadrado
            x2 = (self.center_x + int(lado / 2))    #Coordenada x del vértice opuesto del cuadrado
            y2 = (self.center_y + int(lado / 2))    #Coordenada y del vértice del cuadrado
            self.shape = cv2.rectangle(self.img, (x1, y1), (x2, y2), (255, 255, 0), -1) #Función que dibuja el cuadrado y lo rellena de color cyan
            M_rot = cv2.getRotationMatrix2D(self.center, 45, 1) #Calcula una matriz afin de rotación en 2D
            self.shape = cv2.warpAffine(self.shape, M_rot, (self.width, self.height))   #Realiza la transformación de la figura, basado en la matriz de rotación

        elif self.aleatorio == 2:   #Rectángulo
            lado_horizontal = self.width / 2    #Valor del lado horizontal del rectángulo
            lado_vertical = self.height / 2     #Valor del lado vertical del rectángulo
            x1 = int(lado_horizontal/2)     #Coordenada x del vértice del rectángulo
            y1 = int(lado_vertical/2)       #Coordenada y del vértice del rectángulo
            x2 = int(x1 + lado_horizontal)  #Coordenada x del vértice opuesto del rectángulo
            y2 = int(y1 + lado_vertical)    #Coordenada y del vértice opuesto del rectángulo
            self.shape = cv2.rectangle(self.img, (x1, y1), (x2, y2), (255, 255, 0), -1) #Función que dibuja el rectángulo y lo rellena de color cyan

        else:   #Círculo
            radio = int(min(self.width, self.height)/4)     #Valor del radio del círculo
            self.shape = cv2.circle(self.img, self.center, radio, (255, 255, 0), -1) #Función que dibuja el círculo y lo rellena de color cyan

    def showShape(self):    # Método showShape
        if self.shape.any() :   #Si hay imagen disponible
            cv2.imshow("ImagenPrueba", self.shape)
            cv2.waitKey(5000)   #Tiempo en ms. 5000ms = 5s
        else:
            size = (self.height, self.width, 3)
            self.img = np.zeros(size, np.uint8)     #Creación de ventana en negro
            cv2.imshow("ImagenPrueba", self.img)    #Muestra la imagen de fondo negro
            cv2.waitKey(0)

    def getShape(self):     #Método getShape
        if self.aleatorio == 0:     #Triángulo
            self.figure = 'Triangle'    #String para el Triángulo
        elif self.aleatorio == 1:   #Cuadrado
            self.figure = 'Square'      #String para el Cuadrado
        elif self.aleatorio == 2:   #Rectángulo
            self.figure = 'Rectangle'   #String para el Rectángulo
        else:                       #Círculo
            self.figure = 'Circle'      #String para el Círculo
        return self.shape, self.figure  #Retorna imagen generada y string con el nombre de la figura

    def whatShape(self, image): #Método whatShape
        self.image_draw = image
        image_gray = cv2.cvtColor(self.image_draw, cv2.COLOR_BGR2GRAY)  #Tranforma imagen de entrada de la función a escala de grises
        ret, Ibw_shape = cv2.threshold(image_gray, 0, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)  #Umbralización con OTSU
        contours, hierarchy = cv2.findContours(Ibw_shape, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) #Genera el/los contornos de la imagen
        for i in contours:
            epsilon = 0.01 * cv2.arcLength(i, True) #Parámetro de precisión aproximada
            approx = cv2.approxPolyDP(i, epsilon, True) #Aproximación de la curva
            x, y, w, h = cv2.boundingRect(approx)   #Función para obtener puntos x,y ancho y alto del contorno actual

            if len(approx) == 3:    #Triángulo
                self.figure_clasi = 'Triangle'      #String para el Triángulo clasificado
                print('Segun la clasificación: La figura es un triángulo')
            elif len(approx) == 4:  #Cuadrado y rectángulo
                aspect = float(w) / h         #Cálculo para validar si es un cuadrado(=1)
                if aspect == 1:   #Cuadrado
                    self.figure_clasi = 'Square'    #String para el Cuadrado clasificado
                    print('Segun la clasificación: La figura es un cuadrado')
                else:                   #Rectángulo
                    self.figure_clasi = 'Rectangle' #String para el Rectángulo clasificado
                    print('Segun la clasificación: La figura es un rectángulo')
            elif len(approx) > 10:      #Círculo
                self.figure_clasi = 'Circle'        #String para el Círculo clasificado
                print('Segun la clasificación: La figura es un circulo')
        return self.figure_clasi    #Retorna string de figura clasificada
