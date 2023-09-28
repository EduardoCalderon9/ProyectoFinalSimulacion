import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import random
import matplotlib
import math
import matplotlib.pyplot as plt
import itertools
matplotlib.use('tkagg')

st.set_page_config(layout="wide")
st.title("Proyecto")
numero_parcelas = st.text_input("Cantidad de Parcelas")
numero_vehiculos = st.text_input("Cantidad de Vehiculos")
numero_trabajadores = st.text_input("Cantidad de Trabajadores")
parcelas = []
vehiculos = []

if (
    numero_parcelas.isdigit()
    and numero_trabajadores.isdigit()
    and numero_vehiculos.isdigit()
):
    valores = [random.randint(100, 1200) for x in range(int(numero_parcelas))]
    pesos = [random.randint(1, 10) for x in range(int(numero_parcelas))]
    vehiculos = pd.DataFrame([random.randint(1000, 2500) for x in range(int(numero_vehiculos))])
    capacidad_trabajo = numero_trabajadores * 40
def cantidad_recolectada(indices):
    return valores[indices].sum(), pesos[indices].sum() 

pares = list(itertools.permutations(range(int(numero_parcelas)), 2))

matriz_peso = pd.DataFrame(index =range(int(numero_parcelas)), columns=range(int(numero_parcelas)))
matriz_peso.fillna(0, inplace=True)

matriz_valor = pd.DataFrame(index =range(int(numero_parcelas)), columns=range(int(numero_parcelas)))
matriz_valor.fillna(0, inplace=True)
for par in pares: 
    valorA=valores[par[0]]
    valorB=valores[par[1]]
    matriz_valor.loc[par[0], par[1]] = valorA + valorB

for par in pares: 
    pesoA=pesos[par[0]]
    pesoB=pesos[par[1]]
    matriz_peso.loc[par[0], par[1]] = pesoA + pesoB

def generate_random_solution(arr):
    solucion = random.sample(arr, random.randint(1 ,len(arr) - 1))
    ruta = [[solucion[i], solucion[i + 1]] for i in range(len(solucion) - 1)]
    return solucion, ruta

arr = list(range(int(numero_parcelas)))
sol, rutas = generate_random_solution(arr)

elementos_solucion = list(matriz_valor.index)[0:]
soluciones_salida = []
soluciones = [itertools.combinations(elementos_solucion, len(elementos_solucion) - x) for x in range(0, int(numero_parcelas))]
soluciones = list(itertools.chain.from_iterable(soluciones))
for sol in soluciones:
       temp_sol = list(sol)
       soluciones_salida.append(temp_sol)

poblacion_0 = random.choices(soluciones_salida, k=200)

def fitness_calculation(solucion, df_distancias):
       valor_total = 0
       peso_total = 0

       for index, rt in enumerate(solucion):
              try:
                     rt_inicial = solucion[index]
                     rt_siguiente = solucion[index + 1]
                     valor = df_distancias.loc[rt_inicial, rt_siguiente]
                     valor_total = valor_total + valor
                     if valor_total > capacidad_trabajo:
                           pass
                     if any(i < peso_total for i in vehiculos):
                           pass
              except:
                     pass
       return valor_total


def calculate_fitness_DF(poblacion):
       finess_solucion_dict = {}
       for solucion in poblacion:
              finess_solucion_dict[''.join([f'''{str(elem)}, ''' for elem in solucion])] = fitness_calculation(solucion, matriz_valor)
       df_poblacion = pd.DataFrame.from_dict(finess_solucion_dict, orient='index').reset_index()
       df_poblacion.columns = ['solucion', 'fitness']
       return df_poblacion

st.header('Algoritmo Genetico')

df_poblacion_0 = calculate_fitness_DF(poblacion_0)

n_mejores = int(len(df_poblacion_0)*0.5)
mejores_pob_0 = df_poblacion_0.nlargest(n_mejores, 'fitness')
st.write(mejores_pob_0)
st.write('Solucion optima:')
st.write(mejores_pob_0.iloc[0]['solucion'])
st.write(f'''Cantidad de caña de azucar recolectada: {mejores_pob_0.iloc[0]['fitness']}''')

st.header('Algoritmo Recocido Simulado')

def swap(ruta):
    i, j = random.sample(range(len(ruta)), 2)
    nueva_ruta = list(ruta)
    nueva_ruta[i] = nueva_ruta[j]
    nueva_ruta[j] = nueva_ruta[i]
    return nueva_ruta

iteraciones = st.text_input('Iteraciones')
#factor = st.text_input('Factor para probabilidad de aceptacion')
if iteraciones.isdigit():
    arr = list(range(int(numero_parcelas)))
    sol, rutas = generate_random_solution(arr)
    iteraciones = int(iteraciones)
    #factor = int(factor)
    fitness = []
    solucion_actual = sol
    valor_actual=fitness_calculation(solucion_actual, matriz_valor)
    mejor_solucion = solucion_actual
    mejor_valor=valor_actual

    for i in range(iteraciones):
        nueva_solucion = swap(solucion_actual)
        nuevo_valor = fitness_calculation(nueva_solucion, matriz_valor)

        if (nuevo_valor > valor_actual):
            solucion_actual = nueva_solucion
            valor_actual = nuevo_valor
            if (nuevo_valor > mejor_valor):
                    mejor_solucion = nueva_solucion
                    mejor_valor=valor_actual
            fitness.append(valor_actual)
        else:
            probabilidad_aceptacion = math.exp((nuevo_valor - valor_actual))
            if (random.random() < probabilidad_aceptacion):
                  solucion_actual = nueva_solucion
                  valor_actual = nuevo_valor

    st.write('Solucion optima:')
    st.write(''.join([f'''{str(mejor_solucion)}''']))
    st.write(f'''Cantidad de caña de azucar recolectada: {mejor_valor}''')