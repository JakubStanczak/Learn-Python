import pygame
import random
import math
import statistics

pygame.init()
info_font = pygame.font.SysFont("calibri", 30, bold=True)

screen_width = 1000
screen_height = 700
background_color = (255, 255, 255)
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dots finding path by Kuba")

time_limit = 500
#  genetic par
initial_pop = 200
mating_pop = initial_pop // 5
stallions = mating_pop // 2  # will not be mutated
agents_for_diversity = 5
mutation_num = mating_pop - stallions // 2
mutations_per = time_limit // 2
crossover_num = initial_pop - stallions - agents_for_diversity
distance_considered_hit = 15
terminate_experiment_after_hits = 1000


class Ball:
    init_x = screen_width // 2
    init_y = screen_height - 10
    init_color = (0, 0, 0)
    stallion_color = (0, 153, 0)
    hit_color = (0, 0, 255)
    best_color = (0, 255, 0)

    def __init__(self):
        self.x = self.init_x
        self.y = self.init_y
        self.radius = 5
        self.color = self.init_color
        self.brain = Brain()
        self.speed = 7
        self.fitness = 0
        self.dead = False
        self.stallion = False
        self.hit = False
        self.best = False

    def draw(self):
        if self.hit:
            color = self.hit_color
        elif self.best:
            color = self.best_color
        elif self.stallion:
            color = self.stallion_color
        else:
            color = self.color
        pygame.draw.circle(win, color, (self.x, self.y), self.radius)

    def move(self):
        if not self.dead:
            ang = deg_to_rad(self.brain.plan[time])
            x = math.sin(ang) * self.radius / (2*math.pi)
            y = math.cos(ang) * self.radius / (2*math.pi)
            self.x += round(x * self.speed)
            self.y += round(y * self.speed)
            if self.x > screen_width:
                self.x = screen_width
                self.dead = True
            elif self.x < 0:
                self.x = 0
                self.dead = True
            if self.y > screen_height:
                self.y = screen_height
                self.dead = True
            elif self.y < 0:
                self.y = 0
                self.dead = True
            dis_tar = distance(self.x, self.y, target.x, target.y)
            if dis_tar < distance_considered_hit:
                self.hit = True
                global hits
                hits += 1

            for barrier in barriers:
                if barrier.x <= self.x <= barrier.x + barrier.dim and barrier.y <= self.y <= barrier.y + barrier.dim:
                    self.dead = True

    def update_fitness(self):
        if not self.dead:
            fitness = 0
            max_dis = distance(0, 0, screen_width, screen_height)
            dis_tar = distance(self.x, self.y, target.x, target.y)
            if self.hit:  # points for hitting target
                fitness += 1000000000 * (time_limit - time)
                self.dead = True

            fitness += (max_dis - dis_tar)**2  # points for proximity to target

            if fitness > self.fitness:
                self.fitness = fitness
        else:  # penalty for dying early
            self.fitness -= 5

    def __repr__(self):
        return "x: {} y: {} fitness {} \n".format(self.x, self.y, self.fitness)

    def __add__(self, other):
        global new_pop
        new_pop.append(Ball())
        plan = []
        for i in range(len(self.brain.plan)):
            pick = random.randint(0, 1)
            if pick == 1:
                plan.append(self.brain.plan[i])
            else:
                plan.append(other.brain.plan[i])
        new_pop[-1].brain.plan = plan


class Brain:
    def __init__(self):
        self.plan = []
        for _ in range(time_limit):
            self.plan.append(random.randint(0, 360))

    def mutate(self):
        for _ in range(mutations_per):
            self.plan[random.randint(0, len(self.plan))-1] = random.randint(0, 360)


class Target:
    def __init__(self):
        self.x = screen_width // 2
        self.y = 20
        self.radius = 10
        self.color = (255, 0, 0)

    def draw(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


class Barrier:
    dim = screen_width // 50

    def __init__(self, x, y,):
        self.x = x
        self.y = y
        self.color = (128, 128, 128)
        self.line_width = 3

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.dim, self.dim))


def deg_to_rad(deg):
    return deg * math.pi / 180


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def add_barrier(x, y):
    x = x // Barrier.dim * Barrier.dim
    y = y // Barrier.dim * Barrier.dim
    already_is = False
    for barrier in barriers:
        if barrier.x == x and barrier.y == y:
            already_is = True
    if not already_is:
        barriers.append(Barrier(x, y))
        print("There is {} barriers on the board".format(len(barriers)))


