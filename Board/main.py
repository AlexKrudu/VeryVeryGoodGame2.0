# Импортируем библиотеку pygame
import pygame
import brd
import MainMenu

# Объявляем переменные
WIN_WIDTH = 1280  # Ширина создаваемого окна
WIN_HEIGHT = 720# Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
#BACKGROUND_COLOR = "darkblue"
SCALE = 16
DELTA = 240

on_ladder = False
pygame.init()
time = pygame.time
clock = pygame.time.Clock()
ladder_group = pygame.sprite.Group()
screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
#подгружаем текстуры, которые не будут меняться)
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


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
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
        self.add(ladder_group)


    def on_click(self, player):
        player.on_ladder = True

    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.left = False
        self.right = False
        self.stage = 3
        self.level = 1
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
        self.image = pygame.transform.scale(player_img.subsurface((530, 30, 50, 125)), (32, 64))
        #self.image.fill(pygame.Color("#888888"))
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.inventory = []
        self.showInventory = False
        self.board = brd.Board(5, 5, self.inventory)
        self.In_rect = pygame.Rect(WIN_WIDTH - self.board.render().get_rect().width, WIN_HEIGHT-self.board.render().get_rect().height, self.board.render().get_rect().width, self.board.render().get_rect().height)

    def move(self, mouse_pos):
        self.mouse_pos = mouse_pos
        if self.mouse_pos > self.rect.x:
            self.left = False
            self.right = True
            self.current_speed = self.move_speed

        if self.mouse_pos < self.rect.x:
            self.right = False
            self.left = True
            self.current_speed = -self.move_speed

        if self.mouse_pos == self.rect.x:
            self.right = False
            self.left = False
            self.moving = False
            self.current_speed = 0
            return False

        self.rect.x += self.current_speed
        return True

    def move_ladder(self, height):
        self.on_ladder = True
        if self.on_bottom_ladder:
            if self.rect.y > height:
                self.rect.y -= self.move_speed
                return False
            if self.rect.y == height:
                self.stage += 1
                self.on_ladder = False
                return True
        else:
            if self.rect.y < height:
                self.rect.y += self.move_speed
                return False
            if self.rect.y == height:
                self.stage -= 1
                self.on_ladder = False
                return True


    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.showInventory:
            inv = self.board.render()
            screen.blit(inv, (self.In_rect.x, self.In_rect.y))


class NPC(pygame.sprite.Sprite):
    d = {"john":john_image, "jane":jane_image, "tom":tom_image}

    def __init__(self, x, y, name, dialogs):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.to_go = x
        self.name = name
        self.move_speed = 1
        self.image = pygame.transform.scale(NPC.d[name].subsurface((0, 0, 50, 123)), (32, 64))
        self.face = pygame.image.load("images/"+name+"F.png").convert_alpha()
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
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.rect.collidepoint(event.pos) and self.rect.colliderect(player.rect):
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
        self.moving = True
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


class EnemyNPC(NPC):
    d = {"tom":tom_image}
    def __init__(self, x, y, name, dialogs):
        super().__init__( x, y, name, dialogs)
        self.die = False
        self.dead = False

    def get_event(self, event, player):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.rect.collidepoint(event.pos) and self.rect.colliderect(player.rect) and not self.die :
            for i in range(len(player.board.board)):
                if self.dialogs[self.level][3] in player.board.board[i] or not self.dialogs[self.level][3]:
                    if self.dialogs[self.level][3]:
                        player.board.board[i][player.board.board[i].index(self.dialogs[self.level][3])] = 0
                    self.text = self.font.render(self.dialogs[self.level][0], 1, pygame.Color("black"), pygame.SRCALPHA)
                    if self.dialogs[self.level][2]:
                        self.text_player = self.font.render(self.dialogs[self.level][2], 1, pygame.Color("black"),
                                                            pygame.SRCALPHA)
                    if self.level != len(self.dialogs) - 1:
                        self.level += 1
                    else:
                        self.die = True

                    text = self.text
                    text_pl = self.text_player
                    self.text = None
                    self.text_player = None
                    if text_pl:
                        return [(text, self.face), (text_pl, self.face_player)]
                    else:
                        return [(text, self.face)]
                self.text = self.font.render(self.dialogs[self.level][1], 1, pygame.Color("black"), pygame.SRCALPHA)
                text = self.text
                self.text = None
                return [(text, self.face)]


