# Импортируем библиотеку pygame
import pygame
import brd
import random
import MainMenu
from resources import *
from levels import Level1
from NPC import *
from mapObjects import *

pygame.init()
time = pygame.time
clock = pygame.time.Clock()
screen = pygame.display.set_mode(DISPLAY)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.steps = player_steps
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
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.inventory = []
        self.showInventory = False
        self.board = brd.Board(5, 5, self.inventory)
        self.In_rect = pygame.Rect(WIN_WIDTH - self.board.render().get_rect().width, WIN_HEIGHT-self.board.render().get_rect().height, self.board.render().get_rect().width, self.board.render().get_rect().height)

    def move(self, mouse_pos):
        self.mouse_pos = mouse_pos
        if self.mouse_pos > self.rect.x:
            if not pygame.mixer.get_busy():
                self.steps.play()
            self.left = False
            self.right = True
            self.current_speed = self.move_speed

        if self.mouse_pos < self.rect.x:
            if not pygame.mixer.get_busy():
                self.steps.play()
            self.right = False
            self.left = True
            self.current_speed = -self.move_speed

        if self.mouse_pos == self.rect.x:
            self.steps.stop()
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

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.showInventory:
            inv = self.board.render()
            screen.blit(inv, (self.In_rect.x, self.In_rect.y))


class DialogBox:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dialogs = []
        self.image = pygame.image.load("images/dialog.png")

    def update(self, dialog):
        if dialog:
            random.choice(speech).play()
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
            count += 50

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

    tom_die_anim = [
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
    map = Level1()
    map.render(screen)

    dialog = DialogBox(50, 10)
    font = pygame.font.Font(None, 20)
    dialog.update([(font.render("Черт, совсем забыл! Надо спуститься на 2 этаж к Джону. Ему что-то нужно", 1, pygame.Color("black")), pl_face)])
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
                            if e.pos[0] <= i*SCALE <= player.rect.x:
                                flag = True
                        else:
                            if player.rect.x <= i*SCALE <= e.pos[0]:
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
            if map.npc[2].image == tom_anim[1].get_sprite():
                pass
                # hit.play()
                # scream.play()
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
            map.npc[0].steps.play()
            if john_counter == 6:
                for i in john_anim:
                    i.update(dt)
                map.npc[0].image = john_anim[0].get_sprite()
                john_counter = 0
        if not map.npc[0].moving:
            map.npc[0].steps.stop()
            map.npc[0].image = pygame.transform.scale(john_image.subsurface((0, 0, 50, 123)), (32, 64))
            john_counter = 0

        if map.npc[1].moving:
            map.npc[1].steps.play()
            if jane_counter == 5:
                for i in jane_anim:
                    i.update(dt)
                map.npc[1].image = jane_anim[0].get_sprite()
                jane_counter = 0
        if not map.npc[1].moving:
            map.npc[1].steps.stop()
            map.npc[1].image = pygame.transform.scale(jane_image.subsurface((0, 0, 50, 123)), (32, 64))
            jane_counter = 0

        if map.npc[2].moving:
            map.npc[2].steps.play()
            if tom_counter == 5:
                for i in tom_anim:
                    i.update(dt)
                map.npc[2].image = tom_anim[0].get_sprite()
                tom_counter = 0
        if not map.npc[2].moving and not map.npc[2].die:
            map.npc[2].steps.stop()
            map.npc[2].image = pygame.transform.scale(tom_image.subsurface((0, 0, 50, 123)), (32, 64))
            tom_counter = 0
        if map.npc[2].dead and not map.npc[2].die:
            map.npc[2].steps.stop()
            map.npc[2].image = pygame.transform.scale(tom_death_image.subsurface((600, 0, 100, 123)), (64, 64))

        if not player.moving:
            if player.on_ladder:
                player.image = pygame.Surface((0, 0))
            else:
                counter = 0
                player.image = pygame.transform.scale(player_img.subsurface((530, 30, 50, 125)), (32, 64))
        counter += 1
        john_counter += 1
        jane_counter += 1
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
                    if not map.npc[2].dead:
                        dialog.update([(font.render("Ха, вот он. Зачем ты мне врал?", 1, pygame.Color("black")), pl_face),
                               (font.render("Хорошо, можешь уйти, только ключ оставь здесь", 1, pygame.Color("black")), pygame.image.load("images/tomF.png"))])
                        is_level_up = True

        if player.rect.x == WIN_WIDTH-90:
            while player.rect.x <= WIN_WIDTH:
                player_steps.stop()
                player.rect.x+=1
                clock.tick(60)
                pygame.display.flip()
            return
        print(clock.get_fps())
        dt = clock.tick(60)
        pygame.display.flip()


if __name__ == "__main__":
    while True:
        MainMenu.start_screen()
        MainMenu.predyslovie()
        main()
        MainMenu.pobeda1()

print("@Authors AlexKrudu and valer1435 all rights is not reserved, not for commercial using")