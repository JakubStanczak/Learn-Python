import pygame
import random

pygame.init()
number_font = pygame.font.SysFont("calibri", 10, bold=True)
menu_font = pygame.font.SysFont("calibri", 30, bold=True)
comment_font = pygame.font.SysFont("calibri", 20, bold=True)
num_in_path = False
red_nodes = False

class Block:
    dim = 20

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.path = False
        self.dead_end = False
        self.excavation_num = None
        self.color = (0, 0, 0)

    def draw(self):
        if self.dead_end and not lab_finished:
            color = (255, 0, 0)
        elif self.path:
            color = (255, 255, 255)
        else:
            color = self.color

        pygame.draw.rect(win, color, (self.x * self.dim, self.y * self.dim, self.dim, self.dim))
        text = str(self.excavation_num)
        if num_in_path:
            rendered_text = number_font.render(text, True, (0, 0, 0))
            win.blit(rendered_text, (self.x * self.dim + 2, self.y * self.dim + 2))

    def excavate(self):
        global excavation_number
        self.path = True
        self.excavation_num = excavation_number
        excavation_number += 1
        if self.x == end_object.x and self.y == end_object.y:
            self.excavation_num += 1

    def __repr__(self):
        return "({}, {} - {})".format(self.x, self.y, self.path)

