"""This module defines all functionality of different people"""
import pygame
import numpy as np
import math


def get_angle(target,pos):
    return np.arctan2(target[1]-pos[1],target[0]-pos[0])

def is_inside_rectangle(pos,rectangle):
    if rectangle[0] <= pos[0] <=  rectangle[0] + rectangle[2]:
        if rectangle[1] <= pos[1] <=  rectangle[1] + rectangle[3]:
            return True
    return False


class Person:
    radius = 10
    can_collide = True
    collsion_cooldown = 0
    speed = 1
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
        previous = self.pos.copy()
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        for rectangle in rects:   
            if is_inside_rectangle(self.pos,rectangle):
                if rectangle[0] >=  previous[0]  or previous[0] >= rectangle[0] + rectangle[2]:
                    self.vel[0] *= -1
                if rectangle[1] >=  previous[1]  or previous[1] >= rectangle[1] + rectangle[3]:
                    self.vel[1] *= -1
                self.pos = previous
                self.can_collide = False
                self.collsion_cooldown = 5
                break


    def check_collision(self,point,radius):
        # NOTE: doing this using numpy functions has a lot of
        # overhead with small arrays. switched from:
        # np.linalg.norm -> np.sqrt -> math.sqrt (best perfomance) 
        diff = [self.pos[0] - point[0],self.pos[1] - point[1]]
        return 0 < math.sqrt((diff[0])**2 + (diff[1])**2) < self.radius + radius


    def update(self,people):
        if self.can_collide:
            for p in people:
                if self.check_collision(p.pos,p.radius):
                    self.can_collide = False
                    self.collsion_cooldown = 220 - np.random.randint(10,60)
                    direction =  p.give_direction(self)
                    # check sin cos stuff
                    self.vel[0] = self.speed*np.cos(direction)
                    self.vel[1] = self.speed*np.sin(direction)
                    #print(self)
                    

        else:
            self.collsion_cooldown -= 1
            if self.collsion_cooldown == 0:
                self.can_collide = True
    
    def give_direction(self,other):
        return 2*np.pi*np.random.random()

    def draw(self):
        pygame.draw.circle(pygame.display.get_surface(), pygame.Color(self.color),self.pos, self.radius)



class Fuksi(Person):
    identity="Fuksi"
    speed = 1.5

    def __init__(self, pos,target,vel=None,major="Fysiikka"):
        super().__init__(pos,target,vel=vel)
        self.major = major

    def give_direction(self,other):
        angle = get_angle(other.target,other.pos)
        return np.random.vonmises(angle - np.pi,1.0)
    
    def __str__(self):
        quotes = ["ARRGGHHH MISSÄ MINÄ OLEN!",
                  "Saako tästä fuksipisteitä?"]
        return np.random.choice(quotes)



        


class Proffa(Person):
    color = "gray"
    identity="proffa"
    speed = 0.5
    radius = 15

    def __init__(self, pos,target,vel=None):
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
        """"""
        angle = get_angle(other.target,other.pos)
        return angle 
        

class Opiskelija(Person):
    identity="Opiskelija"
    color="blue"

    def __init__(self, pos,target,n,vel=None,major="Fysiikka"):
        super().__init__(pos,target,vel=vel)
        self.major = major
        self.target = target
        self.n = n
        self.radius = 10 + self.n//2
    
    def move(self,rects):
        if self.n <= 5:
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
        if self.n <= 5:
            angle = get_angle(other.target,other.pos)
            return np.random.vonmises(angle,self.n)
        else:
            return 2*np.pi*np.random.random()
    
