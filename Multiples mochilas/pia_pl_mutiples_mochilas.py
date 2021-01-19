# Librerias
import pandas as pd
import math

# Variables
# Leer el archivo
articulos = pd.read_csv('data.csv', usecols=(0,1,2))
mochilas = pd.read_csv('data.csv', usecols=(4,5))

#
# Mediciones para evitar problemas (mas filas en una tabla que en otra)
#

# medir cantidad de filas de articulos
for i in range(len(articulos)):
  if math.isnan(articulos['Peso'][i]):
    break
articulos = articulos.iloc[:i+1, :]

# medir cantidad de filas de mochilas
for i in range(len(mochilas)):
  if math.isnan(mochilas['Capacidad'][i]):
    break
mochilas = mochilas.iloc[:i, :]


#
# Modificaciones a tabla de articulos
# 

# Llenar columna de ratio (beneficio / peso)
articulos['Ratio'] = [articulos['Beneficio'][i] / articulos['Peso'][i] for i in range(len(articulos))]
# Llenar columna X (numero de mochila donde entrara)
articulos['X'] = [0 for i in range(len(articulos))]
# Ordenar por Ratio de forma descendente
articulos = articulos.sort_values('Ratio', ascending=False)

#
# Modificaciones a tabla de mochilas
# 

# Ordenar por capacidad de mayor a menor
mochilas = mochilas.sort_values('Capacidad', ascending=False)

# Para cada mochila...(ordenada)
beneficio_total = 0
peso_total = 0
for i in mochilas.index:
  #
  # Ejecutar el algoritmo
  #
  peso = 0
  for j in articulos.index:
    if articulos['X'][j] == 0:
      if peso + articulos['Peso'][j] <= mochilas['Capacidad'][i]:
        peso += articulos['Peso'][j]
        beneficio_total += articulos['Beneficio'][j]
        # Para evitar conflictos se uso la funcion loc[fila, columna]
        articulos.loc[j,'X'] = mochilas['Mochila'][i]
  peso_total += peso

# Imprimir solucion
for i in mochilas.index:
  print(f"\nArticulos en mochila {mochilas['Mochila'][i]}: ")
  for j in articulos.index:
    if articulos['X'][j] == mochilas['Mochila'][i]:
      print(f"\tPeso: {articulos['Peso'][j]} --- Beneficio {articulos['Beneficio'][j]} --- Nombre: {articulos['Nombre'][j]}")
print("\n\n\t=====================================================")
print(f" \n\t     Se obtiene un valor total de beneficio de {beneficio_total}")
print(f" \n\t     con un valor total de peso de {peso_total}")
print("\n\t=====================================================")