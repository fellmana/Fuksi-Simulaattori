import pygame
from sys import exit
from people import Fuksi,Proffa,Opiskelija,is_inside_rectangle
from maps import Kumpula,Areena
import numpy as np

#--------------------------------
# Initialize pygame and constants
#--------------------------------
SCREEN_WIDTH = 1440
SCREEN_HEIGHT= 1000

# SEED USED FOR DEBUGGING
#np.random.seed(1234)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Fuksisimulaattori")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial" , 18 , bold = True)

#------------
# FUNCTIONS
#------------
def fps_counter():
    fps = "FPS: " + str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    screen.blit(fps_t,(0,0))


def initialize_simulation():
    campus = Kumpula()
    targets = campus.targets
    n_fuksi = 1000
    n_opiskelija = 20 
    n_proffa = 20
    people = []

    def get_spawn_pos(fuksi=True):
        if fuksi:
            spawn = campus.spawn_points[np.random.choice(len(campus.spawn_points))]
            pos = [spawn[0] + np.random.randint(10) - 5,
                   spawn[1] + np.random.randint(10) - 5]
            return pos
        else:                   
            spawn = campus.spawn_areas[np.random.choice(len(campus.spawn_areas))]
            # This loop is to reduce chanse of spawning inside a wall (10 attempts)
            # NOTE: Maps spawn_areas should be better defined to make this unnecessary
            for _ in range(10):
                pos = [np.random.randint(spawn[0],spawn[0] + spawn[2]),
                       np.random.randint(spawn[1],spawn[1] + spawn[3])]
                for rect in campus.rects:
                    if is_inside_rectangle(pos,rect):
                        break
                else:
                    return pos
            return pos
        
    for _ in range(n_fuksi):
        people.append(Fuksi(get_spawn_pos(),list(campus.targets[np.random.choice(campus.target_mapping["fuksi"])])))

    for _ in range(n_opiskelija):
        people.append(Opiskelija(get_spawn_pos(fuksi=False),
                                 list(campus.targets[np.random.choice(campus.target_mapping["opiskelija"])]),
                                 np.random.randint(1,8)))
    
    for _ in range(n_proffa):
        people.append(Proffa(get_spawn_pos(fuksi=False),list(campus.targets[np.random.choice(len(campus.targets))])))

    return campus, targets, people

# ==============================#
#      START OF  GAME LOOP      #
# ==============================#
campus,targets,people = initialize_simulation()

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill(pygame.Color("darkslategrey"))

    for i,person in enumerate(reversed(people.copy())):
        person.move(campus.rects)
        person.draw()
        if isinstance(person,Proffa):
            continue
        person.update(people)
        for t in targets:
            if person.check_collision(t,20) and list(t) == person.target:
                del(people[len(people) - i - 1])
                break

    # NOTE: changing the order of loops below can change visual look.        
    for border in campus.rects:
        pygame.draw.rect(pygame.display.get_surface(),pygame.Color("BLACK"), border )     
    for t in targets:
        pygame.draw.circle(pygame.display.get_surface(), pygame.Color("RED"),t, 20)

    fps_counter()
    pygame.display.update()
    clock.tick(60)