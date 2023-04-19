import pygame
import random

pygame.init()
window = pygame.display.set_mode((600, 300))
window.fill((255, 255, 255))
pygame.display.set_caption('Dino')


class Pic(pygame.sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.width = w - 20
        self.rect.height = h - 10
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Cactus(Pic):
    def __init__(self, picture, w, h, x, y, speed_x=6):
        super().__init__(picture, w, h, x, y)
        self.speed_x = speed_x

    def update(self):
        self.rect.left -= self.speed_x
        if self.rect.x <= -50:
            self.kill()


class Dino(Pic):
    def __init__(self, picture, w, h, x, y, speed_y=9, y_min=140, y_max=190):
        super().__init__(picture, w, h, x, y)
        self.speed_y = speed_y
        self.y_min = y_min
        self.y_max = y_max
        self.direction = 'up'

    def update(self):
        if self.rect.y >= self.y_max:
            self.direction = 'up'
        if self.rect.y <= self.y_min:
            self.direction = 'down'
        if self.direction == 'up':
            self.rect.y -= self.speed_y
        else:
            self.rect.y += self.speed_y


class Bar(Pic):
    def __init__(self, picture, w, h, x, y):
        super().__init__(picture, w, h, x, y)


class ScoreBar(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y, speed_s=-0.312, h_score=0):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed_s
        self.text = 0
        self.text1 = "HI"
        self.font = pygame.font.Font('PressStart2P.ttf', 12)
        self.h_score = h_score
        self.oo = "0"
        self.oo1 = "0"

    def draw(self):
        if self.text < 10:
            self.oo = "0000"
        elif 100 > self.text > 10:
            self.oo = "000"
        elif 1000 > self.text > 100:
            self.oo = "00"
        elif 10000 > self.text > 1000:
            self.oo = "0"
        else:
            self.oo = ""
        pygame.draw.rect(window, (255, 255, 255), self.rect)
        window.blit(self.font.render(self.oo + str(int(self.text)), True, (80, 80, 80)), (self.rect.x, self.rect.y))

    def hs_draw(self):
        pygame.draw.rect(window, (255, 255, 255), self.rect)
        window.blit(self.font.render(self.text1, True, (100, 100, 100)), (self.rect.x, self.rect.y))

    def update(self):
        with open('score.txt', 'r') as file1:
            self.h_score = file1.read()
        if int(self.h_score) < 10:
            self.oo1 = "0000"
        elif 100 > int(self.h_score) > 10:
            self.oo1 = "000"
        elif 1000 > int(self.h_score) > 100:
            self.oo1 = "00"
        elif 10000 > int(self.h_score) > 1000:
            self.oo1 = "0"
        else:
            self.oo1 = ""
        pygame.draw.rect(window, (255, 255, 255), self.rect)
        window.blit(self.font.render(self.oo1 + self.h_score, True, (100, 100, 100)), (self.rect.x, self.rect.y))


class Ground(pygame.sprite.Sprite):
    def __init__(self, picture, w, h, x, y, speed_g=-6):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture), (w, h))
        self.image1 = pygame.transform.scale(pygame.image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect1 = self.image1.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_g = speed_g

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        window.blit(self.image, (self.rect.x + 600, self.rect.y))

    def update(self):
        self.rect.left += self.speed_g
        self.rect1.left += self.speed_g
        if self.rect.x <= -600:
            self.rect.x = 600


class Sky(pygame.sprite.Sprite):

    def __init__(self, picture, w, h, x, y, speed_s=-3):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_s = speed_s

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        self.rect.left += self.speed_s
        if self.rect.x <= -600:
            self.rect.x = 600


def Animation(dino, img1, img2, img3):
    time_now = pygame.time.get_ticks()
    if dino.rect.y > 147:
        if time_now % 1000 < 500:
            dino.image = img1
        else:
            dino.image = img2
    else:
        dino.image = img3


score = ScoreBar(100, 30, 490, 30)

highest_score1 = ScoreBar(100, 30, 420, 30)

highest_score = ScoreBar(100, 30, 390, 30)

cacti = pygame.sprite.Group()

cloud = Sky('cloud.png', 50, 30, 610, 50)

new_ground = Ground('ground.png', 600, 30, 0, 200)
new_ground1 = Ground('ground.png', 600, 30, 600, 200)

dino = Dino('dino.png', 55, 65, 80, 143)
dino_run1 = Dino('dino.png', 55, 65, 80, 143)
dino_run2 = Dino('dino.png', 55, 65, 80, 143)

dinos = pygame.sprite.Group()

replay = Pic('replay.png', 200, 90, 200, 50)

clock = pygame.time.Clock()

next_cactus_time = 0

n = 0
dino_up = False
finish = False
speed: int = 0
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if dino.rect.y > 140:
                    dino_up = True
            elif event.key == pygame.K_r and finish:
                cacti.empty()
                dino.rect.x = 80
                dino.rect.y = 143
                finish = False

    if pygame.time.get_ticks() > next_cactus_time:  # Random Cacti
        next_cactus_time += 1500
        c = random.randint(1, 4)
        b = random.randint(600, 750)
        if c == 1:
            cactus1 = Cactus('cactus-1.png', 30, 50, b, 170)
            cacti.add(cactus1)
        elif c == 2:
            cactus2 = Cactus('cacti-3.png', 40, 50, b, 170)
            cacti.add(cactus2)
        elif c == 3:
            cactus3 = Cactus('cacti-2.png', 40, 50, b, 170)
            cacti.add(cactus3)
        elif c == 4:
            cactus4 = Cactus('cacti-4.png', 40, 50, b, 170)
            cacti.add(cactus4)

    if dino.rect.y >= 130:  # Jump Speed
        speed = 10
    if dino.rect.y < 130:
        speed = 6

    if dino_up:  # Dino Jump
        if dino.rect.y >= 40:
            dino.rect.y -= speed
        else:
            dino_up = False
    else:
        if dino.rect.y <= 147:
            dino.rect.y += speed

    if pygame.sprite.spritecollide(dino, cacti, True):
        finish = True
        replay.reset()
        with open('score.txt', 'r') as file:
            old_score = file.read()
        if int(old_score) < int(score.text):
            with open('score.txt', 'w') as file:
                file.write(str(int(score.text)))
        score.text = 0
    score.text -= score.speed

    #Animation(dino, 'dino_run1.png', 'dino_run2.png', 'dino.png')
    # if dino.rect.y == 143:  # Animation
    #     if n <= 20:
    #         dinos.empty()
    #         dino_run1 = Dino('dino_run1.png', 55, 65, 80, 143)
    #         dinos.add(dino_run1)
    #         n += 1
    #     elif 40 >= n > 20:
    #         dinos.empty()
    #         dino_run2 = Dino('dino.png', 55, 65, 80, 143)
    #         dinos.add(dino_run2)
    #         n += 1
    #     elif n == 40:
    #         n = 0
    # elif dino.rect.y < 143:
    #     dinos.empty()
    #     dino_jump = Dino('dino.png', 55, 65, 80, 143)
    #     dinos.add(dino_jump)

    if not finish:
        window.fill((255, 255, 255))
        dino.reset()
        dinos.update()
        cacti.draw(window)
        cacti.update()
        new_ground1.reset()
        new_ground1.update()
        new_ground.reset()
        new_ground.update()
        highest_score.hs_draw()
        highest_score1.update()
        score.draw()

    clock.tick(40)
    pygame.display.update()
