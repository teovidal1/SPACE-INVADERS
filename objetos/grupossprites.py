import pygame
from config import *
from objetos.clases import *
from pygame.sprite import Group

def crear_enemigos(grupo_enemigos: Group):
   num_enemigos_creados = 0

   for fila in range(NUM_FILAS):
      for columna in range(NUM_COLUMNAS):
            if num_enemigos_creados >= CANTIDAD_ENEMIGOS:
               break
            
            x = 50 + columna * (100 + columna // 2)
            y = 100 + fila * (70 + fila // 3)

            enemigo = NaveEnemiga(x, y)
            
            grupo_enemigos.add(enemigo)
            num_enemigos_creados += 1


def calcular_colisiones_grupos (grupo_balas: Group, grupo_enemigos: Group,
                        grupo_balas_enemigas: Group, player_group: Group,
                        grupo_cohetes: Group, player: Nave, grupo_vidas: Group,
                        grupo_explosiones: Group, grupo_boss:Group) -> None:
   """Busca las colisiones entre los distintos grupos de sprites y mata los sprites cuando es necesario, y llama métodos de otros cuando es necesario según convenga

   Args:
      grupo_balas (Group): Grupo sprites clase Balas
      grupo_enemigos (Group): Grupo sprites clase NavesEnemigas
      grupo_balas_enemigas (Group): Grupo sprites clase BalasEnemigas
      player_group (Group): Grupo sprites jugador
      grupo_cohetes (Group): Grupo sprites clase Cohetes
      player (Nave): Grupo sprites clase Nave
      grupo_vidas (Group): Grupo sprites clase Vidas
      grupo_explosiones (Group): Grupo sprites clase Explosiones
      grupo_boss (Group): Grupo sprites clase JefeFinal
   """
   pygame.sprite.groupcollide(grupo_balas, grupo_balas_enemigas, True, True)
   
   if pygame.sprite.groupcollide(grupo_balas_enemigas , player_group, True, False): #Colisión entre balas enemigas y jugador
      player.recibir_daño(grupo_vidas)
      explosion_fx.play(0)
      explosion = Explosion(player.x, player.y)
      grupo_explosiones.add(explosion)
   
   colisiones = pygame.sprite.groupcollide(grupo_cohetes, grupo_enemigos, True, True)
   for cohete, enemigos_alcanzados in colisiones.items():
      for enemigo in enemigos_alcanzados:
         cohete.kill()
         explosion_fx.play(0)
         explosion = Explosion(enemigo.x,enemigo.y)
         grupo_explosiones.add(explosion)
         
   colisiones = pygame.sprite.groupcollide(grupo_balas, grupo_enemigos, True, False)

   for bala, enemigos_alcanzados in colisiones.items():
      for enemigo in enemigos_alcanzados:
            enemigo.recibir_daño()
            bala.kill()
            explosion_fx.play(0)
            explosion = Explosion(enemigo.x, enemigo.y)
            grupo_explosiones.add(explosion)

   colisiones=pygame.sprite.groupcollide(grupo_boss,grupo_balas,False,True)
   for boss,bala in colisiones.items():
      boss.recibir_daño()
      explosion_fx.play(0)
      explosion = Explosion(boss.x, boss.y)
      grupo_explosiones.add(explosion)

   colisiones= pygame.sprite.groupcollide(grupo_boss,grupo_cohetes,False,True)
   for boss, cohete in colisiones.items():
      boss.recibir_daño()
      boss.recibir_daño()
      explosion_fx.play(0)
      explosion = Explosion(boss.x, boss.y)
      grupo_explosiones.add(explosion)

   if pygame.sprite.groupcollide(grupo_enemigos, player_group, True, False):
      player.recibir_daño(grupo_vidas)
      explosion_fx.play(0)
      explosion = Explosion(player.x, player.y)
      grupo_explosiones.add(explosion)


def actualizar_grupos(grupos: list[Group]):
   """Actualiza con UPDATE todos los grupos de sprites en la ventana."""
   for grupo in grupos:
      grupo.update()


def dibujar_grupos(grupos: list[Group], ventana):
   """Dibuja todos los grupos de sprites en la ventana."""
   for grupo in grupos:
      grupo.draw(ventana)


def crear_boss(grupo_boss: Group):
   """Crea una instancia de JefeFinal
   Args:
      grupo_boss (Group): Grupo de sprites
   """
   boss_final = JefeFinal(ANCHO_VENTANA//2, LARGO_VENTANA*0.15)
   grupo_boss.add(boss_final)
