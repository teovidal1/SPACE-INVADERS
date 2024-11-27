import pygame
from pygame.sprite import Group
from config import *
from audio_graficos_fuentes.graficos import *
from audio_graficos_fuentes.sonido import *
import random 

pygame.init()


class Bala(pygame.sprite.Sprite):
    def __init__(self,x,y) -> None:
        super().__init__()
        self.image = imagen_bala_jugador
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad= VELOCIDAD_BALA_JUGADOR
    def update(self):
        self.rect.y += self.velocidad

class BalaEnemiga(Bala):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = imagen_bala_enemiga
        self.velocidad=VELOCIDAD_BALAS_ENEMIGAS

class Cohete(Bala):
    def __init__(self, x, y) -> None:
        super().__init__(x, y)
        self.image = imagen_cohete
        self.velocidad = VELOCIDAD_COHETE_JUGADOR


class Naves(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = imagen_nave
        self.x = x
        self.y = y
        self.vidas = 3
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.rect.inflate_ip(0, -45) #Me quedaba muy grande la hitbox
        
    def recibir_daño(self, grupo_vidas: Group):
        self.vidas -= 1
        if self.vidas == 0:
            grupo_vidas.remove(grupo_vidas.sprites()[-1])
            self.actualizar_vidas(grupo_vidas)
            self.kill()
        else:
            grupo_vidas.remove(grupo_vidas.sprites()[-1])
            self.actualizar_vidas(grupo_vidas)

    def actualizar_vidas(self,grupo_vidas: Group):
        grupo_vidas.empty()
        x = 70
        for _ in range(self.vidas):
            vida = Vida(x, 50)
            grupo_vidas.add(vida)
            x += vida.rect.width + 10

class NaveEnemiga(pygame.sprite.Sprite):

    def __init__(self, x, y):
        imagenes_enemigos = [path_imagen_alien_1,
                            path_imagen_alien_2,
                            path_imagen_alien_3,
                            path_imagen_alien_4,
                            path_imagen_alien_5,
                            path_imagen_alien_6,
                            path_imagen_alien_7]
        imagen_aleatoria = random.choice(imagenes_enemigos)
        super().__init__()  
        self.image = pygame.transform.scale((pygame.image.load(imagen_aleatoria)), (TAMANIO_ENEMIGOS, TAMANIO_ENEMIGOS))
        self.direccion = 1
        self.x = x
        self.y = y
        self.velocidad = VELOCIDAD_ENEMIGOS
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vidas = 2
        self.tiempo_ultimo_disparo = 0
        self.tiempo_entre_disparos = random.randint(500, 1500)   
        
        self.probabilidad_disparo = VELOCIDAD_DISPARO_ENEMIGO * 0.01


    def update(self) -> None:
        self.x += self.velocidad * self.direccion
        # Si llega al borde de la pantalla, cambia de dirección
        if self.x <= 0 or self.x >= (ANCHO_VENTANA - self.rect.width):
            self.direccion *= -1
        self.rect.x = self.x

        if self.vidas == 1 :
            self.direccion = 0
            self.y += VELOCIDAD_ENEMIGOS_AVANCE
            self.rect.y = self.y
            if self.y >= LARGO_VENTANA:
                self.kill()

        elif self.vidas == 0:
            self.kill()

    def disparar(self, grupo_balas_enemigas):
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.tiempo_ultimo_disparo > self.tiempo_entre_disparos and random.random() < self.probabilidad_disparo:
            bala_enemiga = BalaEnemiga(self.rect.centerx, self.rect.y + 15)
            grupo_balas_enemigas.add(bala_enemiga)
            self.tiempo_ultimo_disparo = tiempo_actual

    def recibir_daño(self):
        self.vidas -= 1

class JefeFinal(NaveEnemiga):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vidas = VIDAS_BOSS_FINAL
        self.image = imagen_boss_final
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.velocidad = VELOCIDAD_BOSS_FINAL
        self.probabilidad_disparo = VELOCIDAD_DISPARO_BOSS * 0.01
        self.tiempo_entre_disparos = random.randint(250, 750) 
    def disparar(self, grupo_balas_enemigas):
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.tiempo_ultimo_disparo > self.tiempo_entre_disparos and random.random() < self.probabilidad_disparo:
            bala_enemiga = BalaEnemiga(self.rect.centerx, self.rect.centery + 15)
            grupo_balas_enemigas.add(bala_enemiga)
            self.tiempo_ultimo_disparo = tiempo_actual

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.imagenes = [imagen_explosion1, imagen_explosion2, imagen_explosion3, imagen_explosion4]
        self.indice = 0
        self.image = self.imagenes[self.indice]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.ultima_explosion = 0
        self.x = x
        self.y = y
        self.duracion = TIEMPO_EXPLOSION
        self.tiempo_inicio = pygame.time.get_ticks()

    def update(self) -> None:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_inicio > self.duracion:
            self.kill()

        self.indice += 1
        if self.indice >= len(self.imagenes):
            self.kill()  
        else:
            self.image = self.imagenes[self.indice]

class Vida(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = imagen_corazon
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    