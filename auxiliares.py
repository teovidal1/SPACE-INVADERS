import pygame
from pygame.sprite import Group
    

def salir_juego():
    """
    Permite salir del juego haciendo click en la x de la ventana.
    """
    pygame.quit()
    exit()


def validar_fin_juego(boss_creado:bool, grupo_boss:Group, player_group:Group) -> str:
    """
    Valida el fin del juego
    
    Args:
        grupo_enemigos(Group): El grupo de enemigos
        player_group(Group): El grupo del jugador
    Returns:
        Victoria(str)
        Derrota(str)
    """
    
    if len(grupo_boss) == 0 and boss_creado:
        return "Victoria"
    
    if len(player_group) == 0:
        return "Derrota"