import pygame
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Doodle py')

clock = pygame.time.Clock()
background = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
jump_line = pygame.draw.line(background, 'red', (0, 375), (600, 375))
start_time = 0


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        height_player = 50
        width_player = 50
        self.gravity = 0
        self.image = pygame.surface.Surface((width_player, height_player))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT-50)
        self.image.fill('red')

    def update(self):
        self.gravity += 1
        self.rect.bottom += self.gravity
        if self.rect.top >= 375:
            self.rect.top = 375

    def movement(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.left -= 5
            if self.rect.left < -10:
                self.rect.left = SCREEN_WIDTH + 10
        if keys[pygame.K_RIGHT]:
            self.rect.right += 5
            if self.rect.right > SCREEN_WIDTH + 10:
                self.rect.right = -10
        if keys[pygame.K_SPACE]:
            self.gravity = -20


class Platform(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        height_platform = 10
        width_platform = 100
        x_platform = random.randint(50, SCREEN_WIDTH-50)
        self.image = pygame.surface.Surface((width_platform, height_platform))
        self.rect = self.image.get_rect()
        self.rect.center = (x_platform, -100)
        self.image.fill('blue')

    def update(self):
        self.rect.bottom += 10
        if self.rect.top >= SCREEN_HEIGHT + 5:
            self.kill()


platforms = pygame.sprite.Group()
player = Player()


def spawn_platform():
    global platforms, start_time
    break_time = int(pygame.time.get_ticks() / 100) - start_time
    if break_time >= 3:
        platform = Platform()
        platforms.add(platform)
        start_time = int(pygame.time.get_ticks() / 100)


def collision_platform(platf):
    if player.rect.colliderect(platf.rect) and player.gravity > 0:
        player.gravity = -25


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    input_key = pygame.key.get_pressed()
    spawn_platform()
    screen.blit(background, (0, 0))
    screen.blit(player.image, player.rect)
    platforms.draw(screen)
    player.update()
    player.movement(input_key)
    for i in platforms:
        collision_platform(i)
    pygame.display.update()
    clock.tick(60)
    pygame.display.flip()
