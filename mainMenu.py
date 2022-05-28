import pygame
import globals
import ui
import enum

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)


class MainMenu:
    def __init__(self):
        self.start = startButton()
        self.stop = stopButton()
        self.addObs = addObservation()
        self.removeObs = removeObservation()
        self.obsCounter = observationCounter()
        self.obsText = obserationText()
        self.nextCir = nextCircuit()
        self.prevCir = previousCircuit()
        self.cirCounter = circuitCounter()
        self.cirText = circuitText()
        self.immortal = immortalCheckBox()
        self.immortalTxt = immortalText()

    def draw(self, window):
        self.start.draw(window)
        self.stop.draw(window)
        self.addObs.draw(window)
        self.removeObs.draw(window)
        self.obsCounter.draw(window)
        self.obsText.draw(window)
        self.nextCir.draw(window)
        self.prevCir.draw(window)
        self.cirCounter.draw(window)
        self.cirText.draw(window)
        self.immortal.draw(window)
        self.immortalTxt.draw(window)

    def update(self):
        self.start.update()
        self.stop.update()
        self.addObs.update()
        self.removeObs.update()
        self.nextCir.update()
        self.prevCir.update()
        self.immortal.update()

class immortalCheckBox(ui.ImageButton):
    def __init__(self):
        super(immortalCheckBox, self).__init__(1200, 1000, "resources/unchecked.png", width=40)
        self.uncheckedImage = self.image.copy()
        self.checkedImage = pygame.image.load("resources/checked.png")
        self.checkedImage = pygame.transform.scale(self.checkedImage, (self.width, int(self.width * self.checkedImage.get_height() / self.checkedImage.get_width())))

    def pressed(self):
        globals.immortal = not globals.immortal
        print("pressed")
        self.image = self.checkedImage if globals.immortal else self.uncheckedImage

class immortalText(ui.TextBox):
    def __init__(self):
        super(immortalText, self).__init__(1200+60, 1000, "immortal", (0, 0, 0), font=50)

class addObservation(ui.ImageButton):
    def __init__(self):
        super(addObservation, self).__init__(1000, 525, "resources/plus.png", width=50)

    def pressed(self):
        print("plus")
        if globals.observation < 8:
            globals.observation += 1

class removeObservation(ui.ImageButton):
    def __init__(self):
        super(removeObservation, self).__init__(1000, 600, "resources/minus.png", width=50)

    def pressed(self):
        print("minus")
        if globals.observation > 1:
            globals.observation -= 1

class observationCounter(ui.TextBox):
    def __init__(self):
        super(observationCounter, self).__init__(850, 525, str(globals.observation), width=80, color=black)

    def draw(self, screen):
        self.changeText(str(globals.observation))
        super(observationCounter, self).draw(screen)

class obserationText(ui.TextBox):
    def __init__(self):
        super(obserationText, self).__init__(150, 550, "OBSERVATIONS:", font=75, color=black)


class nextCircuit(ui.ImageButton):
    def __init__(self):
        super(nextCircuit, self).__init__(1000, 225, "resources/plus.png", width=50)

    def pressed(self):
        print("plus")
        if globals.circuit < 4:
            globals.circuit += 1

class previousCircuit(ui.ImageButton):
    def __init__(self):
        super(previousCircuit, self).__init__(1000, 300, "resources/minus.png", width=50)

    def pressed(self):
        print("minus")
        if globals.circuit > 1:
            globals.circuit -= 1

class circuitCounter(ui.TextBox):
    def __init__(self):
        super(circuitCounter, self).__init__(850, 225, str(globals.circuit), width=80, color=black)

    def draw(self, screen):
        self.changeText(str(globals.circuit))
        super(circuitCounter, self).draw(screen)

class circuitText(ui.TextBox):
    def __init__(self):
        super(circuitText, self).__init__(150, 250, "CIRCUIT:", font=75, color=black)

class startButton(ui.TextButton):
    def __init__(self, ):
        super().__init__((globals.screenWidth-250)/2, 100, 250, "START", defaultColor=black, selectColor=blue, pressedColor=red)

    def pressed(self):
        print("start racing")
        globals.currentScene = globals.Scenes.racing

class stopButton(ui.TextButton):
    def __init__(self):
        super().__init__((globals.screenWidth-250)/2, 700, 250, "QUIT", defaultColor=black, selectColor=blue, pressedColor=red)

    def pressed(self):
        pygame.quit()
        exit()
