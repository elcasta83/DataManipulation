#!/usr/bin/python
# -*- coding: utf-8 -*- 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importamos los datos del archivo al DataFrame
filename = 'vd-victimas-juz.csv'
vic_mun = pd.read_csv(filename, encoding='latin_1')
print(vic_mun.head())

# Nos quedamos con las 3 columnas que nos interesan: Provincia, VICTIMA, Total Denuncias
vic_mun_ = vic_mun[['Provincia', 'VICTIMA', 'Total Denuncias']]

# Estandarizamos los nombres de las provincias para su correcta lectura
provi_mal = ['AlmerÃ\xada', 'CÃ¡diz', 'CÃ³rdoba', 'MÃ¡laga', 'LeÃ³n', 'CastellÃ³n', 'La CoruÃ±a', 'Ã\x81lava',
             'GuipÃºzcoa']
provi_bien = ['Almería', 'Cádiz', 'Córdoba', 'Málaga', 'León', 'Castellón', 'La Coruña', 'Álava', 'Guipúzcoa']
# vic_mun_['Provincia']=vic_mun_['Provincia'].replace(provi_mal,provi_bien)

# cargamos nuevos datos sobre población de mujeres por provincias
filepob = '2852bsc.csv'
pob_muj = pd.read_csv(filepob)
provi_mal2 = ['Almer�a', 'C�diz', 'C�rdoba', 'M�laga', 'Le�n', 'Castell�n', 'La Coru�a', '�lava', 'Gipuzkoa']
pob_muj['Provincias.1'] = pob_muj['Provincias.1'].replace(provi_mal2, provi_bien)
# Unimos los dos dataframes
vic_mun_ = vic_mun_.merge(pob_muj, left_on='Provincia', right_on='Provincias.1')

# Cargamos otro dataframe para saber a qué comunidad autonóma pertenece cada provincia
auton = 'provincias.csv'
autonomia = pd.read_csv(auton)

# unimos los dataframes
vic_mun_ = vic_mun_.merge(autonomia, left_on='Provincia', right_on='name')

# Nos quedamos con las columnas que necesitamos
vic_mun_ = vic_mun_[['Autonomía', 'VICTIMA', 'Total Denuncias', 'Total']]
vic_mun_['Indice'] = (vic_mun_['Total Denuncias'] * 100000) / vic_mun_['Total']

# definimos categorías tipo de víctimas
cat_vic = ['Vï¿½ctima-Mujer-Espaï¿½ola  > Edad', 'Vï¿½ctima-Mujer-Espaï¿½ola  < Edad',
           'Vï¿½ctima-Mujer-Extranjera > Edad', 'Vï¿½ctima-Mujer-Extranjera <  Edad']

# Creamos dos dataframes para posteriormente filtrar por tipo de victima y autonomia
vic = pd.DataFrame()
autonom = pd.DataFrame()
# Realizamos copia para no machacar datos y ordenamos alfabeticamente por autonomía
vic_mun__ = vic_mun_.copy()
vic_mun__ = vic_mun__.sort_values('Autonomía')
# Creamos boolean DF del DF principal para luego filtrar por tipo de victima y por Provincia
for i, cat in enumerate(cat_vic):
    vic[i] = vic_mun__['VICTIMA'] == cat

for l, aut in enumerate(vic_mun__['Autonomía'].unique()):
    autonom[l] = vic_mun__['Autonomía'] == aut

# Creamos 4 DataFrame, uno por cada tipo de víctima. Almacenaremos la suma total por provincia.
vic_pro_esp_may = pd.DataFrame()
vic_pro_esp_men = pd.DataFrame()
vic_pro_ext_may = pd.DataFrame()
vic_pro_ext_men = pd.DataFrame()
for l, aut in enumerate(autonom):
    vic_pro_esp_may[l] = vic_mun__[np.logical_and(autonom[l], vic[0])].sum()
vic_pro_esp_may = vic_pro_esp_may.T
for l, aut in enumerate(autonom):
    vic_pro_esp_men[l] = vic_mun__[np.logical_and(autonom[l], vic[1])].sum()
vic_pro_esp_men = vic_pro_esp_men.T
for l, aut in enumerate(autonom):
    vic_pro_ext_may[l] = vic_mun__[np.logical_and(autonom[l], vic[2])].sum()
vic_pro_ext_may = vic_pro_ext_may.T
for l, aut in enumerate(autonom):
    vic_pro_ext_men[l] = vic_mun__[np.logical_and(autonom[l], vic[3])].sum()
vic_pro_ext_men = vic_pro_ext_men.T

# Creamos las provicias para mostrarlas en el plot
autonomias = vic_mun__['Autonomía'].unique()

# visualizamos en una gráfica
fig, ax = plt.subplots()
ax.bar(autonomias, vic_pro_esp_may['Indice'], label='Española Mayor Edad')
ax.bar(autonomias, vic_pro_esp_men['Indice'], bottom=vic_pro_esp_may['Indice'], label='Española Menor Edad')
ax.bar(autonomias, vic_pro_ext_may['Indice'], bottom=vic_pro_esp_may['Indice'] + vic_pro_esp_men['Indice'],
       label='Extranjera Mayor Edad')
ax.bar(autonomias, vic_pro_ext_men['Indice'],
       bottom=vic_pro_esp_may['Indice'] + vic_pro_esp_men['Indice'] + vic_pro_ext_may['Indice'],
       label='Extranjera Menor Edad')
ax.set_xticklabels(autonomias, rotation=90)
ax.set_ylabel('Indice de Víctimas')
ax.legend()
plt.show()
