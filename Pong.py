# Code Example 2
# Implements a general game template for games with animation
# You must use this template for all your graphical lab assignments
# and you are only allowed to inlclude additional modules that are part of
# the Python Standard Library; no other modules are allowed

import pygame
import random
from pygame.locals import *
# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((500, 400))
    # set the title of the display window
    pygame.display.set_caption('Pong ')
    # get the display surface
    w_surface = pygame.display.get_surface()
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play()
    # quit pygame and clean up the pygame window
    pygame.quit()


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True

        # === game specific objects
        self.score = [0,0]
        self.maxscore = 11

        self.ball = Ball('white', 7, [250, 200], [4, 2], self.surface)
        self.right_paddle = pygame.Rect(380, 180, 10, 50)
        self.left_paddle = pygame.Rect(100, 180, 10, 50)

        self.ball.randomize()
        pygame.key.set_repeat(20, 20)


    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()

            if self.continue_game==True:
                self.update()
                self.decide_continue()
            self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == KEYDOWN and self.continue_game == True:  # while key is pressed and game not over
                self.handle_button_pressed()

    def handle_button_pressed(self):
        # Handle each button press by moving the paddle up or down
        # - self is the Game whose events will be handled
        keys = pygame.key.get_pressed()
        paddle_speed = 15
        if keys[K_q] == True:
            self.move_paddle_up(self.left_paddle, paddle_speed)
        if keys[K_a] == True:
            self.move_paddle_down(self.left_paddle, paddle_speed)
        if keys[K_p] == True:
            self.move_paddle_up(self.right_paddle, paddle_speed)
        if keys[K_l] == True:
            self.move_paddle_down(self.right_paddle, paddle_speed)


    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color)  # clear the display surface first
        self.ball.draw()
        self.draw_score1()
        self.draw_score2()
        #self.collision()
        # self.right_paddle.draw()
        # self.left_paddle.draw()
        pygame.draw.rect(self.surface,pygame.Color('white'),self.right_paddle)
        pygame.draw.rect(self.surface, pygame.Color('white'), self.left_paddle)
        # if self.left_paddle.collidepoint(self.ball.center) and self.ball.velocity[0] < 0:
        #         self.ball.velocity[0] = - self.ball.velocity[0]
        # if self.right_paddle.collidepoint(self.ball.center) and self.ball.velocity[0] > 0:
        #         self.ball.velocity[0] = - self.ball.velocity[0]
        if self.left_paddle.collidepoint(self.ball.center) and self.ball.velocity[0] < 0:
            self.ball.velocity[0] = - self.ball.velocity[0]
        if self.right_paddle.collidepoint(self.ball.center) and self.ball.velocity[0] > 0:
            self.ball.velocity[0] = - self.ball.velocity[0]
        #self.right_paddle = pygame.draw.rect(self.surface,'white', [380, 180], [10, 50])

        #self.big_dot.draw()
        pygame.display.update()  # make the updated surface appear on the display



    def move_paddle_down(self, paddle, paddle_speed):
        # Move a paddle downwards in the window
        # - self is the Game
        # - paddle represents the paddle that will move downwards
        # - paddle_speed is the speed of the paddle

        paddle.bottom = paddle.bottom + paddle_speed
        if paddle.bottom > self.surface.get_height():
            paddle.bottom = self.surface.get_height()

    def move_paddle_up(self, paddle, paddle_speed):
        # Move a paddle upwards in the window
        # - self is the Game
        # - paddle represents the paddle that will move upwards
        # - paddle_speed is the speed of the paddle

        paddle.top = paddle.top - paddle_speed
        if paddle.top < 0:
            paddle.top = 0


    def draw_score1(self):
        # 1. Set the color
        fg_color = pygame.Color('white')
        # 2.create the font object
        font = pygame.font.SysFont('', 70)
        # 3 Create a text box by rendering the font
        text_string = '' + str(self.score[0])
        text_box = font.render(text_string, True, fg_color, self.bg_color)
        # 4 Compute the location of the text box
        location = (0, 0)
        # 5 Blit or pin the text box on the surface
        self.surface.blit(text_box, location)

    def draw_score2(self):
        # 1. Set the color
        size = self.surface.get_width()
        fg_color = pygame.Color('white')
        # 2.create the font object
        font = pygame.font.SysFont('', 70)
        # 3 Create a text box by rendering the font
        text_string = '' + str(self.score[1])
        text_box = font.render(text_string, True, fg_color, self.bg_color)
        surface_height = self.surface.get_width()
        text_box_height = text_box.get_width()
        location = (surface_height - text_box_height, 0)
        # 4 Compute the location of the text box
        #location = (430, 0)
        # 5 Blit or pin the text box on the surface
        self.surface.blit(text_box, location)


    def update(self):
        # Update the game objects.
        # - self is the Game to update'
        self.ball.move()
        if self.ball.center[0] < self.ball.radius and self.continue_game:
            self.score[1] = self.score[1] + 1
        if self.ball.center[0] + self.ball.radius > self.surface.get_size()[0] and self.continue_game:
            self.score[0] = self.score[0] + 1


    def decide_continue(self):

        if self.score[0] == self.maxscore:
            self.continue_game = False
        if self.score[1] == self.maxscore:
            self.continue_game = False


class Ball:
    # An object in this class represents a Dot that moves

    def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, surface):
        # Initialize a Dot.
        # - self is the Dot to initialize
        # - color is the pygame.Color of the dot
        # - center is a list containing the x and y int
        #   coords of the center of the dot
        # - radius is the int pixel radius of the dot
        # - velocity is a list containing the x and y components
        # - surface is the window's pygame.Surface object

        self.color = pygame.Color(dot_color)
        self.radius = dot_radius
        self.center = dot_center
        self.velocity = dot_velocity
        self.surface = surface

    def move(self):
        # Change the location of the Dot by adding the corresponding
        # speed values to the x and y coordinate of its center
        # - self is the Dot
        size = self.surface.get_size()
        for index in range(0, 2):
            self.center[index] = (self.center[index] + self.velocity[index])
            self.center[index] = self.center[index] + self.velocity[index]
            if self.center[index] < self.radius:  # left or top
                self.velocity[index] = -self.velocity[index]  # bounce the dot
            if self.center[index] + self.radius > size[index]:  # right or bottom
                self.velocity[index] = -self.velocity[index]  # bounce the dot

    def randomize(self):
        width = self.surface.get_width()
        height = self.surface.get_height()
        self.center[0] = random.randint(self.radius,width-self.radius)
        self.center[1] = random.randint(self.radius,height - self.radius)

    def draw(self):
        # Draw the dot on the surface
        # - self is the Dot

        pygame.draw.circle(self.surface, self.color, self.center, self.radius)


main()