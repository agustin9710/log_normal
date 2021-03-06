#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""  Requiere cargar un txt con datos en 3 columnas xyz sin encabezado donde z se normalizara con un modelo Log_normal
# Requires load a txt whit data in 3 column 'xyz' whit out heaters, the z column wil be normalize to Log_Normal model"""
__author__ = "Agustin Santamaria"
__version__ = "1"

import numpy as np
import scipy.stats as st


def constante(file):
    # usecols extrae los datos de la columna numero 2
    # The usecols use the column  in the txt
    v = np.loadtxt(file, usecols=2)

    # Definimos algunos datos estadísticos
    # Define some statistics data
    Vmin = min(v)
    Vmax = max(v)
    coef_asimetria = st.stats.skew(v)

    """Encuentra la constate 'c' para un modelo Log_Normal(x + c)
    # find the constant 'c' for Log_Normal(x + c) model"""
    if coef_asimetria > 0:

        # Definimos una constante 'c' y una variable con todos los datos del modelo
        # Define a 'c' constant and create a new variable whit de model data
        C = float(Vmax)
        v_lognor = np.log(v + C)
        print("El coeficiente de asimetría de v es ", coef_asimetria)

        # Coeficiente de asimetría del modelo log normal que buscamos
        # calculate the model skew
        coef_log = st.stats.skew(v_lognor)

        # Evitamos valores nulos para el logaritmo
        # Avoid the null values for the log
        if Vmin > 0:
            Vmin = 0.01 - Vmin
        else:
            pass

        a = st.stats.skew(np.log(v + Vmin))
        b = st.stats.skew(np.log(v + Vmax))

        while True:

            # Encontramos el punto medio
            # Find middle point
            c = (Vmin + Vmax) / 2
            coef_log = st.stats.skew(np.log(v + c))

            # Revisa si el punto medio es 0
            # Check if middle point is root
            if - 0.0001 < coef_log < 0.0001:
                print("Este es el coeficiente de asimetría para  log(x + c)", coef_log)
                print("Este es el valor de la constante c de log(v +c)", c)
                np.savetxt('Log_Normal.txt', np.log(v + c), header='log(v + c)')
                break

            # Decide si se repite el bucle
            # Decide the side to repeat the steps
            elif coef_log > 0.0001:
                Vmax = c

            else:
                Vmin = c
    else:
        # lo mismo para un modelo Log_Norma(c - x)
        # The same for the Log_Normal(x - c) model

        C = float(Vmin - 0.01)
        v_lognor = np.log(v - C)
        print("El coeficiente de asimetría de v es ", coef_asimetria)

        coef_log = st.stats.skew(v_lognor)

        # Avoid the null values for the log
        Vmax = 10000
        Vmin = Vmin - 0.0001

        b = st.stats.skew(np.log(v - Vmax))
        a = st.stats.skew(np.log(v - Vmin))

        while True:

            c = (Vmin + Vmax) / 2
            coef_log = st.stats.skew(np.log(v - c))
            print(coef_log)

            if - 0.0001 < coef_log < 0.0001:
                print("Este es el coeficiente de asimetría para  log(c - x)", coef_log)
                print("Este es el valor de la constante c de log(c - x)", c)
                np.savetxt('Log_Normalv.txt', np.log(c - v), header='log(c - v)')
                break

            elif coef_log < -0.0001:
                Vmin = c

            else:
                Vmax = c
    return
