# Импортируем библиотеку pygame
import pygame

# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640# Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "darkblue"
SCALE = 32


class Wall:
    def __init__(self):
        self.id = 1
        self.width = SCALE
        self.height = SCALE
        self.color = pygame.Color("grey")


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.moving = False
        self.move_speed = 1
        self.id = 2
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

    def draw(self, screen):  # Выводим себя на экран
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Map:
    def __init__(self):
        self.objects = ["1111111111111111111111111",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1                       1",
                        "1111111111111111111111111"]

    def render(self, screen):
        x = 0
        y = 0
        screen.fill(pygame.Color(BACKGROUND_COLOR))
        for i in self.objects:
            for j in i:
                if j == "1":
                    surf = pygame.Surface((Wall().width, Wall().height))
                    surf.fill(Wall().color)
                    screen.blit(surf, (x, y))
                x += Wall().width
            y += Wall().height
            x = 0


def main():
    running = True
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

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                player.moving = True
                player.move(e.pos[0])

        if player.moving:
            player.move(player.mouse_pos)

        #clock.tick(60)
        map = Map()
        map.render(screen)
        player.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
