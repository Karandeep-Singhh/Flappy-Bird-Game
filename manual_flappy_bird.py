import pygame
import os
import random
pygame.init()
WIDTH, HEIGHT = 500,680
win = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
WHITE = (255,255,255)

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(
	os.path.join('imgs',"pipe.png")))
BIRD_IMG = [pygame.transform.scale2x(pygame.image.load(
	os.path.join('imgs','bird'+str(x)+'.png'))) for x in range(1,4)]
BG_IMG =  pygame.transform.scale(pygame.image.load(
	os.path.join('imgs',"bg.png")),(WIDTH,HEIGHT))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(
	os.path.join('imgs',"base.png")))


STARTER_FONT = pygame.font.SysFont('comicsans', 40)
POINTS = pygame.font.SysFont('comicsans', 30)

class Bird:

	MAX_ROTATION = 25
	IMGS = BIRD_IMG
	ROT_VEL = 20
	ANIMATION_TIME = 5

	def __init__(self,x,y):

		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.img = self.IMGS[0]

	def jump(self):

		self.vel = -8.5
		self.tick_count = 0
		self.height = self.y

	def move(self):

		self.tick_count += 1

		displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2

		if displacement >=9.5:
			displacement = 9.5

		if displacement < 0:
			displacement -= 5

		self.y = self.y + displacement

		if displacement < 0 or self.y < self.height + 50:
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION
		else:
			if self.tilt > -90:
				self.tilt -=self.ROT_VEL

	def draw(self,win):
 
		self.img_count += 1

		if self.img_count <= self.ANIMATION_TIME:
			self.img = self.IMGS[0]
		elif self.img_count <= self.ANIMATION_TIME*2:
			self.img = self.IMGS[1]
		elif self.img_count <= self.ANIMATION_TIME*3:
			self.img = self.IMGS[2]
		elif self.img_count == self.ANIMATION_TIME*4 + 1:
			self.img = self.IMGS[0]
			self.img_count = 0

		if self.tilt <=-80:
			self.img = self.IMGS[1]
			self.img_count = self.ANIMATION_TIME*2

		rotated_img = pygame.transform.rotate(self.img, self.tilt)
		new_rect = rotated_img.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
		win.blit(rotated_img,new_rect.topleft)
        #blitRotateCenter(win,self.img,(self.x,self.y),self.tilt)
	
	def get_mask(self):
		return pygame.mask.from_surface(self.img)

class Pipe:
	GAP = 200

	def __init__(self,x,MOTION):
		self.x = x
		self.height = 0
		self.VEL = MOTION
		self.top = 0
		self.bottom = 0
		self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
		self.PIPE_BOTTOM = PIPE_IMG

		self.passed = False
		self.set_height()

	def set_height(self):

		self.height = random.randrange(50,250)
		self.top = self.height - self.PIPE_TOP.get_height()
		self.bottom = self.height + self.GAP

	def move(self):
		self.x -= self.VEL

	def draw(self,win):

		win.blit(self.PIPE_TOP, (self.x,self.top))
		win.blit(self.PIPE_BOTTOM, (self.x,self.bottom))

	def collide(self,bird):

		bird_mask = bird.get_mask()
		top_mask = pygame.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

		# i don't exactly know how offset works

		top_offset = (self.x - bird.x,self.top - round(bird.y))
		bottom_offset = (self.x - bird.x,self.bottom - round(bird.y))

		b_point = bird_mask.overlap(bottom_mask,bottom_offset) # if the co-ordinate 'bottom_offset' exist in 'bottom_mask'
		t_point = bird_mask.overlap(top_mask,top_offset)

		if t_point or b_point:
			return True

		return False

class Base:
	WIDTH = BASE_IMG.get_width()
	IMG = BASE_IMG

	def __init__(self, y, MOTION):
		self.VEL = MOTION
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):

		self.x1 -= self.VEL
		self.x2 -= self.VEL

		if self.x1 + self.WIDTH < 0:
			self.x1 = self.x2 + self.WIDTH
		if self.x2 + self.WIDTH < 0:
			self.x2 = self.x1 + self.WIDTH

	def draw(self,win):

		win.blit(self.IMG,(self.x1,self.y))
		win.blit(self.IMG,(self.x2,self.y))




def draw_win(win,bird,pipes,base,score,start):
	
	win_font = STARTER_FONT.render("PRESS 'SPACE' TO START", 1, WHITE)


	draw_points = POINTS.render("Score : "+str(score), 1, WHITE)
	
	win.blit(BG_IMG,(0,0))
	for pipe in pipes:
		pipe.draw(win)
	
	base.draw(win)
	win.blit(draw_points, (WIDTH-draw_points.get_width()-10, 10))
	bird.draw(win)

	if not start:
		win.blit(win_font, (WIDTH/2-win_font.get_width()//2,HEIGHT/2 - win_font.get_height()//2))
	pygame.display.update()




def main():
	MOTION = 5
	bird = Bird(200, 200)
	pipes = [Pipe(520,MOTION)]
	base = Base(630,MOTION)
	run =True
	start = False
	score = 0
	clock = pygame.time.Clock()	
				
	while run:
		clock.tick(35)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()
				quit()
		
		#key = pygame.key.get_pressed()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					bird.jump()
					start = True

		add_pipe = False
		rem = []
		if start:
			for pipe in pipes:
				if pipe.collide(bird):
					run = False
					pygame.time.delay(2500)


				if pipe.x + PIPE_IMG.get_width() < 0:
					rem.append(pipe)

				if not pipe.passed and pipe.x < bird.x:
					pipe.passed = True
					add_pipe = True
				pipe.move()

			if add_pipe:
				score += 1
				if score%5==0 and score != 1:
					MOTION += 1
					
				pipes.append(Pipe(520,MOTION))

			bird.move()

		if bird.y > base.y:
			run = False
			pygame.time.delay(2000)

		

		base.move()

		draw_win(win,bird,pipes,base,score,start)


	
	main()
main()
