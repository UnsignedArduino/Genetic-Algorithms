import pygame
import random
import math


class Constants(object):
    # Width of play room. Also width of screen, be careful with values!
    WIDTH = 400
    # Height of play room. Also height of screen, be careful with values!
    HEIGHT = 300
    # Color to use as start
    START_COLOR = (255, 0, 0)
    # Color to use as barrier
    BARRIER_COLOR = (255, 255, 0)
    # Color to use as end
    END_COLOR = (0, 255, 0)
    # Color of sprite
    SPRITE_COLOR = (0, 0, 255)
    # Color when sprite touched end
    TOUCHED_COLOR = (0, 0, 0)
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
    MUTATION_RATE = 0.01


class Creature(pygame.sprite.Sprite):
    def __init__(self):
        super(Creature, self).__init__()
        self.surf = pygame.Surface(Constants.SPRITE_SIZE)
        self.surf.fill(Constants.SPRITE_COLOR)
        self.rect = self.surf.get_rect(center=(0, 0))
        self.DNA = []
        self.step = 0
        self.finished = False

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


creatures = []
sprites = pygame.sprite.Group()
creature_group = pygame.sprite.Group()

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
running = True

x1 = start.rect.left + (Constants.SPRITE_LENGTH / 2)
x2 = end.rect.left + (Constants.SPRITE_LENGTH / 2)
y1 = start.rect.top + (Constants.SPRITE_LENGTH / 2)
y2 = end.rect.top + (Constants.SPRITE_LENGTH / 2)
length = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

best = None
best_score = length
percent = 0

print("Welcome to Genetic Algorithms: Path Finding")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    for entity in sprites:
        entity.update()
        screen.blit(entity.surf, entity.rect)
    instruction += 1

    for entity in creature_group:
        if end.rect.colliderect(entity):
            entity.surf.fill(Constants.TOUCHED_COLOR)
            screen.blit(entity.surf, entity.rect)

    for entity in creature_group:
        if entity.finished:
            finished += 1

    if generation < Constants.GENERATIONS + 1:
        if finished > Constants.DNA_LENGTH - 1:
            finished = 0
            instruction = 0
            mutations = 0
            generation += 1
            for entity in creature_group:
                x1 = entity.rect.left + (Constants.SPRITE_LENGTH / 2)
                x2 = end.rect.left + (Constants.SPRITE_LENGTH / 2)
                y1 = entity.rect.top + (Constants.SPRITE_LENGTH / 2)
                y2 = end.rect.top + (Constants.SPRITE_LENGTH / 2)
                distance = math.sqrt((x2-x1)**2+(y2-y1)**2)
                if distance < best_score:
                    best_score = distance
                    best = entity
                entity.finished = False
                entity.step = 0
                entity.rect.top = start.rect.top
                entity.rect.left = start.rect.left
                entity.surf.fill(Constants.SPRITE_COLOR)
                for step in range(Constants.DNA_LENGTH):
                    if random.random() < Constants.MUTATION_RATE:
                        entity.DNA[step] = random.randint(0, 3)
                        mutations += 1
                    else:
                        try:
                            entity.DNA[step] = best.DNA[step]
                        except AttributeError:
                            pass
            fraction = best_score * 100
            percent = fraction / length
            percent = 100 - percent


    text = "Generation: "
    text += str(generation)
    text += " Iteration: "
    text += str(instruction)
    text += " Best Distance: "
    text += str(round(best_score, 2))
    text += " ("
    text += str(round(percent, 2))
    text += "%) Mutations in DNA: "
    text += str(mutations)
    print("\b"*(len(text)+10), end="")
    print(text, end="")

    pygame.display.flip()
    clock.tick(Constants.SPEED)

pygame.quit()
