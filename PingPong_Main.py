import pygame
import random
import csv
import you_won

pygame.init()
you_lost_font = pygame.font.SysFont("calibri", 30, bold=True)

class Block:
    dim = 20

    def __init__(self, x, y, bonus=None):
        self.x = x
        self.y = y
        self.x_mid = self.x + self.dim // 2
        self.y_mid = self.y + self.dim // 2
        self.bonus = bonus
        if self.bonus is not None:
            self.color = bonuses[bonus]["color"]
        else:
            self.color = (0, 0, 0)

    def csv_data(self):
        block_data = {"x": self.x, "y": self.y, "bonus": self.bonus}
        return block_data

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.dim, self.dim))


class Racket:
    height = 10
    color = (0, 0, 255)
    init_width = 80

    def __init__(self):
        self.pos = screen_width//2
        self.width = self.init_width
        self.speed = 2
        self.imp_area_num = 3
        self.imp_area_len = self.width // self.imp_area_num

    def draw(self):
        pygame.draw.rect(win, self.color, (self.pos - self.width//2, screen_height - self.height, self.width, self.height))

    def move(self, dir):
        global first_move
        if not first_move:
            first_move = True
        if dir == "L":
            if self.pos - self.width//2 > 0:
                self.pos -= self.speed
        if dir == "R":
            if self.pos + self.width//2 < screen_width:
                self.pos += self.speed


class FallingBonus:

    def __init__(self, x, y, bonus):
        self.bonus = bonus
        self.x = x
        self.y = y
        self.color = {}
        self.dim = 10

    def move(self):
        self.y += 1
        if self.y > screen_height:
            falling_bonuses.pop(falling_bonuses.index(self))

    def draw(self):
        pygame.draw.rect(win, bonuses[self.bonus]["color"], (self.x, self.y, self.dim, self.dim))

    def __repr__(self):
        return self.bonus


class Bullet:
    dim = 5

    def __init__(self):
        self.x = racket.pos - self.dim // 2
        self.y = screen_height - racket.height
        self.speed = 1
        self.clor = (0, 0, 0)

    def move(self):
        self.y -= self.speed

        for block in blocks:
            if block.y + block.dim > self.y and block.x <= self.x + self.dim // 2 <= block.x + block.dim:
                hit_block = blocks.pop(blocks.index(block))
                if block.bonus is not None:
                    falling_bonuses.append(FallingBonus(hit_block.x, hit_block.y, hit_block.bonus))
                bullets.pop(bullets.index(self))
                return
        if self.y < 0:
            bullets.pop(bullets.index(self))
            return

    def draw(self):
        pygame.draw.rect(win, self.clor, (self.x, self.y, self.dim, self.dim))


class Ball:
    rad = 10

    def __init__(self, x_pos, y_pos, x_vel, y_vel):
        self.cor_col_rad = self.rad - 2
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = 1
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = (255, 0, 0)

    def __repr__(self):
        return "x_pos: " + str(self.x_pos) + " y_pos: " + str(self.y_pos) + " x_vel: " + str(self.x_vel) + " y_vel: " + str(self.y_vel)

    def draw(self):
        # pygame.draw.rect(win, (0, 255, 0), (self.x_pos - self.rad, self.y_pos - self.rad, self.rad * 2, self.rad * 2))
        pygame.draw.circle(win, self.color, (int(self.x_pos), int(self.y_pos)), self.rad)

    def move(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        self.bounce()

    def bounce(self):
        x_bounce = False
        y_bonce = False
        for block in blocks:

            # bounce form block walls
            if (self.x_pos + self.rad == block.x or self.x_pos + self.rad == block.x + 1) and\
                    (self.y_pos - self.rad <= block.y <= self.y_pos + self.rad or
                     self.y_pos - self.rad <= block.y + block.dim <= self.y_pos + self.rad)\
                    and self.x_vel > 0:
                if not x_bounce:
                    x_bounce = True
                    self.x_vel *= -1
                    if block in blocks:
                        hit_block = blocks.pop(blocks.index(block))
                        if block.bonus is not None:
                            falling_bonuses.append(FallingBonus(hit_block.x, hit_block.y, hit_block.bonus))

            if (self.x_pos - self.rad == block.x + block.dim or self.x_pos - self.rad == block.x + block.dim - 1) and\
                    (self.y_pos - self.rad <= block.y <= self.y_pos + self.rad or
                     self.y_pos - self.rad <= block.y + block.dim <= self.y_pos + self.rad)\
                    and self.x_vel < 0:
                if not x_bounce:
                    x_bounce = True
                    self.x_vel *= -1
                    if block in blocks:
                        hit_block = blocks.pop(blocks.index(block))
                        if block.bonus is not None:
                            falling_bonuses.append(FallingBonus(hit_block.x, hit_block.y, hit_block.bonus))

            if (self.y_pos + self.rad == block.y or self.y_pos + self.rad == block.y + 1) and\
                    (self.x_pos - self.rad <= block.x <= self.x_pos + self.rad or
                     self.x_pos - self.rad <= block.x + block.dim <= self.x_pos + self.rad)\
                    and self.y_vel > 0:
                if not y_bonce:
                    y_bonce = True
                    self.y_vel *= -1
                    if block in blocks:
                        hit_block = blocks.pop(blocks.index(block))
                        if block.bonus is not None:
                            falling_bonuses.append(FallingBonus(hit_block.x, hit_block.y, hit_block.bonus))

            if (self.y_pos - self.rad == block.y + block.dim or self.y_pos - self.rad == block.y + block.dim - 1)\
                    and (self.x_pos - self.rad <= block.x <= self.x_pos + self.rad or
                         self.x_pos - self.rad <= block.x + block.dim <= self.x_pos + self.rad)\
                    and self.y_vel < 0:
                if not y_bonce:
                    y_bonce = True
                    self.y_vel *= -1
                    if block in blocks:
                        hit_block = blocks.pop(blocks.index(block))
                        if block.bonus is not None:
                            falling_bonuses.append(FallingBonus(hit_block.x, hit_block.y, hit_block.bonus))


        # bounce from racket
        if self.y_pos + self.rad == screen_height - racket.height and self.y_vel > 0 and racket.pos - racket.width // 2 < self.x_pos < racket.pos + racket.width // 2:
            if racket.pos - racket.width // 2 < self.x_pos < racket.pos - racket.imp_area_len // 2:
                if self.x_vel == -2:
                    pass
                elif self.x_vel == -1:
                    self.x_vel = -2
                elif self.x_vel == 1:
                    self.x_vel = -1
                elif self.x_vel == 2:
                    self.x_vel = 1
            if racket.pos + racket.imp_area_len // 2 < self.x_pos < racket.pos + racket.width // 2:
                if self.x_vel == 2:
                    pass
                elif self.x_vel == 1:
                    self.x_vel = 2
                elif self.x_vel == -1:
                    self.x_vel = 1
                elif self.x_vel == -2:
                    self.x_vel = -1

            if abs(self.x_vel) == 2:
                self.y_vel = -1
            else:
                self.y_vel = -2


        # bounce form screen edge
        if self.x_pos - self.rad <= 0 or self.x_pos + self.rad >= screen_width:
            self.x_vel *= -1
        if self.y_pos - self.rad <= 0 or self.y_pos + self.rad >= screen_height:
            self.y_vel *= -1

        # pop if touches bottom
        if bonuses["bottom_wall"]["time_left"] == 0:
            if self.y_pos + self.rad == screen_height:
                balls.pop(balls.index(self))
                return


screen_width = 25 * Block.dim
screen_height = 25 * Block.dim
offset = 8 * Block.dim
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PingPong by Kuba")


def add_block(x, y):
    x = x // Block.dim * Block.dim
    y = y // Block.dim * Block.dim
    if y > screen_height - offset:
        return
    for block in blocks:
        if block.x == x and block.y == y:
            # blocks.pop(blocks.index(block))
            return
    if with_bonus:
        bonus = random.choice(list(bonuses.keys()) + [None] * 2)
    else:
        bonus = None
    blocks.append(Block(x, y, bonus))


def add_ball(x_vel=None):
    global balls
    if x_vel is None:
        x_vel = random.choice([-2, -1, 1, 2])
    if x_vel == 1 or x_vel == -1:
        y_vel = 2
    else:
        y_vel = 1
    if racket.pos % 2 == 0:
        x_pos = racket.pos
    else:
        x_pos = racket.pos + 1
    y_pos = screen_height - racket.height - Ball.rad - y_vel
    balls.append(Ball(x_pos, y_pos, x_vel, y_vel))
    # print(balls[-1])


def check_if_lost_or_wan():
    global lost
    global won
    global game_state
    global restart
    if not blocks:
        won = True
        print("You Won")
        if not game_state == "won level":
            won = False
            restart = True
            game_state = "won level"
        return
    if not balls and not falling_bonuses and not bullets:
        lost = True
        print("YOU LOST")


def check_if_bonus():
    global bonuses
    # print("falling bonuses ->" + str(falling_bonuses))
    for falling_bonus in falling_bonuses:
        if falling_bonus.y + falling_bonus.dim > screen_height - Racket.height and racket.pos - racket.width // 2 < falling_bonus.x+falling_bonus.dim//2 < racket.pos + racket.width // 2:
            falling_bonuses.pop(falling_bonuses.index(falling_bonus))
            # print("bonus caught")
            if bonuses[falling_bonus.bonus]["time_left"] is not None:
                bonuses[falling_bonus.bonus]["time_left"] = bonuses[falling_bonus.bonus]["init_time"]
            else:
                if falling_bonus.bonus == "add_ball":
                    add_ball()
                elif falling_bonus.bonus == "extra_width":
                    racket.width += 2

    if bonuses["pistol"]["time_left"] > 0 and bonuses["pistol"]["time_left"] % 200 == 0:
        bullets.append(Bullet())


def draw():
    win.fill((255, 255, 255))
    for block in blocks:
        block.draw()
    for bullet in bullets:
        bullet.draw()
    for falling_bonus in falling_bonuses:
        falling_bonus.draw()
    for ball in balls:
        ball.draw()
    racket.draw()
    if bonuses["bottom_wall"]["time_left"] > 0:
        pygame.draw.rect(win, Racket.color, (0, screen_height - racket.height // 2, screen_width, 10))

    # text over the racket
    if won and game_state == "won level":
        text1 = "You won"
        text2 = "    for real this time"
        text_color = (0, 204, 0)
    elif game_state == "won level":
        text1 = "You won"
        text2 = ""
        text_color = (0, 204, 0)
    elif lost:
        text1 = "You lost"
        text2 = "To try again press r"
        text_color = (255, 51, 51)
    elif game_state == "level maker":
        text1 = "Draw your own level"
        text2 = "press s to save it, r to play it"
        text_color = (255, 51, 51)
    elif game_state == "game" and not first_move:
        text1 = "Move to play"
        text2 = "press l to make new level"
        text_color = (0, 0, 0)
    else:
        text1 = ""
        text2 = ""
        text_color = (255, 255, 255)

    rendered_text1 = you_lost_font.render(text1, True, text_color)
    rendered_text2 = you_lost_font.render(text2, True, text_color)
    win.blit(rendered_text1, (screen_width // 2 - 70, screen_height - 120))
    win.blit(rendered_text2, (screen_width // 2 - 150, screen_height - 80))


    pygame.display.update()


def time_pass():
    for ball in balls:
        ball.move()
    for f_bonus in falling_bonuses:
        f_bonus.move()
    for bullet in bullets:
        bullet.move()

    #  retract time from bonus time left
    for bonus in bonuses.keys():
        if bonuses[bonus]["time_left"] is not None:
            if bonuses[bonus]["time_left"] > 0:
                bonuses[bonus]["time_left"] -= time_delay
            else:
                bonuses[bonus]["time_left"] = 0


def save_level():
    with open("level.csv", "w") as level_csv:
        fields = ['x', 'y', 'bonus']
        log_writer = csv.DictWriter(level_csv, fieldnames=fields)

        log_writer.writeheader()
        for block in blocks:
            block_csv = block.csv_data()
            log_writer.writerow(block_csv)


def load_level():
    try:
        with open("level.csv") as level_csv:
            block_reader = csv.DictReader(level_csv)
            for block in block_reader:
                if block["bonus"] == "":
                    block["bonus"] = None
                blocks.append(Block(int(block["x"]), int(block["y"]), block["bonus"]))
    except FileNotFoundError:
        global game_state
        game_state = "level maker"

bonuses = {}
def init_bonuses():
    global bonuses
    bonus_names = ["bottom_wall", "extra_width", "add_ball", "pistol"]
    bonus_colors = [(51, 153, 255), (204, 204, 0), (51, 255, 153), (192, 192, 192)]
    bonus_time = [0, None, None, 0]
    bonus_init_time = [50 * 60, None, None, 15 * 60]
    for i in range(len(bonus_names)):
        bonuses[bonus_names[i]] = {"color": bonus_colors[i], "time_left": bonus_time[i], "init_time": bonus_init_time[i]}
    print(bonuses)



racket = Racket()
blocks = []
balls = []
falling_bonuses = []
bullets = []


print(balls)

with_bonus = True
run = True
time_delay = 10
restart = True
pygame.key.set_repeat(2, 1)
init_bonuses()
key_pressed = False
game_state = "game"
while run:
    if restart:
        restart = False
        lost = False
        first_move = False
        racket.width = Racket.init_width
        racket.pos = screen_width // 2
        balls.clear()
        bullets.clear()
        falling_bonuses.clear()
        if game_state == "won level" and won:
            game_state = "game"
        won = False
        for bonus in bonuses.keys():
            bonuses[bonus]["time_left"] = 0
        add_ball(1)
        if game_state == "game":
            blocks.clear()
            load_level()
        elif game_state == "level maker" and blocks:
            game_state = "game"
        elif game_state == "won level":
            blocks.clear()
            for block_data in you_won.you_won_save_str:
                blocks.append(Block(block_data[0], block_data[1], block_data[2]))
            bonuses["bottom_wall"]["time_left"] = 60 * 60 * 100

        print(game_state)


    pygame.time.delay(time_delay)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


        if event.type == pygame.KEYUP:
            key_pressed = False
        # buttons without hold
        if event.type == pygame.KEYDOWN and not key_pressed:
            key_pressed = True
            if event.key == pygame.K_r:
                restart = True
                print("restart")
            elif event.key == pygame.K_l and not game_state == "level maker":
                game_state = "level maker"
                blocks.clear()
                print("level maker")
            elif event.key == pygame.K_s and game_state == "level maker":
                save_level()
                restart = True
            elif event.key == pygame.K_b:
                add_ball()
                lost = False

        # buttons with hold
        if event.type == pygame.KEYDOWN:
            key_pressed = True
            if event.key == pygame.K_LEFT:
                racket.move("L")
            elif event.key == pygame.K_RIGHT:
                racket.move("R")

    if game_state == "level maker":
        mouse_pos = pygame.mouse.get_pos()
        mouse_but = pygame.mouse.get_pressed()
        if mouse_but[0]:
            add_block(mouse_pos[0], mouse_pos[1])

    if not won and not lost and not game_state == "level maker":
        if first_move:
            time_pass()
        check_if_lost_or_wan()
        check_if_bonus()

    draw()

