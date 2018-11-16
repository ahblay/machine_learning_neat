import random
import pygame
from threading import Timer


def blue_powerup_timer1():
    global gates
    gates["border_apples_on"] = True
    return


def blue_powerup_timer2():
    global gates
    gates["torus_walls"] = False
    gates["border_apples_on"] = False
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
    if r == 0:
        return blue
    return red


def random_chance():
    r = random.randint(0, 1)
    if r == 0:
        return True
    return False


def get_border_squares(board, snake):
    border = []
    for x in range(0, board["board_width"], snake["segment_width"] + snake["segment_margin"]):
        border.append((x, board["y_min"]))
        border.append((x, board["y_max"]))
    for y in range(0, board["board_height"], snake["segment_height"] + snake["segment_margin"]):
        border.append((board["x_min"], y))
        border.append((board["x_max"], y))
    return border


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.colors = {
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "red": (255, 0, 0),
            "blue": (0, 0, 255),
            "green": (0, 255, 0)
        }

        self.snake = {
            "segment_width": 15,
            "segment_height": 15,
            "segment_margin": 3,
            "x_change": 0,
            "y_change": 18
        }

        # Set height, width
        self.image = pygame.Surface([snake["segment_width"], snake["segment_height"]])

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()


class Segment(Apple):
    """ Class to represent one segment of the snake. """

    # -- Methods
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image.fill(self.colors["white"])

        # Make our top-left corner the passed-in location.
        self.rect.x = x
        self.rect.y = y


class GreenApple(Apple):
    def __init__(self):
        super().__init__()

        self.type = "green"
        self.image.fill(self.colors["green"])

        self.rand_x = random.randint(1, 900)
        self.rand_y = random.randint(1, 612)
        self.rect.x = self.rand_x - (self.rand_x % 18)
        self.rect.y = self.rand_y - (self.rand_y % 18)


class RedApple(Apple):
    def __init__(self):
        super().__init__()

        self.type = "red"

        # Set height, width
        self.image.fill(self.colors["red"])

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
        self.image.fill(self.colors["red"])

        # Make our top-left corner the passed-in location.
        self.rect.x = x
        self.rect.y = y


class BlueApple(Apple):
    def __init__(self):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image.fill(self.colors["blue"])
        self.type = "blue"

        # Make our top-left corner the passed-in location.
        self.rand_x = random.randint(1, 900)
        self.rand_y = random.randint(1, 612)
        self.rect.x = self.rand_x - (self.rand_x % 18)
        self.rect.y = self.rand_y - (self.rand_y % 18)


def initialize_snake(size, snake):
    snake_segments = []
    for i in range(size):
        x = (snake["segment_width"] + snake["segment_margin"]) * i
        y = 0
        segment = Segment(x, y)
        snake_segments.append(segment)
    return snake_segments


def spawn_apple(game, type):
    apple = None
    bad_apple = True
    while bad_apple:
        if type == "red":
            apple = RedApple()
        if type == "blue":
            apple = BlueApple()
        if type == "green":
            apple = GreenApple()
        bad_apple = apple_on_snake(apple, game["snake_segments"])
    return apple


def initialize_border_apples(border):
    border_apples = []
    for x, y in border:
        border_apples.append(BorderApple(x, y))
    return border_apples


def assess(snake, apple, rel_look):
    pixel_width = 18
    max_x = 882
    min_x = 0
    max_y = 594
    min_y = 0
    head_x = snake[0].rect.x
    head_y = snake[0].rect.y
    apple_x = apple[0].rect.x
    apple_y = apple[0].rect.y
    direction = None
    if snake[1].rect.x == head_x:
        if snake[1].rect.y > head_y:
            direction = "up"
        else:
            direction = "down"
    if snake[1].rect.y == head_y:
        if snake[1].rect.x < head_x:
            direction = "right"
        else:
            direction = "left"

    orientations = []
    if rel_look == "forward":
        orientations = ["up", "down", "right", "left"]
    if rel_look == "left":
        orientations = ["right", "left", "down", "up"]
    if rel_look == "right":
        orientations = ["left", "right", "up", "down"]

    if direction == orientations[0]:
        print(direction)
        if head_y == min_y:
            return "wall ahead"
        for seg in snake:
            if seg.rect.x == head_x and seg.rect.y + pixel_width == head_y:
                return "obstacle ahead"
        if apple_x == head_x and apple_y + pixel_width == head_y:
            return "apple ahead"
    if direction == orientations[1]:
        print(direction)
        print(head_y)
        if head_y == max_y:
            return "wall ahead"
        for seg in snake:
            if seg.rect.x == head_x and seg.rect.y - pixel_width == head_y:
                return "obstacle ahead"
        if apple_x == head_x and apple_y - pixel_width == head_y:
            return "apple ahead"
    if direction == orientations[2]:
        print(direction)
        if head_x == max_x:
            return "wall ahead"
        for seg in snake:
            if seg.rect.y == head_y and seg.rect.x - pixel_width == head_x:
                return "obstacle ahead"
        if apple_y == head_y and apple_x - pixel_width == head_x:
            return "apple ahead"
    if direction == orientations[3]:
        print(direction)
        if head_x == min_x:
            return "wall ahead"
        for seg in snake:
            if seg.rect.y == head_y and seg.rect.x + pixel_width == head_x:
                return "obstacle ahead"
        if apple_y == head_y and apple_x + pixel_width == head_x:
            return "apple ahead"
    return "all clear"


