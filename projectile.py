import pygame
import math

class Projectile():
    def __init__(self, x, y, screen, scale):
        self.screen = screen
        self.image = pygame.image.load("Assets/EXTRAS/SpongeBullet.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * scale, self.image.get_height() * scale))
        self.rect = pygame.Rect(x, y, self.image.get_width() , self.image.get_height())

    def update(self, x):
        self.rect.x += x
        
    def draw(self):
        self.screen.blit(self.image, self.rect)