import pygame
import os

class Map():
    def __init__(self, folderName, terrainFolderName, scale):
        self.folderName = folderName
        self.terrainFolderName = terrainFolderName
        self.scale = scale
        self.images = self.getImages()
        self.terrainImages = self.getTerrainImages()
        self.scrollCount = 0

    def getImages(self):
        dirPath = f"Assets/Maps/{self.folderName}"
        mapFiles = os.listdir(dirPath)
        images = []
        for file in mapFiles:
            image = pygame.image.load(f"Assets/Maps/{self.folderName}/{file}")
            scaledImage = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale ))
            images.append(scaledImage)
        return images
    
    def getTerrainImages(self):
        dirPath = f"Assets/Maps/{self.terrainFolderName}"
        mapFiles = os.listdir(dirPath)
        images = {}
        for file in mapFiles:
            image = pygame.image.load(f"Assets/Maps/{self.terrainFolderName}/{file}")
            scaledImage = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale ))
            images[file] = scaledImage
        return images

    def drawBackground(self, screen, x, y):
        for image in self.images:
            if x + ((self.scrollCount + 1) * image.get_width()) <= 0:
                self.scrollCount += 1
            screen.blit(image, (x + (self.scrollCount * image.get_width()), y))
            screen.blit(image, (x + ((self.scrollCount + 1) * image.get_width()), y))

    def drawTerrain(self, screen):
        underTerrain = self.terrainImages["terrain1.png"]
        tiles = screen.get_width() // underTerrain.get_width()
        for x in range(tiles):
            screen.blit(underTerrain, (underTerrain.get_width() * x, screen.get_height() - underTerrain.get_height()))

    def draw(self, screen, offset):
        self.drawBackground(screen, -offset,0)
        self.drawTerrain(screen)
