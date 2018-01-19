import pygame
import sys
import random

pygame.init()
SCALE = 32


class Player:
    def __init__(self):
        self.x, self.y = 32, 32
        self.width, self.height = 32, 32
        self.image = pygame.image.load('new_fk.png')
        self.color = (0, 0, 255)
        self.dx, self.dy = 0, 0
        self.jump_power = 700
        self.is_jump = False
        self.remain_jump = 0


class Map:
    def __init__(self):
        self.player = Player()
        self.blocks = [Block(17, 1, 7, 1), Block(16, 8, 2, 1),
                       Block(15, 10, 2, 1), Block(11, 6, 2, 1),
                       Block(12, 10, 1, 1), Block(9, 9, 1, 1),
                       Block(17, 3, 1, 1), Block(14, 13, 2, 1),
                       Block(11, 13, 2, 1), Block(8, 12, 3, 1),
                       Block(13, 16, 1, 1), Block(9, 17, 1, 4),
                       Block(17, 18, 4, 1), Block(13, 20, 2, 1),
                       Block(11, 21, 1, 2), Block(16, 23, 1, 1),
                       Block(15, 26, 1, 1), Block(14, 28, 1, 1),
                       Block(17, 31, 4, 1), Block(16, 37, 2, 1),
                       Block(15, 41, 2, 1), Block(17, 45, 3, 1),
                       Block(16, 49, 1, 1), Block(15, 51, 1, 1),
                       Block(13, 52, 1, 1), Block(12, 54, 1, 1),
                       Block(17, 56, 4, 1), Block(16, 62, 4, 1),
                       Block(15, 63, 3, 1), Block(14, 64, 2, 1),
                       Block(13, 65, 1, 1), Block(14, 67, 1, 1),
                       Block(15, 67, 2, 1), Block(16, 67, 3, 1),
                       Block(16, 73, 3, 1), Block(17, 13, 1, 1),
                       Block(0, 0, 1, 20),Block(0,1,76,1),
                       Block(0, 77, 1, 20)]
        self.objects = []


class Block:
    def __init__(self, x, y, width, height, block_type=-1):
        self.x, self.y = y * SCALE, x * SCALE
        self.width, self.height = width * SCALE, height * SCALE
        self.image = pygame.image.load('new_tiles_32.png')
        if block_type == -1:
            self.type = random.randint(0, 15)
        else:
            self.type = block_type


class Game:
    def __init__(self):
        self.map = Map()
        self.clock = pygame.time.Clock()
        self.size = (800, 640)
        self.screen = pygame.display.set_mode(self.size)
        self.camx = 0

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.map.player.dx = max(self.map.player.dx - 30, -100)
        if keys[pygame.K_RIGHT]:
            self.map.player.dx = min(self.map.player.dx + 30, 100)
        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if not (self.map.player.is_jump):
                self.map.player.remain_jump = self.map.player.jump_power
                self.map.player.is_jump = True
            self.map.player.dy -= self.map.player.remain_jump * 0.1
            self.map.player.remain_jump *= 0.9

    def update(self, dt):
        self.map.player.dy += 9.8 * 80 * dt
        self.map.player.x += self.map.player.dx * dt
        self.map.player.y += self.map.player.dy * dt

        if not (-300 * dt <= self.map.player.dx <= 300 * dt):
            if self.map.player.dx > 0:
                self.map.player.dx -= 300 * dt
            else:
                self.map.player.dx += 300 * dt
        for block in self.map.blocks:
            player_x, player_y = self.map.player.x, self.map.player.y
            player_width, player_height = self.map.player.width, self.map.player.height
            if (block.y < player_y + player_height < block.y + player_height) and (
                    player_x + player_width > block.x) and player_x < block.x + block.width:
                self.map.player.y = block.y - player_height
                self.map.player.dy = 0
                self.map.player.is_jump = False
            if (block.y < player_y < block.y + block.height) and (
                    player_x + player_width > block.x) and player_x < block.x + block.width:
                self.map.player.y = block.y + block.height
                self.map.player.dy = 0
            if player_x + player_width > block.x and player_x < block.x and self.check_range(player_y,player_height, block.y, block.height):
                self.map.player.x = player_x - (player_x + player_width - block.x)
                self.map.player.dx = 0
            if player_x < block.x + block.width and player_x + player_width > block.x + block.width and self.check_range(player_y,player_height, block.y, block.height):
                self.map.player.x = player_x + (block.x + block.width - player_x)
                self.map.player.dx = 0

                # Обработка столкновения с низом окна
        if self.map.player.y + self.map.player.height >= 640:
            self.map.player = Player()

        # Камера
        if self.map.player.x - self.camx > 192:
            self.camx += (self.map.player.x - self.camx - 192)
        if self.map.player.x - self.camx < 64:
            self.camx += (self.map.player.x - self.camx - 64)

    def check_range(self,player_y, player_height, block_y, block_height):
        for i in range(int(player_y),int(player_height+player_y)):
            if i in range(block_y, block_height+block_y):
                return True
        return False


    def draw(self):
        self.screen.fill((4, 4, 35))
        self.screen.blit(self.map.player.image, (self.map.player.x - self.camx, self.map.player.y),
                         (256, 0, self.map.player.width, self.map.player.height))
        for block in self.map.blocks:
            for i in range(block.width // SCALE):
                for j in range(block.height // SCALE):
                    self.screen.blit(block.image, (block.x - self.camx + i * SCALE, block.y + j * SCALE),
                                     (block.type * SCALE, 0, SCALE, SCALE))
        pygame.display.flip()

    def run(self):
        while True:
            self.events()
            for i in range(20):
                self.update(1 / 600)
            self.clock.tick(60)
            self.draw()
            self.key()


if __name__ == '__main__':
    game = Game()
    game.run()
