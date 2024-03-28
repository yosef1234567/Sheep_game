import pygame
import os
from pathlib import Path
from itertools import permutations

from .colores import colores
from .Backgrounds import Background


IMAGES_DIR = os.path.join(Path(__file__).parent.parent, 'assets', 'images')


class Board(Background):

    def __init__(self, screen, size: tuple, white_order=(0, 1, 2, 4, 6, 8, 12), black_ball_loc=7, text=None,
                 color=colores['BEIGE']):
        super().__init__(screen, size, text, color)
        self.hole_size = 70  # configure hole size
        self.edge = 75  # configure distance from edge of screen to outer holes
        self.distance = 190  # distance between holes including hole size
        self.half_distance = self.distance / 2
        self.edge2 = self.edge + self.half_distance  # configure distance from edge of screen to middle holes
        self.start = pygame.time.get_ticks()
        self.holes_group = self.create_holes()  # create a group to store the holes
        self.balls_group = self.create_balls(white_order, black_ball_loc)  # create a group to store the balls
        self.possibilities = self.get_permutations()  # find all permutations of 3 contiguous holes in a straight line
        self.update_possibilities_per_hole()  # update each hole for its possibilities
        self.active_movement = False  # True if a ball movement is taking place right now
        self.active_ball = False
        self.screen_shots = []

    def create_holes(self):

        holes_group = pygame.sprite.Group()

        holes_locations = [
            (self.edge, self.edge),
            (self.edge + self.distance, self.edge),
            (self.edge + self.distance * 2, self.edge),
            (self.edge2, self.edge2),
            (self.edge2 + self.distance, self.edge2),
            (self.edge, self.edge + self.distance),
            (self.edge + self.distance, self.edge + self.distance),
            (self.edge + self.distance * 2, self.edge + self.distance),
            (self.edge2, self.edge2 + self.distance),
            (self.edge2 + self.distance, self.edge2 + self.distance),
            (self.edge, self.edge + self.distance * 2),
            (self.edge + self.distance, self.edge + self.distance * 2),
            (self.edge + self.distance * 2, self.edge + self.distance * 2)
        ]
        holes = [Hole(self.hole_size, holes_locations[i], i, self.screen) for i in range(len(holes_locations))]

        for hole in holes:
            holes_group.add(hole)

        return holes_group

    def get_permutations(self):
        """
        :return: a list of tuples of all possible triples of holes
        """
        permutations3 = permutations(self.holes_group, 3)  # all the 3 holes combinations
        # filter all the permutations that are not in one line or not with the same distance between them
        line_permutations = [permutation for permutation in permutations3 if self.one_line(permutation)]
        return line_permutations

    def one_line(self, permutation):
        """
        Filters triples that are not in one line or not contiguous
        """
        a, b, c, = [i.rect for i in permutation]
        return a.x - b.x == b.x - c.x and a.y - b.y == b.y - c.y and not \
            [i.get_number() for i in permutation] in [[0, 6, 12], [2, 6, 10], [12, 6, 0], [10, 6, 2]]

    def update_possibilities_per_hole(self):
        """
        Find all the possible destinations for each hole, and update the hole
        """
        for hole in self.holes_group:
            possibilities = []
            for permutation in self.possibilities:
                if hole == permutation[0]:
                    possibilities.append(permutation)
            hole.update_possibilities(possibilities)

    def create_balls(self, white_balls, black_ball=None):
        """
        Creates the balls and locate each one at its hole according to the order sent through parameters
        """
        balls_group = pygame.sprite.Group()
        for hole in self.holes_group:
            if hole.number in white_balls:
                ball = Ball(hole, self)
                hole.fill(ball)
                balls_group.add(ball)
            elif hole.number == black_ball:
                ball = Ball(hole, self, color='black', size=(85, 85))
                hole.fill(ball)
                balls_group.add(ball)
        return balls_group

    def show(self):
        """
        Show the board
        """
        middle_square = pygame.Surface((self.size[0] - 100, self.size[0] - 100))
        middle_square.fill(colores['BEIGE'])
        edge = (self.screen.get_rect().width - self.size[0]) // 2
        self.surface.blit(middle_square, (50, 50))
        self.screen.blit(self.surface, (edge, edge))
        self.holes_group.draw(self.screen)
        self.balls_group.draw(self.screen)

    def get_balls(self):
        return self.balls_group

    def get_holes(self):
        return self.holes_group

    def change_moving_state(self):
        self.active_movement = not self.active_movement

    def is_active(self):
        return self.active_movement

    def activate(self, ball):
        self.change_moving_state()
        self.active_ball = ball
        return ball

    def get_active_ball(self):
        return self.active_ball

    def no_possible_movement_left(self):
        possibilities = []
        for ball in self.balls_group:
            possibilities.extend(ball.get_filtered_possibilities())
        return len(possibilities) == 0

    def win(self):
        return len(self.balls_group) == 1


