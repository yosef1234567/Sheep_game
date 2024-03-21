import pygame
from colores import colores
from Buttons import Button, InputBox, HoverButton, TextBox


class Background:

    def __init__(self, screen: pygame.Surface, size: tuple, text=None, color=colores['WHITE']):
        self.screen = screen
        self.size = size
        self.surface = pygame.Surface(self.size)
        self.color = color
        self.surface.fill(self.color)

    def draw(self, position: tuple = (0, 0)):
        self.screen.blit(self.surface, position)

    def add_text(self, text, x, y, size=70, color=colores['RED'], font='Arial', box=False, box_color=colores['WHITE'], no_exceeding=1):
        return TextBox(self.surface, text, x=x, y=y, size=size, color=color, font=font, box=box, box_color=box_color, no_exceeding=no_exceeding)

    def add_box(self, x, y, width, height, color=colores['WHITE']):
        box = pygame.Surface((width, height))
        box.fill(color)
        box_rect = pygame.Rect(x, y, width, height)
        self.surface.blit(box, box_rect)

    def add_button(self, x, y, width, height, color=colores['RED'], text='Press', font='Arial',
                   text_color=colores['BLACK'], onclick_function=None, onclick_args=(), one_press=False):
        return Button(self.surface, x=x, y=y, width=width, height=height, text=text, font=font, color=color,
                      text_color=text_color, onclick_function=onclick_function, onclick_args=onclick_args, one_press=one_press)

    def add_hover_button(self, x, y, width, height, color=colores['RED'], text='Press', font='Arial',
                         text_color=colores['BLACK'], onclick_function=None, onclick_args=()):
        return HoverButton(self.surface, x=x, y=y, width=width, height=height, text=text, font=font, color=color,
                           text_color=text_color, onclick_function=onclick_function, onclick_args=onclick_args)

    def add_input_box(self, x, y, width, height, font='Arial', prompt: str = None,
                      prompt_above=True, limit: int = 20):
        return InputBox(self.surface, x=x, y=y, width=width, height=height, font=font, prompt=prompt,
                        prompt_above=prompt_above, limit=limit)


class BackgroundImage(Background):

    def __init__(self, screen: pygame.Surface, size: tuple, image, text=None):
        super().__init__(screen, size, text)
        self.image = pygame.image.load(image).convert()
        self.surface = pygame.transform.scale(self.image, size)
