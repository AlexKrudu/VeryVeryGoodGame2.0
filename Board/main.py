# Импортируем библиотеку pygame
import pygame
import brd

# Объявляем переменные
WIN_WIDTH = 1280  # Ширина создаваемого окна
WIN_HEIGHT = 720# Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
#BACKGROUND_COLOR = "darkblue"
SCALE = 16
DELTA = 240

on_ladder = False
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
#подгружаем текстуры, которые не будут меняться)
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
pl_face = pygame.image.load("images/player_face.png").convert_alpha()

class Wall:
    def __init__(self, x, y):
        self.id = 1
        self.width = SCALE
        self.height = SCALE
        self.x = x
        self.y = y
        self.color = pygame.Color("black")

    def render(self, surf):
        s = pygame.Surface((self.width, self.height))
        pygame.draw.rect(s, self.color, (0, 0, self.width, self.height))
        surf.blit(s, (self.x, self.y))


class Ladder:
    def __init__(self, x, y):
        self.id = 2
        self.width = SCALE
        self.height = SCALE
        self.image = ladder
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.color = pygame.Color("orange")


    def on_click(self, player):
        player.on_ladder = True

    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.stage = 1
        self.on_bottom_ladder = False
        self.on_top_ladder = False
        self.on_ladder = False
        self.moving = False
        self.move_speed = 1
        self.id = 2
        self.width = 30
        self.height = 64
        self.current_speed = 0
        self.default_x = x
        self.default_y = y
        self.mouse_pos = 0
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color("#888888"))
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.inventory = []
        self.showInventory = False
        self.board = brd.Board(5, 5, self.inventory)
        self.In_rect = pygame.Rect(WIN_WIDTH - self.board.render().get_rect().width, 0, self.board.render().get_rect().width, self.board.render().get_rect().height)

    def move(self, mouse_pos):
        self.mouse_pos = mouse_pos
        if self.mouse_pos > self.rect.x:
            self.current_speed = self.move_speed

        if self.mouse_pos < self.rect.x:
            self.current_speed = -self.move_speed

        if self.mouse_pos == self.rect.x:
            self.moving = False
            self.current_speed = 0
            return False

        self.rect.x += self.current_speed
        return True

    def move_ladder(self, height):
        self.image = pygame.Surface((0, 0))
        if self.on_bottom_ladder:
            if self.rect.y > height:
                self.rect.y -= self.move_speed
                return False
            if self.rect.y == height:
                self.stage += 1
                self.image = pygame.Surface((self.width, self.height))
                return True
        else:
            if self.rect.y < height:
                self.rect.y += self.move_speed
                return False
            if self.rect.y == height:
                self.stage -= 1
                self.image = pygame.Surface((self.width, self.height))
                self.image.fill(pygame.Color("#888888"))
                return True


    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.showInventory:
            inv = self.board.render()
            screen.blit(inv, (self.In_rect.x, self.In_rect.y))

class NPC(pygame.sprite.Sprite):
    def __init__(self, x, y, name, image, dialogs):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.to_go = x
        self.name = name
        self.move_speed = 1
        self.image = pygame.image.load("images/john.png").convert_alpha()
        self.face = pygame.image.load("images/johnF.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (x, y)
        self.moving = False
        self.level = 0
        self.dialogs = dialogs
        self.text = None
        self.text_player = None
        self.face_player = pl_face
        self.font = pygame.font.Font(None, 20)

    def get_event(self, event, player):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.rect.collidepoint(event.pos):
            for i in range(len(player.board.board)):
                if self.dialogs[self.level][3] in player.board.board[i] or not self.dialogs[self.level][3]:
                    if self.dialogs[self.level][3]:
                        player.board.board[i][player.board.board[i].index(self.dialogs[self.level][3])] = 0
                    self.text = self.font.render(self.dialogs[self.level][0], 1,  pygame.Color("black"), pygame.SRCALPHA)
                    if self.dialogs[self.level][2]:
                        self.text_player = self.font.render(self.dialogs[self.level][2], 1, pygame.Color("black"), pygame.SRCALPHA)
                    if self.level != len(self.dialogs)-1:

                        self.level+=1

                    if len(self.dialogs[self.level])== 5:
                        f = False
                        for i in range(len(player.board.board)):
                            if 0 in player.board.board[i]:
                                player.board.board[i][player.board.board[i].index(0)] = self.dialogs[self.level][4]
                                f = True
                                break
                        if not f:
                            self.text = self.font.render("Освободите свой инвентарь.", 1, pygame.Color("black"),
                                                         pygame.SRCALPHA)
                    text = self.text
                    text_pl = self.text_player
                    self.text = None
                    self.text_player = None
                    if text_pl:
                        return [(text, self.face), (text_pl, self.face_player)]
                    else:
                        return  [(text, self.face)]
            self.text = self.font.render(self.dialogs[self.level][1], 1, pygame.Color("black"), pygame.SRCALPHA)
            text = self.text
            self.text = None
            return [(text, self.face)]

    def move(self):
        if self.to_go-self.rect.width > self.x:
            self.x += 1
            self.rect.x+=1

        elif self.to_go < self.x:
            self.x -= 1
            self.rect.x -= 1

        else:
            self.to_go = self.x

            self.moving = False
    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))




