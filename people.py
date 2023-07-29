"""Module defines behaviours of simulation characters"""
import pygame
import numpy as np
import math

#------------------
# HELPER FUNCTIONS
#------------------
def get_angle(target,pos):
    """Gets angle between targets and a given position in radians"""
    return np.arctan2(target[1] - pos[1], target[0] - pos[0])

def is_inside_rectangle(pos,rectangle):
    """Check if given positions is inside defined rectange (x,y,width,height)"""
    if rectangle[0] <= pos[0] <= rectangle[0] + rectangle[2]:
        if rectangle[1] <= pos[1] <= rectangle[1] + rectangle[3]:
            return True
    return False

#------------
# Characters
#------------

class Person:
    """Base class for character definitions

    Parameters:

    radius: int
        used in both drawing and collision detection
    can_collide: bool
        defines if collision between characters is active (doesn't effect borders)
    collision_cooldown: int
        Defines the cooldown time of collision detection between characters
    speed: float
        The magnitude of velocity vector i.e speed of the character
    color: str
        color of drawn shape
    pos: list 
        x,y coordinates of character
    vel: list
        x,y components of velocity i.e velocity vector.
    target: list
        x,y coordinates of characters target location
    """

    radius = 10
    can_collide = True
    collsion_cooldown = 0
    speed = 1.0
    color = "yellow"

    def __init__(self,pos,target,vel=None):
        self.pos = pos
        if vel == None:
            self.vel = [0.0,0.0]
            direction = 2*np.pi*np.random.random()
            self.vel[0] = self.speed*np.cos(direction)
            self.vel[1] = self.speed*np.sin(direction)
        else: 
            self.vel = vel
        self.target = target

    def move(self,rects):
        """ Handles character movement and collision detection between borders.
        
        Parameters:
        
        rects: list
            Contains list of rectangles as tuple(x,y,width,height) 
        """
        previous = self.pos.copy()
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        for rectangle in rects:   
            if is_inside_rectangle(self.pos,rectangle):
                if rectangle[0] >=  previous[0] or previous[0] >= rectangle[0] + rectangle[2]:
                    self.vel[0] *= -1
                if rectangle[1] >=  previous[1] or previous[1] >= rectangle[1] + rectangle[3]:
                    self.vel[1] *= -1
                self.pos = previous
                self.can_collide = False
                if self.collsion_cooldown < 10:
                    self.collsion_cooldown = 5
                break

    def check_collision(self,point,radius):
        """Detect collision between self and given sphere

        Parameters:

        point: list
            x,y coordinates of a given sphere(character)
        radius: int
            radius of sphere
        
        Return: 
            bool
        """

        # NOTE: doing this using numpy functions has a lot of
        # overhead with small arrays. switched from:
        # np.linalg.norm -> np.sqrt -> math.sqrt (best perfomance) 
        diff = [self.pos[0] - point[0], self.pos[1] - point[1]]
        return 0 < math.sqrt((diff[0])**2 + (diff[1])**2) < self.radius + radius


    def update(self,people):
        """Updates self velocity vector

        Parameters:

        people: list 
            Contains list of People
        """
        if self.can_collide:
            for p in people:
                if self.check_collision(p.pos,p.radius):
                    self.can_collide = False
                    self.collsion_cooldown = 150 - np.random.randint(10,60)
                    direction =  p.give_direction(self)
                    self.vel[0] = self.speed*np.cos(direction)
                    self.vel[1] = self.speed*np.sin(direction)

        else:
            self.collsion_cooldown -= 1
            if self.collsion_cooldown == 0:
                self.can_collide = True
    
    def give_direction(self,other):
        """Get angle for new direction"""
        return 2*np.pi*np.random.random()

    def draw(self):
        """Draw character on screen"""
        pygame.draw.circle(pygame.display.get_surface(),pygame.Color(self.color),self.pos,self.radius)



class Fuksi(Person):
    """Definition of Fuksi(Person) object

    Parameters: (Listed only ones not in Person class)

    identity: str
        str representation of the type of character
    major: str
        major of character(physics, Maths, etc) (NOT USED ATM.)
        TODO:(?) define target based on major
    original_target: list
        x,y coordinates of target at init. used in implementation of 
        special rules
    special_rule: dict
        Dictionary containing list of areas (rectangles) and corresponding 
        special target coordinates. Allow for certain areas to be treated
        differently in simulation. Mainly used for areas where characters
        can get stuck. 
    """
    identity = "Fuksi"
    speed = 1.5
    def __init__(self,pos,target,vel=None,special_rule=None,major="Fysiikka"):
        super().__init__(pos,target,vel=vel)
        self.major = major
        self.original_target = target
        self.special_rule = special_rule

    def move(self,rects):
        """Handle movement of Fuksi

        Parameters:

        rects: list
            Contains list of rectangles as tuple(x,y,width,height)
        
        Notes:
            If map contains special rules and self is in one of the areas
            temporarily swap target with special target
        """
        if self.special_rule != None:
            for i, area in enumerate(self.special_rule["special_areas"]):
                if is_inside_rectangle(self.pos,area):
                    self.target = self.special_rule["special_targets"][i]
                    break
            else:
                self.target = self.original_target      
        super().move(rects)
    

    def give_direction(self,other):
        """ Get new direction angle

        Parameter:

        other: Person
            other character object

        Returns: float
            angle in radians

        Notes:
            Uses vonmises distribution weighted away from target
        """
        angle = get_angle(other.target,other.pos)
        return np.random.vonmises(angle - np.pi,1.0)
    
    def __str__(self):
        """Character dialog (Currently not used)
        
        Notes:
            TODO:(?) character dialog to stdout?
            Was an idea to make simulation generate dialog
            between some interractions, not implented atm.
        """
        quotes = ["ARRGGHHH MISSÄ MINÄ OLEN!",
                  "Saako tästä fuksipisteitä?"]
        return np.random.choice(quotes)



        


