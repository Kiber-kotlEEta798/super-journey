from pygame import *
from random import *
from time import time as timer

font.init()
mixer.init()

mixer.music.load('space.ogg')
mixer.music.play()# :)

clock = time.Clock()

win_width = 700
win_height = 500

window = display.set_mode((win_width,win_height))
display.set_caption("шутер")
kick = mixer.Sound('fire.ogg')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

fire_sound = mixer.Sound('fire.ogg')

FPS = 60

x1 = 100
y1 = 300

display.set_caption('«шутер»')

font2 = font.SysFont('Arial',35)
font1 = font.SysFont('Arial',80)
win = font1.render("YOU WIN",True,(255,0,0))
lose = font1.render("YOU LOSE!",True,(0,255,0))

class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x,player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed =player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 645:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.top,15)
        bullets.add(bullet)   
        
puli = 0    
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y  <= 0:
            self.kill()
puli = 0      
             
bullets = sprite.Group()
           
if puli >= 0:
    puli = 1

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y  >= win_height:
            self.rect.y = -10
            self.rect.x = randint(50,650)
            lost += 1


font.init()
font2 = font.SysFont('Arial',35)

lost = 0
score = 0


player = Player('rocket.png', 250,400,10)
Hero = sprite.Group()
Hero.add(player)


monsters = sprite.Group()
for i in range(5):   
    ran1 = randint(5,650)
    speed = randint(2,4)
    monster = Enemy('ufo.png',ran1,80,speed)
    monsters.add(monster)

run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if puli < 3:
                    player.fire()   
                    fire_sound.play()
                    puli += 1

    if not finish:

        window.blit(background,(0,0))
        text = font2.render('Счёт '+str(score),True,(255,255,255))
        window.blit(text,(10,20))
        text_lose = font2.render('Пропущенно '+str(lost),True,(255,255,255))
        window.blit(text_lose,(10,50))
        player.update()
        monsters.update()
        bullets.update()
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters,bullets,True,True)

        for c in collides:
            score += 1
            ran1 = randint(5,650)
            speed = randint(2,3)
            monster = Enemy('ufo.png',ran1,80,speed)
            monsters.add(monster)
            puli -= 1
        
        if sprite.spritecollide(player, monsters,False) or lost > 5:
            finish = True
            window.blit(lose,(200,200))


        if score > 10 :
            finish = True 
            window.blit(win,(200,200))
    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(3000)
        for i in range(5):   
            ran1 = randint(5,650)
            speed = randint(2,3)
            monster = Enemy('ufo.png',ran1,80,speed)
            monsters.add(monster)
            
    display.update()
    clock.tick(FPS)

