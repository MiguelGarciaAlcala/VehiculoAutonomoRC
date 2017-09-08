import numpy as np
import glob
import cv2
import time


class Perceptron(object):
    def __init__(self, capa_oculta):
        # En el constructor se definen las siguientes variables:
        #  * perceptron: es un modelo de red ANN_MLP de OpenCV.
        #  * imagenes: es una matriz que contiene las imagenes
        #    para entrenar a la red neuronal.
        #  * etiquetas: contiene los patrones de direccion que le
        #    corresponden a cada renglon de la matriz de imagenes.
        #  * img_prueba: imagenes de prueba para la red neuronal.
        #  * etq_prueba: etiquetas asociadas a las imagenes de prueba.
        self.perceptron = cv2.ANN_MLP(np.array([200 * 100, capa_oculta, 3]))
        self.imagenes = np.zeros((1, 200 * 100))
        self.etiquetas = np.zeros((1, 3), 'float')
        self.img_prueba = np.zeros((1, 200 * 100))
        self.etq_prueba = np.zeros((1, 3), 'float')

        # Se cargan los datos de entrenamiento y de prueba para la red neuronal.
        self.cargar_datos()

    def cargar_datos(self):

        # Primero cargamos los datos de entrenamiento.
        img = glob.glob(
            'C:\Users\lluis\Desktop\XXII VICTP 2017\RECURSOS\EJEMPLOS PYTHON\OpenCV\Perceptron\img_entrenamiento\*.jpg')

        # Cada imagen se redefine como un arreglo y se apilan en la variable imagenes.
        for jpg in img:
            img_tmp = cv2.imread(jpg, 0).reshape(1, 200 * 100).astype('float32')
            self.imagenes = np.vstack((self.imagenes, img_tmp))

        # Luego cargamos los datos de prueba.
        img = glob.glob(
            'C:\Users\lluis\Desktop\XXII VICTP 2017\RECURSOS\EJEMPLOS PYTHON\OpenCV\Perceptron\img_prueba\*.jpg')

        # Las imagenes de prueba se apilan en la matriz img_prueba
        for jpg in img:
            img_tmp = cv2.imread(jpg, 0).reshape(1, 200 * 100).astype('float32')
            self.img_prueba = np.vstack((self.img_prueba, img_tmp))

        # Por ultimo, se apilan las etiquetas para cada set de imagenes.
        self.etiquetas = np.vstack((self.etiquetas, np.float32([[0, 0, 1],
                                                                [0, 0, 1],
                                                                [0, 0, 1],
                                                                [0, 0, 1],
                                                                [0, 0, 1]])))

        self.etiquetas = np.vstack((self.etiquetas, np.float32([[0, 1, 0],
                                                                [0, 1, 0],
                                                                [0, 1, 0],
                                                                [0, 1, 0],
                                                                [0, 1, 0]])))

        self.etiquetas = np.vstack((self.etiquetas, np.float32([[1, 0, 0],
                                                                [1, 0, 0],
                                                                [1, 0, 0],
                                                                [1, 0, 0],
                                                                [1, 0, 0]])))

        self.etq_prueba = np.vstack((self.etq_prueba, np.float32([[0, 0, 1],
                                                                  [0, 0, 1],
                                                                  [0, 0, 1]])))

        self.etq_prueba = np.vstack((self.etq_prueba, np.float32([[0, 1, 0],
                                                                  [0, 1, 0],
                                                                  [0, 1, 0]])))

        self.etq_prueba = np.vstack((self.etq_prueba, np.float32([[1, 0, 0],
                                                                  [1, 0, 0],
                                                                  [1, 0, 0]])))

        # Elegimos solo los renglones que nos serviran.
        self.imagenes = self.imagenes[1:, :]
        self.img_prueba = self.img_prueba[1:, :]
        self.etiquetas = self.etiquetas[1:, :]
        self.etq_prueba = self.etq_prueba[1:, :]

    def entrenar(self):

        # Se definen dos variables, la primera (criterio_term) es el criterio de
        # terminacion para el algoritmo de entrenamiento; como maximo se haran 1000
        # iteraciones y habra un error de 0.001. La segunda variable (params) es un
        # diccionario que contiene el criterio de terminacion, metodo de entrenamiento y
        # los valores bp_dw_scale y bp_moment_scale.
        criterio_term = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 1000, 0.001)
        params = dict(term_crit=criterio_term,
                      train_method=cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP,
                      bp_dw_scale=0.001,
                      bp_moment_scale=0.0)

        print "Entrenando a la red..."

        # El metodo train() recibe por lo menos cuatro parametros:
        #  * entradas: datos de entrada de la red (en nuestro caso, la matriz de imagenes).
        #  * etiquetas: patrones de salida (matriz de etiquetas)
        #  * pesos_muestra: es posible omitirlos.
        #  * params: diccionario que contiene datos de control para el algoritmo de entrenamiento.
        self.perceptron.train(self.imagenes, self.etiquetas, None, params=params)

        # Una vez que hemos entrenado a la red neuronal, hacemos la prediccion de los
        # datos de entrenamiento e imprimimos el porcentaje de aciertos.
        pred = self.perceptron.predict(self.imagenes)[1].argmax(-1)
        real = self.etiquetas.argmax(-1)

        aciertos = 100 * np.mean(pred == real)
        print "Aciertos entrenamiento: " + str(aciertos) + "%"

        # Luego hacemos una prediccion de las imagenes de prueba.
        pred_p = self.perceptron.predict(self.img_prueba)[1].argmax(-1)
        real_p = self.etq_prueba.argmax(-1)

        aciertos_p = 100 * np.mean(pred_p == real_p)
        print "Aciertos prueba: " + str(aciertos_p) + "%"

        guardar = raw_input('Guardar modelo RNA [s/n]: ')

        if guardar == 's' or guardar == 'S':
            archivo = str(int(time.time()))
            self.perceptron.save('modelo_red{}.xml'.format(archivo))


if __name__ == '__main__':
    ann = Perceptron(20)
    ann.entrenar()
