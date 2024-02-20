import pygame
import plane_sprite
#敌机出场事件代号
ENEMY_EVENT=pygame.USEREVENT
#发射子弹事件
FIRE=pygame.USEREVENT+1

class PlaneGame:
    def __init__(self):
        self.screen=pygame.display.set_mode((480,700))
        #创建时钟对象
        self.clock=pygame.time.Clock()
        #调用函数，创建精灵和精灵组
        self.create_sprite()
        #创建敌机出场定时器（每隔一秒触发一次）
        pygame.time.set_timer(ENEMY_EVENT,1000)
        #创建发射子弹定时器（每隔0.5秒发射一次）
        pygame.time.set_timer(FIRE,500)



    #创建精灵和精灵组
    def create_sprite(self):
        #创建背景精灵组
        #方法一：
        bg1=plane_sprite.Background() #默认为False
        bg2=plane_sprite.Background(True)  #True代表市第二张图
        self.bg_group=pygame.sprite.Group()
        self.bg_group.add(bg1,bg2)
        #创建敌机精灵组
        self.enemy_group=pygame.sprite.Group()
        #创建英雄精灵和精灵组
        self.hero=plane_sprite.Hero()
        self.hero_group=pygame.sprite.Group()
        self.hero_group.add(self.hero)


    #时间监听
    def event_handler(self):
        #获得按键
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  #向左移动
            self.hero.speed=-2
        elif keys[pygame.K_RIGHT]: #向右移动
            self.hero.speed=2

        elif keys[pygame.K_UP]:  #向上移动
            self.hero.upanddown=-2
        elif keys[pygame.K_DOWN]:   #向下移动
            self.hero.upanddown=2
        else:
            self.hero.speed=0
            self.hero.upanddown=0


        event_list=pygame.event.get()
        for event in event_list:
            if event.type==ENEMY_EVENT:
                print("敌机出场")
                #实例化敌机对象
                enemy=plane_sprite.Enemy()
                self.enemy_group.add(enemy)
            elif event.type==pygame.QUIT:
                pygame.quit()

            elif event.type==FIRE:
                print("发射子弹")
                self.hero.fire()

    #碰撞检测
    def check_collide(self):
        #1.子弹碰撞敌机
        ret=pygame.sprite.groupcollide(self.hero.bullet_group,
                                       self.enemy_group,True,False)
        if ret:
            for value in ret.values():
                e=value[0]
                e.blood-=1
                print(e.blood)
                if e.blood==0:
                    e.kill()

        ret2=pygame.sprite.groupcollide(self.enemy_group,
                                        self.hero_group,True,True)
        if ret2:
            pygame.quit()


    #更新/绘制精灵组
    def update_sprites(self):
        #更新绘制背景精灵组
        self.bg_group.update()
        self.bg_group.draw(self.screen)
        #更新绘制敌机精灵组
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        #更新绘制英雄精灵组
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        #更新子弹精灵组
        self.hero.bullet_group.update()
        self.hero.bullet_group.draw(self.screen)

    def start_game(self):
        print('游戏开始')
        while True:
            #设置刷新帧率
            self.clock.tick(60)
            #事件监听
            self.event_handler()
            #碰撞检测
            self.check_collide()
            #更新绘制精灵组
            self.update_sprites()
            #更新屏幕显示
            pygame.display.update()


if __name__=="__main__":
    #创建游戏对象
    game=PlaneGame()
    game.start_game()










