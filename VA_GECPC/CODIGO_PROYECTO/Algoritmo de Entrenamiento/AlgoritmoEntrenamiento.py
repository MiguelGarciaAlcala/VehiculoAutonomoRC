from sklearn.model_selection import train_test_split
import numpy as np
import glob
import time
import cv2


class AlgoritmoEntrenamiento(object):
    def __init__(self):
        self.imagenes = np.zeros((1, 320 * 120), 'float')
        self.etiquetas = np.zeros((1, 3), 'float')
        self.capas = np.int32([320 * 120, 34, 3])
        self.red_neuronal = cv2.ANN_MLP()

        self.cargar_datos()

    def cargar_datos(self):
        datos = glob.glob('C:\Users\lluis\Desktop\XXII VICTP 2017\GENERADO\CODIGO\Algoritmo de Recoleccion\Python\datos_entrenamiento\ITESZ\*.npz')

        for archivo_npz in datos:
            datos_tmp = np.load(archivo_npz)
            self.imagenes = np.vstack((self.imagenes, datos_tmp['imagenes']))
            self.etiquetas = np.vstack((self.etiquetas, datos_tmp['etiquetas']))
            datos_tmp.close()

        self.imagenes = self.imagenes[1:, :]
        self.etiquetas = self.etiquetas[1:, :]

    def entrenar_red(self):
        self.red_neuronal.create(self.capas)

        criterio = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 1000, 0.0001)
        parametros = dict(term_crit=criterio,
                          train_method=cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP,
                          bp_dw_scale=0.001,
                          bp_moment_scale=0.0)

        img_ent, img_prueba, et_ent, et_prueba = train_test_split(self.imagenes, self.etiquetas, test_size=0.25)

        print "Entrenando a la red..."
        self.red_neuronal.train(img_ent, et_ent, None, params=parametros)

        self.test_red(img_prueba, et_prueba)

        guardar = raw_input('Guardar[s/n]: ')

        if guardar == 's':
            self.red_neuronal.save('red_neuronal.xml')

    def test_red(self, img, etq):
        pred = self.red_neuronal.predict(img)[1].argmax(-1)
        aciertos = 100 * np.mean(pred == etq.argmax(-1))

        print "Aciertos: " + str(aciertos) + "%"


if __name__ == '__main__':
    algoritmo_ent = AlgoritmoEntrenamiento()
    algoritmo_ent.entrenar_red()