class Proffa(Person):
    """Definition of Proffa(Person) object

    Parameters: (Listed only ones not in Person class)

    identity: str
        str representation of the type of character
    """
    color = "gray"
    identity = "proffa"
    speed = 0.5
    radius = 15

    def __init__(self,pos,target,vel=None):
        """ Initialization

        Notes:
            Velocity initialization and normalization
            as random direction. This is different from others
            as to not allow bad initialization of velocity, other
            characters would get corrected at first interraction.
        """
        if vel == None:
            vel = [0.0,0.0]
            direction = 2*np.pi*np.random.random()
            vel[0] = self.speed*np.cos(direction)
            vel[1] = self.speed*np.sin(direction)
        magnitude = np.linalg.norm(vel)
        vel[0] *= self.speed/magnitude
        vel[1] *= self.speed/magnitude
        super().__init__(pos,target,vel=vel)

    
    def give_direction(self,other):
        """ Get new direction angle

        Parameter:

        other: Person
            other character object

        Returns: float
            angle in radians
            
        Notes:
            Gives correct direction to others target.
            small randomness added to fix some cases where 
            characters can get stuck. 
        """
        angle = get_angle(other.target,other.pos) + 0.05*np.pi*np.random.rand() - 0.025*np.pi
        return angle 
        

class Opiskelija(Person):
    """Definition of Opiskelija(Person) object

    Parameters: (Listed only ones not in Person class)

    identity: str
        str representation of the type of character
    major: str
        major of character(physics, Maths, etc) (NOT USED ATM.)
        TODO:(?) define target based on major
    original_target: list
        x,y coordinates of target at init. used in implementation of 
        special rules
    special_rule: dict
        Dictionary containing list of areas (rectangles) and corresponding 
        special target coordinates. Allow for certain areas to be treated
        differently in simulation. Mainly used for areas where characters
        can get stuck.
    n: int 
        Academic year (1..n) used to determine behaviour.
    """
    identity = "Opiskelija"
    color = "blue"

    def __init__(self,pos,target,n,vel=None,special_rule=None,major="Fysiikka"):
        super().__init__(pos,target,vel=vel)
        self.major = major
        self.original_target = target
        self.special_rule = special_rule
        self.n = n
        self.radius = 10 + self.n//2
    
    def move(self,rects):
        """Handle movement of Fuksi

        Parameters:

        rects: list
            Contains list of rectangles as tuple(x,y,width,height)
        
        Notes:
            -If map contains special rules and self is in one of the areas
             temporarily swap target with special target. 
            -If n larger than 5 movement is implemented as a biased (towards target)
             random walk. otherwise use parent class method.
        """
        if self.n <= 5:
            if self.special_rule != None:
                for i, area in enumerate(self.special_rule["special_areas"]):
                    if is_inside_rectangle(self.pos,area):
                        self.target = self.special_rule["special_targets"][i]
                        break
                else:
                    self.target = self.original_target
            super().move(rects)
        else:

            x_move = 0
            y_move = 0

            direction = np.random.randint(1,5)
            if direction == 1:
                    x_move = (2 + round(self.vel[0]))
            elif direction == 2:
                    x_move = -(2 + round(self.vel[0]))
            elif direction == 3:
                    y_move = -(2 + round(self.vel[1]))
            elif direction == 4:
                    y_move = (2 + round(self.vel[1]))
            else:
                x_move = np.sign(self.target[0] - self.pos[0])*2
                y_move = np.sign(self.target[1] - self.pos[1])*2

            for rect in rects:
                 if  is_inside_rectangle([self.pos[0] + x_move,self.pos[1] + y_move],rect):
                      break
            else:
                 self.pos[0] += x_move
                 self.pos[1] += y_move

    def give_direction(self,other):
        """ Get new direction angle

        Parameter:

        other: Person
            other character object

        Returns: float
            angle in radians
            
        Notes:
            if n <= 5:
                gives direction using vonmises distribution
                towards target, larger n gives more accuracy.
            else:
                gives completely random direction
        """
        if self.n <= 5:
            angle = get_angle(other.target,other.pos)
            return np.random.vonmises(angle,self.n)
        else:
            return super().give_direction(other)
    
