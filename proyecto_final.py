import streamlit as st
import numpy as np
import pandas as pd
import random
import math
import itertools

st.set_page_config(layout="wide")
st.title("Proyecto")

st.write('Repositorio de Proyecto: https://github.com/EduardoCalderon9/ProyectoFinalSimulacion/')
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
    valores = np.random.choice(range(100, 1200), int(numero_parcelas), replace=True)
    pesos = np.random.choice(range(1, 10), int(numero_parcelas), replace=True)
    vehiculos = np.random.choice(range(1000, 2500), int(numero_vehiculos), replace=True)
    capacidad_trabajo = int(numero_trabajadores) * 40
    st.write(pd.DataFrame(data={'Valor' : valores, 'Peso' : pesos}))
    st.write(pd.DataFrame(data={'capacidad de vehiculos' : vehiculos}))
    st.write(f'''Capacidad de Trabajo: {capacidad_trabajo}''')

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

    for i in matriz_valor:
        matriz_valor[i][i] = valores[i]
        matriz_peso[i][i] = pesos[i]
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


    poblacion_0 = random.choices(soluciones_salida, k=100)

    def fitness_calculation(solucion, df_distancias):
        valor_total = 0
        peso_total = 0
        last_index = 0
        for index, rt in enumerate(solucion):
                last_index = index
                try:
                    if len(solucion) == 1:
                        rt_inicial = solucion[index]
                        rt_siguiente = solucion[index]
                        valor = matriz_valor.loc[rt_inicial, rt_siguiente]
                        peso = matriz_peso.loc[rt_inicial, rt_siguiente]
                        if valor_total + valor > capacidad_trabajo:
                            factible = False
                            break
                        if any(i < peso_total + peso for i in vehiculos):
                            factible = False
                            break
                        peso_total = peso_total + peso
                        valor_total = valor_total + valor
                    else:
                        rt_inicial = solucion[index]
                        rt_siguiente = solucion[index + 1]
                        valor = matriz_valor.loc[rt_inicial, rt_siguiente]
                        peso = matriz_peso.loc[rt_inicial, rt_siguiente]
                        if valor_total + valor > capacidad_trabajo:
                            factible = False
                            break
                        if any(i < peso_total + peso for i in vehiculos):
                            factible = False
                            break
                        peso_total = peso_total + peso
                        valor_total = valor_total + valor
                except:
                        pass
        return last_index, valor_total


    def calculate_fitness_DF(poblacion):
        finess_solucion_dict = {}
        for solucion in poblacion:
            last_index, sol_fitness = fitness_calculation(solucion, matriz_valor)
            finess_solucion_dict[''.join([f'''{str(elem)}, ''' for elem in solucion][0:last_index + 1])] = int(sol_fitness)
        df_poblacion = pd.DataFrame.from_dict(finess_solucion_dict, orient='index').reset_index()
        df_poblacion.columns = ['solucion', 'fitness']
        return df_poblacion

    def swap(ruta):
        
            if len(ruta) > 1:
                i, j = random.sample(range(len(ruta)), 2)
                nueva_ruta = list(ruta)
                nueva_ruta[i] = nueva_ruta[j]
                nueva_ruta[j] = nueva_ruta[i]
                return nueva_ruta
            else:
                 return ruta
    
    tab1, tab2 = st.tabs(["Algoritmo Genetico", "Algoritmo Recocido"])
    with tab1:
        st.header('Algoritmo Genetico')

        st.write('un fitness de 0 representa una solucion no factible')
        df_poblacion_0 = calculate_fitness_DF(poblacion_0)
        st.write(df_poblacion_0)
            
        n_mejores = int(len(df_poblacion_0)*0.5)
        mejores_pob_0 = df_poblacion_0.nlargest(n_mejores, 'fitness')
        st.write(mejores_pob_0)
        st.write('Solucion optima:')
        st.write(mejores_pob_0.iloc[0]['solucion'])
        st.write(f'''Cantidad de caña de azucar recolectada: {mejores_pob_0.iloc[0]['fitness']}''')

        chart_data = df_poblacion_0['fitness']

        st.line_chart(chart_data)


    with tab2: 
        st.header('Algoritmo Recocido Simulado')
        iteraciones = st.text_input('Iteraciones')
        if iteraciones.isdigit():
            arr = list(range(int(numero_parcelas)))
            sol, rutas = generate_random_solution(arr)
            iteraciones = int(iteraciones)
            fitness = []
            solucion_actual = sol
            last_index, valor_actual=fitness_calculation(solucion_actual, matriz_valor)
            mejor_solucion = solucion_actual
            mejor_valor=valor_actual
            for i in range(iteraciones):
                nueva_solucion = swap(solucion_actual)
                last_index, nuevo_valor = fitness_calculation(nueva_solucion, matriz_valor)
                print(last_index)
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
            st.write(fitness)

            fitness_recocido = fitness

            st.line_chart(fitness_recocido)   
