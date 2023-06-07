import pygame
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

image = pygame.image.load(r'picture\ball.png')
image = pygame.transform.scale(image, (100, 100))

image_rect = image.get_rect(center=(400,300))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0,0,0))

    mouse_pos = pygame.mouse.get_pos()

    dx = mouse_pos[0] - image_rect.centerx
    dy = mouse_pos[1] - image_rect.centery
    angle_to_mouse = math.degrees(math.atan2(-dy, dx))
    rotated_image = pygame.transform.rotate(image, angle_to_mouse-90)

    rotated_rect = rotated_image.get_rect(center=image_rect.center)

    screen.blit(rotated_image, rotated_rect.topleft)

    pygame.display.flip()
pygame.quit()