class Node:
    radius = 5
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.distance = float("inf")

    def draw(self):
        if not self.visited:
            # pygame.draw.circle(win, (0, 0, 0), (self.x * Block.dim + Block.dim // 2, self.y * Block.dim + Block.dim // 2), self.radius, 1)
            pass
        else:
            if self.distance == float("inf") and red_nodes:
                color = (255, 0, 0)
            elif self.distance == float("inf") and not red_nodes:
                color = (0, 0, 0)
            else:
                color = (45, 160, 30)
            pygame.draw.circle(win, color, (self.x * Block.dim + Block.dim // 2, self.y * Block.dim + Block.dim // 2), self.radius)

    def activate(self):
        self.visited = True
        if self.x == end_object.x and self.y == end_object.y:
            print("Distance is {}".format(self.distance))
            return True
        adj_nodes = adj_blocks(self.x, self.y, False, True)
        for adjacent in adj_nodes:
            if not adjacent.visited:
                if blocks[adjacent.y][adjacent.x].path:
                    adjacent.distance = self.distance + 1
                else:
                    adjacent.distance = float("inf")
                    adjacent.visited = True
        return False

    def trace_back(self):
        if self.x == start_object.x and self.y == start_object.y:
            return True, None
        adj_nodes = adj_blocks(self.x, self.y, False, True)
        next_node = Node(None, None)
        for node in adj_nodes:
            if node.distance < next_node.distance:
                next_node = node
        return False, next_node

    def __repr__(self):
        return "({}, {}) - {}".format(self.x, self.y, self.distance)


board_width = 50
board_height = 30

screen_width = Block.dim * board_width
screen_height = Block.dim * board_height
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Labyrinth by kuba")


blocks = []
nodes = []
def init():
    for y in range(board_height):
        block_line = []
        node_line = []
        for x in range(board_width):
            block_line.append(Block(x, y))
            node_line.append(Node(x, y))
        blocks.append(block_line)
        nodes.append(node_line)
    for b in blocks:
        print(b)
    print("nodes")
    for n in nodes:
        print(n)


def draw():
    pygame.event.pump()
    win.fill((255, 255, 255))

    if simulation_state != "Menu" and simulation_state != "chose start" and simulation_state != "chose end":
        for line in blocks:
            for block in line:
                block.draw()
        end_object.draw()

    if start_chosen:
        start_object.draw()

    if simulation_state == "find path":
        for line in nodes:
            for node in line:
                node.draw()

    if simulation_state == "find path" and end_found:
        if len(traced_path) >= 2:
            for i in range(len(traced_path) - 1):
                pygame.draw.line(win, (0, 0, 255), (traced_path[i].x * Block.dim + Block.dim // 2, traced_path[i].y * Block.dim + Block.dim // 2),
                                 (traced_path[i + 1].x * Block.dim + Block.dim // 2, traced_path[i + 1].y * Block.dim + Block.dim // 2), 3)

    comment_text = ""
    if simulation_state == "Menu":
        pass
        menu_text = """How would you like the labyrinth to be generated?
        1. snake algorithm
        2. branch algorithm
        3. I will draw it myself"""
        comment_text = "press the appropriate number"
        menu_text_list = menu_text.split("\n")
        for i in range(len(menu_text_list)):
            rendered_menu_text = menu_font.render(menu_text_list[i], True, (0, 0, 0))
            win.blit(rendered_menu_text, (20, 20 + 39 * i))
    if simulation_state == "chose start":
        comment_text = "Chose entrance"
    if simulation_state == "chose end":
        comment_text = "Chose exit"
    if simulation_state == "manual":
        comment_text = "draw the labyrinth, to reverse colors press o, to start the path finding algorithm press space"

    rendered_comment_text = comment_font.render(comment_text, True, (0, 0, 0))
    win.blit(rendered_comment_text, (screen_width // 2 - 3 * len(comment_text), screen_height - 50))

    pygame.display.update()


def check_if_good_choice(act_x, act_y, step_x, step_y):
    act_excavation_num = blocks[act_y][act_x].excavation_num + 1
    if act_x + step_x >= board_width or act_y + step_y >= board_height:
        return False
    if act_x + step_x < 0 or act_y + step_y < 0:
        return False
    if blocks[act_y + step_y][act_x + step_x].path:
        return False
    for adj_block in adj_blocks(act_x + step_x, act_y + step_y, X=False):
        if adj_block.dead_end:
            return False

    paths = 0
    for adj_block in adj_blocks(act_x + step_x, act_y + step_y, X=False):
        if adj_block.path:
            paths +=1
    if paths > 1:
        return False

    x_paths = 0
    for adj_block in adj_blocks(act_x + step_x, act_y + step_y):
        if adj_block.excavation_num is not None:
            if adj_block.excavation_num < act_excavation_num - 2 or adj_block.excavation_num > act_excavation_num:
                return False
            else:
                x_paths += 1
    if x_paths >= 3:
        return False

    return True


def adj_blocks(x, y, X=True, nods=False):
    adjacent_list = []
    if not nods:
        checked_list = blocks
    else:
        checked_list = nodes
    for line in checked_list:
        for adjacent in line:
            if abs(adjacent.x-x) <= 1 and abs(adjacent.y-y) <= 1:
                if X:
                    adjacent_list.append(adjacent)
                else:
                    if adjacent.x-x == 0 or adjacent.y-y == 0:
                        adjacent_list.append(adjacent)
    return adjacent_list


def next_to_end(act_x, act_y):
    if_next_to_end = False
    direction = None
    adjacent_blocks = adj_blocks(act_x, act_y, X=False)
    for adjacent_block in adjacent_blocks:
        if end_object.x == adjacent_block.x + 1 and end_object.y == adjacent_block.y:
            direction = "x+"
            if_next_to_end = True
        elif end_object.x == adjacent_block.x - 1 and end_object.y == adjacent_block.y:
            direction = "x-"
            if_next_to_end = True
        elif end_object.y == adjacent_block.y + 1 and end_object.x == adjacent_block.x:
            direction = "y+"
            if_next_to_end = True
        elif end_object.y == adjacent_block.y - 1 and end_object.x == adjacent_block.x:
            direction = "y-"
            if_next_to_end = True
    return if_next_to_end, direction


def next_step(act_x, act_y):
    good_choice = False
    possibilities = ["x+", "x-", "y+", "y-"]
    step_x = 0
    step_y = 0
    tried = False
    while not good_choice:
        # print(possibilities)
        if not possibilities or (act_x == end_object.x and act_y == end_object.y):
            return False, [act_x, act_y]
        if_next_to_end, end_direction = next_to_end(act_x, act_y)
        if if_next_to_end and not tried:
            print("NEXT TO END")
            direction = end_direction
            tried = True
        else:
            direction = possibilities.pop(possibilities.index(random.choice(possibilities)))

        if direction == "x+":
            good_choice = check_if_good_choice(act_x, act_y, 1, 0)
            if good_choice:
                step_x = 1
        elif direction == "x-":
            good_choice = check_if_good_choice(act_x, act_y, -1, 0)
            if good_choice:
                step_x = -1
        elif direction == "y+":
            good_choice = check_if_good_choice(act_x, act_y, 0, 1)
            if good_choice:
                step_y = 1
        else:
            good_choice = check_if_good_choice(act_x, act_y, 0, -1)
            if good_choice:
                step_y = -1
    blocks[act_y + step_y][act_x + step_x].excavate()

    return True, [act_x + step_x, act_y + step_y]


def double_back(act_x, act_y):
    global excavation_number
    blocks[act_y][act_x].dead_end = True
    excavation_number -= 1

    adjacent_blocks = adj_blocks(act_x, act_y, X=False)
    for adjacent_block in adjacent_blocks:
        if adjacent_block.path and not adjacent_block.dead_end:
            return False, [adjacent_block.x, adjacent_block.y]
    return True, [0, 0]


def mark_dead_ends():
    for line in blocks:
        for block in line:
            if block.path and not block.dead_end:
                dead_end = True
                if check_if_good_choice(block.x, block.y, 1, 0):
                    dead_end = False
                if check_if_good_choice(block.x, block.y, 0, 1):
                    dead_end = False
                if check_if_good_choice(block.x, block.y, -1, 0):
                    dead_end = False
                if check_if_good_choice(block.x, block.y, 0, -1):
                    dead_end = False

                if dead_end:
                    block.dead_end = True
    draw()


def clean_labyrinth():
    for line in blocks:
        for block in line:
            block.dead_end = False



start_pos = [0, 0]
end_pos = [board_width - 1, board_height - 1]
excavation_number = 0
init()

act_pos = start_pos
run = True
step_taken = True
lab_finished = False
simulation_state = "Menu"
start_chosen = False
key_down = False
traced_path = []
end_found = False
tracked_back = False
#  0 manual
# 1 double back
# 2 branches
generation_method = 2
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if simulation_state == "chose start":
                start_chosen = True
                start_pos = [pos // Block.dim for pos in mouse_pos]
                start_object = Block(*start_pos)
                start_object.color = (227, 130, 45)
                start_object.excavation_num = "start"
                simulation_state = "chose end"
                nodes[start_pos[1]][start_pos[0]].distance = 0
            elif simulation_state == "chose end":
                end_pos = [pos // Block.dim for pos in mouse_pos]
                end_object = Block(*end_pos)
                print("END OBJECT {}".format(end_object))
                end_object.color = (218, 227, 45)
                end_object.excavation_num = "end"
                if generation_method != 3:
                    simulation_state = "generating labyrinth"
                    blocks[start_pos[1]][start_pos[0]].excavate()
                else:
                    simulation_state = "manual"
                    for line in blocks:
                        for block in line:
                            block.path = True

        if event.type == pygame.KEYUP:
            key_down = False
        if event.type == pygame.KEYDOWN and not key_down:
            key_down = True
            if simulation_state == "Menu":
                if event.key == pygame.K_1:
                    generation_method = 1
                    simulation_state = "chose start"
                elif event.key == pygame.K_2:
                    generation_method = 2
                    simulation_state = "chose start"
                elif event.key == pygame.K_3:
                    generation_method = 3
                    red_nodes = True
                    simulation_state = "chose start"
            if generation_method == 3:
                if event.key == pygame.K_SPACE:
                    simulation_state = "find path"
                if event.key == pygame.K_o:
                    for line in blocks:
                        for target in line:
                            if target.x != end_object.x or target.y != end_object.y:
                                if target.x != start_object.x or target.y != start_object.y:
                                    if target.path:
                                        target.path = False
                                    else:
                                        target.path = True


    if simulation_state == "manual":
        mouse_pos = pygame.mouse.get_pos()
        mouse_but = pygame.mouse.get_pressed()
        if mouse_but[0]:
            target = blocks[mouse_pos[1] // Block.dim][mouse_pos[0] // Block.dim]
            if target.x != end_object.x or target.y != end_object.y:
                if target.x != start_object.x or target.y != start_object.y:
                    target.path = False

    act_pos = start_pos
    while simulation_state == "generating labyrinth" and generation_method == 1:
        while step_taken:
            # print(act_pos)
            step_taken, act_pos = next_step(*act_pos)
            draw()
            pygame.time.delay(30)
        lab_finished, act_pos = double_back(*act_pos)
        step_taken = True
        draw()
        if lab_finished:
            simulation_state = "find path"

    while simulation_state == "generating labyrinth" and generation_method == 2:
        possible_beginnings = []
        for line in blocks:
            for block in line:
                if block.path and not block.dead_end:
                    possible_beginnings.append(block)
        if possible_beginnings:
            act_block = random.choice(possible_beginnings)
            act_pos = [act_block.x, act_block.y]
            step_taken = True
            excavation_number = act_block.excavation_num + 1
            for _ in range(max(board_width, board_height) // 2):
                if step_taken:
                    step_taken, act_pos = next_step(*act_pos)
                    draw()
                    pygame.time.delay(3)
                    mark_dead_ends()
        else:
            simulation_state = "find path"

    clean_labyrinth()
    while simulation_state == "find path" and not end_found:
        min_distance = float("inf")
        min_dist_nodes = []
        for line in nodes:
            for node in line:
                if node.distance < min_distance and not node.visited:
                    min_distance = node.distance
                    min_dist_nodes = [node]
                elif node.distance == min_distance and not node.visited:
                    min_dist_nodes.append(node)
        print("List of min distance nodes {}".format(min_dist_nodes))
        for min_node in min_dist_nodes:
            if not end_found:
                end_found = min_node.activate()
            else:
                break
        draw()
        pygame.time.delay(40)

    draw()
    act_pos = end_pos
    active_node = None
    while simulation_state == "find path" and end_found and not tracked_back:
        if active_node is None:
            for line in nodes:
                for node in line:
                    if node.x == end_pos[0] and node.y == end_pos[1]:
                        active_node = node
        traced_path.append(active_node)
        active_node.visited = False
        tracked_back, active_node = active_node.trace_back()
        # print(traced_path)
        draw()
        pygame.time.delay(20)



