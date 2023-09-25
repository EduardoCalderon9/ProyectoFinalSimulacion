import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import random
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Proyecto")

numero_parcelas = st.text_input('Cantidad de Parcelas')
numero_vehiculos = st.text_input('Cantidad de Vehiculos')
numero_trabajadores = st.text_input('Cantidad de Trabajadores')
parcelas = []


df = pd.DataFrame(
    [
       {'Valor': 0, 'Peso':0} for x in range(int(numero_parcelas))
   ]
)
st.data_editor(df)
