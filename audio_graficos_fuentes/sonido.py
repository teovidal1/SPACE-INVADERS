import pygame
from config import *

disparo_fx = pygame.mixer.Sound("assets/sonidos/DisparoJugador.wav")
disparo_fx.set_volume(0.2)

explosion_fx = pygame.mixer.Sound("assets/sonidos/Explosion.wav")
explosion_fx.set_volume(VOLUMEN_EXPLOSIONES)

disparo_cohete_fx = pygame.mixer.Sound("assets/sonidos/Cohete.mp3")
disparo_cohete_fx.set_volume(VOLUMEN_COHETES)

path_musica_menu = "assets/Sonidos/musica menu.mp3"