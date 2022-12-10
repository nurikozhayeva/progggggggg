import pygame
import random

# colors for figures
colors = [
    (160, 210, 235),
    (229, 234, 245),
    (208, 189, 244),
    (132, 88, 179),
    (162, 128, 137),
    (128, 0, 128),
    (102, 0, 102)
]

# class for figures
class Figure:
    x = 0
    y = 0

    # potential figures that will be coming down on window
    # different positions in 4x4 matrix
    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    # function for randomly pick color and figures
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

# class for our game GameTetris
class GameTetris:
    level = 2
    score = 0
    start = "start"
    field = []
    h = 0
    w = 0
    x = 100
    y = 60
    zoom = 20
    figure = None

    # function for our game field
    def __init__(self, height, width):
        self.h = height
        self.w = width
        self.field = []
        self.score = 0
        self.start = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    # function for new figure and position
    def new_figure(self):
        self.figure = Figure(3, 0)

    # check if each block in 4X4 matrix of the current figure or not
    # and check if we can or not move or rotate the figure
    def intersect(self):
        intersection = False
        for i in range(4):
            for k in range(4):
                if i * 4 + k in self.figure.image():
                    if i + self.figure.y > self.h - 1 or \
                            k + self.figure.x > self.w - 1 or \
                            k + self.figure.x < 0 or \
                            self.field[i + self.figure.y][k + self.figure.x] > 0:
                        intersection = True
        return intersection

    # function for our score
    def break_lines(self):
        lines = 0
        for i in range(1, self.h):
            scores = 0
            for k in range(self.w):
                if self.field[i][k] == 0:
                    scores += 1
            if scores == 0:
                lines += 10
                for i1 in range(i, 1, -1):
                    for k in range(self.w):
                        self.field[i1][k] = self.field[i1 - 1][k]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersect():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersect():
            self.figure.y -= 1
            self.freeze()

    # function for freeze the game
    # check if our figures equal to figur colors then
    # it go to break lines to count our scores
    # and then will apear our new figure
    # if our intersect will get out of borders it shows us "GAMEOVER"
    def freeze(self):
        for i in range(4):
            for k in range(4):
                if i * 4 + k in self.figure.image():
                    self.field[i + self.figure.y][k + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersect():
            self.start = "GAME OVER"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersect():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersect():
            self.figure.rotation = old_rotation

pygame.init()

# night_blue = (45, 84, 94)
# night_blue_shadow = (18, 52, 59)
# sand_tan_shadow = (200, 150, 10)

night_blue = (45, 84, 94) # color for text "scores"
night_blue_shadow = (18, 52, 59)
sand_tan_shadow = (200, 150, 10)

size = (400, 500) # size of our window
screen = pygame.display.set_mode(size)

pygame.display.set_caption('Tetris')

done = False
clock = pygame.time.Clock()
fps = 30
game = GameTetris(20, 10)
counter = 0

pressing_down = False

# loop if the game figure is none then new figure will apear
# if not it counts
while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.start == "start":
            game.go_down()

    # loop fot the key event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(sand_tan_shadow)

    for i in range(game.h):
        for j in range(game.w):
            pygame.draw.rect(screen, night_blue_shadow, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])
    # fonts and text for game
    font = pygame.font.SysFont('kacstbook', 25, True, False)
    font1 = pygame.font.SysFont('kacstbook', 65, True, False)
    text = font.render("Score: " + str(game.score), True, night_blue)
    text_game_over = font1.render("GAME OVER", True, (26, 0, 0))
    text_game_over1 = font1.render("PRESS ESC", True, (51, 0, 0))

    screen.blit(text, [0, 0])
    if game.start == "GAME OVER":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