def get_state(snake, apple):

    left = assess(snake, apple, "left")
    forward = assess(snake, apple, "forward")
    right = assess(snake, apple, "right")

    state = {
        "left": left,
        "forward": forward,
        "right": right
    }

    return state

if __name__ == "__main__":

    # GLOBALS
    colors = {
        "black": (0, 0, 0),
        "white": (255, 255, 255),
        "red": (255, 0, 0),
        "blue": (0, 0, 255),
        "green": (0, 255, 0)
    }

    snake = {
        "segment_width": 15,
        "segment_height": 15,
        "segment_margin": 3,
        "x_change": 0,
        "y_change": 18
    }

    board = {
        "board_width": 900,
        "board_height": 612,
        "x_max": 882,
        "x_min": 0,
        "y_max": 594,
        "y_min": 0,
    }

    game = {
        "snake_segments": [],
        "red_apples": [],
        "green_apples": [],
        "blue_apples": [],
        "border_apples": []
    }

    info = {
        "clock": pygame.time.Clock(),
        "done": False,
        "speed": 10,
        "score": 0,
    }

    gates = {
        "torus_walls": False,
        "border_apples_on": False,
        "reversing_snake": False,
        "standard_controls": True
    }

    border = get_border_squares(board, snake)

    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create an 800x600 sized screen
    screen = pygame.display.set_mode([board["board_width"], board["board_height"]])

    # Set the title of the window
    pygame.display.set_caption('Snake')

    border_sprites = pygame.sprite.Group()
    snake_sprites = pygame.sprite.Group()
    red_apple_sprites = pygame.sprite.Group()

    # Create an initial snake
    game["snake_segments"] = initialize_snake(15, snake)
    for seg in game["snake_segments"]:
        snake_sprites.add(seg)

    # Create initial apple
    game["red_apples"].append(spawn_apple(game, "red"))
    for ra in game["red_apples"]:
        red_apple_sprites.add(ra)

    # Border apples
    game["border_apples"] = initialize_border_apples(border)

    # controls
    standard = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN}
    alternate = {"left": pygame.K_RIGHT, "right": pygame.K_LEFT, "up": pygame.K_DOWN, "down": pygame.K_UP}
    controls = standard

    while not info["done"]:

        state = get_state(game["snake_segments"], game["red_apples"])
        print(state)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                info["done"] = True

            # Set the speed based on the key pressed
            # We want the speed to be enough that we move a full
            # segment, plus the margin.
            if event.type == pygame.KEYDOWN:
                if event.key == controls["left"]:
                    snake["x_change"] = (snake["segment_width"] + snake["segment_margin"]) * -1
                    snake["y_change"] = 0
                if event.key == controls["right"]:
                    snake["x_change"] = (snake["segment_width"] + snake["segment_margin"])
                    snake["y_change"] = 0
                if event.key == controls["up"]:
                    snake["x_change"] = 0
                    snake["y_change"] = (snake["segment_height"] + snake["segment_margin"]) * -1
                if event.key == controls["down"]:
                    snake["x_change"] = 0
                    snake["y_change"] = (snake["segment_height"] + snake["segment_margin"])

        # Get rid of last segment of the snake
        # .pop() command removes last item in list
        old_segment = game["snake_segments"].pop()
        snake_sprites.remove(old_segment)

        # Figure out where new segment will be
        x = game["snake_segments"][0].rect.x + snake["x_change"]
        y = game["snake_segments"][0].rect.y + snake["y_change"]

        # Can reverse into self
        if (x, y) == (game["snake_segments"][1].rect.x, game["snake_segments"][1].rect.y):
            x = x - 2 * snake["x_change"]
            y = y - 2 * snake["y_change"]

        # Hitting the wall
        if not gates["torus_walls"]:
            if x > board["x_max"] or x < board["x_min"] or y > board["y_max"] or y < board["y_min"]:
                info["done"] = True

        if gates["torus_walls"]:
            if x > board["x_max"]:
                x = board["x_min"]
            if x < board["x_min"]:
                x = board["x_max"]
            if y > board["y_max"]:
                y = board["y_min"]
            if y < board["y_min"]:
                y = board["y_max"]

        # No snake collisions
        for seg in game["snake_segments"]:
            if (seg.rect.x, seg.rect.y) == (x, y):
                info["done"] = True

        segment = Segment(x, y)

        # Insert new segment into the list
        if not gates["reversing_snake"]:
            game["snake_segments"].insert(0, segment)
            snake_sprites.add(segment)

        # Add border apples
        if gates["border_apples_on"]:
            t2 = Timer(3, blue_powerup_timer2)
            for ba in game["border_apples"]:
                border_sprites.add(ba)
            t2.start()
            for ba in game["border_apples"]:
                if (x, y) == (ba.rect.x, ba.rect.y):
                    border_sprites.remove(ba)
                    game["border_apples"].remove(ba)
                    info["score"] += 1
                if not game["border_apples"]:
                    info["score"] += 20
                    game["border_apples"] = initialize_border_apples(border)

        if not gates["border_apples_on"]:
            border_sprites.empty()

        # If snake hits red apple logic
        for ra in game["red_apples"]:
            if (x, y) == (ra.rect.x, ra.rect.y):
                red_apple_sprites.remove(ra)

                game["snake_segments"].append(old_segment)
                snake_sprites.add(old_segment)
                info["speed"] += 3
                info["score"] += 3

                if not gates["torus_walls"]:
                    #apple_type = random_apple("blue", "red")
                    #new_apple = spawn_apple(game, apple_type)
                    new_apple = spawn_apple(game, "red")
                else:
                    new_apple = spawn_apple(game, "red")

                if new_apple.type == "red":
                    game["red_apples"].append(new_apple)
                if new_apple.type == "blue":
                    game["blue_apples"].append(new_apple)

                game["red_apples"].remove(ra)
                red_apple_sprites.add(new_apple)

        '''
                # Randomly spawn green apple
                if random_chance():
                    ga = spawn_apple(game, "green")
                    allspriteslist.add(ga)
                    game["green_apples"].append(ga)

        # If snake hits blue apple logic
        for ba in game["blue_apples"]:
            if (x, y) == (ba.rect.x, ba.rect.y):
                allspriteslist.remove(ba)

                gates["torus_walls"] = True
                t1 = Timer(7, blue_powerup_timer1)
                t1.start()

                if not gates["torus_walls"]:
                    apple_type = random_apple("blue", "red")
                    new_apple = spawn_apple(game, apple_type)
                else:
                    new_apple = spawn_apple(game, "red")

                if new_apple.type == "red":
                    game["red_apples"].append(new_apple)
                if new_apple.type == "blue":
                    game["blue_apples"].append(new_apple)

                game["blue_apples"].remove(ba)
                allspriteslist.add(new_apple)

                # Randomly spawn green apple
                if random_chance():
                    ga = spawn_apple(game, "green")
                    allspriteslist.add(ga)
                    game["green_apples"].append(ga)

        # If snake hits green apple
        for ga in game["green_apples"]:
            if (x, y) == (ga.rect.x, ga.rect.y):
                game["green_apples"].remove(ga)
                allspriteslist.remove(ga)

                if gates["standard_controls"]:
                    controls = alternate
                    standard_controls = False
                else:
                    controls = standard
                    standard_controls = True

                info["speed"] -= 3
        '''

        # -- Draw everything
        # Clear screen
        screen.fill(colors["black"])

        border_sprites.draw(screen)
        snake_sprites.draw(screen)
        red_apple_sprites.draw(screen)

        # Flip screen
        pygame.display.flip()

        #print(info["score"])

        # Pause
        info["clock"].tick(info["speed"])

    pygame.quit()
