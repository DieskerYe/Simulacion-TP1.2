import random
import sys
import numpy as np
import matplotlib.pyplot as plt
import statistics
from statistics import fmean
import argparse

# Lista de números negros en la ruleta
numeros_negros = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

# Función para simular tiradas de la ruleta
def girarRuleta(tiradas):
    return [random.randint(0, 36) for _ in range(tiradas)]

# Estrategia de Martingala
def estrategia_martingala(resultados, capital_inicial, apuesta_inicial):
    capitales_total = []
    apuestas = []
    capital_total = capital_inicial - apuesta_inicial
    apuesta = apuesta_inicial

    for nro in resultados:
        apuestas.append(apuesta)
        capitales_total.append(capital_total)
        if capital_total <= 0:
            apuesta = 0
        elif nro in numeros_negros:
            capital_total += apuesta
            apuesta = apuesta_inicial
        else:
            capital_total -= apuesta
            apuesta *= 2
    
    if capital_total <= 0:
            print("¡Capital agotado!")
            global veces_capital_agotado 
            veces_capital_agotado += 1
        
    return capitales_total, apuestas

# Estrategia de D'Alembert
def estrategia_dalembert(resultados, capital_inicial, unidad_base):
    capitales_total = []
    apuestas = []
    capital_total = capital_inicial - apuesta_inicial
    apuesta = unidad_base
    
    for nro in resultados:
        apuestas.append(apuesta)
        capitales_total.append(capital_total)
        if capital_total <= 0:
            apuesta = 0             
        elif nro in numeros_negros:
            capital_total += apuesta
            if apuesta != unidad_base:
                apuesta -= unidad_base
        else:
            capital_total -= apuesta
            apuesta += unidad_base
    
    if capital_total <= 0:
            print("¡Estas en Banca Rota!")
            global veces_capital_agotado   
            veces_capital_agotado += 1

    print(veces_capital_agotado)        
    return capitales_total, apuestas

# Estrategia de Fibonacci
def estrategia_fibonacci(resultados, capital_inicial, unidad_base):
    capitales_total = []
    apuestas = []
    capital_total = capital_inicial - apuesta_inicial
    secuencia_fibonacci = [1, 1]
    index = 0
    apuesta = secuencia_fibonacci[index] * unidad_base

    for nro in resultados:
        apuestas.append(apuesta)
        capitales_total.append(capital_total)

        if capital_total <= 0:
            apuesta = 0  
        elif nro in numeros_negros:
            capital_total += apuesta
            index = max(index - 1, 0)
        else:
            capital_total -= apuesta
            index += 1

        if index >= len(secuencia_fibonacci):
            secuencia_fibonacci.append(secuencia_fibonacci[-1] + secuencia_fibonacci[-2])

    if capital_total <= 0:
            print("¡Estas en Banca Rota!")
            global veces_capital_agotado   
            veces_capital_agotado += 1
        
    return capitales_total, apuestas

# Estrategia de Paroli
def estrategia_paroli(resultados, capital_inicial, unidad_base):
    capitales_total = []
    apuestas = []
    capital_total = capital_inicial - apuesta_inicial
    apuesta = unidad_base
    cont = 0

    for nro in resultados:
        apuestas.append(apuesta)
        capitales_total.append(capital_total)
        if capital_total <= 0:
            apuesta = 0  
        elif nro in numeros_negros:
            capital_total += apuesta
            cont += 1
            if cont == 3:
                cont = 0
                apuesta = unidad_base
            else:
                apuesta *= 2
        else:
            apuesta = unidad_base
            capital_total -= apuesta

    if capital_total <= 0:
            print("¡Estas en Banca Rota!")
            global veces_capital_agotado   
            veces_capital_agotado += 1
        
    return capitales_total, apuestas

