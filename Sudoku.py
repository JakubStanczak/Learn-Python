import pygame
import random
pygame.init()


s_width = 500
s_height = 400
offset = 20
dif_level = 40  # num of nums left

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Sudoku by Kuba")
font_fields = pygame.font.SysFont("comicsansms", 25)
font_text = pygame.font.SysFont("comicsansms", 12)
font_text_big = pygame.font.SysFont("comicsansms", 20)
pig = pygame.image.load('waddles.png')
calculating = pygame.image.load("calculating.png")

class Field:
    pix_dim = 30
    f_color = (128, 255, 0)
    f_clicked_color = (255, 255, 102)
    sq_color = (76, 153, 0)
    text_color = (0, 0, 255)

    def __init__(self, x_pos, y_pos, num):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sect = pos_to_sek(x_pos, y_pos)
        self.x = self.x_pos * self.pix_dim + offset
        self.y = self.y_pos * self.pix_dim + offset
        self.num = num
        self.clicked = False

    def draw(self):
        if self.clicked:
            pygame.draw.rect(win, self.f_clicked_color, (self.x, self.y, self.pix_dim, self.pix_dim))
        pygame.draw.rect(win, self.f_color, (self.x, self.y, self.pix_dim, self.pix_dim), 2)
        if self.num is not None:
            text = font_fields.render(str(self.num), True, self.text_color)
            win.blit(text, (self.x+7, self.y-3))

    def draw_sq(self):
        if self.x_pos % 3 == 0 and self.y_pos % 3 == 0:
            pygame.draw.rect(win, self.sq_color, (self.x, self.y, self.pix_dim * 3, self.pix_dim * 3), 2)

    def __repr__(self):
        return "x pos = " + str(self.x_pos) + " y pos = " + str(self.y_pos) + " sector = " + str(self.sect) + " number = " + str(self.num)


