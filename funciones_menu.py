import pygame
from pygame.sprite import Group
from config import *
from objetos.clases import *
from objetos.grupossprites import *
from audio_graficos_fuentes.graficos import *
from audio_graficos_fuentes.fuentes import *
from audio_graficos_fuentes.sonido import *
from objetos.movimientoydisparo import *
from auxiliares import *
from funciones_usuarios import *


#Inicializamos pygame
pygame.init()
#Creamos un reloj para controlar los ticks del juego
reloj = pygame.time.Clock()
#Creamos la ventana del juego
ventana = pygame.display.set_mode(DIMENSION_PANTALLA)
pygame.RESIZABLE 
pygame.display.set_icon(icono) 
pygame.display.set_caption(NOMBRE_VENTANA)
#Cargamos música
pygame.mixer.music.load(path_musica_menu)
jugadores = cargar_usuarios()

musica_sonando = True

def juego() -> None:
    """
    Ejecuta el juego.
    
    Args: 
        None
    Returns: 
        None
    """
    
    pygame.mixer.music.stop()
    indice_jugador = crear_usuario(jugadores)
    ultimo_disparo = {'bala_simple': pygame.time.get_ticks(), 'cohete': pygame.time.get_ticks()}
    run = True
    boss_creado = False
    
    grupo_boss=Group()
    grupo_balas = Group()
    grupo_enemigos = Group()
    grupo_balas_enemigas = Group()
    player_group = Group()
    grupo_cohetes = Group()
    grupo_vidas = Group()
    grupo_explosiones = Group()

    grupos = [grupo_cohetes, grupo_enemigos, grupo_balas_enemigas, player_group, grupo_balas, grupo_vidas, grupo_explosiones, grupo_boss]
    #Meter todos los grupos que haya, siempre.

    player = Naves(ANCHO_VENTANA // 2, LARGO_VENTANA * 0.85)
    player_group.add(player)
    crear_enemigos(grupo_enemigos)
    player.actualizar_vidas(grupo_vidas)
    bandera_actualizacion_stats = False
    
    while run:           
        
        #Ponemos el fondo del juego con una imagen predefinida
        blitear_fondo(background_game)
        ventana.blit(imagen_tierra_background, (0, LARGO_VENTANA - 100))

        #Si el usuario cierra la ventana, se finaliza el programa.
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                salir_juego()
            #PAUSA
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    mostrar_texto(ventana, "PAUSA", fuenteinstrucciones, CENTRO_VENTANA, MAGENTA)
                    mostrar_texto(ventana, "Presiona 'p' para continuar", fuenteinstrucciones, (ANCHO_VENTANA // 2, CENTRO_VENTANA[1] + 50), BLANCO)
                    mostrar_texto(ventana, "Presiona 'q' para ir al menu", fuenteinstrucciones, (ANCHO_VENTANA // 2, CENTRO_VENTANA[1] + 100), BLANCO)
                    pygame.display.flip()
                    esperar_usuario(pygame.K_p, pygame.K_q)

        keys = pygame.key.get_pressed()

        #Si presionamos Espacio y se cargo el disparo, tiramos una bala simple
        if keys[pygame.K_SPACE] and (pygame.time.get_ticks()- ultimo_disparo['bala_simple']) > TIEMPO_RECARGA_BALAS_SIMPLES:
            disparar_bala_simple(player, grupo_balas, ultimo_disparo)

        #Si presionamos K y se cargo el disparo, tiramos un cohete
        if keys[pygame.K_r] and (pygame.time.get_ticks()- ultimo_disparo['cohete']) > TIEMPO_RECARGA_COHETES:
            disparar_cohetes(player,grupo_cohetes, ultimo_disparo)

        #Mover el personaje
        movimiento(VELOCIDAD_PERSONAJE, ANCHO_VENTANA, TAMANIO_PERSONAJE, player, keys)
    
        #Chequear colisiones entre balas y enemigos y borrarlos si es así con dokilla y dokillb activados.
        calcular_colisiones_grupos(grupo_balas, grupo_enemigos, grupo_balas_enemigas, player_group, grupo_cohetes, player, grupo_vidas, grupo_explosiones, grupo_boss)
        
        #Los enemigos disparan
        enemigos_disparar(grupo_enemigos, grupo_balas_enemigas)
    
        #Actualizamos y dibujam os todos los grupos de Sprites
        actualizar_grupos(grupos)
        dibujar_grupos(grupos, ventana)


        if len(grupo_enemigos) == 0 and not boss_creado:
            crear_boss(grupo_boss)
            boss_creado = True
        
        boss_disparar(grupo_boss,grupo_balas_enemigas)

        resultado = validar_fin_juego(boss_creado, grupo_boss, player_group)

        if resultado:
            if resultado == "Derrota":
                x_gameover = (ANCHO_VENTANA//2) - ((imagen_derrota.get_width()) // 2)
                ventana.blit(imagen_derrota, (x_gameover, (LARGO_VENTANA // 5)))
                mostrar_texto(ventana, "PERDISTE", fuenteinstrucciones, ((ANCHO_VENTANA//3 + 210), (LARGO_VENTANA * 0.75)), ROJO )
                
                if bandera_actualizacion_stats == False:
                    jugadores[indice_jugador]["partidas jugadas"] += 1
                    bandera_actualizacion_stats = True

            elif resultado == 'Victoria':
                x_gameover = (ANCHO_VENTANA//2) - ((imagen_victoria.get_width()) // 2)
                ventana.blit(imagen_victoria, (x_gameover, (LARGO_VENTANA//3 - 80)))
                mostrar_texto(ventana, "GANASTE", fuenteinstrucciones, ((ANCHO_VENTANA//3 + 210), (LARGO_VENTANA * 0.75)), VERDE)
                
                if bandera_actualizacion_stats == False:
                    jugadores[indice_jugador]["victorias"] += 1 
                    jugadores[indice_jugador]["partidas jugadas"] += 1
                    bandera_actualizacion_stats = True
                    
                    for i in range(len(jugadores)):
                            if jugadores[indice_jugador]["victorias"] > jugadores[i]["victorias"]:
                                jugadores[indice_jugador], jugadores[i] = jugadores[i], jugadores[indice_jugador] 
                                
            dibujar_boton_y_ejecutar("MENU", pygame.Rect((ANCHO_VENTANA//3 + 70), (LARGO_VENTANA * 0.8), ANCHO_BOTON, 50), ROJO, AMARILLO, main_menu)
            guardar_usuarios(jugadores)

        reloj.tick(FPS)
        pygame.display.update()


def main_menu() -> None:
    """
    Muestra el menú principal del juego.
    Dibuja los 4 botones del menú: Jugar, Instrucciones,  Rankings y Salir.
    Si se posiciona el mouse sobre algunos de los botones, el puntero del mouse cambia a la mano del click.
    Args:
        None
    Returns:
        None   
    """
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(VOLUMEN_MENU)
    musica_sonando = True

    while True:
        x_background_text = (ANCHO_VENTANA // 2) - ((background_titulo.get_width()) // 2)
        blitear_fondo(background_menu) 
        ventana.blit(background_titulo,(x_background_text,60))
        
        mouse_sobre_boton = False
        #Si el usuario cierra la ventana, se finaliza el programa.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir_juego()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if musica_sonando:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    musica_sonando = not musica_sonando
        fuente_silenciar= pygame.font.SysFont("Arial", 20,0,True)
        mostrar_texto(ventana, "Pulsa [M] para silenciar la música.", fuente_silenciar, (ANCHO_VENTANA // 2,LARGO_VENTANA - 20), ROJO)
        if dibujar_boton_y_ejecutar("COMENZAR", pygame.Rect((CENTRO_VENTANA[0] - ANCHO_BOTON-25), (500), ANCHO_BOTON, 50), AMARILLO, ROJO, juego):
            mouse_sobre_boton = True
        if dibujar_boton_y_ejecutar("INSTRUCCIONES", pygame.Rect((CENTRO_VENTANA[0] - ANCHO_BOTON - 25), (600), ANCHO_BOTON, 50), AMARILLO, ROJO, instrucciones):
            mouse_sobre_boton = True
        if dibujar_boton_y_ejecutar("RANKINGS", pygame.Rect((CENTRO_VENTANA[0] + 25), (500), ANCHO_BOTON, 50), AMARILLO, ROJO, rankings):
            mouse_sobre_boton = True    
        if dibujar_boton_y_ejecutar("SALIR", pygame.Rect((CENTRO_VENTANA[0] + 25), (600), ANCHO_BOTON, 50), ROJO, AMARILLO, salir_juego):
            mouse_sobre_boton = True

        if mouse_sobre_boton:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) #cambia a manito de click
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW) #cambia a puntero

        pygame.display.flip()


def instrucciones() -> None:
    """
    Muestra las instrucciones del juego una vez que apretamos el botón de instrucciones en el menú principal.
    Dibuja el botón para volver al menú principal.
    Si se posiciona el mouse sobre el botón, el puntero del mouse cambia a la mano del click.

    Args:
        None
    Returns:
        None
    """
    musica_sonando = True
    
    while True:
        blitear_fondo(background_game)
        mouse_sobre_boton = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir_juego()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if musica_sonando:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    musica_sonando = not musica_sonando

        mostrar_instrucciones(ventana)

        if dibujar_boton_y_ejecutar("Volver", pygame.Rect((ANCHO_VENTANA // 2 - ANCHO_BOTON // 2), LARGO_VENTANA - 70, 200, 50), VERDE, AMARILLO, main_menu):
            mouse_sobre_boton = True

        if mouse_sobre_boton:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()


def rankings() -> None:
    """
    Muestra los rankings de juegadores una vez que apretamos el botón de rankings en el menú principal.
    Dibuja el botón para volver al menú principal.
    Si se posiciona el mouse sobre el botón, el puntero del mouse cambia a la mano del click.

    Args:
        None
    Returns:
        None    
    """
    musica_sonando = True
    
    while True:
        blitear_fondo(background_game)
        mouse_sobre_boton = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir_juego()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if musica_sonando:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    musica_sonando = not musica_sonando
        mostrar_rankings()

        if dibujar_boton_y_ejecutar("Volver", pygame.Rect((ANCHO_VENTANA//2 - ANCHO_BOTON//2), LARGO_VENTANA-70, 200, 50), VERDE, AMARILLO, main_menu):
            mouse_sobre_boton = True

        if mouse_sobre_boton:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        pygame.display.flip()


def blitear_fondo(imagen:pygame.surface):
    """
    Blitea los fondos de pantalla
    """
    ventana.blit(imagen, ORIGEN_PANTALLA)


def dibujar_boton_y_ejecutar(texto:str, rect: pygame.Rect, color: tuple[int, int, int], color_con_mouse: tuple[int, int, int], action = None) -> bool:
    """
    Dibuja un botón en pantalla.
    Detecta colision entre mouse y el rectangulo. Si hay colisión, el rectángulo cambia de color.
    Si hay colisión y el usuario presiona el click izquierdo del mouse, se reproduce la acción que le enviamos por parámetro.

    Args:
        texto(str): El texto a blitear dentro del botón
        rect(Rect): El rectángulo a dibujar
        color(tuple[int, int, int]): El color del botón
        color_con_mouse (tuple[int, int, int]): El color del botón cuando el puntero del mouse está encima de él
        action(function): La función que queremos que ejecute
    Returns:
        colision_mouse_rectangulo(bool): Devuelve True si hay colision entre el puntero del mouse y el botón
    """
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    colision_mouse_rectangulo = rect.collidepoint(mouse_pos)
    
    if colision_mouse_rectangulo:
        pygame.draw.rect(ventana, color_con_mouse, rect)
        if click[0] == 1 and action: #el 1 es como decirle True
            pygame.time.delay(200)
            action()
    else:
        pygame.draw.rect(ventana, color, rect)
    
    texto_surf = fuenteinstrucciones.render(texto, True, NEGRO)
    ventana.blit(texto_surf, (rect.x + (rect.width - texto_surf.get_width()) // 2, rect.y + (rect.height - texto_surf.get_height()) // 2))
    
    return colision_mouse_rectangulo


def mostrar_texto(superficie: pygame.surface, texto: str, fuente: pygame.font.Font, posicion: tuple[int, int], color: tuple[int, int, int], color_fondo: tuple[int, int, int] = None) -> None:
    """
    Muestra texto en pantalla
    Args:
        superficie(Surface): La superficie donde se bliteará el texto
        texto(str): El texto a blitear
        fuente(Font): La fuente a utilizar para el texto
        posicion(tuple[int, int]): La posición de x e y en dónde se establecerá la superficie
        color(tuple[int, int, int]): El color del texto
        color_fondo(tuple[int, int, int]): El color de fondo del texto
    Returns:
        None
    """
    sup_texto = fuente.render(texto, True, color, color_fondo)
    rect_texto = sup_texto.get_rect(center = posicion)#le puedo pasar la posicion de movida
    superficie.blit(sup_texto, rect_texto)


def mostrar_instrucciones(ventana:pygame.Surface):
    """
    Muestra las instrucciones del juego centradas en la pantalla.

    Args:
        screen (Surface): la ventana en donde se bliteará el texto de las instrucciones.
    """

    ancho_texto = TAMAÑO_FUENTE_INSTRUCCIONES
    #DEJAR SIN TILDES EL TEXTO
    lineas = [
        "Defiende la Tierra de la invasion alienigena!",
        "Hordas de naves enemigas descienden sobre nosotros.",
        "Usa tu nave para destruirlas antes de que lleguen a la Tierra.",
        "Mueve tu nave de izquierda a derecha con las teclas A y D.",
        "Dispara con balas con [SPACE] y cohetes con [R]",
        "Evita las balas enemigas y los choques.",
        "Cada vez que te golpeen, pierdes una vida.",
        "Si pierdes tus tres vidas, el juego termina.",
        "¡Buena suerte, comandante! La Tierra cuenta contigo."]

    for i, linea in enumerate(lineas):
        x = CENTRO_VENTANA[0] - ancho_texto // 2
        y = 110 + (i * 50)
        mostrar_texto(ventana, linea, fuenteinstrucciones, (x, y), ROJO)


def mostrar_rankings():
    mostrar_texto(ventana, "POSICIONES:", fuenteinstrucciones, (ANCHO_VENTANA//2, 40), ROJO)
    for i in range (len(jugadores)):
        nombre = jugadores[i]["nombre"]
        victorias = jugadores[i]["victorias"]
        partidas_jugadas = jugadores[i]["partidas jugadas"]

        texto_renderizado = fuenteinstrucciones.render(f"{i+1}: {nombre} - {victorias} Victorias en {partidas_jugadas} partidas jugadas.", True, ROJO)
        ancho_texto, alto_texto = texto_renderizado.get_size()
        x = (ANCHO_VENTANA - (ancho_texto * 0.8))
        y = 100 + (i * (alto_texto + 20))

        mostrar_texto(ventana, f"{i+1}: {nombre} - {victorias} Victorias en {partidas_jugadas} partidas jugadas.", fuenteinstrucciones, (x, y), ROJO)
        if i == 9: 
            break #PARA QUE MUESTRE SOLO 10 USUARIOS


def crear_usuario(jugadores:list[dict]) -> int:
    """
    Permite al jugador crear su usuario.

    Retorna:
        jugadores(list[dict]): la lista de diccionarios con los datos de los jugadores
    """
    
    nombre = ""
    nombres_existentes = []
    for i in range(len(jugadores)):
        if "nombre" in jugadores[i]:
            nombres_existentes.append(jugadores[i]["nombre"])

    while True:
        blitear_fondo(background_menu)
        nombre_ingresado = fuenteinstrucciones.render("Ingresa tu nombre:", True, BLANCO)
        texto_nombre = fuenteinstrucciones.render(nombre, True, BLANCO)

        ventana.blit(nombre_ingresado, (350, 200))
        ventana.blit(texto_nombre, (350, 300))

        if nombre in nombres_existentes:
            indice_usuario = buscar_indice_usuario_en_lista(jugadores, nombre)
            texto_usuario_existente = fuenteinstrucciones.render("USUARIO EXISTENTE", True, ROJO)
            texto_usuario_registrado_victorias = fuenteinstrucciones.render(f"VICTORIAS: {jugadores[indice_usuario]['victorias']}", True, ROJO)
            texto_usuario_registrado_partidas_jugadas = fuenteinstrucciones.render(f"PARTIDAS JUGADAS: {jugadores[indice_usuario]['partidas jugadas']}", True, ROJO)
            ventana.blit(texto_usuario_existente, (350, 350))
            ventana.blit(texto_usuario_registrado_victorias, (350, 390))
            ventana.blit(texto_usuario_registrado_partidas_jugadas, (350, 430))
        
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_juego()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if nombre not in nombres_existentes:
                        usuario = {
                        "nombre" : nombre,
                        "victorias":0,
                        "partidas jugadas":0,                        
                        }
                        jugadores.append(usuario)
                        nombres_existentes.append(nombre)
                        indice_usuario = buscar_indice_usuario_en_lista(jugadores, nombre)
                    if indice_usuario is not None:
                        return buscar_indice_usuario_en_lista(jugadores, nombre)
                    else: 
                        return 0
                
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                
                elif evento.unicode.isalnum():
                    nombre += evento.unicode


def esperar_usuario(tecla: int, tecla_2: int):
    """
    Espera al usuario a que haga click para continuar

    Args:
        tecla(int): La tecla a presionar para continuar
    Returns:
        None
    """
    
    continuar = True
    while continuar:
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                salir_juego()
        
            if event.type == pygame.KEYDOWN:#esto es si apreto la tecla
                if event.key == tecla:
                    continuar = False
                if event.key == tecla_2:
                    main_menu()