class DialogBox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dialogs = []

    def update(self, dialog):
        if dialog:
            for i in dialog:
                if len(self.dialogs) == 3:
                    self.dialogs.pop(0)
                    self.dialogs.append(i)
                else:
                    self.dialogs.append(i)

    def render(self, surface):
        count = 0
        for i in self.dialogs:
            surface.blit(i[1], (self.x, self.y+count))
            rendered_rect = i[0].get_rect(x=self.x+50, y=self.y+count)
            surface.blit(i[0], rendered_rect)
            count +=50


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
        if event.type == pygame.MOUSEMOTION:
            was_collided = self.collided
            self.collided = self.Rect.collidepoint(event.pos)
            if self.collided:
                self.image = pygame.image.load("images/" + self.img + "F.png").convert_alpha()
            else:
                self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.Rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.Rect.colliderect(player.rect):
            if self.pressed:
                self.showInventory = True
                player.showInventory = True

            elif self.showInventory and not self.In_rect.collidepoint(event.pos) and not player.In_rect.collidepoint(event.pos):
                self.showInventory = False
                player.showInventory = False
                self.thing = None
            elif self.showInventory and player.In_rect.collidepoint(event.pos):

                self.thing = player.board.get_click((event.pos[0] - player.rect.x + player.In_rect.width,
                                                     event.pos[1] - player.rect.y + player.In_rect.height), self.thing)
                if self.thing:
                    f = True
                    for i in range(len(self.board.board)):
                        for j in range(len(self.board.board[i])):
                            if self.board.board[i][j] == 0:
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
                        if player.board.board[i][j] == 0:
                            f = True
                            break
                    if f:
                        break
                if f:
                    self.thing = self.board.get_click(
                    (event.pos[0] - self.Rect.x + self.In_rect.width, event.pos[1] - self.Rect.y + self.In_rect.height),
                    self.thing)
                    if self.thing:
                        f = False
                        for i in range(len(player.board.board)):
                            for j in range(len(player.board.board[i])):
                                if player.board.board[i][j] == 0:
                                    player.board.board[i][j] = self.thing
                                    f = True
                                    break
                            if f:
                                break
                        self.thing = None
            self.pressed = False

    def render(self, surface):
        surface.blit(self.image, self.Rect)
        if self.showInventory:
            inv = self.board.render()
            r = inv.get_rect()
            surface.blit(inv, (self.x - r.width, self.y - r.height))
            self.In_rect = pygame.Rect(self.x - r.width, self.y - r.height, r.width, r.height)

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
        elif event.type == pygame.MOUSEMOTION:
            was_collided = self.collided
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
                self.img += "O"
                self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)

            else:
                self.img = self.img[:-1]
                self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)
        else:
            f = False
            for i in range(len(player.board.board)):
                for j in range(len(player.board.board[i])):
                    if player.board.board[i][j] == self.key:
                        player.board.board[i][j] = 0
                        self.state = ~self.state
                        if self.state:
                            self.img += "O"
                            self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                            self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)
                            self.key = None
                            f = True

                        else:
                            self.img = self.img[:-1]
                            self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                            self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)
                            f = True

                if f:
                    break
            if self.npc:
                self.npc.to_go = self.Rect.x
                self.npc.moving = True

    def render(self, surface):
        if self.npc and (self.npc.rect.x == self.Rect.x - self.npc.rect.width or self.npc.rect.x == self.Rect.x) and not self.state and  self.npc_door:
            self.state = ~self.state
            self.img += "O"
            self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
            self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)
            self.key = None
            self.npc_door = False
        surface.blit(self.image, self.Rect)







