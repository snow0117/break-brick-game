# coding=utf-8
import pygame
import random
import math
from enum import Enum, auto

def draw_crack(surface, start, end, thickness):
    pygame.draw.line(surface, (255, 255, 255), start, end, thickness)

def create_crack(surface, start, end, thickness, depth=0):
    if thickness < 1 or depth > 20:
        return
    draw_crack(surface, start, end, thickness)
    length = math.hypot(end[0] - start[0], end[1] - start[1])
    num_branches = random.randint(2, 4)
    for _ in range(num_branches):
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        angle += math.pi / 2
        



class Status(Enum):
    READY = auto()
    AIM = auto()
    FIRE = auto()


#  막대 및 벽돌 클래스
class Block(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img.convert_alpha() # 투명도 유지 
        self.image2 = None
        self.image3 = None
        self.rect = img.get_rect()
        self.life = 3

    def add_image(self, img2, img3):
        self.image2 = img2
        self.image3 = img3


# 농구공 클래스
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("picture\\ball.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.velx = 0.0
        self.vely = 0.0
        # self.radius = 20
        # self.speed = random.randint(10, 16)



pygame.init()
screen = pygame.display.set_mode((1200, 768))

# 벽돌
brick_image = [pygame.image.load(r"brick1.png").convert(),
         pygame.image.load(r"brick\brick2.png").convert(),
         pygame.image.load(r"brick\brick3.png").convert(),
         pygame.image.load(r"brick\brick4.png").convert(),
         pygame.image.load(r"brick\brick5.png").convert(),
         pygame.image.load(r"brick\brick6.png").convert(),
         pygame.image.load(r"brick\brick7.png").convert(),
         pygame.image.load(r"brick\brick8.png").convert()
         ]

# 금간 벽돌
broken_brick1 = [pygame.image.load(r"broken_brick\brick1.png").convert(),
                 pygame.image.load(r"broken_brick\brick2.png").convert(),
                 pygame.image.load(r"broken_brick\brick3.png").convert(),
                 pygame.image.load(r"broken_brick\brick4.png").convert(),
                 pygame.image.load(r"broken_brick\brick5.png").convert(),
                 pygame.image.load(r"broken_brick\brick6.png").convert(),
                 pygame.image.load(r"broken_brick\brick7.png").convert(),
                 pygame.image.load(r"broken_brick\brick8.png").convert()
                 ]

#  금간 벽돌 2
broken_brick2 = [pygame.image.load(r"broken_brick2\brick1.png").convert(),
                 pygame.image.load(r"broken_brick2\brick2.png").convert(),
                 pygame.image.load(r"broken_brick2\brick3.png").convert(),
                 pygame.image.load(r"broken_brick2\brick4.png").convert(),
                 pygame.image.load(r"broken_brick2\brick5.png").convert(),
                 pygame.image.load(r"broken_brick2\brick6.png").convert(),
                 pygame.image.load(r"broken_brick2\brick7.png").convert(),
                 pygame.image.load(r"broken_brick2\brick8.png").convert()
                 ]

brick_group = pygame.sprite.Group()

for j in range(0, 7):
    for i in range(0, 6):
        rand = random.randrange(8)
        brick = Block(brick_image[rand])
        brick.add_image(broken_brick1[rand], broken_brick2[rand])
        brick.rect.x = i * 100 + 300
        brick.rect.y = j * 40
        brick.mask = pygame.mask.from_surface(brick.image)
        brick_group.add(brick)

# 공
ball_group = pygame.sprite.Group()
ball_pic = pygame.image.load(r"picture\ball.png").convert_alpha()
last_ball = None
ball_angle = 0

# 화살표
trgimg = pygame.image.load("picture\\삼각형.png")
trg = trgimg.get_rect()
trg.center = (screen.get_rect().centerx, 550)

# 막대
stick_image = pygame.image.load(r'picture\stick.png').convert()
stick = Block(stick_image)
stick.mask = pygame.mask.from_surface(stick_image)

# 배경
BG_LEFT_IMAGE = pygame.image.load("picture\\배경왼쪽.png")
BG_RIGHT_IMAGE = pygame.image.load("picture\\배경오른쪽.png")

Affect = pygame.image.load("picture\\affect.png")

status = Status.READY  # 화살표 애니메이션 / 공 애니메이션      체크
angle = 0.0  # 공의 각도
life = 5  # 던질 수 있는 공의 개수
check = 0  # 충돌 처리가 이상하게 된 횟수
game = -1  #  게임 승패 여부

done = True

while done:
    # 배경세팅
    screen.fill((0, 0, 0))
    screen.blit(BG_LEFT_IMAGE, (0, 0))  # 왼쪽 배경
    screen.blit(BG_RIGHT_IMAGE, (950, 0))  # 오른족 배경

    brick_group.draw(screen)

    #  시작화면
    if status == Status.READY:
        font = pygame.font.Font(r"Amiri\Amiri-Regular.ttf", 50)
        start_text = font.render("press R to start", True, (255, 255, 255))
        screen.blit(start_text, (500, 600))

    # 화살표 조준 및 공 각도 정하기
    elif status == Status.AIM:
        # 화살표
        position = pygame.mouse.get_pos()
        angle = math.atan2(position[1] - 550, position[0] - screen.get_rect().centerx) 
     
        trgrrot = pygame.transform.rotate(trgimg, -angle * 180 / math.pi)
        yplus = 150 * math.sin(angle)                       
        xplus = 150 * math.cos(angle)
        trg.center = (screen.get_rect() .centerx + xplus, 550 + yplus)
        screen.blit(trgrrot, trg)

    #  공 이동 및 막대
    elif status == Status.FIRE:
        position = pygame.mouse.get_pos()
        stick.rect.center = (position[0], 738)
        for ball in ball_group:
            ball.rect.centerx += ball.velx
            ball.rect.centery += ball.vely
            screen.blit(ball.image, ball.rect)
        screen.blit(stick_image, stick.rect)

    ball_angle += 5

    
    # 공위치 조정 
    
    for ball in ball_group:
        ball_rect = ball.image.get_rect(center = ball.rect.center)
        rotated_ball = pygame.transform.rotate(ball.image, ball_angle)
        rotated_rect = rotated_ball.get_rect(center=(ball_rect.center))
        screen.blit(rotated_ball, rotated_rect.topleft)
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and status == Status.AIM:  # 공이 조준중이며 클릭했을때

            # 공의 이동방향 정하기
            last_ball.velx = math.cos(angle) * 8
            last_ball.vely = math.sin(angle) * 8

            status = Status.FIRE  # 공 움직이는 애니메이션으로 변경
        elif event.type == pygame.KEYDOWN and status != Status.AIM and life != 0:  # 공이 조준중이 아니며 공을 쏠 수 있는 횟수가 남아있고
            if event.key == pygame.K_r:  # r키를 눌렀을때
                life -= 1

                #  공 객체 생성
                ball = Ball()
                
                ball.rect.center = (screen.get_rect().centerx, 550)

                ball.radius = 20  # 공의 반지름
                ball_group.add(ball)

                last_ball = ball  # 마지막 공의 주소 저장
                status = Status.AIM  # 공을 조준하는 애니메이션으로 변경

    # 공의 쏠 수 있는 횟수 출력
    font = pygame.font.Font(r"Amiri\Amiri-Regular.ttf", 100)
    if life == 0:  # 공을 쏠 수 있는 횟수가 남지 않았을때 x를 출력
        life_text = font.render("X", True, (255, 255, 255))
    else:
        life_text = font.render(str(life), True, (255, 255, 255))
    screen.blit(life_text, (75, 510))

    # 플레이 한 시간 출력
    font = pygame.font.Font(r"Amiri\Amiri-Regular.ttf", 80)
    timetext = font.render(str((pygame.time.get_ticks()) / 60000) + ":"
                           + str((pygame.time.get_ticks()) / 1000 % 60).zfill(2), True, (255, 255, 255))
    screen.blit(timetext, (1020, 520))

    

    # 벽돌 충돌 체크 및 공의 이동방향 처리
    
    
    for ball in ball_group:
        count = 0
        for brick in brick_group:
            collision_point = \
                pygame.sprite.collide_mask(brick, ball)
            if collision_point:
                brick.life -= 1
                count +=1
                brick.image.set_at(collision_point, (0,0,255) )
                brick_group.remove(brick)

                collision_point_absolute = \
                    (collision_point[0] + brick.rect.left,
                     collision_point[1] + brick.rect.top)
                screen.blit(Affect, collision_point_absolute)
                

                
                if brick.rect.top <= ball.rect.centery <= brick.rect.bottom:
                    ball.velx *= -1
                elif brick.rect.right <= ball.rect.centerx <= brick.rect.left:
                    ball.velx *= -1
                else:
                    ball.velx *= -1
                    ball.vely *= -1

                
    pygame.display.flip()
                    
    #  공이 화면 끝과 충돌 했을 때 및 공의 이동방향 처리
    for ball in ball_group:
        if ball.rect.bottom >= 768:  # 스틱으로 공을 받지 못해 공이 밑으로 나갔을 경우
            ball_group.remove(ball)  # 공삭제
            if life == 0 and len(ball_group) == 0:  # 공을 던질 수 있는 횟수가 0 이며 화면에 있는 공들이 죽었을 때
                done = False
        elif ball.rect.top <= 0:
            ball.rect.centery += 3  # 공이 벽 안으로 들어가는 오류 방지
            ball.vely *= -1
        elif ball.rect.left <= 250:
            ball.rect.centerx += 3  # 공이 벽 안으로 들어가는 오류 방지
            ball.velx *= -1
        elif ball.rect.right >= 950:
            ball.rect.centerx -= 3  # 공이 벽 안으로 들어가는 오류 방지
            ball.velx *= -1

    #  공이 막대와 충돌 했을 때 및 공의 이동방향 처리
    for ball in ball_group:
        if pygame.sprite.collide_mask(ball, stick):
            barx = ball.rect.centerx
            bx = barx - stick.rect.centerx

            if stick.rect.centerx < barx:
                angle = math.radians(-100 + bx * 0.7)
            elif stick.rect.centerx > barx:
                angle = math.radians(-80 + bx * 0.7)

            ball.velx = math.cos(angle) * 8
            ball.vely = math.sin(angle) * 8

    if len(brick_group) == 0:
        done = False
        game = 1


while 1:
    screen.fill((0, 0, 0))
    font = pygame.font.Font(r"Amiri\Amiri-Regular.ttf", 100)
    if game == 1:
        gametext = font.render("YOU WIN", True, (255, 255, 255))
    else:
        gametext = font.render("GAME OVER", True, (255, 255, 255))

    screen.blit(gametext, (500, 500))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
    

