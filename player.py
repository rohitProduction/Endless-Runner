import pygame

class Player():
    def __init__(self, x, y, width, height, screen, animation, scale):
        self.rect = pygame.Rect(x, y, width * scale, height * scale)
        self.screen = screen
        self.animation = animation
        self.isJumping = False
        self.isFalling = False
        self.jumpStart = 0
        self.jumpTime = 15
        self.health = 3
        self.damageCooldown = 100
        self.damageStart = 0
        self.bullets = 3

        self.bulletStart = 0
        self.bulletCooldown = 20

    def jump(self, counter):
        self.isJumping = True
        self.jumpStart = counter

    def move(self, x, y, ground, counter):
        self.rect.x += x
        if self.isJumping and counter - self.jumpStart < self.jumpTime:
            self.rect.y -= 40
        elif self.isJumping and counter - self.jumpStart > self.jumpTime:
            self.isFalling = True
            self.isJumping = False
        else:
            self.rect.y += y
            
        if self.rect.y + self.rect.height> ground:
            self.isFalling = False
            self.rect.y -= y
    
    def collide(self, obstacles, counter):
        for obtacles in obstacles:
            if self.rect.colliderect(obtacles.rect) and counter - self.damageStart > self.damageCooldown:
                self.damageStart = counter
                self.health -= 1

        

    def draw(self, counter):
        self.screen.blit(self.animation[counter], (self.rect.x - 30, self.rect.y - 30))
        #pygame.draw.rect(self.screen, ((255, 0, 0)), self.rect, 1)