# Función para calcular las frecuencias relativas de los números negros
def calcularFR(resultados, tiradas, simulaciones):
    frecuencias = []
    for j in range(simulaciones):
        frecuencias.append([])
        cont = 0

        for i in range(1, tiradas + 1):
            if resultados[j][i - 1] in numeros_negros:
                cont += 1
            frecuencias[j].append(cont / i)
    frecuencias.append([])
    for i in range(tiradas):
        acc = 0
        for j in range(simulaciones):
            acc += frecuencias[j][i]
        frecuencias[simulaciones].append(acc / simulaciones)
    return frecuencias

# Función para graficar el historial de capital y las apuestas
def graficar(valores, capInicial, apuesta_min, giros, sim, title):
    fig, ax = plt.subplots(2)
    x = range(giros)
    fig.suptitle(title, fontsize=24)
    ax[0].axhline(y=capInicial, color='black', label="Capital \ninicial")
    ax[0].axhline(y=0, color='black')
    ax[0].set_xlabel("Tiradas")
    ax[0].set_ylabel("Capital")
    plt.tight_layout()
    ax[1].axhline(y=apuesta_min, color='black', label="Apuesta \nminíma")
    ax[1].set_xlabel("Tiradas")
    ax[1].set_ylabel("Apuestas")
    for i in range(0, sim * 2):
        if i % 2 == 0:
            ax[0].plot(valores[i])
        else:
            ax[1].scatter(x, valores[i], s=5)
    ax[0].legend(bbox_to_anchor=(1.11, 0.6), ncol=2)
    ax[1].legend(bbox_to_anchor=(1.12, 0.6), ncol=2)
    plt.show()

# Función para graficar las frecuencias relativas de los números negros
def graficarFR(fr, sim):
    fig, ax = plt.subplots(2)
    fig.suptitle("Frecuencias relativas números negros", fontsize=24)
    ax[0].axhline(y=18 / 37, color='black', label="Frecuencia \nesperada")
    ax[0].set_ylabel("Frecuencias relativas")
    ax[0].set_xlabel("Tiradas")
    plt.tight_layout()
    for i in range(sim):
        ax[0].plot(fr[i])
    ax[0].legend(bbox_to_anchor=(1.12, 0), ncol=2)
    ax[0].set_ylim(0, 1)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simulación de ruleta')
    parser.add_argument('-n', type=int, help='Cantidad de tiradas', required=True)
    parser.add_argument('-c', type=int, help='Cantidad de corridas', required=True)
    parser.add_argument('-e', type=int, help='Número elegido', required=True)
    parser.add_argument('-s', choices=['m', 'd', 'f', 'p'], help='Estrategia utilizada', required=True)
    parser.add_argument('-a', choices=['f', 'i'], help='Tipo de capital (finito o infinito)', required=True)
    args = parser.parse_args()

    cant_tiradas = args.n
    cant_corridas = args.c
    num_elegido = args.e
    estrategia = args.s
    tipo_capital = args.a
    veces_capital_agotado = 0
    capital_inicial = float('inf') if tipo_capital == 'i' else 40000
    apuesta_inicial = 200

    resultados = [girarRuleta(cant_tiradas) for _ in range(cant_corridas)]
    valores_capital = []

    for res in resultados:
        if estrategia == 'm':
            valores_capital.extend(estrategia_martingala(res, capital_inicial, apuesta_inicial))
        elif estrategia == 'd':
            valores_capital.extend(estrategia_dalembert(res, capital_inicial, apuesta_inicial))
        elif estrategia == 'p':
            valores_capital.extend(estrategia_paroli(res, capital_inicial, apuesta_inicial))
        elif estrategia == 'f':
            valores_capital.extend(estrategia_fibonacci(res, capital_inicial, apuesta_inicial))
    
    print(veces_capital_agotado)
    fr = calcularFR(resultados, cant_tiradas, cant_corridas)
    graficarFR(fr, cant_corridas)
    graficar(valores_capital, capital_inicial, apuesta_inicial, cant_tiradas, cant_corridas, "Historial de capital")