class DialogBox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dialogs = []
        self.image = pygame.image.load("images/dialog.png")

    def update(self, dialog):
        if dialog:
            for i in dialog:
                if len(self.dialogs) == 3:
                    self.dialogs.pop(0)
                    self.dialogs.append(i)
                else:
                    self.dialogs.append(i)

    def render(self, surface):
        surface.blit(self.image, (40, 0))
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
        if not player.rect.colliderect(self.Rect) and self.showInventory:
            self.showInventory = False
            player.showInventory = False
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
                    (event.pos[0] - self.Rect.x + self.In_rect.width, event.pos[1] - self.Rect.y + self.In_rect.height),
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
            surface.blit(inv, (self.x - r.width, self.y - r.height))
            self.In_rect = pygame.Rect(self.x - r.width, self.y - r.height, r.width, r.height)


class Animation:
    def __init__(self, sprites=None, time=100):
        self.sprites = sprites
        self.time = time
        self.work_time = 0
        self.skip_frame = 0
        self.frame = 0

    def update(self, dt):
        self.work_time += dt
        # Считаем сколько кадров надо перелистнуть
        self.skip_frame = self.work_time / self.time
        if self.skip_frame > 0:
            # Не забываем, что у нас, при смене кадров с частотой в
            # 100 мс, вполне могло уже пройти 133 мс, и важно не
            # забыть про эти 33 мс.
            self.work_time = self.work_time % self.time
            #self.frame += self.skip_frame
            self.frame += 1
            if self.frame >= len(self.sprites):
                self.frame = 0

    def get_sprite(self):
        return self.sprites[int(self.frame)]



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
                self.img += "O"
                self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)

            else:
                self.img = self.img[:-1]
                self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)
        else:

            for i in range(len(player.board.board)):
                if self.key in player.board.board[i]:
                    player.board.board[i][player.board.board[i].index(self.key)] = 0
                    self.state = ~self.state
                    if self.state:
                        self.img += "O"
                        self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                        self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)
                        self.key = None

                    else:
                        self.img = self.img[:-1]
                        self.image = pygame.image.load("images/" + self.img + '.png').convert_alpha()
                        self.Rect = pygame.Rect(self.Rect.x, self.Rect.y, self.image.get_rect().width, self.Rect.height)
                break
            if self.npc:
                for i in range(len(player.board.board)):
                    if self.npc.dialogs[0][3] in player.board.board[i] or self.npc.dialogs[0][3] is None:
                        if self.npc.rect.x < self.Rect.x:
                            self.npc.to_go = self.Rect.x
                        else:
                            self.npc.to_go = self.Rect.x+self.Rect.w
                        break
                #self.npc.moving = True

    def render(self, surface):
        if self.npc and (self.npc.rect.x == self.Rect.x + self.Rect.width or self.npc.rect.x+self.npc.rect.w == self.Rect.x) and not self.state and  self.npc_door:
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
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 50, 1, 1, 1, 1, 1, 1, 61, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 30, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 2, 0, 0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 71, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 91, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.npc = [NPC(232, 288 + DELTA, "john",
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

                  ("Отлично, где же этот ключ...",
                   "Без свечки я не найду ключа. Поищи у себя",
                   "",
                   "x",),

                  ("А, вот, держи",
                   "",
                   "",
                   None,
                   "c"),

                  ("Вот это да!",
                   "Я не вижу у тебя за спиной мешок!",
                   "",
                   "p"),

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
                   None),

                  ("Удачи",
                   "",
                   "",
                   None)


                  ]), NPC(640, 288 + DELTA, "jane",
                 [("А что это у тебя в руках?",
                   "Можно потише, у еня ребенок спит",
                   "",
                   "g"),

                  ("Если ты думаешь, что если я одинокая женщина с ребенком, то ты можешь взять меня простым подарком? Даже не думай",
                   "",
                   "Нет, подожди, ты должна мне помочь",
                   None),

                  ("Ну что еще?",
                   "",
                   "Я хочу сбежать оттуда, а единственный выход-через вахтера. Джон сказал мне, что ты знаешь как выйти отсюда",
                   None),

                  ("Ладно. Я знаю, что он в свое время занимал всокую должность при Большом Брате...",
                   "",
                   "И как он оказался здесь?",
                   None),

                  ("Он стал просто не нужен. И все. Самое интересное, что он не оставил своей любви к партии.",
                   "",
                   "Стой, ведь город захватили повстанцы? Как он остался жив?",
                   None),

                  ("Он не выходит из своей дыры уже месяц, даже представить не могу что он там делает.",
                   "",
                   "А если шантажировать его? Сказать, что если он не откроет дверь, то мы сдадим его?",
                   None),

                  ("Хорошая идея. Если честно, меня от него тошнит. И вот, покажи ему это. это досье на него.",
                   "",
                   "Хорошо. Тогда я пошел",
                   None,
                   "v"),

                  ("Я верю в тебя",
                   "",
                   "",
                   None)]),

                EnemyNPC(700, 400 + DELTA, "tom", [
                        ("Что это у тебя? Урод, а ну дай сюда",
                         "А ну пошел вон отсюда!",
                         "",
                         "v"),

                        ("Что тебе надо?",
                         "",
                         "Если ты сейчас же не откроешь мне дверь-этот листок увидят все. Что тут у нас: Политиче..",
                         None),

                        ("Нет! Стой! Я сам не знаю где ключ!",
                        "",
                        "Врешь! Я сейчас пройдусь ломом по твоей пустой башке, если ты не скажешь где ключ!",
                        None),


                        ("Аггггхххх",
                         "Ну давай, попробуй",
                         "",
                         "r")

                    ])
                    ]


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
                    obj = Entity(x, y + DELTA, "shelf",  ["g", "p"])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 4:
                    obj = Entity(x, y + DELTA, "bed1", [])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 5:
                    obj = Entity(x, y + DELTA, "bed", [])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 6:
                    obj = Entity(x, y + DELTA, "table1", ["r"])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 7:
                    obj = Entity(x, y + DELTA, "bed2", [])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 8:
                    obj = Entity(x, y + DELTA, "shelf1", ["d"])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 9:
                    obj = Entity(x, y + DELTA, "comp", ["x"])
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 2:
                    obj = Ladder(x, y+DELTA)
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 40:
                    obj = Door(x, y + DELTA, "Door1")
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 30:
                    obj = Door(x, y + DELTA, "Door1", "c")
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 31:
                    obj = Door(x, y + DELTA, "Door1", "c")
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 50:
                    obj = Door(x, y + DELTA, "Door1", "u", self.npc[0])
                    self.obj1.append(obj)
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 61:
                    obj = Door(x, y + DELTA, "Door1", "u", self.npc[1])
                    self.obj1.append(obj)
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 71:
                    obj = Door(x, y + DELTA, "Door1", "u", self.npc[2])
                    self.obj1.append(obj)
                    self.obj[i][j] = obj
                elif self.objects[i][j] == 91:
                    obj = Door(x, y + DELTA, "Door2", "d")
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

    anim = [pygame.transform.scale(player_img.subsurface((12, 31, 56, 124)), (32, 64)),pygame.transform.scale(player_img.subsurface((93, 31, 41, 124)), (26, 64)),
            pygame.transform.scale(player_img.subsurface((162, 31, 68 ,123)), (32, 64)), pygame.transform.scale(player_img.subsurface((252, 31, 61, 125)), (32, 64))]
    left_anim = [pygame.transform.scale(player_img.subsurface((478, 182, 56, 124)), (32, 64)),
            pygame.transform.scale(player_img.subsurface((404, 182, 41, 124)), (26, 64)),
            pygame.transform.scale(player_img.subsurface((316, 182, 68, 123)), (32, 64)),
            pygame.transform.scale(player_img.subsurface((233, 181, 61, 125)), (32, 64))]
    john_right_anim = [pygame.transform.scale(john_image.subsurface((50, 0, 50, 123)), (32, 64)),
            pygame.transform.scale(john_image.subsurface((100, 0, 50, 123)), (32, 64)),
            pygame.transform.scale(john_image.subsurface((150, 0, 50, 123)), (32, 64)),
            pygame.transform.scale(john_image.subsurface((200, 0, 50, 123)), (32, 64)),
            pygame.transform.scale(john_image.subsurface((250, 0, 45, 123)), (32, 64)),]
    jane_right_anim = [pygame.transform.scale(jane_image.subsurface((50, 0, 50, 123)), (32, 64)),
                       pygame.transform.scale(jane_image.subsurface((100, 0, 50, 123)), (32, 64)),
                       pygame.transform.scale(jane_image.subsurface((150, 0, 50, 123)), (32, 64)),
                       pygame.transform.scale(jane_image.subsurface((200, 0, 50, 123)), (32, 64)) ]
    tom_left_anim = [pygame.transform.scale(tom_image.subsurface((50, 0, 50, 123)), (32, 64)),
                     pygame.transform.scale(tom_image.subsurface((100, 0, 50, 123)), (32, 64)),
                     pygame.transform.scale(tom_image.subsurface((150, 0, 50, 123)), (32, 64)),
                     pygame.transform.scale(tom_image.subsurface((200, 0, 50, 123)), (32, 64)),
                     ]

    tom_die_anim = [pygame.transform.scale(tom_death_image.subsurface((0, 0, 50, 123)), (32, 64)),
                    pygame.transform.scale(tom_death_image.subsurface((50, 0, 50, 123)), (32, 64)),
                    pygame.transform.scale(tom_death_image.subsurface((100, 0, 50, 123)), (32, 64)),
                    pygame.transform.scale(tom_death_image.subsurface((150, 0, 50, 123)), (32, 64)),
                    pygame.transform.scale(tom_death_image.subsurface((200, 0, 50, 123)), (32, 64)),
                    pygame.transform.scale(tom_death_image.subsurface((250, 0, 50, 123)), (32, 64)),
                    pygame.transform.scale(tom_death_image.subsurface((300, 0, 50, 123)), (32, 64)),
                    pygame.transform.scale(tom_death_image.subsurface((350, 0, 50, 123)), (32, 64)),
                    pygame.transform.scale(tom_death_image.subsurface((400, 0, 100, 123)), (64, 64)),
                    pygame.transform.scale(tom_death_image.subsurface((500, 0, 100, 123)), (64, 64)),
                    pygame.transform.scale(tom_death_image.subsurface((600, 0, 100, 123)), (64, 64)),
                    ]
    tom_anim = list()
    john_anim = list()
    jane_anim = list()
    tom_anim.append(Animation(tom_left_anim, 180))
    john_anim.append(Animation(john_right_anim, 180))
    jane_anim.append(Animation(jane_right_anim, 180))
    player_anim = list()
    player_anim.append(Animation(anim, 180))
    player_anim.append(Animation(left_anim, 180))
    tom_anim.append(Animation(tom_die_anim, 180))
    sprite_counter = -1
    pygame.display.set_caption("VeryVeryGoodGame2.0")  # Пишем в шапку
    # будем использовать как фон
    #screen.fill(pygame.Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    counter = 0
    john_counter = 0
    jane_counter = 0
    tom_counter = 0
    tom_death_counter = 0
    screen.blit(bg, (0, 0))
    player = Player(850, 176+DELTA)
    player.draw(screen)
    map = Map()
    map.render(screen)

    dialog = DialogBox(50, 10)
    font = pygame.font.Font(None, 20)
    dialog.update([(font.render("Черт, совсем забыл! Надо спуститься на 2 этаж к Джону. Ему что-то нужно", 1, pygame.Color("black") ), pl_face)])
    screen.blit(begin_img, (0, 0))
    pygame.display.flip()
    time.delay(5000)
    is_level_up = False
    while running:  # Основной цикл программы
        screen.blit(bg, (0, 0))
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == pygame.QUIT:
                MainMenu.terminate()
            choose_ladder = False
            for i in range(len(map.objects)):
                for j in range(len(map.objects[i])):
                    if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and not player.on_ladder:
                        y = len(map.objects) - 1 - player.stage * 7
                        flag = False
                        for k in range(len(map.objects[y])):
                            if map.objects[y][k] in [30, 31, 40,  50, 61, 71, 91] and map.objects[y][k] != map.objects[i][j]:
                                if map.obj[y][k].Rect.collidepoint(e.pos):
                                    flag = True
                                if e.pos[0] < player.rect.x:
                                    if e.pos[0] <= map.obj[y][k].Rect.x + map.obj[y][k].Rect.width <= player.rect.x and \
                                                    map.obj[y][k].state == False:
                                        flag = True
                                else:
                                    if player.rect.x <= map.obj[y][k].Rect.x <= e.pos[0] and map.obj[y][k].state == False:
                                        flag = True
                        if not flag:

                            if map.objects[i][j] == 2 and not choose_ladder:
                                if (player.on_top_ladder or player.on_bottom_ladder) and not player.on_ladder:
                                    player.on_top_ladder = False
                                    player.on_bottom_ladder = False
                                if not player.on_ladder and map.obj[i][j].rect.collidepoint(e.pos) :
                                    player.moving = True
                                    player.move(map.obj[i][j].rect.x+8)
                                    if e.pos[1] <= player.rect.y + player.rect.height and y - i < 6 and i != 9:
                                        height = player.rect.y + player.rect.height - 160 - SCALE
                                        player.on_bottom_ladder = True
                                        # player.on_ladder = True
                                    elif e.pos[1] > player.rect.y + player.rect.height and i - y < 9:
                                        player.on_top_ladder = True
                                        height = player.rect.y - player.rect.height + 160 + SCALE
                                    choose_ladder = True

                            elif map.objects[i][j] in [3, 4, 5, 6, 7, 8, 9, 30, 31, 40,  50, 61, 71, 91]:
                                if map.obj[i][j].Rect.collidepoint(e.pos):
                                    player.on_top_ladder = False
                                    player.on_bottom_ladder = False
                                    if not player.rect.colliderect(map.obj[i][j].Rect):
                                        if e.pos[0] > player.rect.x:
                                            print(1)
                                            player.move(map.obj[i][j].Rect.x - player.rect.width // 2)
                                            player.moving = True
                                        else:
                                            print(2)
                                            player.move(map.obj[i][j].Rect.x + map.obj[i][j].Rect.width)
                                            player.moving = True
                    if map.objects[i][j] in [3, 4, 5, 6, 7, 8, 9]:
                        map.obj[i][j].get_event(e, player)
                    if map.objects[i][j] in [30, 31, 40,  50, 61, 71, 91]:
                        map.obj[i][j].get_event(e, player)

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3 and not player.on_ladder:
                player.on_bottom_ladder = False
                player.on_top_ladder = False
                player.on_ladder = False
                y = len(map.objects) - 1 - player.stage*7
                flag = False
                for i in range(len(map.objects[y])):
                    if map.objects[y][i]in [30, 31, 40,  50, 61, 71, 91]:
                        if map.obj[y][i].Rect.collidepoint(e.pos) and map.obj[y][i].state == False:
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
            if pygame.sprite.spritecollideany(player, ladder_group) or player.on_ladder:
                if player.move_ladder(height):
                    player.on_bottom_ladder = False
                    player.on_top_ladder = False
                    player.on_ladder = False

        if player.moving:
            player.move(player.mouse_pos)
            if counter == 6:
                if not player.on_ladder:
                    if player.right:
                        for i in player_anim:
                            i.update(dt)
                        player.image = player_anim[0].get_sprite()
                        counter = 0
                    elif player.left:
                        for i in player_anim:
                            i.update(dt)
                        player.image = player_anim[1].get_sprite()
                        counter = 0
        if map.npc[2].die and not map.npc[2].dead:
            if sprite_counter == 7:
                map.npc[2].dead = True
            if tom_death_counter == 10:
                for x in tom_anim:
                    x.update(dt)
                map.npc[2].image = tom_anim[1].get_sprite()
                tom_death_counter = 0
                sprite_counter += 1
        if not map.npc[2].die:
            tom_death_counter = 0

        if map.npc[0].moving:
            if john_counter == 6:
                for i in john_anim:
                    i.update(dt)
                map.npc[0].image = john_anim[0].get_sprite()
                john_counter = 0
        if not map.npc[0].moving:
            map.npc[0].image = pygame.transform.scale(john_image.subsurface((0, 0, 50, 123)), (32, 64))
            john_counter = 0

        if map.npc[1].moving:
            if jane_counter == 5:
                for i in jane_anim:
                    i.update(dt)
                map.npc[1].image = jane_anim[0].get_sprite()
                jane_counter = 0
        if not map.npc[1].moving:
            map.npc[1].image = pygame.transform.scale(jane_image.subsurface((0, 0, 50, 123)), (32, 64))
            jane_counter = 0

        if map.npc[2].moving:
            if tom_counter == 5:
                for i in tom_anim:
                    i.update(dt)
                map.npc[2].image = tom_anim[0].get_sprite()
                tom_counter = 0
        if not map.npc[2].moving and not map.npc[2].die:
            map.npc[2].image = pygame.transform.scale(tom_image.subsurface((0, 0, 50, 123)), (32, 64))
            tom_counter = 0
        if map.npc[2].dead:
            map.npc[2].image = pygame.transform.scale(tom_death_image.subsurface((600, 0, 100, 123)), (64, 64))

        if not player.moving:
            if player.on_ladder:
                player.image = pygame.Surface((0, 0))
            else:
                counter = 0
                player.image = pygame.transform.scale(player_img.subsurface((530, 30, 50, 125)), (32, 64))
        counter += 1
        john_counter += 1
        jane_counter+= 1
        tom_counter += 1
        tom_death_counter += 1

        map.render(screen)
        dialog.render(screen)
        for l in map.obj1:
            l.get_event(None, player)
        player.draw(screen)
        for i in player.board.board:
            if "d" in i:
                player.level = 2
                if not is_level_up:
                    print(map.npc[2].level, len(map.npc[2].dialogs)-1)
                    if map.npc[2].level != len(map.npc[2].dialogs)-1:
                        dialog.update([(font.render("Ха, вот он. Зачем ты мне врал?", 1, pygame.Color("black")), pl_face),
                               (font.render("Хорошо, можешь уйти, только ключ оставь здесь", 1, pygame.Color("black")), pygame.image.load("images/tomF.png"))])
                        is_level_up = True





        if player.rect.x == WIN_WIDTH-90:
            while player.rect.x <= WIN_WIDTH:
                player.rect.x+=1
                clock.tick(60)
                pygame.display.flip()
            screen.blit(win_img, (0, 0))
            pygame.display.flip()
            time.delay(5000)
            return
        dt = clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    while True:
        MainMenu.start_screen()
        main()

