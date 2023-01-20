from pygame import *
init()
level = [
       "r                                                                    .",
       "r                                                                    .",
       "r                                                                    .",
       "r                                                                    .",
       "r r   °  °     l                              r    °  °  °    l      .",
       "r  ------------                                ---------------       .",
       "rr / l                                       r / l         r / l     .",
       "rr   l                                       r   l         r   l     .",
       "rr     ° l                          r    °  °     l    r       l     .",
       "  r------                           ------------       -------       .",
       "r     r / l                                          r / l           .",
       "r     r   l                                          r   l           .",
       "r     rr       °  ° ll                        r  °  °   l            .",
       "r       ------------                           ---------             .",
       "r                r / l                       r / l                   .",
       "r                r   l                       r   l                   .",
       "r                                                                    .",
       "----------------------------------------------------------------------"]
# розміри рівня
level_width = len(level[0]) * 40
level_height = len(level) * 40
# розміри вікна
W = 1280
H = 720

window = display.set_mode((W, H))# створення вікна
display.set_caption("Blockada")# додаємо назву вікна
display.set_icon(image.load('images/bgr.png'))# додаємо іконку вікна
bg = transform.scale(image.load('images/bgr.png'), (W, H))# створємо картинку-фон
# додаємо картинки спрайтів
hero_r = "images/sprite1_r.png"
hero_l = "images/sprite1.png"

enemy_r = 'images/cyborg.png'
enemy_l = 'images/cyborg_r.png'

coin = "images/coin.png"
door_img = "images/door.png"
key_img = 'images/key.png'
chest_open = "images/cst_open.png"
chest_close = "images/cst_close.png"
cyborg = "images/cyborg.png"
stair = "images/stair.png"
port = "images/portal.png"
platform ="images/platform.png"
nothing = "images/nothing.png"
power = "images/mana.png"

# звуки
mixer.init()
fire = mixer.Sound('sounds/fire.ogg')
kick = mixer.Sound('sounds/kick.ogg')
k_coll = mixer.Sound('sounds/k_coll.wav')
c_sound = mixer.Sound("sounds/c_coll.wav")
lock = mixer.Sound('sounds/lock.wav')
tp = mixer.Sound('sounds/teleport.ogg')
click = mixer.Sound('sounds/click.wav')
chest_snd = mixer.Sound('sounds/chest.wav')

# додаємо текст в гру
font.init()

font1 = font.SysFont(('font/ariblk.ttf'), 200)
gname = font1.render('Blockada', True, (106, 90, 205), (250, 235, 215))

font2 = font.SysFont(('font/ariblk.ttf'), 60)
e_tap = font2.render('press (e)', True, (255, 0, 255))
k_need = font2.render('You need a key to open!', True, (255, 0, 255))
chest_need = font2.render('You need open chest to open door!', True, (255, 0, 255))
space = font2.render('press (space) to kill the enemy', True, (255, 0, 255))

font3 = font.SysFont(('font/calibrib.ttf'), 45)
wasd_b = font3.render('WASD - move buttons. You can only go up and down the stairs', True, (255, 0, 0))
space_b = font3.render('Space - shoot button. You are a wizard who only knows one spell', True, (255, 0, 0))
e_b = font3.render('E - interaction button. Open doors, collect keys, activate portals', True, (255, 0, 0))

font4 = font.SysFont(('font/ariblk.ttf'), 150)
done = font4.render('LEVEL DONE!', True, (0, 255, 0), (255, 100, 0))
lose = font4.render('YOU LOSE!', True, (255, 0, 0), (245, 222, 179))
pausa = font4.render('PAUSE', True, (255, 0, 0), (245, 222, 179))

calculator = 0
chest_o = False
door1_o = False
door2_o = False






class Settings(sprite.Sprite):# базовий клас для спрайтів
    def __init__(self, x, y, w, h, speed, img):
        super().__init__()
        self.width = w
        self.height = h
        self.speed = speed
        self.image = transform.scale(image.load(img), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):# метод відображення картинки
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(Settings):
    def r_l(self): #управление для игрока
        key_pressed = key.get_pressed()
        move = 'right'
        if key_pressed[K_a]:
            self.rect.x -= self.speed
            move = 'left'
            mana.side = 'left'
        if key_pressed[K_d]:
            move = 'right'
            mana.side='right'
            self.rect.x += self.speed
            
        if move == 'right':
            self.image = transform.scale(image.load(hero_l), (self.width, self.height))
        if move == 'left':
            self.image = transform.scale(image.load(hero_r), (self.width, self.height))
    def u_d(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_w]:
            self.rect.y -= self.speed
        if key_pressed[K_s]:
            self.rect.y += self.speed


class Enemy(Settings):
    def __init__(self, x, y, w, h, speed, img, side):
        Settings.__init__(self, x, y, w, h, speed, img)
        self.side = side
        
    def update(self):
        if self.side == 'left':
            self.rect.x -= self.speed
        if self.side == 'right':
            self.rect.x += self.speed


