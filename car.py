import pygame
from physics import Rigidbody
from pygame.sprite import Sprite

class Car(Sprite):
  def __init__(self, car_position, image):
    super().__init__()
    self.vel = 120
    self.rigidbody = Rigidbody(car_position.x, car_position.y, self.vel, car_position.angle)
    self.rigidbody.setRotation(car_position.angle)
    self.width = 100
    self.height = 50
    self.maxRotation = 18
    self.image = pygame.image.load(image)
    self.image = pygame.transform.scale(self.image, (self.height, self.width))
    self.mask = pygame.mask.from_surface(self.image)
    self.width = self.image.get_width()
    self.height = self.image.get_height()
    self.rect = self.image.get_rect()
    self.rotatedImage = None


  def draw(self, window):
    self.updateImage()
    window.blit(self.rotatedImage, self.rect)

    olist = self.mask.outline()
    pygame.draw.lines(window, (200, 150, 150), 1, olist)

  def updateImage(self):
    self.rotatedImage = pygame.transform.rotate(self.image, -self.rigidbody.getRotation() + 90) #image is rotated 90 degrees
    self.rect = self.rotatedImage.get_rect(center=self.image.get_rect(topleft=(self.rigidbody.x, self.rigidbody.y)).center)
    self.mask = pygame.mask.from_surface(self.rotatedImage)

  def update(self, action, dt):
    self.updateImage()
    self.rigidbody.movePositions(dt)

    if (action == 0):
      self.rigidbody.rotate(-self.maxRotation)
    elif (action == 1):
      self.rigidbody.rotate(self.maxRotation)

  def getAction(self):
    # if (pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]):
    #   return 0

    if (pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]):
      return 0
    elif (pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]):
      return 1
      
class StartPositions:
  def __init__(self, x, y, angle, lineNumber):
    self.x = x
    self.y = y
    self.angle = angle
    self.lineNumber = lineNumber