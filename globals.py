import enum

class Scenes(enum.Enum):
    menu = 0
    racing = 1
    victory = 2

currentScene = Scenes.menu
observation = 8
circuit = 1
immortal = False
winner = None #0: player, 1: AI

sceneRunning = False

screenWidth = 1920
screenHeight = 1080

fps = 30