import pygame
from pygame import locals as keys
import random
import math
import sys
import networkzero as nw0

if len(sys.argv) > 10:
    if int(sys.argv[10]) == 1:
        print("Number of arguments:", len(sys.argv), "arguments.")
        print("Argument List:", str(sys.argv))
        print("PLEASE MAKE SURE YOU PASSED IN THE CORRECT ARGUMENTS!")
        print("Sample command:")
        print("python path_finding.py 400 300 16 50 100 100 250 0.1")
        print("Arguments are in order of WIDTH, HEIGHT, SPRITE SIZE, FPS, GENERATIONS, POPULATION, DNA LENGTH,"
              " MUTATION RATE, NAME TO BROADCAST, and whether to display stats in console (1 = True, 0 = False)")


class Constants(object):
    if len(sys.argv) > 1:
        try:
            WIDTH = int(sys.argv[1])
            HEIGHT = int(sys.argv[2])
            SPRITE_SIZE = (int(sys.argv[3]), int(sys.argv[3]))
            SPRITE_LENGTH = int(sys.argv[3])
            SPEED = int(sys.argv[4])
            GENERATIONS = int(sys.argv[5])
            POPULATION = int(sys.argv[6])
            DNA_LENGTH = int(sys.argv[7])
            MUTATION_RATE = float(sys.argv[8])
            BROADCAST = sys.argv[9]
        except IndexError:
            WIDTH = 400
            HEIGHT = 300
            SPRITE_SIZE = (16, 16)
            SPRITE_LENGTH = 16
            SPEED = 50
            GENERATIONS = 100
            POPULATION = 100
            DNA_LENGTH = 250
            MUTATION_RATE = 0.1
            BROADCAST = None
    else:
        # Width of play room. Also width of screen, be careful with values!
        WIDTH = 400
        # Height of play room. Also height of screen, be careful with values!
        HEIGHT = 300
        # Sprite size
        SPRITE_SIZE = (16, 16)
        # Length of sprite, should match above
        SPRITE_LENGTH = 16
        # FPS
        SPEED = 50
        # How many generations to go through
        GENERATIONS = 100
        # Number of creatures per generation
        POPULATION = 100
        # Length of list of instructions to do
        DNA_LENGTH = 250
        # Chance out of 1 to change an instruction
        MUTATION_RATE = 0.1
    # Color to use as start
    START_COLOR = (255, 0, 0)
    # Color to use as barrier
    BARRIER_COLOR = (255, 255, 0)
    # Color to use as end
    END_COLOR = (0, 255, 0)
    # Color of sprite
    SPRITE_COLOR = (0, 0, 255)
    # Color when sprite touched end
    TOUCHED_COLOR = (255, 128, 0)
    # Color when sprite touched wall
    DEAD_COLOR = (0, 0, 0)
    # Color when erasing sprites
    ERASER_COLOR = (255, 128, 255)


class Creature(pygame.sprite.Sprite):
    def __init__(self):
        super(Creature, self).__init__()
        self.surf = pygame.Surface(Constants.SPRITE_SIZE)
        self.surf.fill(Constants.SPRITE_COLOR)
        self.rect = self.surf.get_rect(center=(0, 0))
        self.DNA = []
        self.step = 0
        self.finished = False
        self.touched_wall = False

    def update(self):
        if self.step < Constants.DNA_LENGTH:
            # Up
            if self.DNA[self.step] == 0:
                self.rect.move_ip(0, -4)
            # Down
            if self.DNA[self.step] == 1:
                self.rect.move_ip(0, 4)
            # Left
            if self.DNA[self.step] == 2:
                self.rect.move_ip(-4, 0)
            # Right
            if self.DNA[self.step] == 3:
                self.rect.move_ip(4, 0)
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > Constants.WIDTH:
                self.rect.right = Constants.WIDTH
            if self.rect.top <= 0:
                self.rect.top = 0
            if self.rect.bottom >= Constants.HEIGHT:
                self.rect.bottom = Constants.HEIGHT
            self.step += 1
        else:
            self.finished = True


class Start(pygame.sprite.Sprite):
    def __init__(self):
        super(Start, self).__init__()
        self.surf = pygame.Surface(Constants.SPRITE_SIZE)
        self.surf.fill(Constants.START_COLOR)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, Constants.WIDTH),
                random.randint(0, Constants.HEIGHT)
            )
        )


