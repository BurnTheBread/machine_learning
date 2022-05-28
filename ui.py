import pygame
import math

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class TextBox:
	def __init__(self, x, y, text, color=WHITE, width=0, font=0):
		self.x = x
		self.y = y
		self.color = color
		self.text = text
		if width:
			self.width = width
			self.calcOptimalFontSize()
			self.height = self.heightByFont(self.font)
		if font:
			self.font = self.getFontBySize(font)
			self.width = self.widthByFont(self.font)
			self.height = self.heightByFont(self.font)


	def getFontBySize(self, size):
		return pygame.font.Font('Resources/font.ttf', size)

	def widthByFont(self, font):
		return pygame.font.Font.size(font, self.text)[0]

	def heightByFont(self, font):
		return pygame.font.Font.size(font, self.text)[1]

	def calcOptimalFontSize(self):
		smallSize = pygame.font.Font.size(self.getFontBySize(10), self.text)
		bigSize = pygame.font.Font.size(self.getFontBySize(110), self.text)

		#find best for width
		deltaWidth = (bigSize[0] - smallSize[0]) / 100
		bestWidthFont = self.width / deltaWidth

		self.font = self.getFontBySize(math.floor(bestWidthFont))
	
	def changeText(self, text):
		self.text = text
		self.calcOptimalFontSize()

	def update(self):
		pass

	def draw(self, screen):
		self.update()
		screen.blit(self.font.render(self.text, True, self.color), (self.x, self.y))

class TextButton:
	def __init__(self, x, y, width, text = "", transparent = False, defaultColor = (10, 10, 10), selectColor = (45, 45, 45), pressedColor = (95, 95, 95)):
		self.x = x
		self.y = y
		self.width = width
		self.text = text
		self.textBox = TextBox(self.x, self.y, self.text, width=self.width)
		self.height = self.textBox.height
		self.defaultColor = defaultColor
		self.selectColor = selectColor
		self.pressedColor = pressedColor
		self.color = self.defaultColor
		self.isPressed = False
		self.transparent = transparent

	def draw(self, screen):
		if(not self.transparent):
			pygame.draw.rect(screen, self.color, [self.x-10, self.y-10, self.width+10, self.height+10])
		self.textBox.draw(screen)

	def update(self):
		self.color = self.defaultColor
		if(pygame.mouse.get_pos()[0] >= self.x and pygame.mouse.get_pos()[0] <= self.x + self.width): #border check x-axis
			if(pygame.mouse.get_pos()[1] >= self.y and pygame.mouse.get_pos()[1] <= self.y + self.height):
				if(pygame.mouse.get_pressed()[0]):
					self.color = self.pressedColor
					if(not self.isPressed):
						self.pressed()
					self.isPressed = True
				else:
					self.color = self.selectColor
					self.isPressed = False

	def pressed(self):
		pass

class ImageButton:
	def __init__(self, x, y, imageAdress, width=0):
		self.x = x
		self.y = y
		self.image = pygame.image.load(imageAdress)
		if width:
			self.image = pygame.transform.scale(self.image, (width, int(width * self.image.get_height() / self.image.get_width()))) #lineair rescale of image to height
		self.width = self.image.get_width()
		self.height = self.image.get_width()
		self.isPressed = False

	def draw(self, screen):
		screen.blit(self.image, (self.x, self.y))

	def update(self):
		if(pygame.mouse.get_pos()[0] >= self.x and pygame.mouse.get_pos()[0] <= self.x + self.width): #border check x-axis
			if(pygame.mouse.get_pos()[1] >= self.y and pygame.mouse.get_pos()[1] <= self.y + self.height):
				if(pygame.mouse.get_pressed()[0]):
					if(not self.isPressed):
						self.pressed()
					self.isPressed = True
				else:
					self.isPressed = False

	def pressed(self):
		pass
