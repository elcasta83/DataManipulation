#!/usr/bin/python
# -*- coding: utf-8 -*- 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Importamos los datos del archivo al DataFrame
filename='vd-victimas-juz.csv'
vic_mun=pd.read_csv(filename, encoding='latin_1')
print(vic_mun.head())

#Nos quedamos con las 3 columnas que nos interesan: Provincia, VICTIMA, Total Denuncias
vic_mun_=vic_mun[['Provincia', 'VICTIMA','Total Denuncias']]

#definimos categorías tipo de víctimas
cat_vic=['Vï¿½ctima-Mujer-Espaï¿½ola  > Edad', 'Vï¿½ctima-Mujer-Espaï¿½ola  > Edad', 'Vï¿½ctima-Mujer-Extranjera <  Edad', 'Vï¿½ctima-Mujer-Extranjera > Edad']
#Creamos el sumatorio por provincias y tipo de Victima y mostramos una muestra
vic_prov_2015=vic_mun_.groupby(by=['Provincia','VICTIMA']).sum()
print(vic_prov_2015[0:50])
#Creamos dos dataframes para posteriormente filtrar por tipo de victima y provincia
vic=pd.DataFrame()
provi=pd.DataFrame()
#Realizamos copia para no machacar datos
vic_mun__=vic_mun_.copy()
#Creamos boolean DF del DF principal para luego filtrar por tipo de victima y por Provincia
for i, cat in enumerate(cat_vic):
	vic[i]=vic_mun__['VICTIMA']==cat

for l, prov in enumerate(vic_mun__['Provincia'].unique()):
	provi[l]=vic_mun__['Provincia']==prov

#Creamos 4 DataFrame, uno por cada tipo de víctima. Almacenaremos la suma total por provincia.
vic_pro_esp_may=pd.DataFrame()
vic_pro_esp_men=pd.DataFrame()
vic_pro_ext_may=pd.DataFrame()
vic_pro_ext_men=pd.DataFrame()
for l, prov in enumerate(provi):
	vic_pro_esp_may[l]=vic_mun__[np.logical_and(provi[l],vic[0])].sum()
vic_pro_esp_may=vic_pro_esp_may.T
for l, prov in enumerate(provi):
	vic_pro_esp_men[l]=vic_mun__[np.logical_and(provi[l],vic[1])].sum()
vic_pro_esp_men=vic_pro_esp_men.T
for l, prov in enumerate(provi):
	vic_pro_ext_may[l]=vic_mun__[np.logical_and(provi[l],vic[2])].sum()
vic_pro_ext_may=vic_pro_ext_may.T
for l, prov in enumerate(provi):
	vic_pro_ext_men[l]=vic_mun__[np.logical_and(provi[l],vic[3])].sum()
vic_pro_ext_men=vic_pro_ext_men.T

#Creamos las provicias para mostrarlas en el plot
prov=vic_mun__['Provincia'].unique()

#visualizamos en una gráfica
fig,ax=plt.subplots()
ax.bar(prov, vic_pro_esp_may['Total Denuncias'], label='Española Mayor Edad')
ax.bar(prov, vic_pro_esp_men['Total Denuncias'],bottom=vic_pro_esp_may['Total Denuncias'], label='Española Menor Edad')
ax.bar(prov, vic_pro_ext_may['Total Denuncias'],bottom=vic_pro_esp_may['Total Denuncias']+vic_pro_esp_men['Total Denuncias'], label='Extranjera Mayor Edad')
ax.bar(prov, vic_pro_ext_men['Total Denuncias'],bottom=vic_pro_esp_may['Total Denuncias']+vic_pro_esp_men['Total Denuncias']+vic_pro_ext_may['Total Denuncias'], label='Extranjera Menor Edad')
ax.set_xticklabels(prov, rotation=90)
ax.set_ylabel('Número de Víctimas')
ax.legend()
plt.show()
