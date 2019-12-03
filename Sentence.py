import string
import random

target_str = "We will, we will rock you"
initial_population = 1000
# generations = 2000
mutations_in_agent = len(target_str) // 3
mating_pool = initial_population // 3
mutation_num = mating_pool // 2
crossover_num = initial_population - mating_pool


letters = string.ascii_lowercase + " \',"
agent_len = len(target_str)

pop = []

class Agent():

    def __init__(self):
        self.str = ""
        for _ in range(agent_len):
            self.str += random.choice(letters)
        self.update_fitness()

    def update_fitness(self):
        self.fitness = 0
        for i in range(len(self.str)):
            if self.str[i] in target_str:
                self.fitness += 1
            if self.str[i] == target_str[i]:
                self.fitness += 50
        for l in letters:
            if self.str.count(l) == target_str.count(l):
                self.fitness += 5

    def mutate(self):
        for _ in range(mutations_in_agent):
            l = list(self.str)
            l[random.randint(0, len(l)-1)] = random.choice(letters)
            self.str = "".join(l)
        self.update_fitness()

    def __add__(self, other):
        mid = len(self.str) // 2
        agent = Agent()
        str = ""
        for i in range(len(self.str)):
            source = random.randint(1,2)
            if source == 1:
                str += self.str[i]
            else:
                str += other.str[i]
        agent.str = str
        agent.update_fitness()
        return agent


    def __repr__(self):
        return "string: {}      fitness: {} \n".format(self.str, self.fitness)


def populate():
    for _ in range(initial_population):
        pop.append(Agent())

a = Agent()
a.str = target_str
a.update_fitness()
max_fitness = a.fitness
print(max_fitness)

populate()
# print(pop)
pop.sort(key=lambda x: x.fitness, reverse=True)
num_of_generations = 0

while pop[0].fitness < max_fitness - 0.05 * max_fitness:
    num_of_generations += 1
    print(pop[0])
    pop = pop[:mating_pool]+pop[-5:]

    for _ in range(mutation_num):  # mutations
        random.choice(pop).mutate()

    new_pop = pop.copy()  # crossover
    for _ in range(crossover_num):
        b = random.choice(pop) + random.choice(pop)
        new_pop.append(b)
    pop = new_pop.copy()
    pop.sort(key=lambda x: x.fitness, reverse=True)

print(pop)
print(num_of_generations)
print(pop[0])
print(target_str)



