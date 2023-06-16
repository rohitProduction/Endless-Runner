import pygame
import os, math
from map import Map
from sprite import Sprite
from player import Player
from projectile import Projectile
from obstacles import Obstacles
from UI import UI
import pygame_textinput
from db import DB

SCALE = 4
GROUND = 900
GREY = (50,50,50)
# 320x240

class Game():
    def __init__(self):
        self.screenWidth = 320 * SCALE
        self.screenHeight = 240 * SCALE
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.counter = 0
        self.playerCounter = 0
        self.animationNumber = 0
        self.playerSprite = Sprite("Red", 48, 48, 3)
        self.spriteDict = self.playerSprite.loadSprites()
        self.projectiles = []
        self.start = False
        self.isGameOver = False
        self.showLeaderboard = False
        self.score = 0
    

    def count(self, player):
        self.counter = round(self.counter + 0.1,4)
        if self.counter.is_integer():
            self.animationNumber += 1
        if self.animationNumber >= len(player.animation):
            self.animationNumber = 0

    def gravity(self, player):
        player.move(0, 20, GROUND, self.counter)

    def movement(self, keyPressed, player):
        if keyPressed[pygame.K_SPACE]:
            if (not player.isJumping) and (not player.isFalling):
                player.jump(self.counter)
                self.animationNumber = 0

        if keyPressed[pygame.K_q] and player.bullets > 0:
            if self.counter - player.bulletStart > player.bulletCooldown:
                player.bulletStart = self.counter
                OFFSETX, OFFSETY = -10, -5
                projectile = Projectile(player.rect.x + player.rect.width + OFFSETX, player.rect.y + (player.rect.height // 2) + OFFSETY, self.screen, SCALE)
                player.bullets -= 1
                self.projectiles.append(projectile)

        if player.isJumping or player.isFalling:
            player.animation = self.spriteDict["jump"]
        else:
            player.animation = self.spriteDict["run"]

    def removeProjectiles(self):
        for projectile in self.projectiles:
            if projectile.rect.x > self.screenWidth:
                self.projectiles.remove(projectile)

    
    def loop(self):
        clock = pygame.time.Clock()
        running = True
        map = Map("Super Mountain Dusk", "Terrain", SCALE)
        player = Player(100, 800, self.playerSprite.width, self.playerSprite.height, self.screen, self.spriteDict["run"], 1.5)
        obstacles = Obstacles(self.screenWidth, 2, self.screen)
        obstacles.generateObstacles()
        ui = UI(3)
        textinput = pygame_textinput.TextInputVisualizer()
        db = DB()
        while running:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            map.draw(self.screen, self.counter)
            self.count(player)
            self.gravity(player)
            player.draw(self.animationNumber)
            ui.draw(self.screen, player.health, player.bullets, self.score)
            if self.showLeaderboard:
                self.showLeaderboard = ui.leaderboard(self.screen, db, self.score)
            elif not self.start:
                start, leaderboard = ui.start(self.screen, self.isGameOver, textinput, db, self.score)
                self.start = start
                self.showLeaderboard = leaderboard
            else:
                if self.isGameOver:
                    self.score = 0
                self.isGameOver = False
                keysPressed = pygame.key.get_pressed()
                self.movement(keysPressed, player)
                for projectile in self.projectiles:
                    projectile.update(5)
                    projectile.draw()
                obstacles.update(self.projectiles, player)
                player.collide(obstacles.obstacles, self.counter)
                self.removeProjectiles()
                self.score += 1
            if player.health <=0:
                self.start = False
                self.isGameOver = True
                self.projectiles = []
                player = Player(100, 800, self.playerSprite.width, self.playerSprite.height, self.screen, self.spriteDict["run"], 1.5)
                obstacles = Obstacles(self.screenWidth, 2, self.screen)
                obstacles.generateObstacles()
                ui = UI(3)
                
                textinput = pygame_textinput.TextInputVisualizer()
            self.counter += 2
            pygame.display.update()


            

    def run(self):
        pygame.init()
        pygame.display.set_caption("Endless Runner")
        self.loop()

if __name__ == "__main__":
    game = Game()
    game.run()

