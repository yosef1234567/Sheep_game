import pygame
from modules.colores import colores


class Button:
    def __init__(self, surface, x, y, width, height, color=colores['WHITE'], text='Press', font='Arial',
                 text_color=colores['BLACK'], onclick_function=None, onclick_args=(), one_press=False):
        if onclick_args is None:
            onclick_args = []
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pressed = False
        self.onclickFunction = onclick_function
        self.onePress = one_press
        self.alreadyPressed = False
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont(font, int(self.height * 0.85))
        self.onclick_args = onclick_args
        self.fillColors = {
            'normal': self.color,
            'hover': tuple(max(component - 45, 0) for component in self.color),
            'pressed': '#333333',
        }
        self.textSurf = self.font.render(text, True, self.text_color)
        if self.textSurf.get_width() > self.width:
            self.width = self.textSurf.get_width() + 2
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.appear()

    def appear(self):
        """
        checks the state of the button and
        """
        mouse_pos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        self.pressed = False
        if self.buttonRect.collidepoint(mouse_pos):
            self.buttonSurface.fill(self.fillColors['hover'])
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.pressed = True
                if self.onclickFunction:
                    if self.onePress:
                        if not self.alreadyPressed:
                            self.onclickFunction(*self.onclick_args)
                            self.alreadyPressed = True
                    else:
                        self.onclickFunction(*self.onclick_args)
            else:
                self.alreadyPressed = False
        else:
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

        self.buttonSurface.blit(self.textSurf, [
            self.buttonRect.width / 2 - self.textSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.textSurf.get_rect().height / 2
        ])
        self.surface.blit(self.buttonSurface, self.buttonRect)

    def get_pressed(self):
        """
        return true if pressed, else false
        """
        return self.pressed


class HoverButton(Button):

    def __init__(self, surface, x, y, width, height, color=colores['WHITE'], text='Press', font='Arial',
                 text_color=colores['BLACK'], onclick_function=None, onclick_args=()):

        self.hovered = True
        super().__init__(surface, x, y, width, height, color, text, font, text_color, onclick_function, onclick_args)

    def appear(self):
        mouse_pos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mouse_pos):
            self.hovered = True
            if self.onclickFunction:
                self.onclickFunction(*self.onclick_args)
        else:
            self.hovered = False

        self.buttonSurface.blit(self.textSurf, [
            self.buttonRect.width / 2 - self.textSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.textSurf.get_rect().height / 2
        ])
        self.surface.blit(self.buttonSurface, self.buttonRect)

    def get_hovered(self):
        return self.hovered


class InputBox:

    def __init__(self, surface, x, y, width, height, font='Arial', prompt: str = None,
                 prompt_above=True, limit: int = 20):
        self.surface = surface
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(font, int(self.height * 0.85))
        self.user_text = ''
        self.box_surface = pygame.Surface((self.width, self.height))
        self.box_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color_active = colores['LIGHT_BLUE2']
        self.color_passive = colores['LIGHT_BLUE1']
        self.color = self.color_passive
        self.active = False
        self.limit = limit
        self.prompt = prompt
        self.prompt_above = prompt_above
        if self.prompt:
            self.set_prompt()
        self.appear()

    def get_user_input(self):
        return self.user_text

    def set_prompt(self):
        self.prompt_surface = self.font.render(self.prompt, True, colores['BLACK'])
        self.prompt_box_surface = pygame.Surface((self.prompt_surface.get_width(), self.height))
        self.prompt_box_rect = pygame.Rect(self.x, self.y, self.prompt_surface.get_width(), self.height)
        TextBox(self.surface, self.prompt, self.x, self.y)
        if self.prompt_above:
            self.box_rect = pygame.Rect(self.x, self.y + self.height + 2, self.width, self.height)
        else:
            self.box_rect = pygame.Rect(self.x + self.prompt_box_rect.width + 4, self.y, self.width, self.height)

    def prompt_user(self):
        if self.prompt:
            self.prompt_box_surface.fill(colores['WHITE'])

            self.prompt_box_surface.blit(self.prompt_surface, [
                (self.prompt_box_rect.width - self.prompt_box_surface.get_rect().width) / 2,
                (self.prompt_box_rect.height - self.prompt_box_surface.get_rect().height) / 2
            ])
            self.surface.blit(self.prompt_box_surface, self.prompt_box_rect)

    def set_color_and_activity_state_input_box(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.box_rect.collidepoint(mouse_pos):
            self.active = True
            self.color = self.color_active
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            self.active = False
            self.color = self.color_passive
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def handle_events(self, event):
        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]

                elif event.key == pygame.K_RETURN:
                    return self.user_text

                # Unicode standard is used for string formation
                else:
                    if self.limit > len(self.user_text):
                        self.user_text += event.unicode

    def appear(self):
        self.set_color_and_activity_state_input_box()

        text_surface = self.font.render(self.user_text, True, colores['BLACK'])
        self.box_surface.fill(self.color)

        self.box_surface.blit(text_surface, [
            (self.box_rect.width - self.box_surface.get_rect().width) / 2,
            (self.box_rect.height - self.box_surface.get_rect().height) / 2
        ])
        self.prompt_user()

        self.surface.blit(self.box_surface, self.box_rect)

        self.box_surface = pygame.transform.scale(self.box_surface,
                                                  (self.box_rect.width, self.box_surface.get_height()))
        self.box_rect.width = max(self.width, text_surface.get_width() + 5)


class TextBox:

    def __init__(self, surface: pygame.Surface, text, x, y, size=40, color=colores['RED'], font='Arial', box=False,
                 box_color=colores['WHITE'], no_exceeding=1):
        self.surface = surface
        self.size = size
        self.font = font
        self.text = text
        self.color = color
        self.text_surface = pygame.font.SysFont(font, self.size).render(text, True, color)
        self.box = box
        self.box_surface = pygame.Surface(self.text_surface.get_rect().size) if self.box else None
        self.box_color = box_color
        self.x = x
        self.y = y
        self.no_exceeding = no_exceeding
        if self.no_exceeding:
            self.prevent_exceeding()
        self.appear()

    def appear(self):
        if self.box:
            self.box_surface.fill(self.box_color)
            self.box_surface.blit(self.text_surface, (2, 2))
            self.surface.blit(self.box_surface, (self.x, self.y))
        else:
            self.surface.blit(self.text_surface, (self.x, self.y))

    def prevent_exceeding(self):
        if self.x < self.surface.get_width():
            while self.x + self.text_surface.get_rect().width + self.no_exceeding > self.surface.get_width():
                self.size -= 1
                self.text_surface = pygame.font.SysFont(self.font, self.size).render(self.text, True, self.color)
                self.box_surface = pygame.Surface(self.text_surface.get_rect().size) if self.box else None
        self.width = self.text_surface.get_width()
        self.height = self.text_surface.get_height()