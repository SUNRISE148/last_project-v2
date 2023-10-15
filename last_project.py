from pygame import *
from random import randint
from time import time as timer
font.init()
font1 = font.SysFont("Arial", 36)
win = font1.render("YOU WIN!", True, (255,255,255))
lose = font1.render("YOU LOSE!", True, (180,0,0))
font2 = font.SysFont("Arial", 36)
mixer.init()
#mixer.music.load('space.ogg')
#mixer.music.play()
#fire_sound = mixer.Sound("fire.ogg")
img_back = "galaxy.jpg"
img_bullet_left = "bullet_left.png"
img_bullet_right = "bullet_right.png"
img_hero_left = "character_left.png"
img_hero_right = "character_right.png"
img_ast= "asteroid.png"
img_enemy = "enemy.png"
img_enemy_right = "enemy_right.png"
img_stand = "stand.png"
img_ammo = "ammo.png"
fire_direction = 1
enemy_direction = 1

score = 0
goal = 20
lost = 0
max_lost = 10
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        #self.direction = direction
        self.size_x = size_x
        self.size_y = size_y
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def reset_direction(self,imaage,size_x,size_y):
        window.blit(transform.scale(image.load(imaage),(size_x, size_y)), (self.rect.x, self.rect.y))
    def fire_left(self):
        bullet = Bullet(img_bullet_left, self.rect.centerx-30, 418,20,15, -15)
        bullets.add(bullet)
    def fire_right(self):
        bullet = Bullet(img_bullet_right, self.rect.centerx+10, 418,20,15, 15)
        bullets.add(bullet)
    def reset_left(self,player_image_left,size_x,size_y):
        a = transform.scale(image.load(player_image_left),(size_x, size_y))
        window.blit(transform.scale(image.load(player_image_left),(size_x, size_y)), (self.rect.x, self.rect.y))
    def reset_right(self,player_image_right,size_x,size_y):
        window.blit(transform.scale(image.load(player_image_right),(size_x, size_y)), (self.rect.x, self.rect.y))
class Enemy(GameSprite):
    def update(self):
        self.rect.x += self.speed
        global lost
        if self.rect.x < 350 and self.rect.x > 300:
            #self.rect.x = randint(80, win_width - 80)
            a = randint(0,1)
            if a == 0:
                self.rect.x = 600
                self.speed = randint(1,5)*-1
                #self.image = transform.scale(image.load(img_enemy_right),(self.size_x, self.size_y))
            if a == 1:
                self.rect.x = 50
                self.speed = randint(1,5)
            lost = lost+1
class Bullet(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x <0 or self.rect.x >700:
            self.kill()

win_width = 700
win_height = 500
display.set_caption("shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
ship = Player(img_hero_left,300,370,80,100,12)
life_station = GameSprite('life.png', 300, 250,100,100,0)
stand = GameSprite('stand.png', 300, 500,100,50,0)
monsters = sprite.Group()
clip = sprite.Group()
for i in range(1,6):
    a = randint(0,1)
    if a == 0:
        monster = Enemy(img_enemy, 700, 410,80,50,randint(1,5)*-1)
        monsters.add(monster)
    if a == 1:
        monster = Enemy(img_enemy_right,-50, 410,80,50,randint(1,5))
        monsters.add(monster)
for i in range(1,7):
    ammo = GameSprite(img_ammo,win_width-(i*25)-25, 50,15,20,0 )
    clip.add(ammo)


asteroids = sprite.Group()
#for i in range(1,3):
#    asteroid = Enemy(img_ast, randint(30,win_width-30),-40,80,50,randint(1,7))
#    asteroids.add(asteroid)
bullets = sprite.Group()
finish = False
run = True
rel_time = False
num_fire = 0
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_a:
                fire_direction = 1
            if e.key == K_d:
                fire_direction = 0
            if e.key == K_SPACE:
                i = 0
                for b in clip:
                            i+=1
                            if i == (6 -num_fire):
                                b.kill()
                if fire_direction == 1:
                    if num_fire < 6 and rel_time == False:
                        num_fire = num_fire +1
                        i = 0
                        ship.fire_left()
                    if num_fire >= 6 and rel_time == False:
                        last_time = timer()
                        rel_time = True
                if fire_direction == 0:
                    if num_fire < 6 and rel_time == False:
                        num_fire = num_fire +1
                        ship.fire_right()
                    if num_fire >= 6 and rel_time == False:
                        last_time = timer()
                        rel_time = True
    if not finish:
        window.blit(background,(0,0))
        ship.update()
        monsters.update()
        clip.update()
        asteroids.update()
        bullets.update()

        if fire_direction == 0:
            ship.reset_right(img_hero_right,80,100)
        if fire_direction == 1:
            ship.reset_left(img_hero_left,80,100)
        monsters.draw(window)
        asteroids.draw(window)
        clip.draw(window)
        bullets.draw(window)
        life_station.reset()
        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 2:
                reload = font2.render("Wait, reload...", 1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
                for i in range(1,7):
                    ammo = GameSprite(img_ammo,win_width-(i*25)-25, 50,15,20,0 )
                    clip.add(ammo)
            
        collides = sprite.groupcollide(monsters,bullets,True,True)
        for c in collides:
            score +=1
            a = randint(0,1)
            if a == 0:
                monster = Enemy(img_enemy, 700, 410,80,50,randint(1,5)*-1)
                monsters.add(monster)
            if a == 1:
                monster = Enemy(img_enemy_right,-50, 410,80,50,randint(1,5))
                monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship,asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship,asteroids, True)
            life -=1
            a = randint(0,1)
            if a == 0:
                monster = Enemy(img_enemy, 700, 410,80,50,randint(1,5)*-1)
                monsters.add(monster)
            if a == 1:
                monster = Enemy(img_enemy_right,-50, 410,80,50,randint(1,5))
                monsters.add(monster)

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        if score >= goal:
            finish = True
            window.blit(win,(200,200))

        text = font2.render("Счет: " + str(score),1,(255,255,255))
        window.blit(text,(10,20))
        text_lose = font2.render("Пропущено: " + str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150, 0,0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life,(650,10))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range(1,4):
            a = randint(0,1)
            if a == 0:
                monster = Enemy(img_enemy, 700, 410,80,50,randint(1,5)*-1)
                monsters.add(monster)
            if a == 1:
                monster = Enemy(img_enemy_right,-50, 410,80,50,randint(1,5))
                monsters.add(monster)

        #for i in range(1,3):
        #    asteroid = Enemy(img_ast, randint(30,win_width-30),-40,80,50,randint(1,7))
        #    asteroids.add(asteroid)
    time.delay(50)