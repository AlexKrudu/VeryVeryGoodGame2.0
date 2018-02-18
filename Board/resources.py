import pygame

WIN_WIDTH = 1280
WIN_HEIGHT = 720
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

screen = pygame.display.set_mode(DISPLAY)

player_steps = pygame.mixer.Sound('music/steps.ogg')
player_steps1 = pygame.mixer.Sound('music/steps1.ogg')
speech = [pygame.mixer.Sound('music/speech-entrant.wav'),
          pygame.mixer.Sound('music/speech-inspector.wav'),
          pygame.mixer.Sound('music/speech-out.wav')]
scream = pygame.mixer.Sound('music/scream.ogg')
player_img = pygame.image.load("images/player.png").convert_alpha()
player_img.set_colorkey(pygame.Color("white"))
wall1 = pygame.image.load("images/wall1.png").convert()
wall2 = pygame.image.load("images/wall2.png").convert()
wall3 = pygame.image.load("images/wall3.png").convert()
wall4 = pygame.image.load("images/wall4.png").convert()
wall6 = pygame.image.load("images/wall6.png").convert()
wall7 = pygame.image.load("images/wall7.png").convert()
wall8 = pygame.image.load("images/wall8.png").convert()
roof = pygame.image.load("images/roof.png").convert_alpha()
ladder = pygame.image.load("images/ladder.png").convert_alpha()
bg = pygame.image.load("images/back.png").convert()
candle = pygame.image.load("images/candle.png").convert_alpha()
lom = pygame.image.load("images/lom.png").convert_alpha()
key = pygame.image.load("images/c.png").convert_alpha()
key2 = pygame.image.load("images/d.png").convert_alpha()
paper = pygame.image.load("images/v.png").convert_alpha()
bag = pygame.image.load("images/p.png").convert_alpha()
guitar = pygame.image.load("images/g.png").convert_alpha()
john_image = pygame.image.load("images/john.png").convert_alpha()
jane_image = pygame.image.load("images/jane.png").convert_alpha()
tom_image = pygame.image.load("images/tom.png").convert_alpha()
pl_face = pygame.image.load("images/player_face.png").convert_alpha()
tom_death_image = pygame.image.load("images/tom_death.png").convert_alpha()
win_img = pygame.image.load("images/win.png").convert()
begin_img = pygame.image.load("images/begin.png").convert()

ladder_group = pygame.sprite.Group()
SCALE = 16
DELTA = 240


