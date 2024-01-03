# JORDI JOSUE DOMINGUEZ OVANDO

import pygame
from pygame.locals import *
import random

pygame.init()

# ventana
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('NO CHOQUES!!!')

# colores
gray = (100, 100, 100)
green = (50, 150, 50)
blue = (0, 5, 150)
white = (255, 255, 255, 200)
yellow = (255, 254, 0)

# configuraciones del juego
gameover = False
speed = 2
score = 0

# tamaño de los marcos
marker_width = 5
marker_height = 50

# camino y borde de marcos
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# coordenadas de las carriles
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# animación de las lineas de los carriles
lane_marker_move_y = 0

class Vehicle(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        # escala de la imagen
        image_scale = 90 / image. get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):

    def __init__(self, x, y):
        image = pygame.image.load('imagenes/Black_viper.png')
        super().__init__(image, x, y)

# coordenadas de inicio
player_x = 250
player_y = 400

# carro del jugador
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# otros vehiculos
image_filenames = ['Audi.png', 'truck.png', 'taxi.png', 'Mini_truck.png', 'Mini_van.png', 'Police.png','Ambulance.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('imagenes/' + image_filename)
    vehicle_images.append(image)

# grupo de carros (sprite group)
vehicle_group = pygame.sprite.Group()

# imagen de choque
crash = pygame.image.load('imagenes/explosion1.png')
crash_rect = crash.get_rect()

# imagen de pasto
pasto_image = pygame.image.load('imagenes/pasto.png')

# bucle del juego
clock = pygame.time.Clock()
fps = 120
running = True

# Pregunta al jugador que presione Enter para comenzar
font = pygame.font.Font(pygame.font.get_default_font(), 20)
start_text = font.render('PRESIONE ENTER PARA COMENZAR', True, white)
start_text_rect = start_text.get_rect(center=(width // 2, height // 2))

screen.blit(start_text, start_text_rect)
pygame.display.flip()

waiting_for_start = True
while waiting_for_start:
    for event in pygame.event.get():
        if event.type == QUIT:
            waiting_for_start = False
            running = False
        elif event.type == KEYDOWN and event.key == K_RETURN:
            waiting_for_start = False

while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # movimiento del carro con las teclas der/izq
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100

            # revisar si hay golpe de lado después de estar cambiando de carril
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    gameover = True

                    # acomoda el coche del jugador al lado de otro vehículo y determina la posición
                    # de la imagen de choque
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.centery + vehicle.rect.centery) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.centery + vehicle.rect.centery) / 2]

    # pasto
    for x in range(0, width, pasto_image.get_width()):
        for y in range(0, height, pasto_image.get_height()):
            screen.blit(pasto_image, (x, y))

    # carretera
    pygame.draw.rect(screen, gray, road)

    # marcos de la carretera
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # marcas de carriles
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))

    # carro del jugador dibujo
    player_group.draw(screen)

    # añadir dos vehiculos
    if len(vehicle_group) < 2:
        # asegura espacio suficiente entre los carros
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:
            # selecciona un carril random
            lane = random.choice(lanes)

            # selecciona una imagen random de un carro
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)

    # movimiento de los carros
    for vehicle in vehicle_group:
        vehicle.rect.y += speed

        # quita el carro una vez esté fuera de la pantalla
        if vehicle.rect.top >= height:
            vehicle.kill()

            # añade puntaje
            score += 1

            # aumenta velocidad al pasar 5 carros
            if score > 0 and score % 8 == 0:
                speed += 1

    # dibujo de los otros carros
    vehicle_group.draw(screen)

    # muestra el puntaje
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Puntaje: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 450)
    screen.blit(text, text_rect)

    #revisa si en frente hay un choque
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]

    # muestra game over
    if gameover:
        screen.blit(crash, crash_rect)

        pygame.draw.rect(screen, blue, (0, 50, width, 100))

        # pantalla de finalizado
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Juego Finalizado. ¿Reintentar? Presiona S o N', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)

    pygame.display.update()

    # revisa si el jugador quiere jugar de nuevo
    while gameover:

        clock.tick(fps)

        for event in pygame.event.get():

            if event.type == QUIT:
                gameover = False
                running = False

            # permite ingresar al jugador s o n
            if event.type == KEYDOWN:
                if event.key == K_s:
                    # reinicia el juego
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # cierra el bucle
                    gameover = False
                    running = False


pygame.quit()
