import pygame
import random

# Initializing pygame
pygame.init()

# Setting up the window
Width, Height = 1000, 650
window = pygame.display.set_mode ((Width, Height))
pygame.display.set_caption("Fruit Collecter")

# Background image
backgroundImg = pygame.image.load('images/background.png').convert()
backgroundImg = pygame.transform.scale(backgroundImg, (1000, 600))

# Floor image
floorImg = pygame.image.load('images/floor.png').convert()
floorImg = pygame.transform.scale(floorImg, (1000, 200))

# Global variables
score = 0
apples_needed = 10
icon_fruit = pygame.image.load('images/apple.png').convert_alpha()
score_font = pygame.font.SysFont('Arial', 50)
game_over_font = pygame.font.SysFont('Arial', 100)
level = 1

# Timer for reducing the width of the rect
timer = 200
timer_event = pygame.USEREVENT
pygame.time.set_timer(timer_event, 10000)

# Boolean values
valid = True
timer_valid = True
won_screen = True


class Player(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, speed):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.speed = speed
        self.x_pos = x_pos
        self.y_pos = y_pos

    def update(self):
        self.boundaries()

        mouse = pygame.mouse.get_pos()
        self.rect.centerx = mouse[0]

    def boundaries(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= Width:
            self.rect.right = Width


class Fruit(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, y_speed):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.y_speed = y_speed

    def update(self):
        self.rect.centery += self.y_speed

        if self.rect.centery >= 700:
            self.kill()


class Rotten_fruit(pygame.sprite.Sprite):
    def __init__(self, path, x, y, speed):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.y_speed = speed

    def update(self):
        self.rect.centery += self.y_speed


# Increasing levels and game over screen and winner screen
def levels():
    global level, level_can, apples_needed, timer, score, valid, spawn_rotten_apple, won_screen

    # Checking for level increased and if that is true then increase the apples needed

    if level == 1:
        apples_needed = 10

    if level == 2:
        apples_needed = 15

    if level == 3:
        apples_needed = 20

    if level == 4:
        apples_needed = 25

    if level == 5:
        apples_needed = 30

    if level == 6:
        apples_needed = 35

    if level == 7:
        apples_needed = 40

        # This is the last level and if this is cleared then display you won and set the game to false and restart it
        if score >= 40:
            won_screen = False
            win_text = game_over_font.render('You won', True, (255, 0, 0))
            window.blit(win_text, (150, 300))
            valid = False

    # If score is more than apples needed then increase the level, reset the timer and score
    if score >= apples_needed:
        if won_screen is True:
            level += 1
            timer = 200
            score = 0

    # if time is reached and you cannot get the apples needed then game is not running and
    # restart it and display game over
    if timer <= 0 and score <= apples_needed:
        valid = False
        end_screen()


# Displaying this when the game is over and valid is False
def end_screen():
    # Displaying this when it is game over and apples needed is not reached
    game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
    window.blit(game_over_text, (150, 300))


# Displaying the text
def displaying_text():
    pygame.draw.rect(window, (0, 0, 0), (750, 40, 200, 30))
    pygame.draw.rect(window, (0, 255, 0), (750, 40, timer, 30))
    timer_font = score_font.render('Time: ', True, (255, 255, 255))
    window.blit(timer_font, (600, 40))

    window.blit(icon_fruit, (10, 10))
    score_text = score_font.render(f'{score}', True, (255, 255, 255))
    window.blit(score_text, (80, 20))

    apples_text = score_font.render(f'Needed:{apples_needed}', True, (255, 255, 255))
    window.blit(icon_fruit, (10, 80))
    window.blit(apples_text, (80, 90))

    level_text = score_font.render(f' Level: {level}', True, (255, 255, 255))
    window.blit(level_text, (10, 160))


# Player group
player = Player('images/shopping-cart.png', 470, 500, 20)
player_group = pygame.sprite.GroupSingle(player)

# Fruit group
fruit_group = pygame.sprite.Group()
fruit_event = pygame.USEREVENT
pygame.time.set_timer(fruit_event, 700)

# Timer for spawning the rotten apple
time = pygame.USEREVENT + 1
pygame.time.set_timer(time, 2500)
rotten_fruit_group = pygame.sprite.Group()

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Event for spawning apples when the userevent is triggered by the timer
        if event.type == fruit_event:
            x_pos = random.randrange(0, 1000)
            y_pos = random.randrange(-500, -50)
            y_speed = 10
            fruit = Fruit('images/apple.png', x_pos, y_pos, y_speed)
            fruit_group.add(fruit)

        # Event for spawning rotten apples when the userevent is triggered
        if event.type == time:
            x = random.randrange(100, 900)
            y = random.randrange(-500, -50)
            speed = 10
            rotten_fruit = Rotten_fruit('images/rotten apple.png', x, y, speed)
            rotten_fruit_group.add(rotten_fruit)

        # When this is triggered then reduce the time
        if valid:
            if event.type == timer_event:
                timer -= 4

    # getting keys
    keys = pygame.key.get_pressed()

    # If valid is False and this key is pressed restart the game
    if keys[pygame.K_SPACE] and valid is False:
        valid = True
        level = 1
        score = 0
        timer = 200
        fruit_group.empty()
        rotten_fruit_group.empty()

    window.fill((0, 0, 0))

    # Background
    window.blit(backgroundImg, (0, 0))

    # Calling the text function
    displaying_text()

    # If the game is running this will display
    if valid:

        # Fruit
        fruit_group.draw(window)
        fruit_group.update()

        # Rotten fruit
        rotten_fruit_group.draw(window)
        rotten_fruit_group.update()

        # Player(cart)
        player_group.draw(window)
        player_group.update()

        # Collision between player and fruit
        if pygame.sprite.spritecollide(player_group.sprite, fruit_group, True):
            score += 1

        # Collision between player and rotten fruit
        if pygame.sprite.spritecollide(player_group.sprite, rotten_fruit_group, True):
            score -= 1

    # Calling the levels functions
    levels()

    # Displaying the floor
    window.blit(floorImg, (0, 550))

    # Frame rate and updating the window
    clock.tick(60)
    pygame.display.update()
