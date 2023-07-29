import pygame
from sys import exit
from people import Fuksi,Proffa,Opiskelija,is_inside_rectangle
from commandline_arguments import parse_args
from maps import Kumpula,Areena
import numpy as np


#--------------------------------
# Initialize pygame and constants
#--------------------------------
SCREEN_WIDTH  = 1440
SCREEN_HEIGHT = 1000
CLOCK_SPEED   = 500

args = parse_args()

if args.debug:
    np.random.seed(1234)

# Dictionary containing all text for easy language options.
text_dict = {
    "fin":{
    "caption":"Fuksisimulaattori",
    "all_at_goal":["Kaikki fuksit luennolla, JEE!!","Paina 'ENTER' aloittaaksesi uudelleen."],
    "fcounter_text":"Fuksit luennolla",
    "clock_text":"AIKA"
    },
    "eng":{
    "caption":"Freshmansimulator",
    "all_at_goal":["All freshmen at lectures!!","Press 'ENTER' to restart."],
    "fcounter_text":"Freshmen at lectures",
    "clock_text":"TIME"
    },
    "swe":{
    "caption":"gulis-simulator",
    "all_at_goal":["Alla gulisar på föreläsning!!","Tryck 'ENTER',för att starta om."],
    "fcounter_text":"gulisar på föreläsning",
    "clock_text":"TID"
    }    
}

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption(text_dict[args.language]["caption"])
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, CLOCK_SPEED)
font = pygame.font.SysFont("Arial" , 18 , bold = True)
titlefont = pygame.font.SysFont("Arial" , 60 , bold = True)
counter_font = pygame.font.SysFont("Arial" , 36 , bold = True)

#------------
# FUNCTIONS
#------------
def fps_counter():
    fps = "FPS: " + str(int(clock.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("RED"))
    screen.blit(fps_t,(0,0))

def draw_title(campus):
    title = titlefont.render(campus.name[args.language] , 1, pygame.Color("BLACK"))
    screen.blit(title,(SCREEN_WIDTH//2 - titlefont.size(campus.name[args.language])[0]//2,10))

def draw_fuksi_number(n_fuksi,total):
    if n_fuksi == total:
        fcounter = counter_font.render(text_dict[args.language]["all_at_goal"][0] , 1, pygame.Color("RED"))
        screen.blit(fcounter,(0,20)) 
        fcounter = counter_font.render(text_dict[args.language]["all_at_goal"][1] , 1, pygame.Color("RED"))
        screen.blit(fcounter,(0,60)) 

    else:
        fcounter = counter_font.render(f"{text_dict[args.language]['fcounter_text']}: {n_fuksi}/{total}"  , 1, pygame.Color("BLACK"))
        screen.blit(fcounter,(0,20))    

def draw_clock(text):
    fcounter = counter_font.render(f"{text_dict[args.language]['clock_text']}: {text}", 1, pygame.Color("BLACK"))
    screen.blit(fcounter,(SCREEN_WIDTH//2 + 400,20))

def initialize_simulation(args):

    match args.map.lower():
        case "kumpula":
            campus = Kumpula()
        case "areena":
            campus = Areena()
        
    targets = campus.targets
    n_fuksi = args.fuksi
    n_opiskelija = args.opiskelija 
    n_proffa = args.proffa
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
        people.append(Fuksi(get_spawn_pos()
                            ,list(campus.targets[np.random.choice(campus.target_mapping["fuksi"])]),
                            special_rule=campus.special_rule))

    for _ in range(n_opiskelija):
        people.append(Opiskelija(get_spawn_pos(fuksi=False),
                                 list(campus.targets[np.random.choice(campus.target_mapping["opiskelija"])]),
                                 np.random.randint(1,8),
                                 special_rule=campus.special_rule))
    
    for _ in range(n_proffa):
        people.append(Proffa(get_spawn_pos(fuksi=False),list(campus.targets[np.random.choice(len(campus.targets))])))

    return campus, targets, people, n_fuksi

# ==============================#
#      START OF  GAME LOOP      #
# ==============================#
campus,targets,people,total = initialize_simulation(args)
n_goal = 0
h = 8; m = 0
clock_text = f"{h:02d}:{m:02d}"

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if n_goal != total:
                clock_text = f"{h:02d}:{m:02d}"
                if m == 59: h = (h + 1) % 24 
                m = (m + 1) % 60 
            
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and n_goal == total:

                campus,targets,people,total = initialize_simulation(args)
                n_goal = 0
                h = 8; m = 0
                

    screen.fill(pygame.Color("darkslategrey"))

    
    highlight_index = []
    for i,person in enumerate(reversed(people.copy())):
        person.move(campus.rects)
        person.draw()
        if isinstance(person,Proffa):
            continue
        person.update(people)
        for j,t in enumerate(targets):
            if person.check_collision(t,20):# and list(t) == person.target:
                if isinstance(person,Fuksi):
                    n_goal += 1
                del(people[len(people) - i - 1])
                highlight_index.append(j)
                break


    # NOTE: changing the order of loops below can change visual look.        
    for border in campus.rects:
        pygame.draw.rect(pygame.display.get_surface(),pygame.Color("BLACK"), border )     
    for j,t in enumerate(targets):
        color = pygame.Color("ORANGE") if j in highlight_index else pygame.Color("RED") 
        size = 23 if j in highlight_index else 20
        pygame.draw.circle(pygame.display.get_surface(), color,t, size)
    
    if args.debug:
        for special in campus.special_rule["special_areas"]:
            pygame.draw.rect(pygame.display.get_surface(),pygame.Color("GRAY"), special,1 )

    fps_counter()
    draw_title(campus)
    draw_fuksi_number(n_goal,total)
    draw_clock(clock_text)
    pygame.display.update()
    clock.tick(60)
