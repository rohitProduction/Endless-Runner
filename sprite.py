import pygame
import os

class Sprite():
    def __init__(self, folderName, width, height, scale):
        self.folderName = folderName
        self.width = width
        self.height = height
        self.scale = scale

    def loadSprites(self):
        dirPath = f"Assets/Characters/{self.folderName}"
        animationFolders = os.listdir(dirPath)
        animationDict = {}
        for animation in animationFolders:
            animationDict[animation] = []
        for animation in animationDict:
            folder = os.listdir(dirPath + f"\{animation}")
            for x in range(len(folder)):
                imageDirPath = dirPath + f"\{animation}\{folder[x]}"
                image = pygame.image.load(imageDirPath)
                image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
                animationDict[animation].append(image)
            
        return animationDict

    # def draw(self, action, window):
    #     animationDict = self.seperateSprites()
    #     images = animationDict[action]
    #     for image in images:
    #         image.blit(window, (0, 0), ((frame * width), (row * height), width, height))