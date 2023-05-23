import pygame


def draw_smooth_line(display, color, start_pos, end_pos, width):
    pygame.draw.circle(display, color, start_pos, width / 2)
    pygame.draw.circle(display, color, end_pos, width / 2)

    pygame.draw.line(display, color, start_pos, end_pos, width)
    return
