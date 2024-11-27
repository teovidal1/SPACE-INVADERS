import pygame
from configuracion import *
pygame.init()

#Icono.
icono = pygame.image.load("assets/imagenes/Logo/asteroid-1.png")

#Fondo del menu.
background_menu = pygame.transform.scale(pygame.image.load("assets/imagenes/Background/blue-with-stars.png"), (DIMENSION_PANTALLA))
background_titulo = pygame.image.load("assets/imagenes/Background/textospaceinvaders.png")

background_game = pygame.transform.scale(pygame.image.load("assets/imagenes/Background/space Background.png"), (DIMENSION_PANTALLA))
imagen_tierra_background = pygame.transform.scale(pygame.image.load("assets/imagenes/Background/Mundo.png"),(ANCHO_VENTANA,LARGO_VENTANA-100))

#Nave del jugador.
imagen_nave = pygame.transform.scale((pygame.image.load("assets/imagenes/Nave Jugador/NaveJugador.png")), (TAMANIO_PERSONAJE, TAMANIO_PERSONAJE))

#Explosion.
imagen_explosion1 = pygame.transform.scale((pygame.image.load("assets/imagenes/Explosiones/exp1.png")), (TAMANIO_ENEMIGOS,TAMANIO_ENEMIGOS))
imagen_explosion2 = pygame.transform.scale((pygame.image.load("assets/imagenes/Explosiones/exp2.png")), (TAMANIO_ENEMIGOS,TAMANIO_ENEMIGOS))
imagen_explosion3 = pygame.transform.scale((pygame.image.load("assets/imagenes/Explosiones/exp3.png")), (TAMANIO_ENEMIGOS,TAMANIO_ENEMIGOS))
imagen_explosion4 = pygame.transform.scale((pygame.image.load("assets/imagenes/Explosiones/exp4.png")), (TAMANIO_ENEMIGOS,TAMANIO_ENEMIGOS))

#Cohete del jugador.
imagen_cohete= pygame.transform.scale(pygame.image.load("assets/imagenes/Balas/rocket.png"),(TAMANIO_COHETE,TAMANIO_COHETE))

#Imagenes de aliens.
path_imagen_alien_1 = "assets/imagenes/Aliens/alien1.png"
path_imagen_alien_2 = "assets/imagenes/Aliens/alien2.png"
path_imagen_alien_3 = "assets/imagenes/Aliens/alien3.png"
path_imagen_alien_4 = "assets/imagenes/Aliens/alien4.png"
path_imagen_alien_5 = "assets/imagenes/Aliens/alien5.png"
path_imagen_alien_6 = "assets/imagenes/Aliens/alien6.png"
path_imagen_alien_7 = "assets/imagenes/Aliens/alien7.png"
imagen_boss_final = pygame.image.load("assets/imagenes/Aliens/boss2.png")

#Bala del jugador.
imagen_bala_jugador= pygame.transform.scale((pygame.image.load("assets/imagenes/Balas/disparoamarillo.png")), (TAMANIO_BALA_JUGADOR, TAMANIO_BALA_JUGADOR))
#Bala Enemiga.
imagen_bala_enemiga = pygame.transform.scale(pygame.image.load("assets/imagenes/Balas/BalaEnemigos.png"), (TAMANIO_BALA_ENEMIGOS, TAMANIO_BALA_ENEMIGOS))
#Corazones del jugador.
imagen_corazon = pygame.image.load("assets/imagenes/CORAZONES/heart.png")

#Pantalla final.
imagen_victoria = pygame.image.load('assets/imagenes/Pantalla Fin/won.png')
imagen_derrota = pygame.transform.scale(pygame.image.load('assets/imagenes/Pantalla Fin/GameOver.png'),(400,400))

