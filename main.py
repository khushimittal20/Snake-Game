import pygame
from pygame.locals import *
import time
import random
SIZE = 40
#BACKGROUND_COLOR = (47, 168, 108)

class Apple:
    def __init__(self, screen):
        self.screen = screen
        self.apple = pygame.image.load('resources/apple.png').convert()
        self.resized_apple = pygame.transform.scale(self.apple, (SIZE, SIZE))
        self.x = SIZE*3
        self.y = SIZE*3
    def draw(self):
        self.screen.blit(self.resized_apple, (self.x, self.y))
        pygame.display.flip()
    def move(self):
        max_x = self.screen.get_width() // SIZE
        max_y = self.screen.get_height() // SIZE
        self.x = random.randint(0, max_x - 1) * SIZE
        self.y = random.randint(0, max_y - 1) * SIZE

        # self.x -= random.randint(0, 17)*SIZE
        # self.y -= random.randint(0, 17)*SIZE

class Snake:
    def __init__(self, screen):
        # self.length = length
        self.screen = screen
        self.block = pygame.image.load('resources/square.png').convert()
        self.resized_block = pygame.transform.scale(self.block, (SIZE, SIZE))
        # self.x = 350
        # self.y = 350
        self.length = 1
        self.x = [SIZE]
        self.y = [SIZE]
        self.direction = 'down'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        #self.screen.fill((47, 168, 108))

        for i in range(self.length):
            self.screen.blit(self.resized_block, (self.x[i], self.y[i]))
        pygame.display.flip()
        # time.sleep(5) -> I dont want this, I want the user to hit escape or cancel

    def move_left(self):
        self.direction = 'left'
        # self.x -= 10
        # self.draw()
    def move_right(self):
        self.direction = 'right'
        # self.x += 10
        # self.draw()
    def move_up(self):
        self.direction = 'up'
        # self.y -= 10
        # self.draw()
    def move_down(self):
        self.direction = 'down'
        # self.y += 10
        # self.draw()

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        self.draw()
        # if self.x[0] < 0 or self.x[0] >= 700 or self.y[0] < 0 or self.y[0] >= 700:
        #     raise Exception("Hit the wall!")
        # for i in range(1, self.length):
        #     if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
        #         raise Exception("Ate itself!")


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Khushi's Snake And Apple Game")
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((700, 700))
        # self.surface.fill((47, 168, 108))
        self.snake= Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def collision(self, x1, y1, x2, y2):
        return x1 == x2 and y1 == y2
        # if x1 >= x2 and x1 < x2 + SIZE:
        #     if y1 >= y2 and y1 < y2 + SIZE:
        #         return True
        # return False

    def render_bg(self):
        bg=pygame.image.load('resources/background.jpg').convert()
        self.surface.blit(bg, (0, 0))
    def play(self):
        self.render_bg()
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.flip()

        #Snake colliding with Apple
        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            sound = pygame.mixer.Sound("resources/ding.mp3")
            pygame.mixer.Sound.play(sound)
            # print('Collision occurred')
            self.snake.increase_length()
            self.apple.move()
            # self.snake.length += 1
            # self.snake.x.append(-1)  # Dummy values, will be corrected in next walk
            # self.snake.y.append(-1)
        #Snake colliding with itself
        for i in range (3, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                # print('Game over')
                # exit(0)
                sound = pygame.mixer.Sound("resources/crash.mp3")
                pygame.mixer.Sound.play(sound)
                # raise "Collision Occurred"
                raise Exception("Collision Occurred")
        #Snake colliding with the boundaries
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            sound = pygame.mixer.Sound("resources/crash.mp3")
            pygame.mixer.Sound.play(sound)
            # raise "Hit the boundary error"
            raise Exception("Hit the Boundary error")

    def score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score:{self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (600,10))

    def game_over(self):
        #self.surface.fill((47, 168, 108))
        self.render_bg()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is Over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (50,300))
        line2 = font.render(f"To play again, press ENTER. To exit press ESCAPE", True, (255, 255, 255))
        self.surface.blit(line2, (50,350))

        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface)
        # self.snake.draw()
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.game_over()
                pause = True
                self.reset()

            # self.snake.walk()
            # self.apple.draw()
            # self.play()
            time.sleep(0.25)


if __name__ == "__main__":
    #Create an object of game and just run it
    game=Game()
    game.run()

