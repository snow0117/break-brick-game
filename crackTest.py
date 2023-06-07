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
    num_branches = random.randint(2, 6)
    for _ in range(num_branches):
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        angle += math.pi / 3
        angle += random.uniform(-1, 1)  # 방향의 무작위성 증가
        new_length = random.uniform(0.5, 0.8) * length
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
            end = start[0] + random.uniform(-35, 35), start[1] + random.uniform(-35, 35)
            create_crack(surface, start, end, 3)

    pygame.display.flip()

pygame.quit()
