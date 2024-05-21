import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))

clock = pygame.time.Clock()
running = True
dt = 0
current_direction = None
player_pos = pygame.Vector2(screen.get_width() - 1240, screen.get_height() / 2)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill("purple")
    pygame.draw.circle(screen, "violet", player_pos, 20)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] and current_direction != "down":
        current_direction = "up"
    elif keys[pygame.K_s] and current_direction != "up":
        current_direction = "down"
    elif keys[pygame.K_a] and current_direction != "right":
        current_direction = "left"
    elif keys[pygame.K_d] and current_direction != "left":
        current_direction = "right"

    if current_direction == "up":
        player_pos.y -= 300 * dt if player_pos.y > 0 else 0
    elif current_direction == "down":
        player_pos.y += 300 * dt if player_pos.y < screen.get_height() else 0
    
    elif current_direction == "left":
        player_pos.x -= 300 * dt if player_pos.x > 0 else 0

    elif current_direction == "right":
        player_pos.x += 300 * dt if player_pos.x < screen.get_width() else 0


    #flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
