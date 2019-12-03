import pygame
import random
import sys

sys.setrecursionlimit(1500)

pygame.init()


offset = 10
offset_y = 50
game_bacground_color = (192, 192, 192)
menu_bacground_color = (0, 0, 0)
levels = ["easy", "medium", "expert"]
level_stats = {"easy": {"x_dim": 9, "y_dim": 9, "prob": 0.13}, "medium": {"x_dim": 16, "y_dim": 16, "prob": 0.15}, "expert": {"x_dim": 30, "y_dim": 16, "prob": 0.20}}

font_sq = pygame.font.SysFont("calibri", 20, bold=True)
font_menu = pygame.font.SysFont("calibri", 20, bold=True)
font_game_mines = pygame.font.SysFont("calibri", 20, bold=True)
font_game_text = pygame.font.SysFont("calibri", 15, bold=True)
font_game_sorry = pygame.font.SysFont("calibri", 18, bold=True)
game_mine_color = (225, 0, 0)
game_text_color = (0, 0, 0)
game_sorry_color = (0, 0, 255)


class Square:
    dim = 25
    line_thic = 1
    color_mine = (204, 0, 0)
    color_num = [(0, 0, 0), (51, 51, 255), (0, 153, 0),
                 (255, 51, 51), (255, 128, 0), (127, 0, 255), (204, 0, 0), (0, 102, 0), (255, 0, 127)]
    color_mark = (0, 0, 0)

    def __init__(self, column, row):
        self.column = column
        self.row = row
        self.mine = False
        self.revealed = False
        self.marked = False
        self.x = offset + column * self.dim
        self.y = offset_y + row * self.dim
        self.color_square = (224, 224, 224)
        self.num = None
        self.prob = None
        self.color_line = (128, 128, 128)

    def draw(self):
        pygame.draw.rect(win, self.color_line, (self.x + self.line_thic, self.y+self.line_thic, self.dim - self.line_thic, self.dim - self.line_thic), self.line_thic) # lines
        if self.mine:  # mine
            pygame.draw.circle(win, self.color_mine, ((self.x*2 + self.dim) // 2 + 1, (self.y*2 + self.dim) // 2 + 1), self.dim // 3)
        if self.num is not None: # number
            text_sq = font_sq.render(str(self.num), True, self.color_num[self.num])
            win.blit(text_sq, (self.x + 7, self.y + 4))
        if not self.revealed: #square
            pygame.draw.rect(win, self.color_square, (self.x + self.line_thic, self.y + self.line_thic, self.dim - self.line_thic, self.dim - self.line_thic))
        if self.marked:
            pygame.draw.line(win, self.color_mark, (self.x, self.y), (self.x+self.dim, self.y + self.dim), 3)
            pygame.draw.line(win, self.color_mark, (self.x, self.y + self.dim), (self.x + self.dim, self.y), 3)
        if show_mines:
            if self.mine:  # mine
                pygame.draw.circle(win, self.color_mine, ((self.x * 2 + self.dim) // 2, (self.y * 2 + self.dim) // 2), self.dim // 3)

    def mine_det(self):
        self.revealed = False
        self.color_square = (255, 0, 0)
        self.num = None

    def calc_prob(self):
        if self.revealed:
            num_mines = 0
            num_unrev = 0
            num_marked = 0
            for adj_sq in adj_sqs(self):
                if adj_sq.marked:
                    num_marked += 1
                if not adj_sq.revealed:
                    num_unrev += 1
                if adj_sq.mine:
                    num_mines +=1
            try:
                self.prob = (num_mines-num_marked)/(num_unrev-num_marked)
            except ZeroDivisionError:
                self.prob = None

    def mark(self, auto=False):
        if not self.marked and self.revealed is False:
            self.marked = True
        elif self.marked and auto is False:
            self.marked = False

    def reveal(self):
        boom = False
        if not self.marked:
            self.revealed = True
            adj_mines = 0
            for sq in adj_sqs(self):
                if sq.mine:
                    adj_mines += 1
            self.num = adj_mines

            if self.mine:
                self.mine_det()
                boom = True
        if boom:
            lost()

    def __repr__(self):
        return "column " + str(self.column) + " row " + str(self.row)

class Button(Square):
    dim = 30
    line_thic = 3

    def __init__(self, column, row):
        super().__init__(column, row)
        self.indicated = False
        self.color_square = (0, 225, 0)
        self.color_line = (0, 225, 0)
        self.color_text = (0, 225, 0)
        self.text = None


    def draw(self):
        pygame.draw.rect(win, self.color_line, (self.x + self.line_thic, self.y+self.line_thic, self.dim - self.line_thic, self.dim - self.line_thic), self.line_thic)
        if self.indicated:
            pygame.draw.rect(win, self.color_line, (self.x + self.line_thic, self.y + self.line_thic, self.dim - self.line_thic, self.dim - self.line_thic))
        text_sq = font_menu.render(str(self.text), True, self.color_text)
        win.blit(text_sq, (self.x - 70, self.y + 4))


def reveal_sq(sq):
    sq.reveal()
    still_0 = True
    while still_0:
        still_0 = spread_0()


board_dim_x = 0
board_dim_y = 0
s_width = 0
s_height = 0
chosen_lvl = 0
mine_num = 0
squares = []
buttons = [Button(1, 1), Button(1, 2), Button(1, 3)]
win = None

def init_board(change_level_to = None):
    global win
    global chosen_lvl
    global board_dim_x
    global board_dim_y
    global s_width
    global s_height
    global mine_num

    if change_level_to is not None:
        chosen_lvl = levels[change_level_to]
        board_dim_x = level_stats[chosen_lvl]["x_dim"]
        board_dim_y = level_stats[chosen_lvl]["y_dim"]
        mine_num = round(board_dim_y * board_dim_x * level_stats[chosen_lvl]["prob"])
        print("mine num = " + str(mine_num))
        s_width = board_dim_x * Square.dim + offset * 2
        s_height = board_dim_y * Square.dim + offset + offset_y
        win = pygame.display.set_mode((s_width, s_height))
        pygame.display.set_caption("Saper by Kuba")

    squares.clear()
    for i in range(board_dim_x):
        for j in range(board_dim_y):
            squares.append(Square(i, j))

    chosen = random.choices(squares, k=mine_num)
    for c in chosen:
        c.mine = True

    for b in buttons:
        b.x = s_width//2
        b.y = s_height//3 + buttons.index(b)*(b.dim + 10)
        b.text = levels[buttons.index(b)]
        print(b.text)


def draw():
    global menu
    if menu:
        win.fill(menu_bacground_color)
    else:
        win.fill(game_bacground_color)

    if menu:
        for b in buttons:
            b.draw()
        text = "During game:\nleft click to check square,\nright click to mark as mine\n\n            Now choose level:"
        text_l = text.split("\n")
        for t in text_l:
            text_rend = font_menu.render(t, True, (0, 225, 0))
            win.blit(text_rend, (10, 20 + text_l.index(t) * 25))

    else:
        for sq in squares:
            sq.draw()


    if won_game:
        mines_left = 0
    else:
        mines_left = mine_num
    for sq in squares:
        if sq.marked:
            mines_left -= 1

    if not menu and not autos and not won_game:
        mine_left_text = font_game_mines.render("Mines left to mark: " + str(mines_left), True, game_mine_color)
        win.blit(mine_left_text, (10, 2))

        text = "To auto solve press SPACE\nTo restart press R"
        test_l = text.split("\n")
        for t in test_l:
            text_rend = font_game_text.render(t, True, game_text_color)
            win.blit(text_rend, (10, 20 + test_l.index(t)*12))

    if won_game:
        text_sorry = font_game_sorry.render("Ow yeah. That's how it's done", True, game_sorry_color)
        win.blit(text_sorry, (10, 15))

    pygame.display.update()


def clicked(x, y):
    global menu
    if not menu:
        for sq in squares:
            if sq.x < x < sq.x + sq.dim and sq.y < y < sq.y + sq.dim:
                return sq
    else:
        for b in buttons:
            if b.x < x < b.x + b.dim and b.y < y < b.y + b.dim:
                return b
    return None


def calc_dist(sq1, sq2):
    return ((sq1.column - sq2.column) ** 2 + (sq1.row - sq2.row) ** 2) ** 0.5


def adj_sqs(target_sq, rev=True, marked=True):
    adj_sq = []
    for sq in squares:
        distance = calc_dist(target_sq, sq)
        if 0 < distance < 2:
            if sq.marked and marked == True:
                adj_sq.append(sq)
            elif sq.revealed and rev == True:
                adj_sq.append(sq)
            if sq.revealed == False and sq.marked == False:
                adj_sq.append(sq)
    return adj_sq


def spread_0():
    revealed = True
    while revealed:
        revealed = False
        for sq in squares:
            if sq.num == 0:
                for adj_sq in adj_sqs(sq):
                    if not adj_sq.revealed:
                        reveal_sq(adj_sq)
                        revealed = True
                sq.num = None
    return revealed

def if_won():
    won = True
    for sq in squares:
        if sq.mine == True and sq.marked == False:
            won = False
    if won:
        won_prot()


def won_prot():
    global won_game
    for sq in squares:
        sq.revealed = True
    won_game = True


def lost():
    global boom
    global show_mines
    global autos
    global restart
    boom = True
    show_mines = True
    print("BOOOOOOM")
    if autos:
        draw()
        text_sorry = font_game_sorry.render("Upss, sorry. Will try Again", True, game_sorry_color)
        win.blit(text_sorry, (10, 15))
        pygame.display.update()
        pygame.time.delay(2000)
        restart = True


def update_prob():
    for sq in squares:
        sq.calc_prob()

def clean_squares():
    for sq in squares:
        if sq.revealed and sq.num is None and not sq.mine:
            squares.pop(squares.index(sq))

def shot_0p():
    for sq in squares:
        if sq.prob == 0:
            for adj_sq in adj_sqs(sq):
                reveal_sq(adj_sq)


def mark_100p():
    for sq in squares:
        if sq.prob == 1:
            for adj_sq in adj_sqs(sq):
                adj_sq.mark(auto=True)


def shot_5050():
    #print("running shot_5050 protocol for")
    eff_5050 = False
    marked_5050 = []
    for target_sq in squares:
        adj_sqs_target = adj_sqs(target_sq, rev=False, marked=False)
        if target_sq.prob == 0.5 and len(adj_sqs_target) == 2:
            #print()
            #print(target_sq)
            #target_sq.color_line = (0, 255, 128)
            for adj_sq in adj_sqs_target:
                if not adj_sq.revealed and not adj_sq.marked:
                    adj_sq.marked = True
                    marked_5050.append(adj_sq)
                    #print(marked_5050)
            draw()
            update_prob()
            for sq in squares:
                adj_sqs_local = adj_sqs(sq, rev=False)
                if sq.prob is not None and len(adj_sqs(sq,rev=False,marked=False)) == 1:
                    nexto = True
                    for m in marked_5050:
                        if m not in adj_sqs_local:
                            nexto = False
                    #if nexto:
                        #sq.color_line = (0, 0, 0)
                        #print("Nex to is " + str(sq))
                    if sq.prob < 0 and nexto:
                        for adj_sq in adj_sqs_local:
                            if not adj_sq.revealed and not adj_sq.marked:
                                reveal_sq(adj_sq)
                                adj_sq.color_line = (204, 102, 0)
                                print("5050 REVEALED " + str(adj_sq))
                                draw()
                                eff_5050 = True

                    elif sq.prob == 0 and nexto:
                        for adj_sq in adj_sqs_local:
                            if not adj_sq.revealed and not adj_sq.marked:
                                adj_sq.mark()
                                adj_sq.color_square = (153, 255, 255)
                                adj_sq.color_line = (0, 0, 255)
                                print("5050 MARKED " + str(adj_sq))
                                draw()
                                eff_5050 = True

            for marked in marked_5050:
                marked.marked = False
            marked_5050.clear()
            update_prob()
    return eff_5050


def rnd_shot():
    num_mines = 0
    num_unrev = 0
    potencial_sq = []
    for sq in squares:
        if not sq.revealed and not sq.marked:
            potencial_sq.append(sq)
            num_unrev += 1
            if sq.mine:
                num_mines += 1
    board_prob = num_mines/num_unrev

    min_sq_prob = 1
    sq_min_prob = None
    for sq in squares:
        if sq.prob is not None:
            if sq.prob < min_sq_prob:
                sq_min_prob = sq
                min_sq_prob = sq.prob

    if board_prob < min_sq_prob:
        target = random.choice(potencial_sq)
        print("min prob board")

    else:
        target = random.choice(adj_sqs(sq_min_prob, rev=False, marked=False))
        print("min prob adj")

    print("random shot executed" + str(target))
    target.color_line = (255, 0, 0)
    reveal_sq(target)

def autosolve():
    global boom
    go_100p = True
    go_5050 = True
    go_rnd_shot = True
    revealed_list = []
    marked_list = []
    while go_rnd_shot:
        while go_5050:
            while go_100p:
                revealed_list.clear()
                marked_list.clear()
                for sq in squares:
                    revealed_list.append(sq.revealed)
                    marked_list.append(sq.marked)
                update_prob()
                shot_0p()
                mark_100p()
                pygame.time.delay(100)
                go_100p = False
                for i in range(len(revealed_list)):
                    if squares[i].revealed != revealed_list[i] or squares[i].marked != marked_list[i]:
                        go_100p = True
                draw()
                clean_squares()

            go_5050 = shot_5050()
            if go_5050:
                go_100p = True

        if_won()
        go_rnd_shot = False
        if not won_game:
            rnd_shot()
            if not boom:
                go_rnd_shot = True
                go_100p = True
                go_5050 = True

    print("autosolve terminated")

def restart_fu():
    global restart
    global boom
    global won_game
    global autos
    global show_mines
    init_board()
    restart = False
    boom = False
    won_game = False
    show_mines = False
    print("________________________________________________________________")


click_delay_countdown = 0
click_delay = 500
disp_delay = 10
run = True
restart = False
show_mines = False
autos = False
menu = True
boom = False
won_game = False
init_board(change_level_to=1)
while run:
    if restart:
        restart_fu()
    pygame.time.delay(disp_delay)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if menu:
        indicated_button = clicked(*pygame.mouse.get_pos())
        if indicated_button is not None:
            for b in buttons:  # highlight button
                if b == indicated_button:
                    b.indicated = True
                else:
                    b.indicated = False
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0]:
                menu = False
                pygame.display.quit()
                init_board(change_level_to=buttons.index(indicated_button))



    if not boom and not menu:
        if click_delay_countdown > 0:
            click_delay_countdown -= 1
        if click_delay_countdown == 0:
            mouse_click = pygame.mouse.get_pressed()
            if mouse_click[0] or mouse_click[2]:
                click_delay_countdown = click_delay // disp_delay
                clicked_sq = clicked(*pygame.mouse.get_pos())
                if clicked_sq and mouse_click[0]:
                    reveal_sq(clicked_sq)
                elif clicked_sq and mouse_click[2]:
                    print(clicked_sq.prob)
                    clicked_sq.mark()

    if click_delay_countdown > 0:
        click_delay_countdown -= 1
    if click_delay_countdown == 0:
        kays = pygame.key.get_pressed()
        if kays[pygame.K_SPACE] and not menu:
            click_delay_countdown = click_delay // disp_delay
            autos = True
        if kays[pygame.K_r] and not menu:
            click_delay_countdown = click_delay // disp_delay
            restart = True
            autos = False
        if kays[pygame.K_d] and not menu:
            click_delay_countdown = click_delay // disp_delay
            if show_mines:
                show_mines = False
            else:
                show_mines = True
    if autos and not won_game:
        autosolve()

    if_won()

    draw()

