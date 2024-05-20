import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
direction = pygame.Vector2(0, 0)
direction1 = pygame.Vector2(0, 0)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_pos1 = pygame.Vector2(screen.get_width() / 2 + 1, screen.get_height() / 2 + 1)
circle_radius = 40
transparent = (0, 0, 0, 0)  # Fully transparent color
hitbox_size = pygame.Vector2(circle_radius * 2, circle_radius * 2)

def check_collision(pos1, pos2, radius):
    distance = pos1.distance_to(pos2)
    if distance <= radius * 2:
        return True
    return False

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    pygame.draw.rect(screen, transparent, (player_pos.x - circle_radius, player_pos.y - circle_radius, hitbox_size.x, hitbox_size.y))
    pygame.draw.rect(screen, transparent, (player_pos1.x - circle_radius, player_pos1.y - circle_radius, hitbox_size.x, hitbox_size.y))

    pygame.draw.circle(screen, "orange", player_pos, circle_radius)
    pygame.draw.circle(screen, "red", player_pos1, circle_radius)

    if check_collision(player_pos, player_pos1, circle_radius):
        print("test")

    # Check collision with screen boundaries
    if player_pos1.x - circle_radius <= 0:
        direction1.x = 0
    if player_pos1.x + circle_radius >= screen.get_width():
        direction1.x = 0
    if player_pos1.y - circle_radius <= 0:
        direction1.y = 0
    if player_pos1.y + circle_radius >= screen.get_height():
        direction1.y = 0

    if player_pos.x - circle_radius <= 0:
        direction.x = 0
    if player_pos.x + circle_radius >= screen.get_width():
        direction.x = 0
    if player_pos.y - circle_radius <= 0:
        direction.y = 0
    if player_pos.y + circle_radius >= screen.get_height():
        direction.y = 0


    keys = pygame.key.get_pressed()
    keys_arrow = pygame.key.get_pressed()  # Get arrow key presses

    if keys[pygame.K_w] and direction.y != 1: 
        direction = pygame.Vector2(0, -1)
    elif keys[pygame.K_s] and direction.y != -1:
        direction = pygame.Vector2(0, 1)
    elif keys[pygame.K_a] and direction.x != 1:
        direction = pygame.Vector2(-1, 0)
    elif keys[pygame.K_d] and direction.x != -1:
        direction = pygame.Vector2(1, 0)

    if keys_arrow[pygame.K_UP] and direction1.y != 1: 
        direction1 = pygame.Vector2(0, -1)
    elif keys_arrow[pygame.K_DOWN] and direction1.y != -1:
        direction1 = pygame.Vector2(0, 1)
    elif keys_arrow[pygame.K_LEFT] and direction1.x != 1:
        direction1 = pygame.Vector2(-1, 0)
    elif keys_arrow[pygame.K_RIGHT] and direction1.x != -1:
        direction1 = pygame.Vector2(1, 0)

    player_pos += direction * 300 * dt 
    player_pos1 += direction1 * 300 * dt 

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()

