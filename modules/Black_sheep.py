import pygame
import sys
import os
from pathlib import Path


from .orders import orders
from .colores import colores
from .Backgrounds import BackgroundImage
from .Board import Board


FPS = 60


IMAGES_DIR = os.path.join(Path(__file__).parent.parent, 'assets', 'images')

class BlackSheep:

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.size = pygame.display.Info().current_h - 320
        self.size = 600 
        self.screen = pygame.display.set_mode((self.size, self.size), pygame.RESIZABLE)
        pygame.display.set_caption('BLACK SHEEP')
        self.opening_page()

    def opening_page(self):
        background = BackgroundImage(self.screen, (self.size, self.size), os.path.join(IMAGES_DIR, 'BlackSheepSign.png'))
        background.add_box(int(self.size/1.48), int(self.size/9.68), int(self.size/3.11), int(self.size/5.0), color=colores['BROWN'])
        background.add_text('Welcome', int(self.size/1.4), int(self.size/10.0), size=int(self.size/20.0), color=colores['BLACK'], font='Arial Black')
        background.add_text('to', int(self.size/1.22), int(self.size/6.67), size=int(self.size/30.0), color=colores['BLACK'], font='Arial Black')
        background.add_text('Black Sheep!', int(self.size/1.46), int(self.size/5.41), size=int(self.size/20.0), color=colores['BLACK'], font='Viner Hand ITC.')
        button = background.add_button(int(self.size/1.3), int(self.size/4.14), int(self.size/7.5), int(self.size/17.14), color=colores['RED'], text='Start',
                                       text_color=colores['WHITE'], onclick_function=self.menu_page)
        hover_button = background.add_hover_button(int(self.size/1.62), int(self.size/30.0), int(self.size/7.5), int(self.size/17.14), color=colores['YELLOW'],
                                                   text='Hover for instructions',
                                                   onclick_function=self.instructions_page)

        run_background = True
        while run_background:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            background.draw()
            button.appear()
            hover_button.appear()
            pygame.display.flip()
            self.clock.tick(FPS)

    def menu_page(self):
        background = BackgroundImage(self.screen, (self.size, self.size), os.path.join(IMAGES_DIR, 'Black_sheep_bass.png'))
        background.add_text('Choose your level', int(self.size/60.0), int(self.size/1.54), size=int(self.size/15.0), font='Viner Hand ITC.', color=colores['YELLOW'])
        input_box = background.add_input_box(x=int(self.size/30.0), y=int(self.size/1.2), width=int(self.size/18.18), height=int(self.size/15.0), prompt='Choose a level from 1 to 48: ',
                                             prompt_above=False, limit=2)

        run_background = True
        while run_background:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        number = input_box.get_user_input()
                        number = int(number) if number.isdigit() else 0
                        if 0 < number < 49:
                            self.main_game(number)
                input_box.handle_events(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            background.draw()
            input_box.appear()
            pygame.display.flip()
            self.clock.tick(FPS)

    def main_game(self, level):
        active_ball = None
        active_game = True
        order = orders[level - 1]
        board = Board(self.screen, (self.size, self.size), white_order=order[:-1], black_ball_loc=order[-1],
                      color=colores['BLACK1'])
        board.add_text(f'LEVEL {level}', int(self.size/60.0), int(self.size/300.0), size=int(self.size/17.14), color=colores['YELLOW'], font='Arial black')
        buttons = [board.add_button(x=int(self.size/2.73), y=int(self.size/60.0), width=int(self.size/60.0), height=int(self.size/17.14), text='Go back to menu.', onclick_function=self.menu_page)]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            board.show()
            for button in buttons:
                button.appear()

            balls = board.get_balls()

            # if there is a ball movement taking place right now, you can't move other balls
            if not board.is_active():
                for ball in balls:
                    if ball.is_dragged():
                        active_ball = board.activate(ball)
            else:
                hole_touched = active_ball.is_touching_hole()  # if there's no a hole colliding, it's set to None
                possible_destinations = active_ball.get_possible_destinations(
                    highlight=True)  # a list of all permitted destinations
                if active_ball.is_dragged():  # if the ball is dragged by the mouse
                    active_ball.follow_mouse()
                elif hole_touched in possible_destinations:  # if the ball is released at a permitted hole
                    active_ball.release_at_hole(hole_touched)
                else:  # if the ball is released somewhere else across the board
                    active_ball.move_back()

            if board.no_possible_movement_left() and not board.is_active() and active_game:
                active_game = False
                if board.win():
                    if level < 48:
                        board.add_text('Hooray! You won.', int(self.size/12.0), int(self.size/1.11), size=int(self.size/12.5), box=True, color=colores['RED'],
                                       box_color=colores['YELLOW'])
                        buttons.append(board.add_button(x=int(self.size/1.28), y=int(self.size/60.0), width=int(self.size/60.0), height=int(self.size/17.14), text='Next level', onclick_function=self.main_game, onclick_args=(level + 1,), one_press=True))
                    else:
                        board.add_text('WOW, You definitely cracked the system...', x=int(self.size/60.0), y=int(self.size/1.09), size=int(self.size/15.38), box=True, color=colores['RED'], box_color=colores['YELLOW'])
                else:
                    board.add_text("Stuck?  Never mind,  Maybe  you'll  succeed  next  time.", int(self.size/60.0), int(self.size/1.08), size=int(self.size/25.0),
                                   box=True, color=colores['YELLOW'], box_color=colores['RED'], font='Viner Hand ITC.')

                    buttons.append(board.add_button(x=int(self.size/1.28), y=int(self.size/60.0), width=int(self.size/60.0), height=int(self.size/17.14), text='Try again', onclick_function=self.main_game, onclick_args=(level,), one_press=True))

            pygame.display.flip()
            self.clock.tick(FPS)

    def instructions_page(self):
        page = BackgroundImage(self.screen, (self.size, self.size), os.path.join(IMAGES_DIR, 'Black_sheep_sign_blur.png'))
        text = [
            "Goal: Stay with only one ball on the board.",
            "How:",
            "1) A ball is removed if it's bypassed by another.",
            "2) You cannot bypass multiple balls.",
            "3) You cannot bypass an empty hole.",
            "4) You cannot bypass the black ball.",
            "5) though, if there's a black ball, it will be the one left.",
            "6) you have to figure out the way to solve an order at the ",
            "   beginning, Once you've moved, there's no moving back.",
            "7) So stay focused and 1 2 3..."]

        hover_button = page.add_hover_button(int(self.size/1.62), int(self.size/30.0), int(self.size/2.5), int(self.size/17.14), color=colores['BRIGHT YELLOW'], text='Leave to go back',
                                             text_color=colores['BROWN'])
        page.add_box(int(self.size/1.48), int(self.size/9.68), int(self.size/3.11), int(self.size/5.0), color=colores['BRIGHT BROWN'])
        page.add_text("Instructions.", int(self.size/60.0), int(self.size/60.0), color=colores['BLACK'])
        line_size = int(self.size/6.0)
        for line in text:
            page.add_text(line,  int(self.size/60.0), line_size, size=int(self.size/33.33), font='Arial black', color=colores['BLACK']).appear()
            line_size += int(self.size/13.33)

        run_background = True
        while run_background:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if not hover_button.get_hovered():
                run_background = False
                self.opening_page()

            page.draw()
            hover_button.appear()

            pygame.display.flip()
            self.clock.tick(FPS)
