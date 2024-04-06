import pygame
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Doodle py')

font = pygame.font.Font('FONT/DoodleJump.ttf', 75)
font2 = pygame.font.Font('FONT/DoodleJump.ttf', 50)
clock = pygame.time.Clock()
background = pygame.transform.rotozoom(pygame.image.load('Assets/background.png'), 0, 1.5)
jump_line = pygame.draw.line(screen, 'red', (0, 375), (600, 375))
start_time = 0
game_start = True
list_pos = [100, 150, 200, 250, 300, 350, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950]
game_run = True
score = 0
game_over_txt = font.render('Game Over !', True, 'red')
game_over_txt_rect = game_over_txt.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
restart_txt = font2.render('press SPACE to restart', True, 'black')
restart_txt_rect = restart_txt.get_rect(center=(SCREEN_WIDTH/2, 450))


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.gravity = 0
        self.player1 = pygame.transform.rotozoom(pygame.image.load('Assets/player.png'), 0, 0.1)
        self.player2 = pygame.transform.rotozoom(pygame.image.load('Assets/player2.png'), 0, 0.1)
        self.image = self.player1
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)

    def update(self):
        global game_run
        self.gravity += 0.5
        self.rect.bottom += self.gravity
        if self.rect.clipline((-50, 175), (700, 175)):
            self.rect.top = 175
        if self.rect.top >= SCREEN_HEIGHT:
            game_run = False

    def movement(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.left -= 5
            self.image = self.player2
            if self.rect.left < -10:
                self.rect.left = SCREEN_WIDTH + 10
        if keys[pygame.K_RIGHT]:
            self.image = self.player1
            self.rect.right += 5
            if self.rect.right > SCREEN_WIDTH + 10:
                self.rect.right = -10


class Platform(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        x_platform = random.randint(50, SCREEN_WIDTH-50)
        self.image = pygame.transform.rotozoom(pygame.image.load('Assets/plaform.png'), 0, 0.5)
        self.rect = self.image.get_rect()
        self.rect.center = (x_platform, -50)

    def update(self):
        global score
        self.rect.bottom += 10
        score += 0.1
        if self.rect.top >= SCREEN_HEIGHT + 5:
            self.kill()


platforms = pygame.sprite.Group()
player = Player()


def spawn_platform():
    global platforms, start_time
    break_time = int(pygame.time.get_ticks() / 100) - start_time
    platform = Platform()
    if player.rect.clipline((-50, 175), (700, 175)):
        platforms.update()
        player.update()
        for _ in range(5):
            if break_time >= 3:
                platforms.add(platform)
                start_time = int(pygame.time.get_ticks() / 100)


def collition_platform(platf):
    if player.rect.colliderect(platf.rect) and player.gravity > 0:
        player.gravity = -15


def first_platform():
    global game_start
    for _ in list_pos:
        platfrm = Platform()
        platforms.add(platfrm)
        platfrm.rect.bottom += _
    game_start = False


platform = Platform()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if not game_run:
            if event.type == pygame.KEYDOWN:
                game_run = True
                score = 0
                game_start = True
                pygame.sprite.Group.empty(platforms)
                player.rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50)

    if game_run:
        score_txt = font.render(str(round(score)), True, 'black')
        score_txt_rect = score_txt.get_rect(center=(300, 150))

        if game_start:
            first_platform()
        input_key = pygame.key.get_pressed()
        spawn_platform()
        screen.blit(background, (0, 0))
        screen.blit(player.image, player.rect)
        platforms.draw(screen)
        screen.blit(score_txt, score_txt_rect)
        player.update()
        player.movement(input_key)
        for i in platforms:
            collition_platform(i)

    else:
        game_over_score_txt = font2.render(f'Score : {round(score)}', True, 'black')
        game_over_score_txt_rect = game_over_score_txt.get_rect(center=(SCREEN_WIDTH / 2, 300))
        screen.blit(background, (0, 0))
        screen.blit(game_over_score_txt, game_over_score_txt_rect)
        screen.blit(game_over_txt, game_over_txt_rect)
        screen.blit(restart_txt, restart_txt_rect)
    pygame.display.update()
    clock.tick(65)
