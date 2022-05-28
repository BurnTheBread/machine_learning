import ui
import env
import car
from keras.models import load_model
import globals
import numpy as np
import random
import time

class RacingScene:
    def __init__(self):
        self.env = env.RacerEnv()
        self.car = car.Car(self.env.start_positions[0], "resources/car2.png")
        self.model = load_model(f"networks/racer-{globals.observation}.h5")
        self.observation = self.env.reset().reshape([1, self.env.n_observations])
        self.startRace = False
        self.timer = 5
        self.previousCountDown = time.time()
        self.countDownText = ui.TextBox(globals.screenWidth/2-350, globals.screenHeight/2-500, str(self.timer), color=(100, 100, 100), width=700)

    def getAction(self):
        if np.random.random() <= 0.01:
            return random.choice([0, 1, 2])
        else:
            return np.argmax(self.model(self.observation, training=False).numpy())

    def reset(self):
        self.model = load_model(f"networks/racer-{globals.observation}.h5")
        self.observation = self.env.reset().reshape([1, self.env.n_observations])
        self.car = car.Car(self.env.start_positions[0], "resources/car2.png")
        self.timer = 5
        self.startRace = False
        self.previousCountDown = time.time()

    def update(self):
        if not self.startRace:
            self.countDown()
            return
        self.observation, reward, done, info = self.env.step(self.getAction())
        self.observation = np.reshape(self.observation, [1, self.env.n_observations])
        self.car.update(self.car.getAction(), 1/globals.fps)
        if done:
            print("player wins")
            globals.winner = 0
            globals.currentScene = globals.Scenes.victory
        if self.env.circuit.isOffTrack(self.car) and not globals.immortal:
            print("AI wins")
            globals.winner = 1
            globals.currentScene = globals.Scenes.victory

    def draw(self, window):
        self.env.circuit.draw(window)
        self.env.car.draw(window)
        self.car.draw(window)
        if not self.startRace:
            self.countDownText.draw(window)

    def countDown(self):
        self.timer -= time.time() - self.previousCountDown
        print(self.timer)
        self.previousCountDown = time.time()
        self.countDownText.changeText(str(round(self.timer)))

        if self.timer <= 0:
            self.startRace = True

