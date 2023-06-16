import pygame
import math
import random
from sprite import Sprite
import os

class Obstacles():
    def __init__(self, screenWidth, scale, screen,):
        self.screenWidth = screenWidth
        self.scale = scale
        self.screen = screen
        self.minObstacles = 1
        self.maxObstacles = 3
        self.obstacles = []
        self.items = []
        self.enemies = list(self.getEnemies().items())
        self.deathAnimation = self.getDeathAnimation()
        self.obstacleGap = 600
        self.bulletChance = 0.8
        
    def getDeathAnimation(self):
        dirPath = f"Assets/Characters/enemy-death"
        animationFolders = os.listdir(dirPath)
        animationList = []
        for animation in animationFolders:
            imageDirPath = dirPath + f"\{animation}"
            image = pygame.image.load(imageDirPath)
            animationList.append(image)
        return animationList
    
    def getEnemies(self):
        sprite = Sprite("Enemies", 40, 40, self.scale)
        return sprite.loadSprites()

    def generateObstacles(self):
        lower = self.screenWidth
        higher = self.screenWidth * 2
        bulletRand = random.uniform(0, 1)
        if bulletRand <= self.bulletChance:
            randomSpawn = random.randint(lower, higher)
            image = pygame.image.load("Assets/UI/Ammo/bullet.png").convert_alpha()
            item = Item(randomSpawn, 600, self.screen, self.scale, image)
            self.items.append(item)
        noOfObstacles = random.randint(self.minObstacles, self.maxObstacles)
        
        for x in range(noOfObstacles):
            randEnemyNum = random.randint(0, len(self.enemies) - 1)
            randomEnemy = self.enemies[randEnemyNum]
            randomSpawn = random.randint(lower, higher)
            # y = 0
            # if randomEnemy[0] == "eagle":
            #     y = 600
            # else:
            #     y = 770
            for obstacle in self.obstacles:
                while(not(abs(obstacle.rect.x - randomSpawn) > self.obstacleGap)):
                    randomSpawn = random.randint(lower, higher)
            enemy = Enemy(randomSpawn, 840, self.screen, self.scale, randomEnemy[1], randomEnemy[0], self.deathAnimation)
            self.obstacles.append(enemy)
            


    def update(self, projectiles, player):
        generateNewObstacles = True
        for obstacle in self.obstacles:
            if obstacle.rect.x > self.screenWidth:
                generateNewObstacles = False
        for obstacle in self.obstacles:
            if obstacle.rect.x + obstacle.rect.width < 0:
                self.obstacles.remove(obstacle)

        for item in self.items:
            if item.rect.x + item.rect.width < 0:
                self.items.remove(item)
            elif player.rect.colliderect(item):
                player.bullets +=1
                self.items.remove(item)
                print("True")
            else:
                item.update(20)

        if generateNewObstacles:
            self.generateObstacles()

        for obstacle in self.obstacles:
            if obstacle.isAlive:
                obstacle.update(20, projectiles)
        
        
    def draw(self):
        self.screen.blit(self.image, self.rect)

class Item():
    def __init__(self, x, y, screen, scale, image):
        self.screen = screen
        self.image = image
        self.rect = pygame.Rect(x, y, self.image.get_width() * 2, self.image.get_height() * 2)


    def update(self, x):
        self.rect.x -= x
        self.draw()
    
        
    def draw(self):
        self.screen.blit(self.image, (self.rect.x - 20, self.rect.y - 30))
        #pygame.draw.rect(self.screen, ((255, 0, 0)), self.rect, 1)

class Enemy():
    def __init__(self, x, y, screen, scale, animation, name, deathAnimation):
        self.screen = screen
        self.name = name
        self.animation = animation
        self.image = animation[0]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 0.3, self.image.get_height() * 0.3))
        self.rect = pygame.Rect(x, y, self.image.get_width() * 2, self.image.get_height() * 2)
        self.counter = 0
        self.animationNumber = 0
        self.isAlive = True
        self.startDeathAnimation = False
        self.deathAnimation = deathAnimation
        self.deathAnimationImage = deathAnimation[0]
        self.deathAnimationImage = pygame.transform.scale(self.deathAnimationImage, (self.deathAnimationImage.get_width() * 0.5, self.deathAnimationImage.get_height() * 0.5))

    def count(self):
        self.counter = round(self.counter + 0.1,4)
        if self.counter.is_integer():
            self.animationNumber += 1


    def update(self, x, projectiles):
        for projectile in projectiles:
            if self.rect.colliderect(projectile.rect) and self.isAlive and not self.startDeathAnimation:
                self.startDeathAnimation = True
                projectiles.remove(projectile)
                self.animationNumber = 0
                self.deathAnimationImage = self.deathAnimation[self.animationNumber]
            if self.startDeathAnimation:
                self.death()
                return
        if self.startDeathAnimation:
            self.death()
            return
        if self.animationNumber >= len(self.animation):
            self.animationNumber = 0
        self.image = self.animation[self.animationNumber]
        self.rect.x -= x
        self.draw()
        self.count()
        #self.counter += 1
    
    def death(self):
        if self.animationNumber >= len(self.deathAnimation):
            self.isAlive = False
            self.startDeathAnimation = False
            return
        self.deathAnimationImage = self.deathAnimation[self.animationNumber]
        self.screen.blit(self.deathAnimationImage, self.rect)
        self.count()
        #self.counter += 1
        
    def draw(self):
        self.screen.blit(self.image, (self.rect.x - 20, self.rect.y - 30))
        #pygame.draw.rect(self.screen, ((255, 0, 0)), self.rect, 1)