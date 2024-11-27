import pygame
from config import *
from audio_graficos_fuentes.graficos import *
from objetos.clases import *
from pygame.sprite import Group


def disparar_cohetes (player, grupo_cohetes:Group, ultimo_disparo:dict):
   disparo_cohete_fx.play(0)
   cohete = Cohete(player.x, player.y)
   grupo_cohetes.add(cohete)
   ultimo_disparo["cohete"] = pygame.time.get_ticks()

def disparar_bala_simple(player, grupo_balas:Group, ultimo_disparo:dict):
   disparo_fx.play(0)
   bala = Bala(player.x, player.y)
   grupo_balas.add(bala)
   ultimo_disparo["bala_simple"] = pygame.time.get_ticks()

def enemigos_disparar(grupo_enemigos:Group, grupo_balas_enemigas:Group):
   for enemigo in grupo_enemigos:
            enemigo.disparar(grupo_balas_enemigas)


def movimiento(VELOCIDAD_PERSONAJE:int, ANCHO_VENTANA:int,
               TAMANIO_PERSONAJE:int, player:Naves,keys):
   
   if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.x > 0 + TAMANIO_PERSONAJE: 
      player.x -= VELOCIDAD_PERSONAJE

   if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.x < ANCHO_VENTANA - TAMANIO_PERSONAJE : 
      player.x += VELOCIDAD_PERSONAJE

   player.rect.center = (player.x, player.y) 


def boss_disparar(grupo_boss,grupo_balas_enemigas):
   for enemigo in grupo_boss:
            enemigo.disparar(grupo_balas_enemigas)