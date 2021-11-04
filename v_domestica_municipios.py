#!/usr/bin/python
# -*- coding: utf-8 -*- 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Importamos los datos del archivo al DataFrame
filename = 'vd-victimas-juz.csv'
vic_mun = pd.read_csv(filename, encoding='latin_1')
print(vic_mun)
# Eliminamos las filas cuyo valor 'Total Denuncias' sea igual a cero
#vic_mun=vic_mun[vic_mun['Total Denuncias']!=0]
#print(vic_mun)

# Nos quedamos con las 3 columnas que nos interesan: Provincia, VICTIMA, Total Denuncias
vic_mun_ = vic_mun[['Provincia', 'VICTIMA', 'Total Denuncias']]
print(vic_mun_)
# Agrupamos por Provincia y tipo de víctima y hacemos el sumatorio por cada agrupamiento
vic_group=vic_mun_.groupby(['Provincia','VICTIMA'])
vic_group_=vic_group.aggregate(np.sum)
# Le aplicamos el reset_index para convertir el DataFrameGroupBy a DataFrame con las columnas
vic_group_.reset_index(inplace=True)
print(vic_group_)

# Estandarizamos los nombres de las provincias para su correcta lectura
provi_mal = ['AlmerÃ\xada', 'CÃ¡diz', 'CÃ³rdoba', 'MÃ¡laga', 'LeÃ³n', 'CastellÃ³n', 'La CoruÃ±a', 'Ã\x81lava',
             'GuipÃºzcoa']
provi_bien = ['Almería', 'Cádiz', 'Córdoba', 'Málaga', 'León', 'Castellón', 'La Coruña', 'Álava', 'Guipúzcoa']
vic_group_['Provincia'] = vic_group_['Provincia'].replace(provi_mal, provi_bien)

print("Aqui el vic_group_")
print(vic_group_)

# cargamos nuevos datos sobre población de mujeres por provincias
filepob = '2852bsc.csv'
pob_muj = pd.read_csv(filepob)
provi_mal2 = ['Almer�a', 'C�diz', 'C�rdoba', 'M�laga', 'Le�n', 'Castell�n', 'La Coru�a', '�lava', 'Gipuzkoa']
pob_muj['Provincias.1'] = pob_muj['Provincias.1'].replace(provi_mal2, provi_bien)

# Unimos los dos dataframes relacionando la población de mujeres por cada provincia
vic_group_ = vic_group_.merge(pob_muj, left_on='Provincia', right_on='Provincias.1')
print(vic_group_)

# Nos quedamos con las columnas que necesitamos
vic_group_ = vic_group_[['Provincia', 'VICTIMA', 'Total Denuncias', 'Total']]
print(vic_group_)

# Calculamos el índice por cada cien mil habitantes
vic_group_['Indice'] = (vic_group_['Total Denuncias'] * 100000) / vic_group_['Total']
print(vic_group_.head())

# visualizamos en una gráfica el total de denuncias por provincia
vic_num_total = vic_group_[vic_group_['VICTIMA'] == 'TOTAL MUJERES VICTIMAS DE VIOLENCIA DOMESTICA']
print("Aqui el numero total por provincia")
print(vic_num_total)

#exportamos a CSV el dataframe vic_group
vic_group_.to_csv('vdom.csv')

"""

#Preparamos para visualización
prov = vic_group_['Provincia'].unique()
# definimos categorías tipo de víctimas
cat_vic=['Vï¿½ctima-Mujer-Espaï¿½ola  > Edad', 'Vï¿½ctima-Mujer-Espaï¿½ola  < Edad', 'Vï¿½ctima-Mujer-Extranjera > Edad', 'Vï¿½ctima-Mujer-Extranjera <  Edad']
print(cat_vic)
print("probando oooo")
print(vic_group_[vic_group_["VICTIMA"]==cat_vic[3]]['Indice'])
print(prov)

vic_esp_may = vic_group_[vic_group_["VICTIMA"]==cat_vic[0]]['Indice']
vic_esp_men = vic_group_[vic_group_["VICTIMA"]==cat_vic[1]]['Indice']
vic_ext_may = vic_group_[vic_group_["VICTIMA"]==cat_vic[2]]['Indice']
vic_ext_men = vic_group_[vic_group_["VICTIMA"]==cat_vic[3]]['Indice']
print("longitud españ mayo")
print(len(vic_esp_may))
print("longitud españ menor")
print(vic_esp_men)
print("longitud extranj mayo")
print(len(vic_ext_may))
print("longitud extranj menor")
print(len(vic_ext_men))

# Visualizamos en dos gráficas: 1 Datos absolutos entre provinvias; 2 Diferenciando por tiposd e victimas
vic_num_total.groupby(by='Provincia')['Indice'].sum().plot(kind='bar')
fig, ax = plt.subplots()
ax.bar(prov, vic_esp_may, label='Española Mayor Edad')
ax.bar(prov, vic_esp_men, bottom=vic_esp_may, label='Española Menor Edad')
ax.bar(prov, vic_ext_may, bottom=vic_esp_may+vic_esp_men, label='Extranjera Mayor Edad')
ax.bar(prov, vic_ext_men, bottom=vic_esp_may +vic_esp_men+ vic_ext_may, label='Extranjera Menor Edad')
ax.set_xticklabels(prov, rotation=90)
ax.set_ylabel('Indice de Víctimas')
ax.legend()
plt.show()


########################
"""

