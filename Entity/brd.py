import pygame


class Board:
    def __init__(self, width, height, inventory):
        self.inventory = inventory
        self.width = width
        self.height = height
        self.cell_size = 20
        self.top = 0
        self.left = 0
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.inventory:
                    self.board[i][j] = self.inventory[-1]
                    self.inventory.pop(-1)
                else:
                    break

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        surface = pygame.Surface((self.width*self.cell_size, self.height*self.cell_size))
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 'x':
                    image = pygame.image.load("images\candle.png")
                    rect = image.get_rect()
                    rect.left, rect.top = (j * self.cell_size + self.left, i * self.cell_size + self.top)
                    surface.blit(image, rect)

                pygame.draw.rect(surface, pygame.Color("white"), (
                j * self.cell_size + self.left, i * self.cell_size + self.top, self.cell_size, self.cell_size), 1)
        return surface

    def get_click(self, mouse_pos, thing=''):
        cell = self.get_cell( mouse_pos)
        if cell:
            self.on_click(cell, thing=thing)

    def on_click(self, cell, thing = ''):
        print(cell)
        print(thing)
        if thing:
            self.board[cell[1]][cell[0]] = thing
    def get_cell(self, mouse_pos):
        if mouse_pos[0] <= self.top or mouse_pos[0] >= self.top + self.cell_size * len(self.board[0]) or mouse_pos[1] <= self.left or mouse_pos[1] >= self.left + self.cell_size * len(self.board):
            return None
        else:
            x = (mouse_pos[0] - self.left) // self.cell_size
            y = (mouse_pos[1] - self.top) // self.cell_size
            return (x, y)

if __name__ == '__main__':
    pygame.init()
    size = width, height = 300, 300
    screen = pygame.display.set_mode(size)
    running = True
    board = Board(5, 7)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                print(board.get_click(event.pos))
            screen.fill((0, 0, 0))
            board.render()
            pygame.display.flip()
