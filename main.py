import pygame
import globals
from mainMenu import MainMenu
from racingScene import RacingScene
from victoryScene import VictoryScene

pygame.init()

window = pygame.display.set_mode((globals.screenWidth, globals.screenHeight))
pygame.display.set_caption("AI Racer")
pygame.display.set_icon(pygame.image.load("resources/icon.png"))

pygame.display.flip()

mainMenu = MainMenu()
racingScene = RacingScene()
victoryScene = VictoryScene()

currentScene = globals.currentScene

def update():
    global currentScene

    if globals.currentScene != currentScene:
        globals.sceneRunning = False
        currentScene = globals.currentScene
    if globals.currentScene == globals.Scenes.menu:
        mainMenu.update()
    elif globals.currentScene == globals.Scenes.racing:
        if not globals.sceneRunning:
            racingScene.reset()
            globals.sceneRunning = True
        racingScene.update()
    elif globals.currentScene == globals.Scenes.victory:
        if not globals.sceneRunning:
            victoryScene.reset()
            globals.sceneRunning = True
        victoryScene.update()

def draw():
    window.fill((255, 255, 255))

    if globals.currentScene == globals.Scenes.menu:
        mainMenu.draw(window)
    elif globals.currentScene == globals.Scenes.racing:
        racingScene.draw(window)
    elif globals.currentScene == globals.Scenes.victory:
        victoryScene.draw(window)

    pygame.display.update()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update()
    draw()

pygame.quit()
