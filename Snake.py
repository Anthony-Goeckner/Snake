import pygame
import pygame.locals as pyg
import random
pygame.init()

GRID_SIZE = 20
# extra 20 pixels added to y value of size so score does not overlap game window
SIZE = (GRID_SIZE*20, (GRID_SIZE*20) + 20)
STARTING_POSITION = GRID_SIZE / 2	
FPS = 30
SPEED = 6
FONT = pygame.font.Font('freesansbold.ttf', 20)
SCREEN = pygame.display.set_mode(SIZE)
CLOCK = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.score = 0
        self.turns_remaining = 1  # number of times you can input directions
        self.direction = 'E'  # starting direction: East
        self.positions = [(STARTING_POSITION-3, STARTING_POSITION),
                          (STARTING_POSITION-2, STARTING_POSITION),
                          (STARTING_POSITION-1, STARTING_POSITION),
                          (STARTING_POSITION, STARTING_POSITION)]
        # tells snake which way to move based on direction
        self.change_pos = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
        self.prev = None  # holds the most recent tail piece removed when the snake moves

    # loops through self.positions to draw a square for each position snake is in
    def draw(self):
        for pos in self.positions:
            x, y = pos
            pygame.draw.rect(SCREEN, (255, 255, 255), (x*GRID_SIZE, y*GRID_SIZE, 20, 20))

    # using the directions defined in self.change_pos,
    # adds a new position at the end of self.positions for the new
    # head, then removes the last section of the tail
    def move(self):
        x, y = self.change_pos[self.direction]
        prev_x, prev_y = self.positions[-1]
        self.positions.append((prev_x+x, prev_y+y))
        self.prev = self.positions.pop(0)

    # detects input from the player's keyboard, changing the direction stored for the snake
    def change_direction(self):
        keys = pygame.key.get_pressed()
        new_direction = self.direction
        # can only move up or down when facing left or right, and vice versa for the elif
        # K_UP corresponds with N', K_DOWN with 'S', etc.
        if self.direction == 'E' or self.direction == 'W':
            if keys[pyg.K_UP]:
                new_direction = 'N'
            elif keys[pyg.K_DOWN]:
                new_direction = 'S'
        elif self.direction == 'N' or self.direction == 'S':
            if keys[pyg.K_LEFT]:
                new_direction = 'W'
            elif keys[pyg.K_RIGHT]:
                new_direction = 'E'
        if self.direction != new_direction:
            self.turns_remaining = 0
        self.direction = new_direction

    # when the snake touches a fruit, the most recent tail that was removed when the snake moved on to the fruit is
    # added back to the tail of the snake
    def lengthen(self):
        self.positions.insert(0, self.prev)
        self.score += 1


class Fruit:
    def __init__(self):
        self.position = None

    def make_position(self, snake):
        pos = False
        while not pos:
            x, y = (random.randint(0, GRID_SIZE-1), random.randint(1, GRID_SIZE-1))
            if (x, y) not in snake.positions:
                self.position = (x, y)
                pos = True

    def draw(self):
        x, y = self.position
        pygame.draw.rect(SCREEN, (255, 0, 0), (x*GRID_SIZE, y*GRID_SIZE, 20, 20))


def main():
    # initialize objects
    snake = Snake()
    fruit = Fruit()
    fruit.make_position(snake)
    frame = 0
    done = False

    # game loop
    while not done:
        frame += 1
        if frame > SPEED:
            frame = 1
            snake.move()

            # check if dead to walls
            x, y = snake.positions[-1]
            if x < 0 or x > GRID_SIZE-1:
                done = True
                continue
            if y < 1 or y > GRID_SIZE-1:
                done = True

            # check if dead to self
            need_count = snake.positions[-1]
            total = 0
            for i in snake.positions:
                if i == need_count:
                    total += 1
            if total > 1:
                done = True
            
            snake.turns_remaining = 1

            # check if food eaten
            if snake.positions[-1] == fruit.position:
                snake.lengthen()
                fruit.make_position(snake)

        # kills the loop when the close button on the window is clicked
        for event in pygame.event.get():
            if event.type == pyg.QUIT:
                done = True

        # ensures inputs don't need to be frame perfect
        if snake.turns_remaining == 1:
            snake.change_direction()

        # draw things on screen
        SCREEN.fill((0, 0, 0))
        pygame.draw.rect(SCREEN, (255, 255, 255), (0, 0, SIZE[1], 20))
        snake.draw()
        fruit.draw()

        # draw score
        score_txt = 'Score: ' + str(snake.score)
        text = FONT.render(score_txt, True, (0, 0, 0), (255, 255, 255))
        SCREEN.blit(text, (0, 0))

        # draw grid
        for i in range(0, SIZE[0], 20):
            pygame.draw.line(SCREEN, (0, 0, 0), (i, 20), (i, SIZE[1]))
        for i in range(20, SIZE[1], 20):
            pygame.draw.line(SCREEN, (0, 0, 0), (0, i), (SIZE[0], i))

        # updates display and clock.tick caps frames at var FPS
        pygame.display.update()
        CLOCK.tick(FPS)

    return snake.score


score = main()
print('Your score was ' + str(score))
