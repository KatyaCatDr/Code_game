import pygame
import random

WIDTH = 360
HEIGHT = 650
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # создаём экземпляр класса экран
pygame.display.set_caption('Flappy bird')
clock = pygame.time.Clock() # отсчёты времени (FPS)

bg = pygame.image.load('img/bg.png') # ИЗОБРАЖЕНИЕ ФОНА
ground = pygame.image.load('img/ground.png') # изб земли
ground_x = 0
button = pygame.image.load('img/restart.png')
button_rect = button.get_rect()
button_rect.topleft = 100, 300
score = 0
font = pygame.font.Font('game_font.ttf', 25)
text = font.render(f'Score: {int(score)}', True, (255, 255, 255))
text_rect = text.get_rect()
text_rect.topleft = 0, 0

def count_score():
    global score
    if not game_over:
        score += 0.1
    elif game_over:
        score = score

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, position: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - 75]
        if position == -1:
            self.rect.bottomleft = [x, y + 75]

    def update(self):
        self.rect.x -= 1

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.velocity = 0.1
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
    def update(self):
        global game_over
        if not game_over:
            self.counter += 1
            self.bird_time = 5
            if self.counter > self.bird_time:
                self.counter = 0
                self.index += 1
                if self.index > 2:
                    self.index = 0
            self.image = self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity * -3)
            self.velocity += 0.2
            # self.rect.y += 1.5
            self.rect.y += self.velocity
            if self.rect.y > 536:
                self.rect.y = 536
                self.velocity = 0
                game_over = True
            if not game_over:
            # space click
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    if self.rect.y >= 50:
                        self.velocity = -3

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
flappy1 = Bird(50, HEIGHT // 2)
bird_group.add(flappy1)
last_pipe = pygame.time.get_ticks()
pipe_freq = 5000

game_over = False
running = True
while running:
    '''Игровой цикл'''
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # условие нажатие накрестик
            running = False

    ground_x = ground_x - 2
    if ground_x <= -500:
        ground_x = 0
    screen.blit(bg, (0, 0))

    time_now = pygame.time.get_ticks()
    if pipe_freq < time_now - last_pipe:
        pipe_height = random.randint(-100, 250)
        top_pipe = Pipe(WIDTH, HEIGHT // 2 + pipe_height + 400, -1)
        bot_pipe = Pipe(WIDTH, HEIGHT // 2 + pipe_height - 200, 1)
        last_pipe = time_now
        pipe_group.add(top_pipe, bot_pipe)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, True):
        game_over = True

    if score == 80:
        pipe_freq -= 4500
           #pipe_freq = pipe_freq

    pipe_group.draw(screen)
    pipe_group.update()

    bird_group.draw(screen)
    bird_group.update()
    text = font.render(f'Score: {int(score)}', True, (255, 255, 255))
    count_score()
    screen.blit(text, text_rect)
    screen.blit(ground, (ground_x, 570))
    if game_over:
        screen.blit(button, button_rect)
        score = 0
        top_pipe.kill()
        bot_pipe.kill()

    if pygame.mouse.get_pressed()[0] == 1:
        game_over = False
    pygame.display.flip() # обновление экрана

pygame.quit()
