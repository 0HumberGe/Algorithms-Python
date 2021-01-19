import re
import sys
import json

def mapa_nodos():
    with open('grafo.json') as json_file:
        data = json.load(json_file)
    return data

#Aqui damos el nodo de inicio
inicio = input("Ingrese el inicio: ")
#El nodo de destino
destino = input("Ingresa el destino: ")

#Una lista de los nodos visitados
visitados = []
auxiliar = []
#Aqui se guarda en el stack los nodos para despues visitar sus vecinos
stack = []
grafo = mapa_nodos()
#Guardamos el camino que lleva a el destino
camino = []
minimo = '0'
#Dejamos el nodo inicial en el stack y en los visitados
stack.append(inicio)
visitados.append(inicio)
#Hacemos un ciclo mientras el stack tenga algo seguira comprobando 
#los vecinos del nodo actual hasta encontrar el destino
while stack:
    switch = bool(False)
    auxmod = {}
    n=0
    lista = []
    actual = stack.pop()
    camino.append(actual)
    for vecino in grafo[actual]:
        aux = (grafo[actual])
        n+=1
        if vecino not in visitados:
            visitados.append(vecino)
            if len(aux) == n:
                #Se obtiene el indice del valor minimo del directorio
                if switch == False:
                    minimo = (min(aux,key=aux.get))
                    stack.append(minimo)
                else:
                    minimo = (min(auxmod,key=auxmod.get))
                    stack.append(minimo)
                    switch = bool(False)
            if vecino == destino :
                print("Encontrado:",vecino)
                print(camino)
                sys.exit(0)
        else:
            #Se eliminan los nodos ya visitados en una copia
            if switch == True:
                continue
            else:
                auxmod = dict(aux)
                switch = bool(True)
                for i in aux:
                    if i in visitados:
                        del auxmod[i]
print("No Encontrado")
print(camino)