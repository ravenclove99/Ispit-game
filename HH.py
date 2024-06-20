import pygame
import random
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, K_s

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render("SRDJAN", True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 8

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        return Bullet((self.rect.right, self.rect.centery))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=position)
        self.speed = 10

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 36)
        self.image = self.font.render("ISPIT", True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH + 20, random.randint(0, SCREEN_HEIGHT)))
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

pygame.init()

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

player = Player()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
game_over = False
victory = False
kill_count = 0

while running:
    if game_over:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 60)
        text = font.render("Kolega Ovo Nije Dovoljno Za Prolaz", True, (255, 255, 255))
        screen.blit(text, (50, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
        continue

    if victory:
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 75)
        text = font.render("Ovo Vam Je Jedva Za Sesticu", True, (255, 255, 255))
        screen.blit(text, (50, SCREEN_HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
        continue

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_s:
                bullet = player.shoot()
                all_sprites.add(bullet)
                bullets.add(bullet)
        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    bullets.update()
    enemies.update()

    for bullet in bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
        if hit_enemies:
            bullet.kill()
            kill_count += 1
            if kill_count >= 20:
                victory = True

    if pygame.sprite.spritecollideany(player, enemies):
        game_over = True

    if random.randint(1, 50) == 1:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    font = pygame.font.Font(None, 36)
    kill_text = font.render(f"ISPITNI POENI: {kill_count}", True, (255, 255, 255))
    screen.blit(kill_text, (10, 10))

    pygame.display.update()
    pygame.time.wait(20)

pygame.time.wait(1000)
pygame.quit()
