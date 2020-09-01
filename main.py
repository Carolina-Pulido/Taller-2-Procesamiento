# Taller 2 -- main.py
# Leidy Carolina Pulido Feo
# Procesamiento de Imágenes y visión

import numpy as np
from imageShape import * # Importa la clase "imageShape"
import cv2
import os

if __name__ == '__main__':

    width = int(input("Introducir el ancho de la imagen"))
    height = int(input("Introducir el alto de la imagen"))
    Image_New = imageShape(width, height)   #Image_New es la nueva instancia de la clase de imageShape
    Image_New.generateShape()   #Método generación de figuras (trángulo, cuadrado(rotado 45 grados), rectángulo y círculo)
    Image_New.showShape()   #Método visiualización de imagen por 5 segundos
    image_generate,figure_string =Image_New.getShape()  #Método que retomar imagen y string de figura generada
    string_classify = Image_New.whatShape(image_generate)   #Método de clasificación de la imagen de entrada
    #Para indicar si la clasificación es correcta o no
    if figure_string == string_classify:    #¿El string del método getShape es el mismo al de la clasificación?
        print("La clasificación realizada es correcta")
    else:
        print("La clasificación realizada es incorrecta")
