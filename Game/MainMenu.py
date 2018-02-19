import pygame, sys

pygame.init()
running = True
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
pygame.mixer.music.load("music/Inception.mp3")
pygame.mixer.music.play(loops=-1)


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load("images/menubg.png")

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (0, 0)


class GUI:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def render(self, surface):
        for element in self.elements:
            render = getattr(element, "render", None)
            if callable(render):
                element.render(surface)

    def update(self):
        for element in self.elements:
            update = getattr(element, "update", None)
            if callable(update):
                element.update()

    def get_event(self, event):
        for element in self.elements:
            get_event = getattr(element, "get_event", None)
            if callable(get_event):
                r = element.get_event(event)
                if r:
                    return r



class LabelMenu:
    def __init__(self, rect, text):
        self.Rect = pygame.Rect(rect)
        self.text = text
        self.bgcolor = pygame.Color("white")
        self.bgcolor = None
        self.font_color = pygame.Color("black")
        self.font = pygame.font.Font("font/10930.ttf", self.Rect.height - 4)
        self.rendered_text = None
        self.rendered_rect = None

    def render(self, surface):

        self.rendered_text = self.font.render(self.text, 1, self.font_color, pygame.SRCALPHA)
        self.rendered_rect = self.rendered_text.get_rect(x=self.Rect.x + 2, centery=self.Rect.centery)

        surface.blit(self.rendered_text, self.rendered_rect)


class ButtonMenu(LabelMenu):
    def __init__(self, rect, text, value):
        super().__init__(rect, text)
        self.bgcolor = pygame.Color("blue")
        self.pressed = False
        self.collided = False
        self.value = value
        self.font_color = {'up': pygame.Color("black"), "collide":pygame.Color("white")}
        self.soundObj = pygame.mixer.Sound('music/menubtn.ogg')

    def render(self, surface):
        if self.collided:
            self.rendered_text = self.font.render(self.text, 1, self.font_color["collide"])
            self.rendered_rect = self.rendered_text.get_rect(x=self.Rect.x , y=self.Rect.y )
            surface.blit(self.rendered_text, self.rendered_rect)
        else:
            self.rendered_text = self.font.render(self.text, 1, self.font_color["up"])
            self.rendered_rect = self.rendered_text.get_rect(x=self.Rect.x + 2, y=self.Rect.y + 2)
            surface.blit(self.rendered_text, self.rendered_rect)

    def get_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            was_collided  = self.collided
            self.collided  = self.Rect.collidepoint(event.pos)
            if not was_collided and self.collided:
                self.soundObj.play(1)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.pressed = self.Rect.collidepoint(event.pos)
            if self.pressed:
                return self.value
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.pressed = False

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    BackGround = Background()
    gui = GUI()
    gui.add_element(LabelMenu((600, 30, 300, 70), "Escape from War"))
    gui.add_element(ButtonMenu((800, 310, 170, 50), "новая игра", "n"))
    gui.add_element(ButtonMenu((800, 370, 170, 50), "правила", "r"))
    gui.add_element(ButtonMenu((800, 430, 170, 50), "выйти", "q"))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if gui.get_event(event) == "q":
                terminate()
            elif gui.get_event(event) == "r":
                rules()
            elif gui.get_event(event) == "n":
                return

        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)

        gui.render(screen)
        gui.update()
        pygame.display.flip()


def predyslovie():
    pygame.mixer.music.set_volume(0.1)
    image = pygame.image.load("images/begin.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            print(event.type)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return

        screen.blit(image, (0, 0))
        pygame.display.flip()


def pobeda1():
    image = pygame.image.load("images/win.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return
        screen.blit(image, (0, 0))
        pygame.display.flip()

def rules():
    image = pygame.image.load("images/rules.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return
        screen.blit(image, (0, 0))
        pygame.display.flip()