class Map:
    def __init__(self):
        self.objects = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 30, 1, 1, 1, 1, 1, 1, 40, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 40, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 2, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 50, 1, 1, 1, 1, 1, 1, 60, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 30, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 2, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 30, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 30, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.npc = [NPC(232, 288 + DELTA, "h", "john",
                 [("Привет, проходи. У меня есть для тебя задание",
                   "",
                   "",
                   None),

                  ("Ты же знаешь, что 3 квартира давно заброшена? Недавно я нашел ключи от нее. Но я боюсь туда зайти. Я до ужаса боюсь крыс. Я слышу по ночам там шуршание.",
                   '',
                   "",
                   None),

                  ("Ты не мог бы осмотреть комнату за меня? можешь забрать что-нибудь оттуда. Я дам тебе ключи, но перед этим, ты можешь принести свечу, уж больно темновато тут.",
                   "",
                   "Да, конечно",
                   None),

                  ("Спасибо, Но не мог бы ты найти свечу, без нее мне не найти ключа",
                   "",
                   "",
                   None),

                  ("Отлично, Вот, держи",
                   "Без свечки я не найду ключа",
                   "",
                   "x"),

                  ("Вот это да!",
                   "Я не вижу у тебя за спиной мешок!",
                   "",
                   "r"),

                  ("Слушай, я знаю, что ты хочешь сбежать.",
                   "",
                   "",
                   None),

                    ("Джейн из 2 квартиры живет тут больше всех. Я думаю если ты подаришь ей что нибудь, то она может тебе помочь.",
                     "",
                     "А что она любит? Может в этом барахле найдется что-нибудь",
                     None),

                  ("Я знаю, она любит музыку.Ты можешь дать ей что-нибудь и разговорить ее.",
                   "",
                   "Хорошо, я подумаю",
                   None,
                   'r'),

                  ("Удачи",
                   "",
                   "",
                   None)


                  ]), NPC(640, 288 + DELTA, "h", "john",
                 [("Привет, есть свечка?", "Спасибо", "x"), ("Я думаю тебе стоит пойти вниз", '', None)])]
        self.obj = []
        self.obj1 = []
        x = 0
        y = 0
        for i in range(len(self.objects)):
            self.obj.append(
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],)
            for j in range(len(self.objects[i])):
                if self.objects[i][j] == 3:
                    obj = Entity(x, y + DELTA, "shelf",  [])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 4:
                    obj = Entity(x, y + DELTA, "bed1", [])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 5:
                    obj = Entity(x, y + DELTA, "bed", [])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 6:
                    obj = Entity(x, y + DELTA, "table1", [])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 7:
                    obj = Entity(x, y + DELTA, "bed2", ["r", "x", "x"])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 8:
                    obj = Entity(x, y + DELTA, "shelf1", ["r", "x", "x"])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 9:
                    obj = Entity(x, y + DELTA, "comp", ["r", "x", "x"])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 2:
                    obj = Ladder(x, y+DELTA)
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 40:
                    obj = Door(x, y + DELTA, "Door1")
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 30:
                    obj = Door(x, y + DELTA, "Door1", "x")
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 50:
                    obj = Door(x, y + DELTA, "Door1", "x", self.npc[0])
                    self.obj1.append(obj)
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 60:
                    print(1)
                    obj = Door(x, y + DELTA, "Door1", "x", self.npc[1])
                    self.obj1.append(obj)
                    self.obj[i][j] = obj
                x += SCALE
            y += SCALE
            x = 0
    def render(self, screen):
        x = 0
        y = 0
        for i in range(len(self.objects)):
            for j in range(len(self.objects[i])):
                if self.objects[i][j] == 1:
                    obj = (Wall(x, y+DELTA))
                    surf = pygame.Surface((obj.width, obj.height))
                    surf.fill(obj.color)
                    screen.blit(surf, (x, y + DELTA))
                elif self.objects[i][j] == 2:
                    self.obj[i][j].render(screen)
                elif self.objects[i][j] == 10:
                    screen.blit(wall2, (x, y + DELTA))
                elif self.objects[i][j] == 11:
                    screen.blit(wall1, (x, y + DELTA))
                elif self.objects[i][j] == 12:
                    screen.blit(wall3, (x, y + DELTA))
                elif self.objects[i][j] == 13:
                    screen.blit(wall4, (x, y + DELTA))
                elif self.objects[i][j] == 14:
                    screen.blit(wall6, (x, y + DELTA))
                elif self.objects[i][j] == 15:
                    screen.blit(wall7, (x, y + DELTA))
                elif self.objects[i][j] == 16:
                    screen.blit(wall8, (x, y + DELTA))
                elif self.objects[i][j] == 20:
                    screen.blit(roof, (x, y + DELTA))
                x += SCALE
            y += SCALE
            x = 0

            for k in self.obj:
                for p in k:
                    if p and type(p) not in [Ladder, Wall] :
                        p.render(screen)

            for k in self.npc:
                k.render(screen)




