import pygame
import random

pygame.init()

font_coord = pygame.font.SysFont("calibri", 20, bold=True)
font_game_state = pygame.font.SysFont("calibri", 30, bold=True)
font_game_instruction = pygame.font.SysFont("calibri", 15, bold=True)

class Square:
    sq_dim = 30
    ship_offset = 6

    def __init__(self, x_pos, y_pos,):
        self.x = x_pos * self.sq_dim + offset + self.sq_dim
        self.y = y_pos * self.sq_dim + offset + self.sq_dim
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.shot = False
        self.shot_ship_color = (255, 0, 0)
        self.shot_water_color = (51, 255, 255)
        self.ship = False
        self.ship_dir = {"x": 0, "y": 0}
        self.ship_num = None
        self.ship_len = None
        self.ship_sunk = False
        self.ship_color = (0, 128, 255)
        self.marked = False
        self.marked_color = (255, 178, 102)
        self.line_color = (0, 0, 0)
        self.line_thic = 2

    def draw(self, show_ships):
        pygame.draw.rect(win, self.line_color, (self.x, self.y, self.sq_dim, self.sq_dim), self.line_thic)  # lines
        if self.marked:
            pygame.draw.rect(win, self.marked_color, (self.x, self.y, self.sq_dim, self.sq_dim))
        if self.ship_sunk:
            pygame.draw.rect(win, self.shot_ship_color, (self.x, self.y, self.sq_dim, self.sq_dim))
        if self.ship and show_ships:
            if self.ship_dir["x"]:
                pygame.draw.rect(win, self.ship_color, (self.x, self.y + self.ship_offset, self.sq_dim, self.sq_dim - 2 * self.ship_offset))
            if self.ship_dir["y"]:
                pygame.draw.rect(win, self.ship_color, (self.x + self.ship_offset, self.y, self.sq_dim - 2 * self.ship_offset, self.sq_dim))
        if self.shot:
            if self.ship:
                pygame.draw.circle(win, self.shot_ship_color, ((self.x + self.x + self.sq_dim)//2, (self.y + self.y + self.sq_dim)//2), self.sq_dim//5)
            else:
                pygame.draw.circle(win, self.shot_water_color, ((self.x + self.x + self.sq_dim)//2, (self.y + self.y + self.sq_dim)//2), self.sq_dim//3)


    def reset(self):
        self.shot = False
        self.ship = False
        self.ship_num = None
        self.ship_len = None
        self.marked = False
        self.ship_dir = {"x": 0, "y": 0}

    def __repr__(self):
        return "x = " + str(self.x_pos) + " y = " + str(self.y_pos) + " ship num = " + str(self.ship_num) + " shot " + str(self.shot) + " sunk " + str(self.ship_sunk)




offset = 30
s_width = offset * 2 + Square.sq_dim * 11
s_height = (offset * 2  + Square.sq_dim * 11) * 2 - offset
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Statki by Kuba")


def sq_clicked(mouse_x, mouse_y):
    for sq in players_board:
        if sq.x < mouse_x < sq.x + sq.sq_dim and sq.y < mouse_y < sq.y + sq.sq_dim:
            return sq

    for sq in target_board:
        if sq.x < mouse_x < sq.x + sq.sq_dim and sq.y < mouse_y < sq.y + sq.sq_dim:
            return sq

def adj_sqrs(target_sq, x=False, nx=True):
    if target_sq in players_board:
        board = players_board
    elif target_sq in target_board:
        board = target_board
    else:
        print("Sq not found")
        return None

    adj_sqrs = []
    if nx:
        for sq in board:
            if sq.x_pos == target_sq.x_pos and (sq.y_pos == target_sq.y_pos - 1 or sq.y_pos == target_sq.y_pos + 1):
                adj_sqrs.append(sq)
            if sq.y_pos == target_sq.y_pos and (sq.x_pos == target_sq.x_pos - 1 or sq.x_pos == target_sq.x_pos + 1):
                adj_sqrs.append(sq)

    if x:
        for sq in board:
            if sq.x_pos == target_sq.x_pos + 1 and (sq.y_pos == target_sq.y_pos - 1 or sq.y_pos == target_sq.y_pos + 1):
                adj_sqrs.append(sq)
            if sq.x_pos == target_sq.x_pos - 1 and (sq.y_pos == target_sq.y_pos - 1 or sq.y_pos == target_sq.y_pos + 1):
                adj_sqrs.append(sq)

    return adj_sqrs

ships = {}  # len: num
def max_ship_size():
    for ship in ships:
        if ships[ship] != 0:
            return ship
    return None

ship_num = 0
def mark_ship(ship, oponent = False):
    global ships
    global ship_num
    for s in ship:
        s.marked = False
        s.ship = True
        s.ship_num = ship_num
        s.ship_len = len(ship)
    ship_num += 1
    if not oponent:
        ships[len(ship)] -= 1
        print(ships)

    for s in ship:
        for adj_sq in adj_sqrs(s, True):
            if adj_sq.marked:
                adj_sq.reset()


def destroy_ship(target_sq):
    global ships
    ships[target_sq.ship_len] += 1
    for sq in players_board:
        if sq.ship_num == target_sq.ship_num and sq != target_sq:
            sq.ship_num = None
            sq.ship = False
            sq.marked = True
    target_sq.reset()
    print(ships)


def mark_sq(target_sq):
    if target_sq in target_board:
        return
    target = target_sq
    if target.marked:
        target.reset()
        return
    else:
        ok = True
        for adj_sq in adj_sqrs(target_sq, True):
            if adj_sq.ship:
                ok = False
        if ok:
            target.marked = True

    if target.ship:
        destroy_ship(target)

    if not ok:
        return

    #  find ships beggining
    if target.ship_dir["x"] == 0 and target.ship_dir["y"] == 0:  # add ship_dir
        for adj_sq in adj_sqrs(target):
            if adj_sq.marked:
                if target.x_pos == adj_sq.x_pos:
                    target.ship_dir["y"] = 1
                    adj_sq.ship_dir["y"] = 1
                    target.ship_dir["x"] = 0
                    adj_sq.ship_dir["x"] = 0
                if target.y_pos == adj_sq.y_pos:
                    target.ship_dir["x"] = 1
                    adj_sq.ship_dir["x"] = 1
                    target.ship_dir["y"] = 0
                    adj_sq.ship_dir["y"] = 0
                break

    #  find ships end
    last = False
    while not last:
        last = True
        for adj_sq in adj_sqrs(target):
            if adj_sq.marked and adj_sq.x_pos == target.x_pos - target.ship_dir["x"] and adj_sq.y_pos == target.y_pos - target.ship_dir["y"]:
                adj_sq.ship_dir = target.ship_dir
                # target.ship = False
                target = adj_sq
                last = False
                break

    global ships
    firs_sq = target
    ship = []
    end = False
    while not end:
        ship.append(target)
        end = True
        for adj_sq in adj_sqrs(target):
            if adj_sq.marked and adj_sq.x_pos == target.x_pos + target.ship_dir["x"] and adj_sq.y_pos == target.y_pos + target.ship_dir["y"]:
                adj_sq.ship_dir = target.ship_dir
                target = adj_sq
                end = False
        if len(ship) == max_ship_size():
            mark_ship(ship)
            break


def shoot_sq(target):
    if lost:
        return
    if target in target_board:
        board = target_board
    else:
        board = players_board
    target.shot = True
    sunk = True
    for sq in board:
        if sq.ship_num == target.ship_num and not sq.shot:
            sunk = False
    if sunk:
        for sq in board:
            if sq.ship_num == target.ship_num:
                sq.ship_sunk = True



coords = [["A", 1], ["B", 2], ["C", 3], ["D", 4], ["E", 5], ["F", 6], ["G", 7], ["H", 8], ["I", 9], ["J", 10]]
def draw():
    text_color = (0, 0, 0)
    win.fill((255, 255, 255))
    for sq in players_board:
        sq.draw(True)
        # coordinates
        if sq.x_pos == 0:
            rend_text = font_coord.render(str(coords[sq.y_pos - 12][0]), True, text_color)
            win.blit(rend_text, (sq.x - 20, sq.y + 7))
        if sq.y_pos == 0:
            rend_text = font_coord.render(str(coords[sq.x_pos][1]), True, text_color)
            win.blit(rend_text, (sq.x + 8, sq.y - 20))

    show_ships = False
    text2 = None
    if debug:
        show_ships = True
    for sq in target_board:
        sq.draw(show_ships)
        #coordinates
        if sq.x_pos == 0:
            rend_text = font_coord.render(str(coords[sq.y_pos][0]), True, text_color)
            win.blit(rend_text, (sq.x - 20, sq.y + 7))
        if sq.y_pos == 0:
            rend_text = font_coord.render(str(coords[sq.x_pos][1]), True, text_color)
            win.blit(rend_text, (sq.x + 8, sq.y - 20))
    # game state
    if prep_faze:
        text = font_game_state.render("position your ships", True, (0, 255, 0))
        text2 = font_game_instruction.render("place ship len: " + str(max_ship_size()), True, (0, 0, 0))
    else:
        text = font_game_state.render("FIGHT", True, (255, 0, 0))

    if won or lost:
        if won:
            text = font_game_state.render("You won!! Congratulations", True, (0, 255, 0))
        if lost:
            text = font_game_state.render("You lost", True, (255, 0, 0))
        text2 = font_game_instruction.render("To restart press r", True, (0, 0, 0))

    win.blit(text, (5, 5))
    if text2 is not None:
        win.blit(text2, (15, offset + Square.sq_dim * 12))

    pygame.display.update()


def randomize_op_board(opponent=True):
    if opponent:
        board = target_board
    else:
        board = players_board

    ops_ships = ships
    ships_lst = []
    for s_len, s_num in ops_ships.items():
        for i in range(s_num):
            ships_lst.append(s_len)
    # print(ships_lst)

    for ship_len in ships_lst:
        ship_ok = False
        while not ship_ok:
            # print()
            adj_ship_ok = True
            adj_sq_ok = True
            ship = []
            rnd_pix = random.choice(board)
            rnd_vec = random.choice(["x", "y"])
            rnd_dir = random.choice([-1, 1])
            target = rnd_pix
            for sq in range(ship_len):
                # print(target)
                ship.append(target)
                for adj_sq in adj_sqrs(target, True):
                    if adj_sq.ship:
                        adj_ship_ok = False

                if sq != ship_len - 1:
                    for adj_sq in adj_sqrs(target):
                        adj_sq_ok = False
                        if vars(adj_sq)[rnd_vec + "_pos"] - vars(target)[rnd_vec + "_pos"] == rnd_dir and not adj_sq.ship:
                            target = adj_sq
                            adj_sq_ok = True
                            break
            if adj_ship_ok and adj_sq_ok:
                ship_ok = True
            else:
                ship_ok = False

        for s in ship:
            s.ship_dir[rnd_vec] = 1
        mark_ship(ship, oponent=True)

def shoot_op():
    for sq in players_board:  # if sq shot and adj sq shot shoot opposite form already shot
        if sq.shot and sq.ship and not sq.ship_sunk:
            a_sqrs = adj_sqrs(sq)
            for adj_sq in a_sqrs:
                if adj_sq.shot and adj_sq.ship:
                    for op_adj_sq in a_sqrs:
                        ok = True
                        if op_adj_sq.x_pos - sq.x_pos == (adj_sq.x_pos - sq.x_pos) * -1 and op_adj_sq.y_pos - sq.y_pos == (adj_sq.y_pos - sq.y_pos) * -1:
                            if not op_adj_sq.shot:
                                for adj_sq_2 in adj_sqrs(op_adj_sq, True):
                                    if adj_sq_2.shot and adj_sq_2.ship and adj_sq_2.ship_num != sq.ship_num:
                                        ok = False
                                if ok:
                                    shoot_sq(op_adj_sq)
                                    return

    for sq in players_board:  # if sq shot shoot adj sq
        if sq.shot and sq.ship and not sq.ship_sunk:
            a_sqrs = adj_sqrs(sq)
            while a_sqrs:
                ok = True
                # print(a_sqrs)
                rnd_adj_sq = a_sqrs.pop(a_sqrs.index(random.choice(a_sqrs)))
                if not rnd_adj_sq.shot:
                    for adj_sq_2 in adj_sqrs(rnd_adj_sq, True):
                        if adj_sq_2.shot and adj_sq_2.ship and adj_sq_2.ship_num != sq.ship_num:
                            ok = False
                    if ok:
                        shoot_sq(rnd_adj_sq)
                        return

    #  shoot not next to shot and shot ship
    ok = False
    posible_picks = list(range(len(players_board)))
    while not ok and posible_picks:
        ok = True
        rnd_i = posible_picks.pop(posible_picks.index(random.choice(posible_picks)))
        rnd_pick = players_board[rnd_i]
        if not rnd_pick.shot:
            for adj_sq in adj_sqrs(rnd_pick):
                if adj_sq.shot:
                    ok = False
            for adj_sq in adj_sqrs(rnd_pick, True):
                if adj_sq.shot and adj_sq.ship:
                    ok = False
        else:
            ok = False
        if ok:
            shoot_sq(rnd_pick)
            return

    # shoot antyhing
    print("shot anything")
    posible_picks = list(range(len(players_board)))
    while posible_picks:
        ok = True
        rnd_i = posible_picks.pop(posible_picks.index(random.choice(posible_picks)))
        target = players_board[rnd_i]
        if not target.shot:
            for adj_sq_2 in adj_sqrs(target, True):
                if adj_sq_2.shot and adj_sq_2.ship:
                    ok =False
            if ok:
                shoot_sq(target)
                return

def if_won():
    global won
    global lost
    if won or lost:
        return

    won = True
    for sq in target_board:
        if sq.ship and not sq.shot:
            won = False
    if won:
        print("you WON!!")
        won = True

    lost = True
    for sq in players_board:
        if sq.ship and not sq.shot:
            lost = False
    if lost:
        print("you LOST!!")
        lost = True


players_board = []
target_board = []
def init_game():
    global ships
    ships = {5: 1, 4: 2, 3: 2, 2: 3}
    target_board.clear()
    players_board.clear()
    for i in range(10):
        for j in range(10):
            target_board.append(Square(i, j))

    for i in range(10):
        for j in range(12, 22):
            players_board.append(Square(i, j))

def end_prep_faze():
    global prep_faze
    prep_faze = False
    for sq in players_board:
        if sq.marked:
            sq.reset()


run = True
restart = True
prep_faze = True
rnd_players_board = False
while run:

    if restart:
        init_game()
        randomize_op_board()
        won = False
        lost = False
        debug = False
        if rnd_players_board:
            randomize_op_board(opponent=False)
            prep_faze = False
            rnd_players_board = False
        else:
            prep_faze = True
        restart = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_button = pygame.mouse.get_pressed()
            sq_clic = sq_clicked(*mouse_pos)

            if sq_clic is not None:
                if prep_faze:
                    if mouse_button[0]:
                        mark_sq(sq_clic)
                    if mouse_button[2]:
                        print(sq_clic)
                else:
                    if mouse_button[0]:
                        shoot_sq(sq_clic)
                        draw()
                        shoot_op()
                    if mouse_button[2]:
                        print(sq_clic)

    kays = pygame.key.get_pressed()
    if kays[pygame.K_r]:
        restart = True
    if kays[pygame.K_d]:
        debug = True

    if prep_faze:
        if kays[pygame.K_a]:
            rnd_players_board = True
            restart = True
        if max_ship_size() is None:
            end_prep_faze()

    if not prep_faze:
        if_won()
    draw()
