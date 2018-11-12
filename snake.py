import random
import pygame
from threading import Timer


def blue_powerup_timer1():
    global border_apples_on
    border_apples_on = True
    return


def blue_powerup_timer2():
    global torus_walls
    torus_walls = False
    global border_apples_on
    border_apples_on = False
    return


def apple_on_snake(apple, snake):
    apple_x = apple.rect.x
    apple_y = apple.rect.y

    for segment in snake:
        if (apple_x, apple_y) == (segment.rect.x, segment.rect.y):
            return True

    return False


def random_apple(blue, red):
    r = random.randint(0, 1)
    print(r)
    if r == 0:
        return blue
    return red

# --- Globals ---
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the width and height of each snake segment
segment_width = 15
segment_height = 15

# Margin between each segment
segment_margin = 3

# Set initial speed
x_change = 0
y_change = segment_height + segment_margin

# Game space
board_width = 900
board_height = 612
x_max = board_width - (segment_width + segment_margin)
x_min = 0
y_max = board_height - (segment_height + segment_margin)
y_min = 0
border = []
for x in range(0, board_width, segment_width + segment_margin):
    border.append((x, y_min))
    border.append((x, y_max))
for y in range(0, board_height, segment_height + segment_margin):
    border.append((x_min, y))
    border.append((x_max, y))


class Segment(pygame.sprite.Sprite):
    """ Class to represent one segment of the snake. """

    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])
        self.image.fill(WHITE)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([segment_width, segment_height])

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()


class RedApple(Apple):
    def __init__(self):
        super().__init__()

        self.type = "red"

        # Set height, width
        self.image.fill(RED)

        # Make our top-left corner the passed-in location.
        self.rand_x = random.randint(1, 900)
        self.rand_y = random.randint(1, 612)
        self.rect.x = self.rand_x - (self.rand_x % 18)
        self.rect.y = self.rand_y - (self.rand_y % 18)


class BorderApple(Apple):
    def __init__(self, x, y):
        super().__init__()

        self.type = "red"

        # Set height, width
        self.image.fill(RED)

        # Make our top-left corner the passed-in location.
        self.rect.x = x
        self.rect.y = y


class BlueApple(Apple):
    def __init__(self):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image.fill(BLUE)
        self.type = "blue"

        # Make our top-left corner the passed-in location.
        self.rand_x = random.randint(1, 900)
        self.rand_y = random.randint(1, 612)
        self.rect.x = self.rand_x - (self.rand_x % 18)
        self.rect.y = self.rand_y - (self.rand_y % 18)


# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([900, 612])

# Set the title of the window
pygame.display.set_caption('Snake Example')

allspriteslist = pygame.sprite.Group()
border_sprites = pygame.sprite.Group()

# Create an initial snake
snake_segments = []
for i in range(15):
    x = (segment_width + segment_margin) * i
    y = 0
    segment = Segment(x, y)
    snake_segments.append(segment)
    allspriteslist.add(segment)

# Create initial apple
apple = None
bad_apple = True
while bad_apple:
    apple = RedApple()
    bad_apple = apple_on_snake(apple, snake_segments)
allspriteslist.add(apple)

# Border apples
border_apples = []
for x, y in border:
    border_apples.append(BorderApple(x, y))

clock = pygame.time.Clock()
done = False
speed = 10

# Gates
torus_walls = False
border_apples_on = False


while not done:
    reversing_snake = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        # We want the speed to be enough that we move a full
        # segment, plus the margin.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = (segment_width + segment_margin) * -1
                y_change = 0
            if event.key == pygame.K_RIGHT:
                x_change = (segment_width + segment_margin)
                y_change = 0
            if event.key == pygame.K_UP:
                x_change = 0
                y_change = (segment_height + segment_margin) * -1
            if event.key == pygame.K_DOWN:
                x_change = 0
                y_change = (segment_height + segment_margin)

    # Get rid of last segment of the snake
    # .pop() command removes last item in list
    old_segment = snake_segments.pop()
    allspriteslist.remove(old_segment)

    # Figure out where new segment will be
    x = snake_segments[0].rect.x + x_change
    y = snake_segments[0].rect.y + y_change

    # Can reverse into self
    if (x, y) == (snake_segments[1].rect.x, snake_segments[1].rect.y):
        x = x - 2 * x_change
        y = y - 2 * y_change

    # Hitting the wall
    if not torus_walls:
        if x > x_max or x < x_min or y > y_max or y < y_min:
            done = True

    if torus_walls:
        if x > x_max:
            x = x_min
        if x < x_min:
            x = x_max
        if y > y_max:
            y = y_min
        if y < y_min:
            y = y_max

    # No snake collisions
    for seg in snake_segments:
        if (seg.rect.x, seg.rect.y) == (x, y):
            done = True

    segment = Segment(x, y)

    # Insert new segment into the list
    if not reversing_snake:
        snake_segments.insert(0, segment)
        allspriteslist.add(segment)

    # Add border apples
    if border_apples_on:
        t2 = Timer(3, blue_powerup_timer2)
        for ba in border_apples:
            border_sprites.add(ba)
        t2.start()
        for ba in border_apples:
            if (x, y) == (ba.rect.x, ba.rect.y):
                print("ATE border apple")
                border_sprites.remove(ba)
                border_apples.remove(ba)
                speed = speed + 1

    if not border_apples_on:
        border_sprites.empty()

    # If snake hits apple logic
    if (x, y) == (apple.rect.x, apple.rect.y):
        allspriteslist.remove(apple)

        if apple.type == "red":
            snake_segments.append(old_segment)
            allspriteslist.add(old_segment)
            speed = speed + 1

        if apple.type == "blue":
            torus_walls = True
            t1 = Timer(7, blue_powerup_timer1)
            t1.start()

        apple = None
        bad_apple = True

        while bad_apple:
            if torus_walls:
                apple = random_apple(BlueApple(), RedApple())
            else:
                apple = RedApple()
            bad_apple = apple_on_snake(apple, snake_segments)

        allspriteslist.add(apple)


    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)

    border_sprites.draw(screen)
    allspriteslist.draw(screen)

    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(speed)

pygame.quit()
