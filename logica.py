import random

# -------Configuraciones del juego ---------#

NUMERO_JUEGO = 2048 #PUEDE PONER CUALQUIER NÚMERO GANADOR
                    #PERO EL JUEGO YA NO SE LLAMARÍA 2048! :P
                    #¿ O SI ?

RANGO_GRILLA =  4# MÍNIMO RANGO 2
ARRIBA,ABAJO,IZQUIERDA,DERECHA="W".lower(),"S".lower(),"A".lower(),"D".lower()
VACIO= '' #LA GRILLA SE RELLENA CON ESTE VALOR, PUEDE PONER CUALQUIERA
FICHAS_DISPONIBLES=[4,2] # PUEDE AGREGAR MÁS NÚMEROS O CAMBIAR LOS QUE YA ESTÉN

# ------------------------------------------#

def inicializar_juego():
    print("\n\n     ¡¡ Bienvenido a \"{}\" !! Juego hecho por Lucas Ferreira\n".format(NUMERO_JUEGO))
    print("     Cátedra: Essaya")
    print("     Práctica: Alan")
    print("     Objetivo: Sumar las casillas hasta llegar a {}".format(NUMERO_JUEGO))
    fila= fila_columna_random()
    columna = fila_columna_random()
    grilla= armar_matriz(RANGO_GRILLA)
    grilla[fila_columna_random()][fila_columna_random()] = FICHAS_DISPONIBLES[ficha_aleatoria()]
    while grilla[fila][columna] != VACIO:
        fila= fila_columna_random()
        columna = fila_columna_random()
    grilla[fila][columna] = FICHAS_DISPONIBLES[ficha_aleatoria()]

    return grilla

def mostrar_juego(juego):
    print()
    cantidad_guiones = "-"*10
    print("{}{}".format(" "*5,cantidad_guiones*RANGO_GRILLA),end='-\n')
    for fila in juego:
        print(" "*5,end='')
        for columna in fila:
            print("|{:^9}".format(columna), end='')
        print("|")
        print("{}{}".format(" "*5,cantidad_guiones*RANGO_GRILLA),end='-\n')
    print()

def juego_ganado(juego):
    for fila in juego:
        if NUMERO_JUEGO in fila:
            return True

def juego_perdido(juego):
    contador_vacios=0

    for fila in juego:
        contador_vacios += fila.count(VACIO)

    if contador_vacios !=0:
        return False
    
    for fila in range(RANGO_GRILLA-1):
        for columna in range(RANGO_GRILLA-1):
            if juego[fila][columna] == juego[fila][columna+1] or juego[fila][columna] == juego[fila+1][columna] or juego[fila][-1] == juego[fila+1][-1] or juego[-1][columna] == juego[-1][columna+1]:
                return False
    return True

def pedir_direccion(juego):

    dirección = input("Use las teclas {} - {} - {} - {} para desplazarse: ".format(ARRIBA,IZQUIERDA,ABAJO,DERECHA))
    dire = dirección.lower()
    
    return dire

def no_dejar_espacios(dire,juego):
    # NO deja ningún espacio entre fichas 
    # deja todos los espacios en el sentido opuesto donde movió el jugador
    if dire == ABAJO or dire == ARRIBA:
        transponer_juego(juego,RANGO_GRILLA)
    if dire == DERECHA or dire == ABAJO:
        for fila in juego:
            ceros = fila.count(VACIO)
            mover_fichas(fila)
    if dire == IZQUIERDA or dire == ARRIBA:
        for fila in juego:
            fila.reverse()
            ceros = fila.count(VACIO)
            mover_fichas(fila)
            fila.reverse()
            
    if dire == ABAJO or dire == ARRIBA:
        transponer_juego(juego,RANGO_GRILLA)
    
def actualizar_juego(juego,dire):
    juego_nuevo = [fila.copy() for fila in juego]
    no_dejar_espacios(dire,juego_nuevo)
    #deja todos los 0 a la izquierda
    if dire == ABAJO or dire == ARRIBA:
        transponer_juego(juego_nuevo,RANGO_GRILLA)

    if dire == DERECHA or dire == ABAJO:
        for fila in juego_nuevo:
            ceros = fila.count(VACIO)
            combinar_filas(fila)
            #necesita que los ceros esten a la izquierda
    
    if dire == IZQUIERDA or dire == ARRIBA:
        for fila in juego_nuevo:
            fila.reverse()
            ceros = fila.count(VACIO)
            combinar_filas(fila)
            fila.reverse()
        
    if dire == ABAJO or dire == ARRIBA:
        transponer_juego(juego_nuevo,RANGO_GRILLA)

    no_dejar_espacios(dire,juego_nuevo)
    #vuelve a dejar todos los ceros a la izquierda
    
    return juego_nuevo


def insertar_nuevo_random(nuevo_juego):
    fila= fila_columna_random()
    columna = fila_columna_random()
    if nuevo_juego[fila][columna] == VACIO:
        nuevo_juego[fila][columna] = FICHAS_DISPONIBLES[ficha_aleatoria()]
    else: 
        while nuevo_juego[fila][columna] != VACIO:
            fila= fila_columna_random()
            columna = fila_columna_random()
            
        nuevo_juego[fila][columna] = FICHAS_DISPONIBLES[ficha_aleatoria()]
    return nuevo_juego
        

def fila_columna_random():
    return random.randrange(RANGO_GRILLA)

def ficha_aleatoria():
    cantidad_fichas= len(FICHAS_DISPONIBLES)
    return random.randrange(cantidad_fichas)

def transponer_juego(juego,n):        
    for i in range(n):
        for j in range(i+1,n):    
            if i!=j:
                juego[i][j],juego[j][i]=juego[j][i],juego[i][j]
    
def mover_vacio_izquierda(lista):
    #Recorre la lista una vez, si hay una casilla vacía la mueve a la izquierda
    for i in range (RANGO_GRILLA-1):
            if lista[i+1] == VACIO:
                lista[i],lista[i+1] =lista[i+1],lista[i]

def mover_fichas(fila):
    # mueve las fichas a la dirección que el jugador decida
    cantidad_nulos = fila.count(VACIO)
    nulo=[]
    for i in range(cantidad_nulos):
        nulo.append(VACIO)
    while fila[:cantidad_nulos] != nulo:
        mover_vacio_izquierda(fila)

def combinar_filas(fila):
    final = len(fila)
    ceros = fila.count(VACIO)
    indice=-1
    while indice >= -final+1:
        if fila[indice] == fila[indice-1]:
            fila[indice],fila[indice-1]= fila[indice]+fila[indice-1],VACIO
            indice-=2
        else:
            indice-=1

def armar_matriz(n):
    juego=[]
    for i in range(n):
        fila =[]
        for j in range(n):
            fila.append(VACIO)
        juego.append(fila)
    return juego
