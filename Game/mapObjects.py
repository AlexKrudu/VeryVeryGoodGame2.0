import pygame
import brd
from resources import *



class Wall:
    def __init__(self, x, y):
        self.id = 1
        self.width = SCALE
        self.height = SCALE
        self.x = x
        self.y = y
        self.Rect = pygame.Rect(x, y, SCALE, SCALE)
        self.color = pygame.Color("black")

    def render(self, surf):
        s = pygame.Surface((self.width, self.height))
        pygame.draw.rect(s, self.color, (0, 0, self.width, self.height))
        surf.blit(s, self.Rect)


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.id = 2
        self.width = SCALE
        self.height = SCALE
        self.image = ladder
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.add(ladder_group)

    def on_click(self, player):
        player.on_ladder = True

    def render(self, surface):
        surface.blit(self.image, self.rect)


class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image, inventory):
        pygame.sprite.Sprite.__init__(self)
        self.img = image
        self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
        self.Rect = self.image.get_rect()
        self.Rect.left, self.Rect.top = (x, y)
        self.x = x
        self.y = y
        self.inventory = inventory
        self.board = brd.Board(5, 5, self.inventory)
        self.collision = False
        self.collided = False
        self.pressed = False
        self.usable = False
        self.colliseable = False
        self.showInventory = False
        self.In_rect = None
        self.thing = None

    def get_event(self, event, player):
        if not player.rect.colliderect(self.Rect) and self.showInventory:
            table_closed.play()
            self.showInventory = False
            player.showInventory = False
        if event.type == pygame.MOUSEMOTION:
            self.collided = self.Rect.collidepoint(event.pos)
            if self.collided:
                self.image = pygame.image.load("images/" + self.img + "F.png").convert_alpha()
            else:
                self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.Rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.Rect.colliderect(player.rect):

            if self.pressed:
                table_opened.play()
                self.showInventory = True
                player.showInventory = True

            elif self.showInventory and not self.In_rect.collidepoint(event.pos) and not player.In_rect.collidepoint(event.pos):
                table_closed.play()
                self.showInventory = False
                player.showInventory = False
                self.thing = None
            elif self.showInventory and player.In_rect.collidepoint(event.pos):
                self.thing = player.board.get_click((event.pos[0]-player.In_rect.x,
                                                     event.pos[1]-player.In_rect.y), self.thing)
                if self.thing:
                    f = True
                    for i in range(len(self.board.board)):
                        for j in range(len(self.board.board[i])):
                            if not self.board.board[i][j]:
                                self.board.board[i][j] = self.thing
                                f = False
                                break
                        if not f:
                            break
                self.thing = None
            elif self.showInventory and self.In_rect.collidepoint(event.pos):
                f = False
                for i in range(len(player.board.board)):
                    for j in range(len(player.board.board[i])):
                        if not  player.board.board[i][j]:
                            f = True
                            p = (i, j)
                            break
                    if f:
                        break
                if f:
                    self.thing = self.board.get_click(
                    (event.pos[0] - (WIN_WIDTH - self.In_rect.width), event.pos[1] - self.In_rect.y),
                    self.thing)
                    if self.thing:
                        player.board.board[p[0]][p[1]] = self.thing
                        self.thing = None
            self.pressed = False

    def render(self, surface):
        surface.blit(self.image, self.Rect)
        if self.showInventory:
            inv = self.board.render()
            r = inv.get_rect()
            self.In_rect = pygame.Rect(WIN_WIDTH - r.width, 300, r.width, r.height)
            surface.blit(inv, self.In_rect)


class Door(Entity):
    def __init__(self, x, y, image, key=None, npc=None):
        super().__init__(x,y,image, [])
        self.state = False
        self.key = key
        self.npc = npc
        self.npc_door = True

    def get_event(self, event, player):
        if not event:
            self.npc.move()
            #self.npc.moving = True
        elif event.type == pygame.MOUSEMOTION:
            self.collided = self.Rect.collidepoint(event.pos)
            if self.collided:
                self.image = pygame.image.load("images/" + self.img + "F.png").convert_alpha()
            else:
                self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and (self.Rect.colliderect(player.rect) or self.Rect.colliderect(pygame.Rect(player.rect.x-player.rect.width, player.rect.y, player.rect.width, player.rect.height))):
            if self.Rect.collidepoint(event.pos):
                self.change_state(player)


    def change_state(self, player):
        if not self.key:
            self.state = ~self.state
            if self.state:
                door_open.play()
                self.img += "O"
                self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)

            else:
                door_close.play()
                self.img = self.img[:-1]
                self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)
            return
        else:
            for i in range(len(player.board.board)):
                if self.key in player.board.board[i]:
                    player.board.board[i][player.board.board[i].index(self.key)] = 0
                    self.state = ~self.state
                    if self.state:
                        key_m.play()
                        door_open.play()
                        self.img += "O"
                        self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                        self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)
                        self.key = None

                    else:
                        door_close.play()
                        self.img = self.img[:-1]
                        self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                        self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)
                    return
            if self.npc:
                for i in range(len(player.board.board)):
                    if self.npc.dialogs[0][3] in player.board.board[i] or self.npc.dialogs[0][3] is None:
                        if self.npc.rect.x < self.Rect.x:
                            self.npc.to_go = self.Rect.x
                        else:
                            self.npc.to_go = self.Rect.x+self.Rect.w
                        return
        door_closed.play()


    def render(self, surface):
        if self.npc and (self.npc.rect.x == self.Rect.x + self.Rect.width or self.npc.rect.x+self.npc.rect.w == self.Rect.x) and not self.state and  self.npc_door:
            self.state = ~self.state
            door_open.play()
            self.img += "O"
            self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
            self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)
            self.key = None
            self.npc_door = False
        surface.blit(self.image, self.Rect)




