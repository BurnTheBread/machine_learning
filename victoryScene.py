import pygame.image
import globals
import time
import ui


class VictoryScene:
    def __init__(self):
        self.previousUpdate = time.time()
        self.startTime = time.time()
        self.displayTime = 8
        self.delayBetweenPhotos = 0.1
        self.photoIndex = 0
        self.amountPhotos = 68 if globals.winner == 0 else 37
        self.winnerFolder = "human" if globals.winner == 0 else "robot"
        self.winner = "Jij" if globals.winner == 0 else "De computer"
        print(globals.winner)
        self.currentImage = pygame.image.load(f"resources/{self.winnerFolder}/{self.photoIndex+1}.gif")
        self.text = ui.TextBox(100, 100, f"{self.winner} wint!!", font=200, color=(65, 65, 65))

    def reset(self):
        self.winnerFolder = "human" if globals.winner == 0 else "robot"
        self.winner = "Jij" if globals.winner == 0 else "De computer"
        self.text = ui.TextBox(100, 100, f"{self.winner} wint!!", font=200, color=(65, 65, 65))
        self.photoIndex = 0
        self.currentImage = pygame.image.load(f"resources/{self.winnerFolder}/{self.photoIndex + 1}.gif")
        self.startTime = time.time()

    def update(self):
        if time.time() - self.previousUpdate > self.delayBetweenPhotos:
            if self.photoIndex < self.amountPhotos:
                self.photoIndex += 1
            else:
                self.photoIndex = 0

            self.currentImage = pygame.transform.scale2x(pygame.image.load(f"resources/{self.winnerFolder}/{self.photoIndex+1}.gif"))
            self.previousUpdate = time.time()

        if time.time() - self.startTime > self.displayTime:
            globals.currentScene = globals.Scenes.menu

    def draw(self, window):
        self.text.draw(window)
        window.blit(self.currentImage, ((globals.screenWidth-self.currentImage.get_width())/2, (globals.screenHeight-self.currentImage.get_height())/2))