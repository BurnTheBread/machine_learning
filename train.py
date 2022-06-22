import random
import time
import numpy as np
from collections import deque
from keras.models import Model, load_model, clone_model
from keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam, RMSprop
from env import RacerEnv
import matplotlib.pyplot as plt


def createModel(input_shape, action_space): #returns a netwerk with 3 hidden layers
    X_input = Input(input_shape)
    X = Dense(64, input_shape=input_shape, activation="relu", kernel_initializer='he_uniform')(X_input)
    X = Dense(32, activation="relu", kernel_initializer='he_uniform')(X)
    X = Dense(64, activation="relu", kernel_initializer='he_uniform')(X)
    X = Dense(action_space, activation="linear", kernel_initializer='he_uniform')(X)

    model = Model(inputs=X_input, outputs=X, name='AI-racer')
    model.compile(loss="mse", optimizer=RMSprop(lr=0.01, rho=0.95, epsilon=0.01), metrics=["accuracy"])

    model.summary()
    return model


class DQL:
    def __init__(self):
        self.env = RacerEnv()
        self.EPISODES = 2000
        self.memory = deque(maxlen=1500)

        self.points_history = []
        self.mean_point_history = []

        self.gamma = 0.98  # discount rate
        self.epsilon = 1. # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.998
        self.batch_size = 750

        # create main model
        self.q_network = createModel((self.env.n_observations,), self.env.n_actions)
        self.strategy_network = clone_model(self.q_network)
        self.strategy_network.set_weights(self.q_network.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def reduce_eps(self):
        if len(self.memory) > self.batch_size:
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

    def get_action(self, state):
        if np.random.random() <= self.epsilon:
            return random.randint(0, 2)
        else:
            print(np.argmax(self.strategy_network(state, training=False).numpy()))
            act = np.argmax(self.strategy_network(state, training=False).numpy())
            return act

    def copy_weights(self):
        print("copy weights")
        self.strategy_network.set_weights(self.q_network.get_weights())

    def train(self):
        if len(self.memory) < self.batch_size:
            return
        print("training")

        minibatch = random.sample(self.memory, min(len(self.memory), self.batch_size))

        observation = np.zeros((self.batch_size, self.env.n_observations))
        next_observation = np.zeros((self.batch_size, self.env.n_observations))
        action, reward, done = [], [], []

        for i in range(self.batch_size):
            observation[i] = minibatch[i][0]
            action.append(minibatch[i][1])
            reward.append(minibatch[i][2])
            next_observation[i] = minibatch[i][3]
            done.append(minibatch[i][4])

        target = self.q_network(observation, training=False).numpy()
        target_next = self.q_network(next_observation, training=False).numpy()

        for i in range(self.batch_size):
            if done[i]:
                target[i][action[i]] = reward[i]
            else:
                target[i][action[i]] = reward[i] + self.gamma * np.amax(target_next[i]) #Bellman equation

        # Train the Q-network
        self.q_network.fit(observation, target, batch_size=self.batch_size, verbose=0)

    def load(self, name):
        self.strategy_network = load_model(name)

    def save(self, name):
        print(f"Saving trained model as racer-{name}.h5")
        self.strategy_network.save(f"racer-{name}.h5")

    def run(self):
        for e in range(self.EPISODES):
            observation = self.env.reset()
            observation = np.reshape(observation, [1, self.env.n_observations])
            done = False
            epsReward = 0
            while not done:
                action = self.get_action(observation)

                next_observation, reward, done, info = self.env.step(action)
                next_observation = np.reshape(next_observation, [1, self.env.n_observations])

                epsReward += reward
                self.remember(observation, action, reward, next_observation, done)
                observation = next_observation

                if done:
                    print(f"episode: {e}/{self.EPISODES}, score: {epsReward}, eps: {self.epsilon}")
                    self.points_history.append(epsReward)
                    if epsReward >= 1200:
                        self.save("kaka")
            self.train()
            self.reduce_eps()

            if e % 15 == 0:
                self.copy_weights()

            if e % 50 == 0:
                self.mean_point_history.append(np.mean(self.points_history))
                self.points_history = []

    def test(self, name):
        self.load(f"racer-{name}.h5")
        done = False
        observation = self.env.reset()
        observation = np.reshape(observation, [1, self.env.n_observations])
        while not done:
            self.env.render()
            action = self.get_action(observation)
            observation, reward, done, info = self.env.step(action)
            observation = np.reshape(observation, [1, self.env.n_observations])

if __name__ == "__main__":
    agent = DQNAgent() 
    agent.run()
    agent.save("kaka")
    plt.plot([i for i in range(len(agent.mean_point_history))], agent.mean_point_history)
    plt.ylabel("points")
    plt.xlabel("epochs (x50)")
    plt.show()