# definimos categorías tipo de víctimas
cat_vic=['Vï¿½ctima-Mujer-Espaï¿½ola  > Edad', 'Vï¿½ctima-Mujer-Espaï¿½ola  < Edad', 'Vï¿½ctima-Mujer-Extranjera > Edad', 'Vï¿½ctima-Mujer-Extranjera <  Edad']

# Creamos dos dataframes para posteriormente filtrar por tipo de victima y provincia
vic = pd.DataFrame()
provi = pd.DataFrame()

# Realizamos copia para no machacar datos
vic_mun__ = vic_mun_.copy()

# Creamos boolean DF del DF principal para luego filtrar por tipo de victima y por Provincia
for i, cat in enumerate(cat_vic):
    vic[i] = vic_mun__['VICTIMA'] == cat

for l, prov in enumerate(vic_mun__['Provincia'].unique()):
    provi[l] = vic_mun__['Provincia'] == prov

# visualizamos en una gráfica el total de denuncias por provincia
vic_num_total = vic_mun__[vic_mun__['VICTIMA'] == 'TOTAL MUJERES VICTIMAS DE VIOLENCIA DOMESTICA']
print("Aqui el numero total por provincia")

print(vic_num_total.groupby(by='Provincia')['Total Denuncias'].sum())
# Creamos las provicias para mostrarlas en el plot
prov = vic_mun__['Provincia'].unique()

# Creamos 4 DataFrame, uno por cada tipo de víctima. Almacenaremos la suma total por provincia.
vic_pro_esp_may = pd.DataFrame()
vic_pro_esp_men = pd.DataFrame()
vic_pro_ext_may = pd.DataFrame()
vic_pro_ext_men = pd.DataFrame()
for l, pro in enumerate(provi):
    vic_pro_esp_may[l] = vic_mun__[np.logical_and(provi[l], vic[0])].sum()
vic_pro_esp_may = vic_pro_esp_may.T
for l, pro in enumerate(provi):
    vic_pro_esp_men[l] = vic_mun__[np.logical_and(provi[l], vic[1])].sum()
vic_pro_esp_men = vic_pro_esp_men.T
for l, pro in enumerate(provi):
    vic_pro_ext_may[l] = vic_mun__[np.logical_and(provi[l], vic[2])].sum()
vic_pro_ext_may = vic_pro_ext_may.T
for l, pro in enumerate(provi):
    vic_pro_ext_men[l] = vic_mun__[np.logical_and(provi[l], vic[3])].sum()
vic_pro_ext_men = vic_pro_ext_men.T

vic_num_total.groupby(by='Provincia')['Indice'].sum().plot(kind='bar')

# visualizamos en una gráfica por provincias anidando el tipo de víctima
fig, ax = plt.subplots()
ax.bar(prov, vic_pro_esp_may['Indice'], label='Española Mayor Edad')
ax.bar(prov, vic_pro_esp_men['Indice'], bottom=vic_pro_esp_may['Indice'], label='Española Menor Edad')
ax.bar(prov, vic_pro_ext_may['Indice'], bottom=vic_pro_esp_may['Indice'] + vic_pro_esp_men['Indice'],
       label='Extranjera Mayor Edad')
ax.bar(prov, vic_pro_ext_men['Indice'],
       bottom=vic_pro_esp_may['Indice'] + vic_pro_esp_men['Indice'] + vic_pro_ext_may['Indice'],
       label='Extranjera Menor Edad')
ax.set_xticklabels(prov, rotation=90)
ax.set_ylabel('Indice de Víctimas')
ax.legend()
plt.show()

"""