class End(pygame.sprite.Sprite):
    def __init__(self):
        super(End, self).__init__()
        self.surf = pygame.Surface(Constants.SPRITE_SIZE)
        self.surf.fill(Constants.END_COLOR)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, Constants.WIDTH),
                random.randint(0, Constants.HEIGHT)
            )
        )


class Barrier(pygame.sprite.Sprite):
    def __init__(self, xy):
        super(Barrier, self).__init__()
        self.surf = pygame.Surface(Constants.SPRITE_SIZE)
        self.surf.fill(Constants.BARRIER_COLOR)
        self.rect = self.surf.get_rect(center=xy)


class Eraser(pygame.sprite.Sprite):
    def __init__(self, xy):
        super(Eraser, self).__init__()
        self.surf = pygame.Surface(Constants.SPRITE_SIZE)
        self.surf.fill(Constants.ERASER_COLOR)
        self.rect = self.surf.get_rect(center=xy)

    def move(self, xy):
        self.rect = self.surf.get_rect(center=xy)


def percent(top, bottom):
    fraction = top * 100
    return fraction / bottom


creatures = []
sprites = pygame.sprite.Group()
creature_group = pygame.sprite.Group()
barrier_group = pygame.sprite.Group()

start = Start()
end = End()
sprites.add(start)
sprites.add(end)

# end.rect.top = start.rect.top - 100
# end.rect.left = start.rect.left

for _ in range(Constants.POPULATION):
    creatures.append(Creature())

for creature in creatures:
    for _ in range(Constants.DNA_LENGTH):
        creature.DNA.append(random.randint(0, 3))
    creature.rect.top = start.rect.top
    creature.rect.left = start.rect.left
    sprites.add(creature)
    creature_group.add(creature)

pygame.init()
screen = pygame.display.set_mode([Constants.WIDTH, Constants.HEIGHT])
clock = pygame.time.Clock()

pygame.display.set_caption("Genetic Algorithms: Path Finding")

generation = 0
instruction = 0
mutations = 0
finished = 0
dead = 0
running = True
do = False
draw_barrier = False
last_xy = None
erase = False

x1 = start.rect.left + (Constants.SPRITE_LENGTH / 2)
x2 = end.rect.left + (Constants.SPRITE_LENGTH / 2)
y1 = start.rect.top + (Constants.SPRITE_LENGTH / 2)
y2 = end.rect.top + (Constants.SPRITE_LENGTH / 2)
length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

best = None
best_score = length
best_last = None
best_last_round = length

if len(sys.argv) > 10:
    if int(sys.argv[10]) == 1:
        print("Welcome to Genetic Algorithms: Path Finding")
        print("Click and hold anywhere to draw a barrier.")
        print("Use [BACKSPACE] to toggle the eraser.")
        print("Use [SPACE] to paused and resume.")
if Constants.DNA_LENGTH * 4 < length:
    if len(sys.argv) > 10:
        if int(sys.argv[10]) == 1:
            print("The creature's possible traveling distance is shorter than the distance from start to end. Aborting.")
    running = False
if len(sys.argv) > 10:
    if int(sys.argv[10]) == 1:
        print("Press [SPACE] to start.")
        print("When done, use CTRL + C or click on the Genetic Algorithms: Path Finding's X button.")

console = nw0.discover("GeneticAlgorithmsPathFindingGUIConsole")
counter = 0

screen.fill((255, 255, 255))
for entity in sprites:
    screen.blit(entity.surf, entity.rect)
pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == keys.KEYDOWN:
            if event.key == keys.K_SPACE:
                do = not do
            if event.key == keys.K_BACKSPACE:
                erase = not erase
                if erase:
                    eraser = Eraser(last_xy)
                    sprites.add(eraser)
                else:
                    eraser.kill()
        if event.type == keys.MOUSEMOTION:
            last_xy = event.pos
        if event.type == keys.MOUSEBUTTONDOWN:
            draw_barrier = True
        if event.type == keys.MOUSEBUTTONUP:
            draw_barrier = False

    if draw_barrier:
        barrier = Barrier(last_xy)
        barrier_group.add(barrier)
        sprites.add(barrier)
    if erase:
        eraser.move(last_xy)
        for entity in barrier_group:
            if entity.rect.colliderect(eraser):
                entity.kill()

    screen.fill((255, 255, 255))
    for entity in sprites:
        if do:
            try:
                if not entity.touched_wall:
                    entity.update()
            except AttributeError:
                entity.update()
        screen.blit(entity.surf, entity.rect)
    if do:
        instruction += 1
        for entity in creature_group:
            if end.rect.colliderect(entity):
                entity.surf.fill(Constants.TOUCHED_COLOR)
                screen.blit(entity.surf, entity.rect)
                best_score = 0
                best = entity
            if pygame.sprite.spritecollideany(entity, barrier_group) and not entity.touched_wall:
                entity.touched_wall = True
                entity.surf.fill(Constants.DEAD_COLOR)
                dead += 1

        for entity in creature_group:
            if entity.finished:
                finished += 1

        if generation < Constants.GENERATIONS + 1:
            if finished > Constants.DNA_LENGTH - 1 or instruction > Constants.DNA_LENGTH - 1:
                finished = 0
                instruction = 0
                mutations = 0
                generation += 1
                best_last = best
                best_last_round = best_score
                for entity in creature_group:
                    if not entity.touched_wall:
                        x1 = entity.rect.left + (Constants.SPRITE_LENGTH / 2)
                        x2 = end.rect.left + (Constants.SPRITE_LENGTH / 2)
                        y1 = entity.rect.top + (Constants.SPRITE_LENGTH / 2)
                        y2 = end.rect.top + (Constants.SPRITE_LENGTH / 2)
                        distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
                        if distance < best_score:
                            best_score = distance
                            best = entity
                    entity.touched_wall = False
                    entity.finished = False
                    entity.step = 0
                    entity.rect.top = start.rect.top
                    entity.rect.left = start.rect.left
                    entity.surf.fill(Constants.SPRITE_COLOR)
                    if best_score > best_last_round - 1:
                        for step in range(Constants.DNA_LENGTH):
                            if random.random() < Constants.MUTATION_RATE:
                                entity.DNA[step] = random.randint(0, 3)
                                mutations += 1
                            else:
                                try:
                                    entity.DNA[step] = best_last.DNA[step]
                                except AttributeError:
                                    pass
                    else:
                        for step in range(Constants.DNA_LENGTH):
                            if random.random() < Constants.MUTATION_RATE:
                                entity.DNA[step] = random.randint(0, 3)
                                mutations += 1
                            else:
                                try:
                                    entity.DNA[step] = best.DNA[step]
                                except AttributeError:
                                    pass
                dead = 0

    if len(sys.argv) > 10:
        if int(sys.argv[10]) == 1:
            text = "Generation: "
            text += str(generation)
            text += " Iteration: "
            text += str(instruction)
            text += " Best Distance (Last Generation): "
            text += str(round(best_last_round, 2))
            text += " ("
            text += str(round(percent(best_last_round, length), 2))
            text += "%) Best Distance (This Generation): "
            text += str(round(best_score, 2))
            text += " ("
            text += str(round(percent(best_score, length), 2))
            text += "%) Mutations in DNA: "
            text += str(mutations)
            text += " Dead: "
            text += str(dead)
            text += " ("
            text += str(round(percent(dead, Constants.POPULATION), 2))
            text += "%)"
            if not do:
                text += " [PAUSED]"
            print("\b"*(len(text) + 19), end="")
            print(text, end="")

    counter += 1
    if counter > (Constants.SPEED / 2) - 1:
        counter = 0
        try:
            nw0.send_message_to(console, {"generation": str(generation),
                                          "iteration": str(instruction),
                                          "bestlastgen": str(round(best_last_round, 2)),
                                          "bestlastgenper": str(round(percent(best_last_round, length), 2)),
                                          "bestthisgen": str(round(best_score, 2)),
                                          "bestthisgenper": str(round(percent(best_score, length), 2)),
                                          "dnamutcount": str(mutations),
                                          "dead": str(dead),
                                          "deadper": str(round(percent(dead, Constants.POPULATION), 2)),
                                          "paused": not do})
        except NameError:
            pass

    pygame.display.flip()
    clock.tick(Constants.SPEED)

pygame.quit()
