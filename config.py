
#VENTANA

DIMENSION_PANTALLA = (1280, 720)
ANCHO_VENTANA = DIMENSION_PANTALLA[0]
LARGO_VENTANA = DIMENSION_PANTALLA[1]
NOMBRE_VENTANA = "SPACE INVADERS"
ORIGEN_PANTALLA = (0,0)
CENTRO_VENTANA = (ANCHO_VENTANA // 2, LARGO_VENTANA // 2)


FPS = 60

#BOTONES
ANCHO_BOTON = 275
LARGO_BOTON = 100

#COLORES
ROJO = (255,0,0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
AMARILLO = (255, 255, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
CUSTOM = (226, 203, 95)

#PERSONAJE
TAMANIO_PERSONAJE = 100
VELOCIDAD_PERSONAJE = 5 #Velocidad de Movimiento
TIEMPO_RECARGA_BALAS_SIMPLES = 700 #Ticks
TIEMPO_RECARGA_COHETES = 3 * TIEMPO_RECARGA_BALAS_SIMPLES #NO TOCAR

#BALAS
TAMANIO_BALA_JUGADOR = 25
TAMANIO_BALA_ENEMIGOS = 20
VELOCIDAD_BALA_JUGADOR = -13
VELOCIDAD_COHETE_JUGADOR= -5
VELOCIDAD_BALAS_ENEMIGAS = 7
TAMANIO_COHETE = 60

#ENEMIGOS
TAMANIO_ENEMIGOS = 55 
CANTIDAD_ENEMIGOS = 15 #El Maximo es NUM_COLUMNAS*NUM_FILAS
VELOCIDAD_ENEMIGOS = 4 #Velocidad de movimiento
VELOCIDAD_DISPARO_ENEMIGO = 1  #Tendencia a disparar del enemigo
VELOCIDAD_ENEMIGOS_AVANCE = 4
VELOCIDAD_BOSS_FINAL = 8
VELOCIDAD_DISPARO_BOSS =  10000
VIDAS_BOSS_FINAL= 10

#CELDAS ENEMIGOS
NUM_FILAS = 3
NUM_COLUMNAS = 6

#VOLUMEN
VOLUMEN_MENU = 0.05
VOLUMEN_EXPLOSIONES = 0.4
VOLUMEN_COHETES = 0.25

#FUENTES
TAMAÑO_FUENTE_INSTRUCCIONES = 25

#EXPLOSIONES

TIEMPO_EXPLOSION = 4000