def main():
    running = True

    pygame.display.set_caption("VeryVeryGoodGame2.0")  # Пишем в шапку
    # будем использовать как фон
    #screen.fill(pygame.Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    screen.blit(bg, (0, 0))
    player = Player(16, 720-64-16)
    player.draw(screen)
    map = Map()
    map.render(screen)

    dialog = DialogBox(50, 10)
    while running:  # Основной цикл программы
        screen.blit(bg, (0, 0))
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == pygame.QUIT:
                running = False

            for i in range(len(map.objects)):
                for j in range(len(map.objects[i])):
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                        y = len(map.objects) - 1 - player.stage * 7
                        flag = False
                        for k in range(len(map.objects[y])):
                            if map.objects[y][k] in [30, 40, 50, 60] and map.objects[y][k] != map.objects[i][j]:
                                if map.obj[y][k].Rect.collidepoint(e.pos):
                                    flag = True
                                if e.pos[0] < player.rect.x:
                                    if e.pos[0] <= map.obj[y][k].Rect.x + map.obj[y][k].Rect.width <= player.rect.x and \
                                                    map.obj[y][k].state == False:
                                        flag = True
                                else:
                                    if player.rect.x <= map.obj[y][k].Rect.x <= e.pos[0] and map.obj[y][
                                        k].state == False:
                                        flag = True
                        if not flag:
                            if map.objects[i][j] == 2:
                                if map.obj[i][j].rect.collidepoint(e.pos) and not player.on_ladder:
                                    player.moving = True
                                    player.move(e.pos[0])

                                    if e.pos[1] <= player.rect.y + player.rect.height:
                                        height = player.rect.y + player.rect.height - 160 - SCALE
                                        player.on_bottom_ladder = True
                                    else:
                                        player.on_top_ladder = True
                                        height = player.rect.y - player.rect.height + 160 + SCALE
                                    player.on_ladder = True
                            if map.objects[i][j] in [3, 4, 5, 6, 7, 8, 9, 30, 40, 50, 60]:
                                if map.obj[i][j].Rect.collidepoint(e.pos):
                                    player.moving = True
                                    if e.pos[0] > player.rect.x:
                                        player.move(e.pos[0] - player.rect.width)
                                    else:
                                        player.move(e.pos[0] + player.rect.width // 2)
                    if map.objects[i][j] in [3, 4, 5, 6, 7, 8, 9]:
                        map.obj[i][j].get_event(e, player)
                    if map.objects[i][j] in [30, 40, 50, 60]:
                        map.obj[i][j].get_event(e, player)



            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3 and not (player.on_bottom_ladder or player.on_top_ladder):
                y = len(map.objects) - 1 - player.stage*7
                flag = False
                for i in range(len(map.objects[y])):
                    if map.objects[y][i]in [30, 40, 50, 60]:
                        if map.obj[y][i].Rect.collidepoint(e.pos):
                            flag = True
                        if e.pos[0] < player.rect.x:
                            if e.pos[0] <= map.obj[y][i].Rect.x +  map.obj[y][i].Rect.width <= player.rect.x and map.obj[y][i].state == False:
                                flag = True
                        else:
                            if player.rect.x <= map.obj[y][i].Rect.x <= e.pos[0] and map.obj[y][i].state == False:
                                flag = True
                    elif map.objects[y+1][i] == 1:
                        if e.pos[0] < player.rect.x:
                            if e.pos[0] <= i*SCALE  <= player.rect.x:
                                flag = True
                        else:
                            if player.rect.x <= i*SCALE  <= e.pos[0]:
                                flag = True
                if not flag:
                    player.moving = True
                    player.move(e.pos[0])
            if e.type == pygame.KEYDOWN and e.key == pygame.K_TAB:
                player.showInventory = ~player.showInventory
            for l in map.npc:
                dialog.update(l.get_event(e, player))
        if (player.on_bottom_ladder or player.on_top_ladder) and not player.moving:
            if player.move_ladder(height):
                player.on_bottom_ladder = False
                player.on_top_ladder = False
                player.on_ladder = False

        if player.moving:
            player.move(player.mouse_pos)


        map.render(screen)
        dialog.render(screen)
        for l in map.obj1:
            l.get_event(None, player)
        player.draw(screen)
        clock.tick(60)
        print(clock.get_fps())
        pygame.display.flip()


if __name__ == "__main__":
    main()
