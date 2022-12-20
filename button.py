import pygame

#button class
class Button():
	def __init__(self, x, y, image_off, image_on, scale):
		width = image_on.get_width()
		height = image_on.get_height()
		self.image_on = pygame.transform.scale(image_on, (int(width * scale), int(height * scale)))
		width = image_off.get_width()
		height = image_off.get_height()
		self.image_off = pygame.transform.scale(image_off, (int(width * scale), int(height * scale)))
		self.rect = self.image_on.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface, status: bool):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		if status:
			surface.blit(self.image_on, (self.rect.x, self.rect.y))
		else:
			surface.blit(self.image_off, (self.rect.x, self.rect.y))

		return action