def pos_to_sek(xp, yp):
    return (xp//3+yp//3*3)+1


fields = []
buttons = []
lvl_buttons = []


def start_fields():
    fields.clear()
    buttons.clear()

    # fields
    for i in range(9):
        for j in range(9):
            fields.append(Field(i, j, None))
    print(fields)

    # buttons
    for i in range(3):
        for j in range(3):
            buttons.append(Field(i+10, j+3, i+1+j*3))

    # lvl_buttones
    # for i in range(3):
    #     lvl_buttons.append(Field(14, i, None))


def rand_gen():
    empty_ind = list(range(len(fields)))
    num = 1
    res_num = False
    res_num_num = 0
    while num < 10:
        if res_num == False:
            for sect in range(1, 10):
                t = 0
                choice_ok = False
                while choice_ok == False and res_num == False:
                    ind = random.choice(empty_ind)
                    f = fields[ind]
                    if f.sect == sect:
                        #print("num = " + str(num))
                        #print("sek = " + str(sect))
                        if if_ok(f, num):
                            f.num = num
                            t = 0
                            choice_ok = True
                            empty_ind.pop(empty_ind.index(ind))
                            print(empty_ind)
                            draw(generating=True)
                            if sect == 9:
                                num += 1
                                res_num_num = 0
                    else:
                        t += 1

                    if t > 1000:
                        res_num = True
                        if res_num_num > 10:
                            print("sektor = " + str(sect) + " num = " +str(num))
                            return False
        else:
            for f in fields:
                if f.num == num:
                    f.num = None
                    empty_ind.append(fields.index(f))
            res_num = False
            res_num_num += 1
            print("res num num = " + str(res_num_num))

    f_ind = list(range(len(fields)))
    for i in range(9 * 9 - dif_level):
        ind = random.choice(f_ind)
        fields[ind].num = None
        f_ind.pop(f_ind.index(ind))
    return True

def autosolve():
    m5050 = True
    autosolve = True
    while m5050 == True:
        change = True
        while change == True:
            old_f = []
            for f in fields:
                old_f.append(f.num)
            other_opt = []
            for f_target in fields:
                if f_target.num is None:
                    num_options = list(range(1, 10))
                    other_opt.clear()
                    pas = False
                    while len(num_options) > 0 and pas == False:
                        num = random.choice(num_options)
                        num_options.pop(num_options.index(num))
                        if if_ok(f_target, num):
                            for f_check in fields:
                                if f_check.num == None and (f_target.x_pos == f_check.x_pos or f_target.y_pos == f_check.y_pos or f_target.sect == f_check.sect) and f_target != f_check:
                                    if if_ok(f_check, num):

                                        other_opt.append(f_check)
                            other_x = 0
                            other_y = 0
                            other_s = 0
                            for f in other_opt:
                                if f.x_pos == f_target.x_pos:
                                    other_x += 1
                                if f.y_pos == f_target.y_pos:
                                    other_y += 1
                                if f.sect == f_target.sect:
                                    other_s += 1
                            if other_y == 0 or other_x == 0 or other_s == 0:
                                pas = True
                                f_target.num = num
                            draw(autosolve)

            change = False
            new_f = []
            for f in fields:
                new_f.append(f.num)
            for i in range(len(fields)):
                if old_f[i] != new_f[i]:
                    change = True
    # 50/50
        left_in_sect = [0] * 9
        for f in fields:
            if f.num == None:
                 left_in_sect[f.sect-1] += 1
        if 2 in left_in_sect:
            for s in left_in_sect:
                if s == 2:
                    sect = left_in_sect.index(s)+1
                    for f in fields:
                        if f.sect == sect and f.num == None:
                            for i in range(1, 10):
                                if if_ok(f, i):
                                    f.num = i
                                    m5050 = True
                                    print("5050 True")
                                    print("num -> field (x,y) " + str(f.num) + " -> " + str(f.x_pos) + "," + str(f.y_pos))
                                    break
        else:
            m5050 = False
            print("5050 False")
    autosolve = False

def if_won():
    for f in fields:
        if f.num == None or if_ok(f ,f.num) == False:
            return False
    return True

def pressed_field(what, fb):
    if what == "f":
        for f in fields:
            f.clicked = False
        fb.clicked = True

    if what == "b":
        for f in fields:
            if f.clicked == True:
                if if_ok(f, fb.num):
                    f.num = fb.num
                    return True
                else:
                    f.num = None
                    return False


def check_lines(field, num):  # True == OK
    for f in fields:
        if (f.x_pos == field.x_pos or f.y_pos == field.y_pos) and f != field:
            if f.num == num:
                return False
    #print("lines OK")
    return True


def check_sectors(field, num):
    for f in fields:
        if f != field and f.sect == field.sect:
            if f.num == num:
                return False
    #print("sektors OK")
    return True


def if_ok(field, num):
    if check_sectors(field, num) == True and check_lines(field, num) == True:
        return True
    else:
        return False


def draw(autosolve=False, generating=False, err_time_counter=0, err_counter=0):
    win.fill((255, 255, 255))
    for f in fields:
        f.draw()
    for f in fields:
        f.draw_sq()
    for b in buttons:
        b.draw()
    pygame.time.delay(20)
    # for lb in lvl_buttons:
    #     lb.draw()
    won = if_won()
    if won == True and run == True:
        text1 = font_text.render("Good job!", True, (51, 51, 255))
        text2 = font_text.render("Waddles approves", True, (51, 51, 255))
        win.blit(text1, (offset + Field.pix_dim * 10, offset + Field.pix_dim * 6))
        win.blit(text2, (offset + Field.pix_dim * 10, offset + Field.pix_dim * 6.5))
        win.blit(pig, (offset + Field.pix_dim * 10, offset + Field.pix_dim * 7 + 4))

    if autosolve == True or generating == True:
        win.blit(calculating, (offset + Field.pix_dim * 10, offset + Field.pix_dim * 3))

    if generating == True:
        tekst_g = font_text_big.render("Generating board!", True, (255, 51, 51))
        win.blit(tekst_g, (offset + Field.pix_dim * 10, offset + Field.pix_dim * 0.5))

    if won == False and generating == False and autosolve == False:
        tekst_wa1 = font_text.render("If you want waddles to do your job", True, (51, 51, 255))
        tekst_wa2 = font_text.render("press space", True, (51, 51, 255))
        win.blit(tekst_wa1, (offset + Field.pix_dim * 9.5, offset + Field.pix_dim * 0.5))
        win.blit(tekst_wa2, (offset + Field.pix_dim * 9.5, offset + Field.pix_dim * 1))

    if err_time_counter > 0:
        tekst_err = "N"
        for i in range(err_counter):
            tekst_err = tekst_err + "o"
        tekst_err_rend = font_text_big.render(tekst_err, True, (255, 51, 51))

        win.blit(tekst_err_rend, (offset, offset + Field.pix_dim * 10))

    pygame.display.update()




def which_field_clicked(x, y):
    for f in fields:
        if f.x < x < f.x + f.pix_dim and f.y < y < f.y + f.pix_dim:
            return "f", f
    for b in buttons:
        if b.x < x < b.x + b.pix_dim and b.y < y < b.y + b.pix_dim:
            return "b", b
    return None, None


run = False

f_ready = False
while f_ready == False:
    start_fields()
    f_ready = rand_gen()


run = True
select_lvl = True
err_time_counter = 0
err_counter = 0
while run:

    # if X pressed stop program
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_spot = pygame.mouse.get_pos()
            what, fb = which_field_clicked(*mouse_spot)
            # print(str(w_clicked) + str(x_pos) + str(y_pos))
            picked_num_ok = pressed_field(what, fb)
            if picked_num_ok == False:
                err_time_counter = 50
                err_counter += 1

    kays = pygame.key.get_pressed()
    if kays[pygame.K_SPACE]:
        autosolve()

    if err_time_counter > 0:
        err_time_counter -= 1
    draw(err_time_counter=err_time_counter, err_counter=err_counter)

