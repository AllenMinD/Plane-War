#coding=utf-8
from __future__ import division #用于除法计算
import pygame, sys, traceback
from pygame.locals import *
from random import *
import myplane
import enemy
import bullet
import supply

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

#载入背景图
background = pygame.image.load("Images/shoot_background/background.png").convert_alpha()
#载入音乐
pygame.mixer.music.load("Sounds/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("Sounds/bullet.wav")
bullet_sound.set_volume(0.1)
bomb_sound = pygame.mixer.Sound("Sounds/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("Sounds/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("Sounds/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("Sounds/get_double_laser.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("Sounds/achievement.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("Sounds/big_spaceship_flying.wav")
enemy3_fly_sound.set_volume(0.1)
enemy1_down_sound = pygame.mixer.Sound("Sounds/enemy1_down.wav")
enemy1_down_sound.set_volume(0.1)
enemy2_down_sound = pygame.mixer.Sound("Sounds/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("Sounds/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("Sounds/out_porp.wav")
me_down_sound.set_volume(0.2)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size) #创建小型飞机实例化对象
        group1.add(e1)#把生成的小型飞机添加到small_enemies中
        group2.add(e1)#把生成的小型飞机添加到 enemies中

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size) #创建中型飞机实例化对象
        group1.add(e2)#把生成的中型飞机添加到mid_enemies中
        group2.add(e2)#把生成的中型飞机添加到 enemies中

def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size) #创建大型飞机实例化对象
        group1.add(e3)#把生成的大型飞机添加到big_enemies中
        group2.add(e3)#把生成的大型飞机添加到 enemies中

def inc_speed(target, inc):
    for each in target:
        each.speed += inc


def main():
    pygame.mixer.music.play(-1)# -1代表音乐循环播放

    #生成我方飞机的实例化对象
    me = myplane.MyPlane(bg_size) #引用别的文件的类，要把文件名打在类名前面
    #生成敌方飞机的实例化对象
    enemies = pygame.sprite.Group() #建一个Group来装入所有类型的敌机，用于进行碰撞检测
    #生成小型飞机
    small_enemies = pygame.sprite.Group() #建一个Group来装小型飞机，用于处理小型飞机的变化
    add_small_enemies(small_enemies, enemies, 15)#调用方法，用来把飞机添加到Group中
    #生成中型飞机
    mid_enemies = pygame.sprite.Group() #建一个Group来装小型飞机，用于处理小型飞机的变化
    add_mid_enemies(mid_enemies, enemies, 4)#调用方法，用来把飞机添加到Group中
    #生成大型飞机
    big_enemies = pygame.sprite.Group() #建一个Group来装小型飞机，用于处理小型飞机的变化
    add_big_enemies(big_enemies, enemies, 2)#调用方法，用来把飞机添加到Group中

    #生成普通子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    #生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx-33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx+30, me.rect.centery)))

    #中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    #用于我方飞机切换图片的判断变量
    switch_image = True

    #用于延时的变量
    delay = 100

    #分数初始化
    score = 0
    #载入分数字体
    score_font = pygame.font.Font("font/font.ttf", 30)

    #游戏难度初始化
    level = 1

    #炸弹初始化
    bomb_num = 3
    bomb_image = pygame.image.load("Images/shoot/bomb.png").convert_alpha()
    bomb_font = pygame.font.Font("font/font.ttf", 40)
    bomb_rect = bomb_image.get_rect()

    #游戏暂停按钮
    paused = False
    paused_nor_image = pygame.image.load("Images/shoot/game_pause_nor.png").convert_alpha()
    paused_pressed_image = pygame.image.load("Images/shoot/game_pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("Images/shoot/game_resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("Images/shoot/game_resume_pressed.png").convert_alpha()
    paused_rect = paused_nor_image.get_rect() #获取图片矩形位置
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = paused_nor_image #pause按钮的默认初始状态

    #游戏道具的发放
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    #设定道具发放为自定义事件
    SUPPLY_TIME = USEREVENT #定义一个自定义事件 名叫 SUPPLY_TIME
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000) #每30秒产生一次自定义事件SUPPLY_TIME

    #超级子弹定时器（自定义事件）
    DOUBLE_BULLET_TIME_FINISH = USEREVENT + 1 #定义一个自定义事件 名叫 DOUBLE_BULLET_TIME_FINISH 用来限制超级子弹使用的事件
    #标志是否正在使用超级子弹
    is_double_bullet = False

    #解除我方飞机无敌状态计时器
    INVINCIBLE_TIME_FINISH = USEREVENT +2 #自定义事件：用于暂停飞机无敌

    #我方飞机生命数量
    life_image = pygame.image.load("Images/shoot/life.png").convert_alpha()
    life_image_rect = life_image.get_rect()
    life_num_font = pygame.font.Font("font/font.ttf", 40)
    life_num = 3

    #用于阻止重复打开记录文件
    recorded = False

    #游戏结束画面，字体
    record_score_font = pygame.font.Font("font/font.ttf", 35)
    finial_score_font = pygame.font.Font("font/font.ttf", 40)
    gameover_font = pygame.font.Font("font/font.ttf", 25)
    again_image = pygame.image.load("Images/shoot/kuangkuang.png").convert_alpha()
    again_image_rect = again_image.get_rect()
    close_image = pygame.image.load("Images/shoot/kuangkuang.png").convert_alpha()
    close_image_rect = close_image.get_rect()

    #用于延时主循环，控制游戏帧数，保护cpu
    clock = pygame.time.Clock()

    #游戏主循环
    running = True
    while running:
        for event in pygame.event.get(): #检测事件循环
            #触发退出事件
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #触发鼠标移动事件
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos): #第二个条件的意思：当鼠标移动到paused_rect位置时返回True
                    paused = not paused
                    if paused:#如果按了暂停，所有声音暂停，补给事件 暂停产生
                        pygame.time.set_timer(SUPPLY_TIME, 0) #如果暂停，“补给事件”自定义事件 暂停产生
                        pygame.mixer.music.pause()#背景音乐暂停
                        pygame.mixer.pause()#音效暂停
                    else: #如果不是暂停，所有声音正常播放，补给事件正常产生
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos): #判断鼠标的位置是否在paused_rect这个位置上，如果是就显示“深 色”图标
                    if paused:
                        paused_image = resume_pressed_image #如果在暂停的情况下，图片变成“深 色 继 续”图片
                    else:
                        paused_image = paused_pressed_image #如果在继续的情况下，图片变成“深 色 暂 停”图片
                else: #如果鼠标没在paused_rect上方的话，就显示 “浅 色” 图标
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = paused_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            #触发道具补给事件
            elif  event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]): #在True 和 False 中 随机选一个
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            #触发超级子弹结束
            elif event.type == DOUBLE_BULLET_TIME_FINISH:
                is_double_bullet = False #超级子弹效果取消
                pygame.time.set_timer(DOUBLE_BULLET_TIME_FINISH, 0)#暂停自定义事件的产生

            #触发解除飞机无敌事件
            elif event.type == INVINCIBLE_TIME_FINISH:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME_FINISH, 0)

        #游戏难度
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            #增加3架小型机，2架中型机，1架大型机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            #提升小型机的速度
            inc_speed(small_enemies, 1)
        elif level == 2 and score > 100000:
            level = 3
            upgrade_sound.play()
            #增加5架小型机，3架中型机，2架大型机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小型机和中型机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 3 and score > 200000:
            level = 4
            upgrade_sound.play()
            #增加5架小型机，3架中型机，2架大型机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小型机、中型机、大型机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 450000:
            level = 5
            upgrade_sound.play()
            #增加5架小型机，3架中型机，2架大型机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小型机和中型机的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
        elif level == 4 and score > 800000:
            level = 5
            upgrade_sound.play()
            #增加5架小型机，3架中型机，2架大型机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小型机、中型机、大型的速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        #绘制背景图
        screen.blit(background, (0, 0))

        #当生命数大于0，还有没按下暂停时，游戏才继续进行
        if life_num and not paused:
            #检测用户的键盘操作
            key_press = pygame.key.get_pressed()#获取键盘上所有键的状态，返回一个bool值序列，表示键是否被按下
            if key_press[K_w] or key_press[K_UP]:
                me.moveUp()
            if key_press[K_s] or key_press[K_DOWN]:
                me.moveDown()
            if key_press[K_a] or key_press[K_LEFT]:
                me.moveLeft()
            if key_press[K_d] or key_press[K_RIGHT]:
                me.moveRight()

            #绘制全屏炸弹补给，并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect) #绘制炸弹补给
                if pygame.sprite.collide_mask(bomb_supply, me): #直接检测bomb_supply, me两个精灵是否发生碰撞
                    get_bomb_sound.play()
                    if bomb_num < 3: #如果原本炸弹数<=3个，就能获得一个炸弹
                        bomb_num += 1
                    bomb_supply.active = False #获得炸弹补给后，该补给图片消失

            #绘制超级子弹补给，并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me): #直接检测bomb_supply, me两个精灵是否发生碰撞
                    get_bullet_sound.play()
                    #发射超级子弹
                    is_double_bullet = True #开始发射超级子弹
                    pygame.time.set_timer(DOUBLE_BULLET_TIME_FINISH, 18 * 1000) #自定义事件DOUBLE_BULLET_TIME_FINISH将在18秒后产生（18秒后，超级子弹失效）
                    bullet_supply.active = False

            #绘制大型飞机
            for each in big_enemies:
                if each.active:
                    #飞机移动
                    each.move()
                    #绘制飞机
                    if each.hit:
                        screen.blit(each.hit_image, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    #绘制血槽
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5), (each.rect.right, each.rect.top - 5), 2)
                    #当生命值大于20%时，显示绿色血条，否则显示红色
                    energy_remain = each.energy / enemy.BigEnemy.energy #计算血量的百分比
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + energy_remain * each.rect.width, each.rect.top - 5), 2)

                    #即将出现在画面中前，播放音效
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                else:
                    #飞机毁灭
                    if not(delay % 3): #每次当delay能整除3的时候，就显示一张图片
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6 #这里是一个小技巧，这样 e3_destroy_index的值只能是0~5
                        if e3_destroy_index == 0: #当飞机毁灭图片显示完时，就重置飞机
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()

            #绘制中型飞机
            for each in mid_enemies:
                if each.active:
                    #飞机移动
                    each.move()
                    #绘制飞机
                    if each.hit:
                        screen.blit(each.hit_image, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    #绘制血槽
                    pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5), (each.rect.right, each.rect.top - 5), 2)
                    #当生命值大于20%时，显示绿色血条，否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy #计算血量的百分比
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + energy_remain * each.rect.width, each.rect.top - 5), 2)
                else:
                    #飞机毁灭
                    if not(delay % 3): #每次当delay能整除3的时候，就显示一张图片
                        if e2_destroy_index == 0:
                           enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4 #这里是一个小技巧，这样 e2_destroy_index的值只能是0~3
                        if e2_destroy_index == 0: #当飞机毁灭图片显示完时，就重置飞机
                            score += 6000
                            each.reset()

            #绘制小型飞机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    #飞机毁灭
                    if not(delay % 3): #每次当delay能整除3的时候，就显示一张图片
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4 #这里是一个小技巧，这样 e1_destroy_index的值只能是0~3
                        if e1_destroy_index == 0: #当飞机毁灭图片显示完时，就重置飞机
                            score += 1000
                            each.reset()

            #绘制子弹
            #子弹延时显示设置
            if not(delay % 10): #每10帧重置一次图片
                bullet_sound.play()
                if is_double_bullet: #如果是超级子弹
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx-33, me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx+30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM #索引+1
                else: #如果是普通子弹
                    bullets = bullet1
                    bullet1[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM #索引+1
            #显示子弹
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    #子弹碰撞检测
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            #绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                #飞机毁灭
                if not(delay % 3): #每次当delay能整除3的时候，就显示一张图片
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4 #这里是一个小技巧，这样 me_destroy_index的值只能是0~3
                    if me_destroy_index == 0: #当飞机毁灭图片显示完时，就重置飞机
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME_FINISH, 3 * 1000) #调用自定义事件，3秒后结束飞机无敌

            #检测我方飞机是否发生碰撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)#判断me是否与enemies中的任何一个发生碰撞，返回一个列表，里面装了与me发生碰撞的enemies
            if enemies_down and not me.invincible: #当有敌机坠毁，而且我方飞机不是无敌的时候
                me.active = False #我方飞机坠毁
                for each in enemies_down:
                    each.active = False #敌方飞机坠毁

            #绘制全屏炸弹图片
            bomb_text = bomb_font.render("x %d" % bomb_num, True, BLACK) #把text转化成surface
            bomb_text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height)) #显示图片
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 10 - bomb_text_rect.height)) #显示数字

            #绘制剩余生命数量
            life_text = life_num_font.render(str(life_num), True, BLACK) #把text转化为surface
            life_text_rect = life_text.get_rect()
            screen.blit(life_image, (width - life_image_rect.width - life_text_rect.width, height - 10 - life_image_rect.height)) #显示图片
            screen.blit(life_text, (width - life_text_rect.width, height - 10 - life_text_rect.height)) #显示数字

            #绘制分数
            score_text = score_font.render("Score : %s" % str(score), True, BLACK)
            screen.blit(score_text, (10, 5))

        #否则,当生命数<0时，就绘制结束画面
        elif life_num == 0:
            pygame.mixer.music.stop() #背景音乐停止
            pygame.mixer.stop() #全部音效停止
            pygame.time.set_timer(SUPPLY_TIME, 0) #补给发放停止

            #读取记录
            if not recorded:
                recorded = True
                #读取历史最高得分
                with open("record.txt", "r") as f:
                    record_score = int(f.read())

                #如果玩家得分高于历史最高得分，则分数存档
                if score > record_score:
                    record_score = score
                    with open("record.txt", "w") as f:
                        f.write(str(score))

            ############################################绘制结束画面######################################################

            #绘制字体“Best:”
            record_score_text = record_score_font.render("Best : %d" % record_score, True, BLACK)
            screen.blit(record_score_text, (50, 50))

            #绘制字体“Your Score”
            gameover_text1 = finial_score_font.render("Your Score ", True, BLACK)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2 , height - 500
            screen.blit(gameover_text1, gameover_text1_rect)

            #绘制最终分数
            gameover_text2 = finial_score_font.render(str(score), True, BLACK)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2 , height - 450
            screen.blit(gameover_text2, gameover_text2_rect)

            #绘制两个框框
            again_image_rect.left, again_image_rect.top = (width - again_image_rect.width) // 2, height - 390
            screen.blit(again_image, again_image_rect)
            close_image_rect.left, close_image_rect.top = (width - close_image_rect.width) // 2, height - 320
            screen.blit(close_image, close_image_rect)

            #绘制框框里的字
            again_text = gameover_font.render("Try Again", True, BLACK)
            again_text_rect = again_text.get_rect()
            again_text_rect.left, again_text_rect.top = (width - again_text_rect.width) // 2, height - 385
            screen.blit(again_text, again_text_rect)
            close_text = gameover_font.render("End", True ,BLACK)
            close_text_rect = close_text.get_rect()
            close_text_rect.left, close_text_rect.top = (width - close_text_rect.width) // 2, height - 315
            screen.blit(close_text, close_text_rect)

            #框框按钮触发
            if pygame.mouse.get_pressed()[0]: #如果用户按下鼠标左键
                pos = pygame.mouse.get_pos() #获取鼠标坐标
                if again_image_rect.left < pos[0] < again_image_rect.right and \
                   again_image_rect.top < pos[1] < again_image_rect.bottom: #如果按了“Try Again”
                    main() # 调用main函数，重新开始游戏

                elif close_image_rect.left < pos[0] < close_image_rect.right and \
                     close_image_rect.top < pos[1] < close_image_rect.bottom: #如果按了“End”
                    pygame.quit() #退出游戏
                    sys.exit()

        #图片延时操作
        if not(delay % 5): #每次当delay能整除5时，就变换图片
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100

        #绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