# class Mana(Settings):
#     def __init__(self, x, y, w, h, speed, img, side):   
#         Settings.__init__(self, x, y, w, h, speed, img)  
#         self.side = side    

#     def update(self):
#         if self.side == 'left':
#             self.rect.x -= self.speed
#         if self.side == 'right':
#             self.rect.x += self.speed



class Camera():
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height) # прозорий прямокутник з'являється у координата (0,0), він і відіграє роль камери

    def apply(self, target):
        return target.rect.move(self.state.topleft) # цей метод буде робити всі об'єкти гри видимими для камери

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect) # оновлюємо положення камери, відносно певної рухомої цілі (гравця)

# налаштування розмірів та положення камери
def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + W / 2, -t + H / 2

    l = min(0, l)                    # Не виходимо за ліву межу
    l = max(-(camera.width - W), l)  # Не виходимо за праву межу
    t = max(-(camera.height - H), t) # Не виходимо за нижню межу
    t = min(0, t)                    # Не виходимо за верхню межу

    return Rect(l, t, w, h)


hero = Player(300, 650, 50, 50, 5, hero_l)
camera = Camera(camera_configure, level_width, level_height)
enemy1 = Enemy(400, 480, 50, 50, 3, enemy_r, 'right')
enemy2 = Enemy(230, 320, 50, 50, 3, enemy_l, 'left')
enemy3 = Enemy(2000, 480, 50, 50, 3, enemy_r, 'right')
enemy4 = Enemy(2000, 160, 50, 50, 3, enemy_r, 'right')
enemy5 = Enemy(1500, 320, 50, 50, 3, enemy_r, 'right')
chest = Settings(500,145,70,70,0,chest_close)
door = Settings(1000,600,60,110,5, door_img)
key1 = Settings(200,335,70,40,0,key_img)
key2 = Settings(1500,335,70,40,0,key_img)
portal = Settings(2600,550 ,150,150,0,port)
mana= Enemy(0,-100, 25, 25 , 25, power, 'left' )
   
items = sprite.Group()
manas = sprite.Group()


blocks_r = []
blocks_l = []
stairs_list = []
coins_list = []
# початкові координати рівня
x = 0
y = 0
for r in level:# перебираємо список
    for c in r:# перебираємо кожну строку
        if c == 'r':
            r1 = Settings(x, y, 40, 40, 0, nothing)
            blocks_r.append(r1)
            items.add(r1)
        if c == 'l':
            r2 = Settings(x, y, 40, 40, 0, nothing)
            blocks_l.append(r2)
            items.add(r2)
        if c == '/':
            r3 = Settings(x, y-40, 40, 180, 0, stair)
            stairs_list.append(r3)
            items.add(r3)
        if c == "°":
            r4 = Settings(x, y, 40, 40, 0, coin)
            coins_list.append(r4)
            items.add(r4)
        if c == '-':
            r5 = Settings(x, y, 40, 40, 0, platform)
            items.add(r5)
        x += 40# рухаємось по ряду рівня
    y += 40# рухаємо ряд нижче
    x = 0# починаємо з початку рівня
#добавление спрайтов в группу для отбражения в камере
items.add(hero)
items.add(enemy1)
items.add(enemy2)
items.add(enemy3)
items.add(enemy4)
items.add(enemy5)
items.add(chest)
items.add(door)
items.add(key1)
items.add(key2)
items.add(portal)


