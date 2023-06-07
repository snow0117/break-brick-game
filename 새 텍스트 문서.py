import pygame

# pygame 초기화
pygame.init()

# 화면 생성
screen = pygame.display.set_mode((800, 600))

# 이미지 로드
image = pygame.image.load(r"brick\brick1.png")

# 이미지를 화면에 그리기
screen.blit(image, (0, 0))

# 화면 업데이트
pygame.display.flip()

# pygame 종료
pygame.quit()