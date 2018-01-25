# Импортируем библиотеку pygame
import pygame
import brd

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
        self.inventory = []
        self.showInventory = False
        self.board = brd.Board(5, 5, self.inventory)

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
        if self.showInventory:
            inv = self.board.render()
            r = inv.get_rect()
            screen.blit(inv, (self.rect.x-r.width, self.rect.y-r.height))
            self.In_rect = pygame.Rect(self.rect.x-r.width, self.rect.y-r.height, r.width, r.height)


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
        self.thing = None

    def get_event(self, event, player):
        if event.type == pygame.MOUSEMOTION:
            was_collided = self.collided
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
                player.showInventory = True
            elif self.showInventory and not self.In_rect.collidepoint(event.pos) and not player.In_rect.collidepoint(event.pos):
                self.showInventory = False
                player.showInventory = False
                self.thing = None
            elif self.showInventory and player.In_rect.collidepoint(event.pos):
                self.thing = player.board.get_click((event.pos[0] - player.rect.x + player.In_rect.width, event.pos[1] - player.rect.y + player.In_rect.height), self.thing)
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
                self.thing = self.board.get_click((event.pos[0]-self.Rect.x+self.In_rect.width, event.pos[1]-self.Rect.y+self.In_rect.height), self.thing)
                if self.thing:
                    f = True
                    for i in range(len(player.board.board)):
                        for j in range(len(player.board.board[i])):
                            if player.board.board[i][j] == 0:
                                player.board.board[i][j] = self.thing
                                f = False
                                break
                        if not f:
                            break
                    self.thing = None
            self.pressed = False

    def render(self, surface):
        surface.blit(self.image, self.Rect)
        if self.showInventory:
            inv = self.board.render()
            r = inv.get_rect()
            surface.blit(inv, (self.x-r.width, self.y-r.height))
            self.In_rect = pygame.Rect(self.x-r.width, self.y-r.height, r.width, r.height)






class Map:
    def __init__(self):
        self.objects = [
                        "    22                  ",
                        "    22                  ",
                        "                        ",
                        "                        ",
                        "                        ",
                        "                        "]

    def render(self, screen):
        x = 0
        y = WIN_HEIGHT-64-32
        screen.fill(pygame.Color(BACKGROUND_COLOR))
        for i in self.objects:
            image = pygame.image.load("images/room.png")
            for j in i:
                if j == "1":
                    surf = pygame.Surface((Wall().width, Wall().height))
                    surf.fill(Wall().color)
                    screen.blit(surf, (x, y))
                if j == "2":
                    surf = pygame.Surface((image.get_rect().width, image.get_rect().height))
                    surf.blit(image, (0, 0))
                    screen.blit(surf, (x, y))
                x += image.get_rect().width
            y -= image.get_rect().height
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
    table = Entity(400, WIN_HEIGHT-50-32, "shelf")
    table1 = Entity(500,  WIN_HEIGHT-50-32, "shelf")
    player.draw(screen)
    map = Map()
    while running:  # Основной цикл программы
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
                player.moving = True
                player.move(e.pos[0])
            table.get_event(e, player)
            table1.get_event(e, player)

        if player.moving:
            player.move(player.mouse_pos)

        #clock.tick(60)
        map.render(screen)
        player.draw(screen)
        table.render(screen)
        table1.render(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
