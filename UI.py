import pygame
import os
import pygame_textinput


class UI():
    def __init__(self, scale):
        self.scale = scale
        self.heartImages = self.getHeartImages()
        self.maxHearts = 3

        self.bulletImage = pygame.image.load("Assets/UI/Ammo/bullet.png").convert_alpha()
        self.maxBullets = 3

    def getHeartImages(self):
        dirPath = f"Assets/UI/Hearts/"
        mapFiles = os.listdir(dirPath)
        images = []
        for file in mapFiles:
            image = pygame.image.load(dirPath + file)
            scaledImage = pygame.transform.scale(image, (image.get_width() * self.scale, image.get_height() * self.scale ))
            images.append(scaledImage)
        return images
    
    def start(self, screen, isGameOver, textInput, db, score):
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        grey = (170,170,170)

        pygame.draw.rect(screen,grey,(screen.get_width()//2 - 100, screen.get_height()//2 - 200, 220,40))
        if isGameOver:
            text_surface = my_font.render('Game Over', False, (255, 255, 255))
        else:
            text_surface = my_font.render('Endless Runner', False, (255, 255, 255))        
        
        screen.blit(text_surface, (screen.get_width()//2 - 100, screen.get_height()//2 - 200))
        
        startGame = pygame.draw.rect(screen,grey,(screen.get_width()//2 - 200, screen.get_height()//2 - 100, 170,40))
        text_surface = my_font.render('Start Game', False, (255, 255, 255))
        screen.blit(text_surface, (screen.get_width()//2 - 200, screen.get_height()//2 - 100))

        leaderboards = pygame.draw.rect(screen,grey,(screen.get_width()//2 , screen.get_height()//2 - 100, 200,40))
        text_surface = my_font.render('Leaderboards', False, (255, 255, 255))
        screen.blit(text_surface, (screen.get_width()//2 , screen.get_height()//2 - 100))

        mousePosition = pygame.mouse.get_pos()
        isMousedPressed = pygame.mouse.get_pressed()

        if isGameOver:
            events = pygame.event.get()
            textInput.update(events)
            userText = pygame.draw.rect(screen,grey,(screen.get_width()//2 - 200, screen.get_height()//2, 240,40))
            screen.blit(textInput.surface, (screen.get_width()//2 - 190, screen.get_height()//2 + 10))

            enter = pygame.draw.rect(screen,grey,(screen.get_width()//2 + 100, screen.get_height()//2, 100,40))
            text_surface = my_font.render('Enter', False, (255, 255, 255))
            screen.blit(text_surface, (screen.get_width()//2 + 100 , screen.get_height()//2))

            if isMousedPressed[0] and enter.collidepoint(mousePosition):
                db.insertScore(textInput.value, score)
                return False, False
            


        
        if isMousedPressed[0] and startGame.collidepoint(mousePosition):
            return True, False
        if isMousedPressed[0] and leaderboards.collidepoint(mousePosition):
            return False, True
        return False, False
    

    def leaderboard(self, screen, db, score):
        screen.fill((170,170,170))
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surface = my_font.render("Leaderboard", False, (255, 255, 255))
        screen.blit(text_surface, (560, 10))
        userScores = db.getScores()
        userScores.sort(key=lambda i: i[1], reverse = True)

        goBack = pygame.draw.rect(screen,(0,0,0),(1000, 10, 130,40))
        text_surface = my_font.render('Go back', False, (255, 255, 255))
        screen.blit(text_surface, (1000, 10))
        for x, userScore in enumerate(userScores):
            if x < 10:
                user = userScore[0]
                score = userScore[1]
                text_surface = my_font.render(user, False, (255, 255, 255))
                screen.blit(text_surface, (400, (50 * x) + 100 ))

                text_surface = my_font.render(str(score), False, (255, 255, 255))
                screen.blit(text_surface, (800, (50 * x) + 100 ))

        mousePosition = pygame.mouse.get_pos()
        isMousedPressed = pygame.mouse.get_pressed()
        if isMousedPressed[0] and goBack.collidepoint(mousePosition):
            return False
        return True

    

    def draw(self, screen, hearts, bullets, score):
        for x in range(self.maxHearts):
            screen.blit(self.heartImages[0], (50*x, 10))
        for x in range(hearts):
            screen.blit(self.heartImages[2], (50*x, 10))
        for x in range(bullets):
            screen.blit(self.bulletImage, (1200 + (10*x), 10))

        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        grey = (170,170,170)
        scoreRect = pygame.draw.rect(screen,grey,(screen.get_width()//2 - 100, 20, 170,40))
        text_surface = my_font.render(f"Score: {score}", False, (255, 255, 255))
        screen.blit(text_surface, (screen.get_width()//2 - 100, 20))