def collides():# перевірка зіткнень
    keys = key.get_pressed()
    #поднимаемся на лестнице
    for s in stairs_list:
        if sprite.collide_rect(hero, s):
            hero.u_d()
            if hero.rect.y <= s.rect.y - 40:
                hero.rect.y = s.rect.y - 40
            if hero.rect.y >= s.rect.y + 130:
                hero.rect.y = s.rect.y + 130
    #действие с блоко влево
    for l in blocks_l:
        if sprite.collide_rect(mana, l):
            items.remove(mana)
            kick.play
        if sprite.collide_rect(hero, l):
            hero.rect.x = l.rect.x - hero.width
        if sprite.collide_rect(enemy1, l):
            enemy1.side = "left"
            enemy1.image = transform.scale(image.load(enemy_l), (enemy1.width, enemy1.height))

        if sprite.collide_rect(enemy2, l):
            enemy2.side = "left"
            enemy2.image = transform.scale(image.load(enemy_l), (enemy2.width, enemy2.height))

        if sprite.collide_rect(enemy3, l):
            enemy3.side = "left"
            enemy3.image = transform.scale(image.load(enemy_l), (enemy3.width, enemy3.height))

        if sprite.collide_rect(enemy4, l):
            enemy4.side = "left"
            enemy4.image = transform.scale(image.load(enemy_l), (enemy4.width, enemy4.height))

        if sprite.collide_rect(enemy5, l):
            enemy5.side = "left"
            enemy5.image = transform.scale(image.load(enemy_l), (enemy5.width, enemy5.height))
        #действие с блоком вправо
    for r in blocks_r:
        if sprite.collide_rect(mana, r):
            items.remove(mana)
            kick.play

        if sprite.collide_rect(hero, r):
            hero.rect.x = r.rect.x + hero.width

        if sprite.collide_rect(enemy1, r):
            enemy1.side = "right"
            enemy1.image = transform.scale(image.load(enemy_r), (enemy1.width, enemy1.height))

        if sprite.collide_rect(enemy2, r):
            enemy2.side = "right"
            enemy2.image = transform.scale(image.load(enemy_r), (enemy1.width, enemy2.height))

        if sprite.collide_rect(enemy3, r):
            enemy3.side = "right"
            enemy3.image = transform.scale(image.load(enemy_r), (enemy3.width, enemy3.height))

        if sprite.collide_rect(enemy4, r):
            enemy4.side = "right"
            enemy4.image = transform.scale(image.load(enemy_r), (enemy4.width, enemy4.height))

        if sprite.collide_rect(enemy5, r):
            enemy5.side = "right"
            enemy5.image = transform.scale(image.load(enemy_r), (enemy5.width, enemy5.height))
    #калкьулятор монет  
    global calculator,chest_o, door1_o, door2_o
    for c in coins_list:
        if sprite.collide_rect(c, hero):
            c_sound.play()
            calculator += 1
            coins_list.remove(c)
            items.remove(c)
    # отображение монеток
    coin_c = font2.render(': '+ str(calculator), True, (255,255,255))
    window.blit(transform.scale(image.load('images/coin.png'), (50,50)), (10,10))
    window.blit(coin_c, (55,15))
        # подбирание ключей
    if sprite.collide_rect(hero,key1):
        window.blit(e_tap,(500,50))
        if keys[K_e]:
            key1.rect.y =-100
            items.remove(key1)
            chest_o = True
    if sprite.collide_rect(hero,key2):
        window.blit(e_tap,(500,50))
        if keys[K_e]:
            key1.rect.y =-100
            items.remove(key2)
            door1_o = True
    #открытие сундука
    if sprite.collide_rect(hero,chest) and chest_o == True:
        window.blit(e_tap, (500,50))
        if keys[K_e]:
            calculator +=15
            chest.image = transform.scale(image.load(chest_open), (chest.width, chest.height))
            chest_snd.play()
            door1_o = True
            chest_o = False
    if sprite.collide_rect(hero,chest) and chest_o == False:
        window.blit(k_need, (330,100))
    #отkрытие двери
    if sprite.collide_rect(hero,door) and door1_o == True:
        hero.rect.x = door.rect.x -50
        window.blit(e_tap, (500,50))
        if keys[K_e]:
            door.rect.x +=1500
            door1_o = False

    if sprite.collide_rect(hero,door) and door1_o == False:
        window.blit(chest_need, (330,100))
        hero.rect.x = door.rect.x -50
     #отkрытие 2 двери
    if sprite.collide_rect(hero,door) and door1_o == True:
        hero.rect.x = door.rect.x -50
        window.blit(e_tap, (500,50))
        if keys[K_e]:
            door.rect.x +=1500
    if sprite.collide_rect(hero,door) and door1_o == False:
        window.blit(k_need, (330,100))
        hero.rect.x = door.rect.x -50
    if keys[K_SPACE] :
        mana.rect.x = hero.rect.centerx
        mana.rect.y = hero.rect.centery      
        manas.add(mana)
        items.add(mana)
        fire.play()

    if sprite.spritecollide(enemy1, manas, True):
        enemy1.rect.y = -150
        items.remove(mana)
        kick.play()
    if sprite.spritecollide(enemy2, manas, True):
        enemy2.rect.y = -150
        items.remove(mana)
        kick.play()
    if sprite.spritecollide(enemy3, manas, True):
        enemy3.rect.y = -150
        items.remove(mana)
        kick.play()
    if sprite.spritecollide(enemy4, manas, True):
        enemy4.rect.y = -150
        items.remove(mana)
        kick.play()
    if sprite.spritecollide(enemy5, manas, True):
        enemy5.rect.y = -150
        items.remove(mana)
        kick.play()


game = True
while game:
    window.blit(bg, (0, 0))  # додавання фонової картинки
    time.delay(5) #затримка оновленя екрану
    hero.r_l()
    enemy1.update()
    enemy2.update()
    enemy3.update()
    enemy4.update()
    enemy5.update()
    mana.update()
    collides()
    for e in event.get():
        if e.type == QUIT:
            game = False
    camera.update(hero)
    for i in items:
        window.blit(i.image, camera.apply(i))
    
    display.update()