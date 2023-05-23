import pygame
from pygame.locals import *

from script.map import Map, Node
from script.line import draw_smooth_line
from script.util import get_distance
from script.path import find_path

# video setting
pygame.init()

# window config
WINDOW_SIZE = (1500, 750)
MONITOR_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)
DISPLAY_SIZE = (1000, 500)
FPS = 60

# map config
SHOW_NODES = False
NODE_RADIUS = 10
NODE_COLOR = (0, 0, 0)
NODE_OUTLINE_RADIUS = 12
NODE_OUTLINE_COLOR = (255, 255, 255)
NODE_NUM_VISIBLE_DISTANCE = 30
LINE_WIDTH = 12
DEFAULT_LINE_COLOR = (100, 100, 100)
SELECTED_PATH_LINE_COLOR = (0, 255, 0)
START_FLAG_COLOR = (255, 0, 0)
END_FLAG_COLOR = (0, 0, 255)

# font config
NODE_FONT_SIZE = 10
NODE_FONT_COLOR = (255, 255, 255)

# window setting
window = pygame.display.set_mode(WINDOW_SIZE)
display = pygame.Surface(DISPLAY_SIZE)
pygame.display.set_caption("School Nav")
clock = pygame.time.Clock()

# image
school_image = pygame.image.load("school.png")

# font
node_font = pygame.font.SysFont("arial", NODE_FONT_SIZE)

# map
node_map = (
    Map()
    # area 100: front of main building
    .add_node(Node(100, (445, 391), [101, 102]))
    .add_node(Node(101, (247, 393), [100, 200]))
    .add_node(Node(102, (640, 394), [100, 702]))
    # area 200
    .add_node(Node(200, (180, 397), [201, 101]))
    .add_node(Node(201, (177, 292), [200, 202, 301]))
    .add_node(Node(202, (177, 233), [201, 400]))
    # area 300: behind of main building
    .add_node(Node(300, (223, 290), [301, 201]))
    .add_node(Node(301, (638, 277), [300, 702]))
    # area 400
    .add_node(Node(400, (224, 233), [401, 202]))
    .add_node(Node(401, (334, 234), [400, 500]))
    # area 500
    .add_node(Node(500, (386, 231), [501, 503, 401]))
    .add_node(Node(501, (386, 166), [502, 500]))
    .add_node(Node(502, (447, 167), [503, 501]))
    .add_node(Node(503, (446, 227), [500, 502, 600]))
    # area 600
    .add_node(Node(600, (494, 224), [601, 503]))
    .add_node(Node(601, (495, 127), [602, 600]))
    .add_node(Node(602, (561, 127), [603, 601]))
    .add_node(Node(603, (626, 125), [602, 700]))
    # area 700
    .add_node(Node(700, (684, 124), [701, 603]))
    .add_node(Node(701, (718, 225), [702, 700]))
    .add_node(Node(702, (708, 355), [701, 102, 301]))
)

# flag
select = 0
start_flag = 100
end_flag = 400
paths = []

# mouse
mouse_pos = (0, 0)

running = True
while running:
    clock.tick(FPS)

    # get mouse pos at display
    """
    window_size = (W, H)
    window_mouse_pos = (X, Y)
    display_size = (w, h)
    display_mouse_pos = (x, y)
    
    x = X * w / W 
    y = Y * h / H
    => mouse_pos = (x, y)
    """
    window_mouse_pos = pygame.mouse.get_pos()
    mouse_pos = (int(window_mouse_pos[0] * DISPLAY_SIZE[0] / WINDOW_SIZE[0]), int(window_mouse_pos[1] * DISPLAY_SIZE[1] / WINDOW_SIZE[1]))

    paths = find_path(node_map, start_flag, end_flag)

    display.fill((255, 255, 255))
    display.blit(school_image, (0, (DISPLAY_SIZE[1] / 2) - (school_image.get_height() / 2)))

    path = paths[select].path
    node1 = node_map[path[0]]
    for node in path[1:]:
        node2 = node_map[node]
        draw_smooth_line(display, SELECTED_PATH_LINE_COLOR, node1.pos, node2.pos, LINE_WIDTH)
        node1 = node2
    pygame.draw.circle(display, START_FLAG_COLOR, node_map[path[0]].pos, LINE_WIDTH / 2)
    pygame.draw.circle(display, END_FLAG_COLOR, node_map[path[-1]].pos, LINE_WIDTH / 2)

    if SHOW_NODES:
        for node in node_map:
            pygame.draw.circle(display, NODE_OUTLINE_COLOR, node.pos, NODE_OUTLINE_RADIUS)
            pygame.draw.circle(display, NODE_COLOR, node.pos, NODE_RADIUS)

        for node in node_map:
            for linked_node in node:
                draw_smooth_line(display, DEFAULT_LINE_COLOR, node.pos, node_map[linked_node].pos, LINE_WIDTH)

        for node in node_map:
            if get_distance(node.pos, mouse_pos) <= NODE_NUM_VISIBLE_DISTANCE:
                node_text = node_font.render(str(node), True, NODE_FONT_COLOR)
                display.blit(node_text, (node.pos[0] - (node_text.get_width() / 2), node.pos[1] - (node_text.get_height() / 2)))

    for event in pygame.event.get():
        # close
        if event.type == QUIT:
            running = False

        # mouse event
        if event.type == MOUSEBUTTONDOWN:
            # left click
            if event.button == 1:
                print(mouse_pos)

        # keyboard event
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                select -= 1 if select >= 1 else 0
            if event.key == K_RIGHT:
                select += 1 if select != len(paths) - 1 else 0

    # screen update
    window.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    pygame.display.update()

pygame.quit()
