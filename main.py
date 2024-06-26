import pygame
from utils import *
from health_bar import draw_scaled_bar

pygame.init()

win = pygame.display.set_mode((500, 500))

player = pygame.transform.scale(load_image("player.png"), (64, 64))
bullet = pygame.transform.scale(load_image("player.png"), (8, 8))

class Bullet:
    def __init__(self, player_x, shots=0):
        if shots % 2 == 0:
            self.x = player_x + 40
        elif shots % 2 == 1:
            self.x = player_x + 16
        self.y = 400
        self.vel = 5
    def draw(self, dis, img):
        dis.blit(img, (self.x, self.y))
        self.y -= self.vel

def main():
    running = True
    player_x = win.get_width() / 2
    clock = pygame.time.Clock()
    bullet_cooldown = None
    bullets = []
    shots = 0

    while running:
        win.fill((0, 0, 0))
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bullet_cooldown is None:
                    bullet_cooldown = pygame.time.get_ticks()
                    bullets.append(Bullet(player_x, shots))
                    shots += 1

        if bullet_cooldown is not None and pygame.time.get_ticks() - bullet_cooldown >= 3000:
            bullet_cooldown = None


        for i in range(len(bullets)):
            bullets[i].draw(win, bullet)

            if bullets[i].y < 0:
                bullets.remove(bullets[i])

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 10:
            player_x -= 5
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < win.get_width() - 74:
            player_x += 5


        win.blit(player, (player_x, 400))
        win.blit(draw_scaled_bar(60, 100, (64, 20)), (player_x, 470))
        pygame.display.update()
    quit()

if __name__ == "__main__":
    main()
