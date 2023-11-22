import pygame
from player import *
from enemy import *
from bullet import *
from global_Var import *

def main_menu():
    menu_font = pygame.font.Font(None, 48)
    menu_text = menu_font.render("Presiona Enter para comenzar", True, white)
    menu_rect = menu_text.get_rect(center=(width // 2, height // 2))

     # Crear una superficie para el fondo del menú
    menu_background = pygame.Surface((width, height))
    menu_background.fill((0, 0, 0))  # Puedes cambiar esto al color que desees para el fondo del menú

    # Cargar la imagen de fondo en la superficie del menú
    menu_background_image = pygame.image.load("img/bge.jpg")
    menu_background.blit(menu_background_image, (0, 0))

    screen.blit(menu_background, (0, 0))  # Dibujar el fondo del menú en lugar de la imagen directamente
    screen.blit(menu_text, menu_rect)
    pygame.display.flip()

    waiting_for_key = True
    while waiting_for_key:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_key = False


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music/Orbital Colossus.mp3')

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Camino Hacia El Anillo")
clock = pygame.time.Clock()

fps = 60

# Carga la imagen de fondo
background = pygame.image.load("img/bg.jpg")

background_position_y = 0

all_sprites = pygame.sprite.Group()
all_enemys = pygame.sprite.Group()
all_bullets = pygame.sprite.Group()

player = Player(all_bullets, all_enemys, screen)
player_rect = player.rect  # Obtén el rectángulo del jugador
all_sprites.add(player)

enemy_spawn_time = 1000  # tiempo para que aparezcan nuevos enemigos
last_enemy_spawn = pygame.time.get_ticks()

score = 0  # Inicializa la score
score_font = pygame.font.Font(None, 36)  # Fuente para la score

player_score = 0

health_increase_counter = 1

health_increase_amount = 20

running = True
paused = False


main_menu()

while running:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Agregar lógica para pausar/reanudar con la tecla "Esc"
                paused = not paused

            if not paused:  # Solo procesa las teclas si el juego no está pausado
                if event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()
                elif event.key == pygame.K_UP:  
                    player.move_up()
                elif event.key == pygame.K_DOWN: 
                    player.move_down()
                elif event.key == pygame.K_SPACE:
                    player.shoot()

        elif event.type == pygame.KEYUP:
            if not paused:  # Solo procesa las teclas si el juego no está pausado
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.stop()
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.stop()
        
    if not paused: 
        all_sprites.update()

        # Actualiza la posición vertical del fondo
        background_position_y += 1
        if background_position_y >= height:
            background_position_y = 0
        # Dibuja la imagen de fondo
        
        screen.blit(background, (0, background_position_y))
        screen.blit(background, (0, background_position_y - height))
        

        all_sprites.draw(screen)
        all_bullets.update()
        all_bullets.draw(screen)

        # Añadir un nuevo enemigo si ha pasado suficiente tiempo
        now = pygame.time.get_ticks()
        if now - last_enemy_spawn > enemy_spawn_time:
            last_enemy_spawn = now
            enemy = Enemy(all_bullets, player_rect)
            all_sprites.add(enemy)
            all_enemys.add(enemy)

        hits = pygame.sprite.groupcollide(all_enemys, all_bullets, False, True)
        for enemy, bullets in hits.items():
            enemy.take_damage(20)
            if enemy.health <= 0:
                enemy.kill()
                score += 10  # Incrementa la score cuando un enemigo es eliminado

        # Colisiones entre balas enemigas y el jugador
        hits_player = pygame.sprite.spritecollide(player, all_bullets, True)
        for bullet in hits_player:
            player.take_damage(10)
        
        # Nueva lógica para colisiones entre el jugador y los enemigos
        hits_enemy_player = pygame.sprite.spritecollide(player, all_enemys, True)
        for enemy in hits_enemy_player:
            player.take_damage(10)  # El jugador pierde más vida al colisionar con un enemigo
    
        player.draw_health()

        # Dibuja la score en la esquina superior derecha
        score_text = score_font.render(f"score: {score}", True, white)
        score_rect = score_text.get_rect()
        score_rect.topright = (width - 10, 10)
        screen.blit(score_text, score_rect)

    if not player.alive() and not paused:
        game_over_font = pygame.font.Font(None, 36)
        game_over_text = game_over_font.render("Game Over", True, white)
        game_over_rect = game_over_text.get_rect(center=(width // 2, height // 2))
        screen.blit(game_over_text, game_over_rect)

        # Muestra la score alcanzada
        score_text = score_font.render(f"score: {score}", True, white)
        score_rect = score_text.get_rect(center=(width // 2, height // 2 + 40))
        screen.blit(score_text, score_rect)

        pygame.display.flip()
        pygame.time.delay(2500)
        running = False
    
    if score >= 100 * health_increase_counter:
            for enemy in all_enemys:
                if not enemy.increased_health:
                    enemy.increase_health(health_increase_amount)
                    enemy.increased_health = True

            health_increase_counter += 1
            health_increase_amount += 20  # Aumenta la cantidad de aumento de salud


    pygame.display.flip()

pygame.quit()