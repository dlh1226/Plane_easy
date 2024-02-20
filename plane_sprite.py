import pygame
import random

class GameSprite(pygame.sprite.Sprite):
    def __init__(self,image_name,speed=1):
        super().__init__()
        self.image=pygame.image.load(image_name)
        #矩形对象,(0,0,图片宽，图片高)
        self.rect=self.image.get_rect()
        self.speed=speed

    def update(self):
        #在屏幕的垂直方向向下移动
        self.rect.y+=self.speed



#背景类
class Background(GameSprite):
    def __init__(self,is_alt=False):
        super().__init__('../images/background.png')
        if is_alt:
            self.rect.y=-self.rect.height

    def update(self):
        #调用父类update方法实现向下移动
        super().update()

        #判断是否分出屏幕，如果是，则将图像设置到屏幕上方
        if self.rect.y>700:
            self.rect.y=-self.rect.height

class Enemy(GameSprite):
    def __init__(self):
        #调用父类方法，指定敌机图片
        image_name=random.choice(['../images/enemy1.png','../images/enemy2.png'])
        super().__init__(image_name)
        #制定随机速度
        self.speed=random.randint(1,3)
        #指定随机位置
        self.rect.x=random.randint(0,400-self.rect.width)
        #设置血量，连续射击3次才会死亡
        self.blood=3

    def update(self):
        #调用父类update方法，保持向下移动
        super(Enemy,self).update()
        #判断是否飞出屏幕，如果是，需要从精灵组中删除
        if self.rect.y>700:
            print("飞出屏幕，需要从精灵组中删除")
            #kill方法可以将精灵从精灵组中移除，精灵就会自动销毁
            self.kill()

    def __del__(self):
        print("敌机挂了")


class Hero(GameSprite):
    def __init__(self):
        #调用父类方法，传递图片
        super().__init__('../images/me1.png',0)
        #设置飞机的初始位置
        self.rect.x=240-self.rect.width/2  #屏幕正中间
        self.rect.y=600-self.rect.height  #距离底部100
        self.upanddown=0  #控制上下移动的属性
        # 子弹精灵组
        self.bullet_group = pygame.sprite.Group()

    def update(self):
        self.rect.x+=self.speed
        self.rect.y+=self.upanddown

        #左右移动不能移出屏幕
        if self.rect.x<0:
            self.rect.x=0
        elif self.rect.x>480-self.rect.width:
            self.rect.x=480-self.rect.width
        #上下移动不能移出屏幕
        if self.rect.y<0:
            self.rect.y=0
        elif self.rect.y>700-self.rect.height:
            self.rect.y=700-self.rect.height


    def fire(self):
        #创建子弹精灵添加子弹精灵组中
        for i in range(3):
            bullet=Bullet()
            #设置子弹的初始位置
            bullet.rect.centerx=self.rect.centerx #子弹的中心点==飞机的中心点
            bullet.rect.y=self.rect.y-(i+1)*15  #每颗子弹距离另一个对象的y15
            self.bullet_group.add(bullet)


class Bullet(GameSprite):
    def __init__(self):
        super().__init__('../images/bullet1.png',-2)

    def update(self):
        #调用父类update方法，实现垂直移动
        super().update()

        #判断子弹是否飞出屏幕
        if self.rect.y<-self.rect.height:
            self.kill()

    def __del__(self):
        print("子弹被销毁")









