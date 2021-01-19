#Libreria importante para pasar del csv a lista de python.
#Antes de ejecutar la linea hay que poner en consola: 'pip install pandas'
import pandas as pd

#importamos el csv a un dataFrame de pandas y regresamos una lista de este dataFrame.
def toMatrix():
    df = pd.read_csv('preferences.csv', header=None)

    return df.values.tolist()


#aqui se obtiene el rank dependiendo de la variable de preferencias
def obtener_rank(preferencias):
    rank = [[None for j in range(len(preferencias))] for i in range(len(preferencias))]

    for i in range(len(preferencias)): 
        for j in range(len(preferencias[i])):
            rank[i][preferencias[i][j]] = j

    return rank

def fase1(preferencias, rank):
    propuesta = [None for x in range(len(preferencias))]
    primero = [0 for x in range(len(preferencias))]
    ultimo = [len(x) for x in preferencias]
    en_lista = [x for x in range(len(preferencias))]

    while len(en_lista) > 0:
        i = en_lista[0]

        #aqui se modifica la primera posicion si es necesario
        while preferencias[i][primero[i]] == None:
            primero[i] +=1

        primera_opcion = preferencias[i][primero[i]]

        #si la primera opcion no tiene propuestas aun, acepta 
        if propuesta[primera_opcion] == None:
            propuesta[primera_opcion] = i

            match_rank = preferencias[primera_opcion].index(i)

            for x in range(match_rank+1, ultimo[primera_opcion]):
                rechazo = preferencias[primera_opcion][x]
                try:
                    preferencias[rechazo][rank[rechazo][primera_opcion]] = None
                except :
                    print("Ocurrio una excepcion")
                    break

            ultimo[primera_opcion] = match_rank
            del en_lista[0]

            continue
        
        actual_match_ind = rank[primera_opcion][propuesta[primera_opcion]]
        potencial_match_ind = rank[primera_opcion][i]

        if actual_match_ind < potencial_match_ind: #el match actual es preferido, i se rechaza
            preferencias[primera_opcion][potencial_match_ind] = None

            primero[i] += 1 #empieza en la siguiente posicion 

            continue

        else: #acepta la propuesta, el match anterior regresa a la lista de preferencias
            preferencias[primera_opcion][actual_match_ind] = None
            #el match viejo es rechazado por la primera opcion, se actualiza la lista
            primera_opcion_ind = rank[propuesta[primera_opcion]][primera_opcion]
            preferencias[propuesta[primera_opcion]][primera_opcion_ind] = None

            del en_lista[0]
            #agregamos el match viejo  a en_lista
            en_lista.insert(0, propuesta[primera_opcion])

            propuesta[primera_opcion] = i
            ultimo[primera_opcion] = potencial_match_ind

    return primero, ultimo, preferencias

def limpiar_preferencias(primero, ultimo, preferencias):
    for i in range(len(preferencias)):
        for j in range(len(preferencias[i])):
            if j < primero[i] or j > ultimo[i]:
                preferencias[i][j] = None

    return preferencias

def buscar_el_segundo(i, primero, ultimo, pref):
    contador = 0
    for j in range(primero[i], ultimo[i]+1):
        if not pref[j]  == None:
            contador += 1           
        elif contador == 0:
            primero[i] += 1
        if contador == 2:
            return pref[j]

    return None

def buscar_rotacion(i, p, q, primero, ultimo, preferencias):
    segundo_fav = buscar_el_segundo(p[i], primero, ultimo, preferencias[p[i]])
    siguiente_pos = preferencias[segundo_fav][ultimo[segundo_fav]]

    if siguiente_pos in p:
        #se busca la rotacion
        j = p.index(siguiente_pos)
        q[j] = segundo_fav

        return p[j:], q[j:]
    
    q.append(segundo_fav)
    p.append(siguiente_pos)
    return buscar_rotacion(i+1, p, q, primero, ultimo, preferencias)

def eliminar_rotacion(p, q, primero, ultimo, preferencias, rank):
    for i in range(len(p)):
        #q_i rechaza a p_i entonces p_i propone a q_i+1
        preferencias[p[i]][rank[p[i]][q[i]]] = None

        for j in range(rank[q[i]][p[i-1]]+1, ultimo[q[i]]):
            rechazado = rank[q[i]].index(j) 
            preferencias[rechazado][rank[rechazado][q[i]]] = None

        ultimo[q[i]] = rank[q[i]][p[i-1]]

def fase2(primero, ultimo, preferencias, rank):
    while True:
        p, q = None, None
        #busca el primero p_0 y obtine la rotacion por la lista de preferencias de p_0
        for i in range(len(preferencias)):
            if ultimo[i] - primero[i] > 0 and buscar_el_segundo(i, primero, ultimo, preferencias[i]) !=None:
                p, q = buscar_rotacion(0, [i], [None], primero, ultimo, preferencias)
                break
        
        if not p and not q:
            return preferencias

        #eliminamos rotacion 
        eliminar_rotacion(p, q, primero, ultimo, preferencias, rank)

def match_compañeros(preferencias):
    rank = obtener_rank(preferencias)
    primero, ultimo, preferencias = fase1(preferencias, rank)
    fase2(primero, ultimo, preferencias, rank)
    limpiar_preferencias(primero, ultimo, preferencias)

    matches = []
    largo = len(preferencias)
    visitado = set()
    i = 0

    for i in range(len(preferencias)):
        if not i in visitado:
            par = (i, preferencias[i][ultimo[i]])
            visitado.add(ultimo[i])
            matches.append(par)
    print('\nLas tuplas son:')
    return matches

#asignamos las preferencias del csv
preferencias = toMatrix()

print(match_compañeros(preferencias))