def check_if_all_dead():
    dead = True
    for ball in balls:
        if not ball.dead:
            dead = False
    return dead



def draw():
    win.fill(background_color)
    for barrier in barriers:
        barrier.draw()

    for ball in reversed(balls):
        if balls.index(ball) == 0:
            ball.best = True
        else:
            ball.best = False
        ball.draw()
    target.draw()

    #  text
    if game_status == "level builder":
        text = "Draw obstacle course and press space"
    elif game_status == "presentation":
        text = "Best subjects in slow motion, r to restart"
    else:
        text = ""
    text_x = screen_width // 2 - len(text) * 7
    text_y = screen_height - 100
    text_color = (0, 0, 0)
    rendered_text = info_font.render(text, True, text_color)
    win.blit(rendered_text, (text_x, text_y))

    pygame.display.update()


def init_board():
    for _ in range(initial_pop):
        balls.append(Ball())


def restart():
    global game_status
    global hits
    global gen_number
    balls.clear()
    barriers.clear()
    game_status = "level builder"
    init_board()
    hits = 0
    gen_number = 0



def restart_pos():
    for ball in balls:
        if balls.index(ball) < stallions:
            ball.stallion = True
        else:
            ball.stallion = False
        ball.x = Ball.init_x
        ball.y = Ball.init_y
        ball.dead = False
        ball.hit = False
        ball.fitness = 0


balls = []
barriers = []
target = Target()
init_board()


time = 0
gen_number = 0
first_hit_gen = 0
run_app = True
hits = 0
game_status = "level builder"
key_pressed = False
all_dead = False
while run_app:
    pygame.time.delay(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_app = False
        if event.type == pygame.KEYUP:
            key_pressed = False
        if event.type == pygame.KEYDOWN and not key_pressed:
            key_pressed = True
            if event.key == pygame.K_SPACE:
                game_status = "run experiment"
            if event.key == pygame.K_r:
                restart()

    if game_status == "level builder":
        mouse_pos = pygame.mouse.get_pos()
        mouse_but = pygame.mouse.get_pressed()
        if mouse_but[0]:
            add_barrier(*mouse_pos)
        draw()

    all_dead = check_if_all_dead()

    if game_status == "run experiment":
        if time < time_limit and not all_dead:
            for ball in balls:
                ball.move()
                ball.update_fitness()
            balls.sort(key=lambda x: x.fitness, reverse=True)
            draw()
            time += 1

        else:  # evaluate mutate and reproduce
            print()
            print("gen number {} hits so far {}".format(gen_number, hits))
            fit = [ball.fitness for ball in balls]
            print("max fitness is {}".format(max(fit)))
            print("average fitness is {}".format(statistics.mean(fit)))

            if hits > terminate_experiment_after_hits:
                game_status = "presentation"
                balls.sort(key=lambda x: x.fitness, reverse=True)
                balls = balls[:stallions]
            else:
                gen_number += 1
                # balls.sort(key=lambda x: x.fitness, reverse=True)
                balls.sort(key=lambda ball: distance(ball.x, ball.y, ball.init_x, ball.init_y), reverse=True)
                diversity_agents = balls[:agents_for_diversity].copy()
                balls.sort(key=lambda x: x.fitness, reverse=True)
                mating_agents = balls[:mating_pop]
                new_pop = balls[:stallions]

                for _ in range(mutation_num):
                    random.choice(mating_agents[stallions:]).brain.mutate()

                mating_agents = mating_agents + diversity_agents
                new_pop = new_pop + diversity_agents
                best = balls[:stallions]
                fit = [ball.fitness for ball in best]
                fit = [round(x//min(fit)) for x in fit]
                probab = []
                for i in range(len(best)):
                    for _ in range(fit[i]):
                        probab.append(best[i])
                for _ in range(crossover_num):
                    _ = random.choice(probab) + random.choice(mating_agents)
                print(len(new_pop))
                balls = new_pop.copy()

                restart_pos()
                time = 0

    if game_status == "presentation":
        if time < time_limit:
            pygame.time.delay(5)
            for ball in balls:
                ball.move()
                if ball.hit:
                    ball.dead = True

            all_dead = check_if_all_dead()
            if all_dead:
                print("task accomplished in {} moves and {} generations".format(time, gen_number))
                time = time_limit
            draw()
            time += 1
        else:
            time = 0
            restart_pos()