class Ball(pygame.sprite.Sprite):

    def __init__(self, hole, board, color='w', size=(50, 50)):
        super().__init__()
        image = os.path.join(IMAGES_DIR, 'bright_ball.png') if color == 'w' else os.path.join(IMAGES_DIR, 'black_sheep_no_background.png')
        img = pygame.image.load(image).convert()
        self.image = pygame.transform.scale(img, size)
        self.image.set_colorkey(colores['WHITE'])
        self.hole = hole
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.center = hole.get_center()
        self.last_rect = self.rect.copy()
        self.moving = False
        self.board = board

    def change_position(self, center=tuple):
        self.rect.center = center

    def is_hovered(self):
        mouse_point = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_point):
            return True
        return False

    def is_dragged(self):
        return self.is_hovered() and pygame.mouse.get_pressed()[0]

    def follow_mouse(self):
        self.start_moving()
        self.rect.center = pygame.mouse.get_pos()

    def is_touching_hole(self):
        collisions = pygame.sprite.spritecollide(self, self.board.get_holes(), dokill=False)
        if len(collisions) == 1:
            return collisions[0]

    def release_at_hole(self, hole):
        """
        If the ball is released at a permitted hole, update all relevant
        """

        self.board.change_moving_state()
        possibilities = self.get_filtered_possibilities()  # get all the possible destinations from the new hole
        for possibility in possibilities:
            # if the destination hole is in a possible series with the current hole, you are allowed to proceed
            if hole == possibility[2]:
                bypassed_hole = possibility[1]  # update the bypassed hole
                bypassed_ball = bypassed_hole.get_ball()  # update the bypassed ball
                bypassed_ball.kill()  # kills the bypassed ball
                bypassed_hole.empty()  # empties the bypassed hole
        self.rect.center = hole.rect.center  # set the ball at the new hole
        self.last_rect = self.rect.copy()  # set the last location to be the new hole (you can't retreat anyway)
        self.stop_moving()
        self.hole = hole  # set its new hole
        hole.fill(self)  # update the hole

    def move_back(self):
        self.board.change_moving_state()
        self.rect = self.last_rect.copy()
        self.hole.fill(self)
        self.stop_moving()

    def start_moving(self):
        self.get_hole().highlight_hole()
        if not self.moving:
            self.moving = True
            self.last_rect = self.rect.copy()
            self.hole.empty()

    def stop_moving(self):
        self.moving = False

    def get_color(self):
        return self.color

    def get_hole(self):
        return self.hole

    def get_filtered_possibilities(self):
        possibilities = self.hole.get_possibilities()
        filtered_possibilities = []
        for possibility in possibilities:
            if possibility[1].is_full() and not possibility[1].is_full(color='b') and not possibility[2].is_full():
                filtered_possibilities.append(possibility)
        return filtered_possibilities

    def get_possible_destinations(self, highlight=False):
        holes = []
        filtered_possibilities = self.get_filtered_possibilities()
        for possibility in filtered_possibilities:
            if highlight:
                possibility[2].highlight_hole(color='blue')
            holes.append(possibility[2])
        return holes



class Hole(pygame.sprite.Sprite):

    def __init__(self, hole_size, position, number, screen):
        super().__init__()
        self.ball = None
        img = pygame.image.load(os.path.join(IMAGES_DIR, 'hole.png')).convert()
        self.image = pygame.transform.scale(img, (hole_size, hole_size)).convert()
        self.image.set_colorkey(colores['WHITE'])
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.position = position
        self.number = number
        self.screen = screen
        self.full = False
        self.full_black = False
        self.possibilities = []

    def get_number(self):
        return self.number

    def get_center(self):
        return self.rect.center

    def update_possibilities(self, possibilities):  # update all the possible triples for this hole
        self.possibilities = possibilities

    def get_possibilities(self):
        return self.possibilities

    def is_full(self, color='w'):
        return self.full if color == 'w' else self.full_black

    def fill(self, ball):
        self.full = True
        self.ball = ball
        if ball.get_color() != 'w':
            self.full_black = True

    def empty(self):
        self.full = False
        self.full_black = False
        self.ball = None

    def highlight_hole(self, color=colores['RED']):
        pygame.draw.circle(self.screen, color, self.rect.center, 50, 7)

    def update_ball(self, ball):
        self.ball = ball

    def get_ball(self):
        return self.ball
