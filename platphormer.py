from typing import Any
from pygame import *
from random import randint
init()

win_width = 700
win_height = 780

clock = time.Clock()  # Ігровий таймер
FPS = 60

img_bac = "galaxy.jpg"
player = "pixil-frame-0.png"
shot = "pixil-frame-0 (1).png"
enemy = "ufo 0.2.png"
roc = "roc2.0.png"
small_roc = "roc1.png"

health = 3
score = 0
lost = 0

f = font.Font(None, 36)

window = display.set_mode((win_width, win_height))  # створення вікна
display.set_caption("galaxy.jpg")  # назва вікна
game = True
finish = False
background = transform.scale(image.load(img_bac), (win_width, win_height))

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed, e_name):
        super().__init__()
        self.w = w
        self.h = h
        self.speed = speed
        self.e_name = e_name

        self.image = transform.scale(image.load(img), (w, h))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, img, x, y, w, h, speed, e_name):
        super().__init__(img, x, y, w, h, speed, e_name)
        self.reloud = 0
        self.rate = 18
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 70:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 400:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
        if keys[K_RSHIFT] and self.reloud >= self.rate:
            self.fire()
            self.reloud = 0 
        elif self.reloud < self.rate:
            self.reloud += 1


    def fire(self):
        bull = Gun(shot, self.rect.centerx, self.rect.top, 15, 20, 15, "BULLET")
        Bullets.add(bull)


class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(20, win_width - 20)
            self.rect.y = 0
            lost += 1


class Gun (GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


player = Player("pixil-frame-0.png", 330, win_height - 80, 80, 80, 3, "PLAYER")

Bullets = sprite.Group()

enemies = sprite.Group()
for i in range(5):
    x = randint(80, win_width - 80)
    enemy = Enemy("ufo 0.2.png", x, win_height - 780 , 80, 80, randint(1, 5), "UFO")
    enemies.add(enemy)

rocs = sprite.Group()
for i in range(6):
    x = randint(80, win_width - 80)
    roc = Enemy("roc2.0.png", x, win_height - 780 , 80, 80, randint(1, 6), "ROC")
    enemies.add(roc)

small_rocs = sprite.Group()
for i in range(5):
    x = randint(80, win_width - 80)
    small_roc = Enemy("roc1.png", x, win_height - 780 , 65, 65, randint(1, 5), "SMALL_ROC")
    enemies.add(small_roc)

while game :
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))
        text = f.render(f"Життя: {health}", True, (255,255,255))
        window.blit(text, (10, 50))

        text = f.render(f"Рахунок: {score}", True, (255,255,255))
        window.blit(text, (10, 20))


        player.update()
        player.reset()
        enemies.update()
        enemies.draw(window)
        Bullets.update()
        Bullets.draw(window)
        collides = sprite. groupcollide(enemies, Bullets, True, True)
        for c in collides:
            if c.e_name == "ROC":
                x, y = c.rect.x, c.rect.y
                enemy = Enemy("roc1.png", x, y , 80, 80, randint(1, 5), "SMALL_ROC")
                enemies.add(enemy)

            else:
                
                
                x = randint(80, win_width - 80)
                imaje = "ufo 0.2.png"
                if c.e_name == "UFO":
                    score += 50
                    if score == 100 or score == 300 or score == 500 or score == 800:
                        health += 1

                a = randint(1, 5)
                if a == 1:
                    imaje = "ufo 0.2.png"
                    e_name = "UFO"
                elif a == 2:
                    imaje = "roc2.0.png"
                    e_name = "ROC"
                elif a == 3:
                    imaje = "roc1.5.png"
                    e_name = "ROC"
                elif a == 2:
                    imaje = "roc2.png"
                    e_name = "SMALL_ROC"
                else:
                    imaje = "roc1.png"
                    e_name = "SMALL_ROC"
                enemy = Enemy(imaje, x, win_height - 780 , 80, 80, randint(1, 5), e_name)
                enemies.add(enemy)
        if score >= 1000:
            finish = True
            f = font.Font(None, 70)
            lose_text = f.render("YOU WIN!", True, (180, 0, 0))
            window.blit(lose_text, (200, 200))

        if sprite.spritecollide(player, enemies, True):
            health -= 1
            if health == 0:
                finish = True
                f = font.Font(None, 70)
                lose_text = f.render("YOU LOSE!", True, (180, 0, 0))
                window.blit(lose_text, (200, 200))





        display.update()
    clock.tick(FPS)