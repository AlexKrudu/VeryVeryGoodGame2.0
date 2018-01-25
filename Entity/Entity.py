import pygame
import brd
pygame.init()
running = True
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y,  image):
        pygame.sprite.Sprite.__init__(self)
        self.img = image
        self.image = pygame.image.load("images/"+self.img+'.png')
        self.Rect = self.image.get_rect()
        self.Rect.left, self.Rect.top = (x, y)
        self.x = x
        self.y = y
        self.inventory = ["x", "x", "r"]
        self.board = brd.Board(5, 5, self.inventory)
        self.collision = False
        self.collided = False
        self.pressed = False
        self.usable = False
        self.colliseable = False
        self.showInventory = False
        self.In_rect = None

    def get_event(self, event, player):
        if event.type == pygame.MOUSEMOTION:
            self.collided = self.Rect.collidepoint(event.pos)
            if self.collided:
                self.image = pygame.image.load("images/"+self.img+"F.png")
            else:
                self.image = pygame.image.load("images/" + self.img + '.png')
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.Rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.pressed:
                self.showInventory = True
            elif self.showInventory and not self.In_rect.collidepoint(event.pos):
                self.showInventory = False
            elif self.showInventory and self.In_rect.collidepoint(event.pos):
                thing = 'x'
                t = self.board.get_click((event.pos[0]-self.Rect.x+self.In_rect.width, event.pos[1]-self.Rect.y+self.In_rect.height), thing)
                player.add_to_inventory(t)
            self.pressed = False



    def render(self, surface):
        screen.blit(self.image, self.Rect)
        if self.showInventory:
            inv = self.board.render()
            r = inv.get_rect()
            screen.blit(inv, (self.x-r.width, self.y-r.height))
            self.In_rect = pygame.Rect(self.x-r.width, self.y-r.height, r.width, r.height)





table = Entity(100, 100, "table")
table1 = Entity(300, 300, "table")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        table.get_event(event)
        table1.get_event(event)
    screen.fill((0, 0, 0))
    table.render()
    table1.render()


    pygame.display.flip()

pygame.quit()