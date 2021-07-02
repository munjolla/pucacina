import pygame, sys, random


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.shields = 5
        self.shield_surface = pygame.image.load('shield.png')

    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        self.screen_constrain()
        self.display_shields()

    def screen_constrain(self):
        if self.rect.right >= 1280:
            self.rect.right = 1280
        if self.rect.left <= 0:
            self.rect.left = 0

    def display_shields(self):
        for index, shield in enumerate(range(self.shields)):
            screen.blit(self.shield_surface, (10 + index * 40, 10))


class Meteor(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos, x_speed, y_speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.x_speed = x_speed
        self.y_speed = y_speed

    def update(self):
        self.rect.centerx += self.x_speed
        self.rect.centery += self.y_speed

        if self.rect.centery >= 800:
            self.kill()


class Laser(pygame.sprite.Sprite):
    def __init__(self, path, pos, speed):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def update(self):
        self.rect.y -= self.speed
        if self.rect.centery <= -100:
            self.kill()


pygame.init()  # initiate pygame
screen = pygame.display.set_mode((1280, 720))  # Create display surface
clock = pygame.time.Clock()  # Create clock object

spaceship = SpaceShip('spaceship.png', 640, 500)
spaceship_group = pygame.sprite.GroupSingle()
spaceship_group.add(spaceship)

laser_group = pygame.sprite.Group()

meteor_group = pygame.sprite.Group()
METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT, 150)

while True:  # Game loop
    for event in pygame.event.get():  # Check for events / Player input
        if event.type == pygame.QUIT:  # Close the game
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            new_laser = Laser('Laser.png', spaceship_group.sprite.rect.center, 15)
            laser_group.add(new_laser)

        if event.type == METEOR_EVENT:
            random_meteor_image = random.choice(('Meteor1.png', 'Meteor2.png', 'Meteor3.png'))
            random_x_pos = random.randrange(0, 1280)
            random_y_pos = random.randrange(-600, -40)
            random_speed_y = random.randint(3, 10)
            random_speed_x = random.randint(-1, 1)
            meteor = Meteor(random_meteor_image, random_x_pos, random_y_pos, random_speed_x, random_speed_y, )
            meteor_group.add(meteor)

    screen.fill((42, 45, 51))

    laser_group.draw(screen)
    spaceship_group.draw(screen)
    meteor_group.draw(screen)

    laser_group.update()
    spaceship_group.update()
    meteor_group.update()

    pygame.display.update()  # Draw frame
    clock.tick(120)  # Control the framerate