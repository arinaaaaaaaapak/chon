from pygame import * 
from random import *
from time import time as timer

lost = 0
killed = 0
font.init()
font1 = font.Font(None, 36) 
bullets = sprite.Group()
finish_win = False
finish_lost = False
lastFire = timer()
firet = timer()
fireCooldown = 0.5

class GameSprite(sprite.Sprite): 
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed): 
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Hero(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            self.fires()
            
    def fires(self):
        global lastFire
        firet = timer()
        print(firet)
        print('last = ' + str(lastFire))

        print('lafire - lastFirest =' + str(firet - lastFire))
        if firet - lastFire >= fireCooldown:
            lastFire = firet
            bullets.add(Bullet("bullet.png", self.rect.centerx-7, self.rect.top, 15, 25, 3))
            fire.play()
        
class Enemy(GameSprite):
    direction = 'down'
    def update(self):
        self.rect.y += self.speed
        global lost
        global killed
        global finish_win
        global finish_lost
        global finish
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
        sprites_list = sprite.groupcollide(monsters, bullets, False, True)
        if len(sprites_list) != 0:
            killed += len(sprites_list)
            if killed >= 10:
                finish_win = True 
                finish = True
            for i in sprites_list:
                i.rect.x = randint(80, win_width - 80)
                i.rect.y = 0
        
        gg = sprite.Group()  
        gg.add(hero) 
        
        if len(sprite.groupcollide(gg, monsters, False, False)) > 0 or lost >= 3:
                finish = True
                finish_lost = True

        if self.rect.x <= 600: 
            self.direction = 'right' 
        if self.rect.x >= win_width - 85:
            self.direction = 'left' 

        if self.direction == 'down':
            self.rect.y -= self.speed 
        else: 
            self.rect.y += self.speed 
        

class Bullet(GameSprite):
    direction = 'up'
    def update(self):
        if self.rect.y > win_height:
            self.rect.x = self.rect.x
            self.rect.y = 0
        if self.direction == 'up': 
            self.rect.y -= self.speed 
        else: 
            self.rect.y += self.speed 


win_width = 700 
win_height = 500
window = display.set_mode((win_width, win_height)) 
display.set_caption('Лабиринт') 
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height)) 
 
mixer.init() 
mixer.music.load('space.ogg') 
mixer.music.play() 

fire = mixer.Sound('fire.ogg')

kick = mixer.Sound('fire.ogg') 
 
x1 = 400
y1 = 300 
x2 = 300 
y2 = 300 
speed = 8

monsters = sprite.Group()
monsters.add(Enemy("ufo.png", 100, 20, 65, 65, 3))
monsters.add(Enemy("ufo.png", 240, 20, 65, 65, 2))
monsters.add(Enemy("ufo.png", 360, 20, 65, 65, 1.75))
monsters.add(Enemy("ufo.png", 480, 20, 65, 65, 2))
monsters.add(Enemy("ufo.png", 595, 20, 65, 65, 3))

hero = Hero("rocket.png", 5, win_height - 80, 65, 65, 8) 

clock = time.Clock()
FPS = 60 
 
font.init() 
font = font.Font(None, 70) 
win = font.render('YOU WIN!', True, (255, 215, 0)) 
lose = font.render('YOU LOSE!', True, (180, 0, 0)) 
 
game = True 
finish = False 
 
while game: 
    clock.tick(FPS) 
    if finish != True: 
        text_win = font1.render("Счет:" + str(killed), 1, (255, 255, 255))
        text_lose = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))

        window.blit(background,(0, 0))
        window.blit(text_lose,(10, 10))
        window.blit(text_win,(10, 40))
        hero.update()
        bullets.draw(window)
        bullets.update()

        hero.reset() 
        monsters.draw(window)
        monsters.update()

    elif finish_win:
        window.blit(win,(230, 250))
    elif finish_lost:
        window.blit(lose,(230, 250))

    for e in event.get(): 
        if e.type == QUIT: 
            game = False

    display.update()