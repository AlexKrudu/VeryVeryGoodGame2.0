# Импортируем библиотеку pygame
import pygame

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640# Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "darkblue"
SCALE = 32
on_ladder = False


class Empty:
    def __init__(self):
        self.id = 9999999999999


class Wall:
    def __init__(self):
        self.id = 1
        self.width = SCALE
        self.height = SCALE
        self.x = None
        self.y = None
        self.color = pygame.Color("grey")


class Ladder:
    def __init__(self):
        self.id = 2
        self.width = SCALE
        self.height = SCALE
        self.x = None
        self.y = None
        self.color = pygame.Color("orange")

    def on_click(self, player):
        player.on_ladder = True



class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.on_bottom_ladder = False
        self.on_top_ladder = False
        self.moving = False
        self.move_speed = 1
        self.id = 0
        self.width = 22
        self.height = 32
        self.current_speed = 0
        self.default_x = x
        self.default_y = y
        self.mouse_pos = 0
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(pygame.Color("#888888"))
        self.rect = pygame.Rect(x, y, self.width, self.height)

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

    def move_ladder(self):
        if self.on_bottom_ladder:
            if self.rect.y > 480:
                self.rect.y -= self.move_speed
                return False
            if self.rect.y == 480:
                return True
        else:
            if self.rect.y < 576:
                self.rect.y += self.move_speed
                return False
            if self.rect.y == 576:
                return True


    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Map:
    def __init__(self):
        self.objects = [[],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [],
                        [Empty(), Wall(), Wall(), Wall()],
                        [Empty(), Ladder()],
                        [Empty(), Ladder()],
                        [Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall(), Wall()]]

    def render(self, screen):
        x = 0
        y = 0
        screen.fill(pygame.Color(BACKGROUND_COLOR))
        for i in self.objects:
            for j in i:
                if j.id == 1:
                    surf = pygame.Surface((Wall().width, Wall().height))
                    surf.fill(Wall().color)
                    screen.blit(surf, (x, y))
                if j.id == 2:
                    surf = pygame.Surface((Ladder().width, Ladder().height))
                    surf.fill(Ladder().color)
                    screen.blit(surf, (x, y))
                j.x = x
                j.y = y
                x += Wall().width
            y += Wall().height
            x = 0


def main():
    running = True
    on_ladder = False
    clock = pygame.time.Clock()
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("VeryVeryGoodGame2.0")  # Пишем в шапку
    # будем использовать как фон
    screen.fill(pygame.Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом
    player = Player(32, 576)
    player.draw(screen)

    while running:  # Основной цикл программы
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for j in map.objects:
                    for i in j:
                        if i.id == 2:
                            if pygame.Rect(i.x, i.y, i.width, i.height).collidepoint(e.pos):
                                player.moving = True
                                player.move(e.pos[0])
                                if player.rect.y == 576:
                                    player.on_bottom_ladder = True
                                else:
                                    player.on_top_ladder = True

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                player.moving = True
                player.move(e.pos[0])

        if (player.on_bottom_ladder or player.on_top_ladder) and not player.moving:
            if player.move_ladder():
                player.on_bottom_ladder = False
                player.on_top_ladder = False

        if player.moving:
            player.move(player.mouse_pos)

        clock.tick(120)
        map = Map()
        map.render(screen)
        player.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
