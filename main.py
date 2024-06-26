import pygame
from utils import *
from health_bar import draw_scaled_bar
from random import choice, randint

pygame.init()
pygame.font.init()

font = pygame.font.SysFont("comicsans", 30)

win = pygame.display.set_mode((500, 500))

player = pygame.transform.scale(load_image("player.png"), (64, 64))
bullet_img = pygame.transform.scale(load_image("player.png"), (8, 8))
enemy_1 = pygame.transform.rotate(pygame.transform.scale(load_image("Enemy 1.png"), (32, 32)), 180)
enemy_2 = pygame.transform.scale(load_image("Enemy 2.png"), (32, 32))

class Enemy(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.x = randint(10, 500-32)
        self.y = 0
        self.img = choice(images)
        self.vel = 4
        self.bullet_cooldown = None
        self.rect = pygame.Rect(self.x, self.y, 32, 32)

    def draw(self, dis):
        dis.blit(self.img, (self.x, self.y))
        self.y += self.vel
        self.rect = pygame.Rect(self.x, self.y, 32, 32)  # Update the rect here
        self.shoot()

    def shoot(self):
        global bullets
        if self.bullet_cooldown is None:
            self.bullet_cooldown = pygame.time.get_ticks()
            bullets.add(Bullet(self.x + 16, self.y, 0, "enemy", pygame.transform.rotate(bullet_img, 180)))
        elif self.bullet_cooldown is not None and pygame.time.get_ticks() - self.bullet_cooldown >= 1000:
            self.bullet_cooldown = None

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y, shots=0, team="player", image=bullet_img):
        super().__init__()
        if team == "player":
            if shots % 2 == 0:
                self.x = player_x + 40
            elif shots % 2 == 1:
                self.x = player_x + 16
        elif team == "enemy":
            self.x = player_x
        self.y = player_y
        self.vel = 5
        self.team = team
        self.img = image
        self.rect = pygame.Rect(self.x, self.y, 8, 8)

    def draw(self, dis):
        dis.blit(self.img, (self.x, self.y))
        if self.team == "player":
            self.y -= self.vel
        elif self.team == "enemy":
            self.y += self.vel
        self.rect = pygame.Rect(self.x, self.y, 8, 8)  # Update the rect here
        return self.y < 0 or self.y > dis.get_height()  # Return True if the bullet is out of the game area

def main():
    global score, bullets
    score = 0
    running = True
    player_x = win.get_width() / 2
    player_vel = 5

    clock = pygame.time.Clock()
    bullet_cooldown = None
    bullets = pygame.sprite.Group()
    shots = 0
    enemy_delay = None
    enemies = pygame.sprite.Group()
    health = 100

    top_speed = 15
    dash_cooldown = None

    while running:
        win.fill((0, 0, 0))
        clock.tick(30)

        text = font.render("Score : " + str(score), True, (255, 255, 255))
        win.blit(text, (470 - text.get_width(), 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and bullet_cooldown is None:
                    bullet_cooldown = pygame.time.get_ticks()
                    bullets.add(Bullet(player_x, 400, shots, "player", bullet_img))
                    bullets.add(Bullet(player_x, 400, shots, "player", bullet_img))
                    temp = Bullet(player_x, 400, shots, "player", bullet_img)
                    temp.x = player_x + 24
                    bullets.add(temp)
                    shots += 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and dash_cooldown is None:
                    dash_cooldown = pygame.time.get_ticks()

        if dash_cooldown is not None and pygame.time.get_ticks() - dash_cooldown >= 1000:
            dash_cooldown = None

        if dash_cooldown is not None and player_vel < top_speed:
            player_vel += 1
        elif dash_cooldown is None and player_vel > 5:
            player_vel -= 1

        if bullet_cooldown is not None and pygame.time.get_ticks() - bullet_cooldown >= 1000:
            bullet_cooldown = None

        for bullet in bullets:
            if bullet.draw(win):  # If the bullet is out of the game area
                bullets.remove(bullet)

        for enemy in enemies:
            if enemy.draw(win):  # If the enemy is out of the game area
                enemies.remove(enemy)

        player_rect = pygame.Rect(player_x, 400, player_x+64, 500-74)
        for enemy in enemies:
            if enemy.rect.colliderect(player_rect):
                health -= 10
                enemies.remove(enemy)

        for bullet in bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect) and bullet.team == "player":
                    score += 1
                    enemies.remove(enemy)
                    bullets.remove(bullet)
            if bullet.team == "enemy" and bullet.rect.colliderect(player_rect):
                health -= 10
                bullets.remove(bullet)
                draw_scaled_bar(health, 100, (64, 20))

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 10:
            player_x -= player_vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < win.get_width() - 74:
            player_x += player_vel

        if enemy_delay is None or len(enemies) == 0:
            enemy_delay = pygame.time.get_ticks()
            enemy_img = [enemy_1, enemy_2]
            enemies.add(Enemy(enemy_img))

        if health <= 0:
            player_x = 100000
            go = font.render("Game Over", True, (255, 255, 255))
            win.blit(go, (250 - go.get_width() / 2, 250))

        win.blit(player, (player_x, 400))
        win.blit(draw_scaled_bar(health, 100, (64, 20)), (player_x, 470))
        pygame.display.update()
        pygame.event.pump()
    quit()

if __name__ == "__main__":
    main()