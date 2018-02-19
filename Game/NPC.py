import pygame
from resources import *


class NPC(pygame.sprite.Sprite):
    d = {"john":john_image, "jane":jane_image, "tom":tom_image}

    def __init__(self, x, y, name, steps, dialogs):
        pygame.sprite.Sprite.__init__(self)
        self.steps = steps
        self.x = x
        self.y = y
        self.to_go = x
        self.name = name
        self.move_speed = 1
        self.image = pygame.transform.scale(NPC.d[name].subsurface((0, 0, 50, 123)), (32, 64))
        self.face = pygame.image.load("images/"+name+"F.png")
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
            self.steps.stop()
            self.to_go = self.x

            self.moving = False
       # if self.moving:
        #    self.steps.play()
        #else:
        #    self.steps.stop()
    def render(self, surface):
        surface.blit(self.image, (self.x, self.y))


class EnemyNPC(NPC):
    d = {"tom":tom_image}
    def __init__(self, x, y, name, steps, dialogs):
        super().__init__( x, y, name, steps, dialogs)
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
                        hit.play()
                        scream.play()

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
