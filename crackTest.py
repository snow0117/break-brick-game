import pygame
import math
import random

# 금을 그리는 함수
def draw_crack(surface, start, end, thickness):
    pygame.draw.line(surface, (255, 255, 255), start, end, thickness)

# 금을 생성하는 재귀 함수
def create_crack(surface, start, end, thickness, depth=0):
    if thickness < 1 or depth > 20:  
        return
    draw_crack(surface, start, end, thickness)
    length = math.hypot(end[0] - start[0], end[1] - start[1])
    num_branches = random.randint(2, 4)
    for _ in range(num_branches):

        center_x, center_y = 400, 300
        angle = math.atan2(center_y - end[1], center_x - end[0])
        angle += random.uniform(-0.5, 0.5)  # 중앙을 향하되 완전히 일직선은 아니게 무작위성 부여

        new_length = random.uniform(0.9, 1.5) * length
        dx = end[0] + new_length * math.cos(angle)
        dy = end[1] + new_length * math.sin(angle)
        new_end = (dx, dy)
        create_crack(surface, end, new_end, thickness - 1, depth+1)

# Pygame 환경 초기화
pygame.init()
surface = pygame.display.set_mode((800, 600))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            start = pygame.mouse.get_pos()
            center = (400, 300)
            angle = math.atan2(center[1] - start[1], center[0] - start[0])
            length = math.hypot(center[1] - start[1], center[0] - start[0])
            new_length = random.uniform(0.1, 0.3)*length
            x = start[0] + new_length * math.cos(angle)
            y = start[1] + new_length * math.sin(angle)
            end = (x, y)

            create_crack(surface, start, end, 3)

    pygame.display.flip()

pygame.quit()
