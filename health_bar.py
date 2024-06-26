import pygame


pygame.init()

dis = pygame.surface.Surface((8, 1))

def draw_bar(win, health, max_health):
    pixels = (health/max_health)/0.125
    pixels = pixels//1
    pygame.draw.rect(win, (255, 0, 0), (0, 0, 8, 2))
    pygame.draw.rect(win, (0, 255, 0), (0, 0, int(pixels), 2))


def draw_scaled_bar(health, max_health, scale):
    draw_bar(dis, health, max_health)
    return pygame.transform.scale(dis, scale)
