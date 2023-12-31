"""Module containing map information

Notes:
    In order to implement new map, create new class with the 
    same parameters as the other maps, add it to commandline options
    and in main file (fuksi_simulaattori.py) add a new case in the 
    match statement in the function initialize_simulation().
"""

class Kumpula:
    """ Map of Kumpula 

    Parameters:

    name: dict
        Dictionary containing name of map in implemented languages
    rects: list
        Rectangles defining the borders of the map
    spawn_points: list
        x,y coordinates of spawn points of Fuksi(People) 
    spawn_areas: list
        Rectangles defining spawn areas of People
    targets: list
        x,y points defining targets of map, these are drawn on screen
    target_mapping: dict
        Dictionary containing spawnarea assigment between different types
        of characters. TODO(?): extend the functionality of this.
    special_rule: dict
        Dictionary containing list of areas (rectangles) and corresponding 
        special target coordinates. Allow for certain areas to be treated
        differently in simulation. Mainly used for areas where characters
        can get stuck.
    """
    name = {"fin":"KUMPULA",
            "eng":"KUMPULA",
            "swe":"GUMTÄKT"}
    
    def __init__(self) -> None:
        self.rects = [
                        (137,252,30,400),
                        (137,252,500,30),
                        (137,252,193,150),
                        (380,252,257,150),
                        (137,652,450,200),
                        (550,542,155,340),
                        (230,460,100,150),
                        (380,460,100,150),
                        (637,372,393,30),
                        (1010,380,20,100),
                        (637,455,25,150),
                        (637,455,320,30),
                        (920,455,25,150),
                        (800,605,150,380),
                        (1000,650,130,260),
                        (1200,630,130,360),
                        (1300,460,30,200),
                        (800,960,450,30),
                        (700,80,100,300),
                        (700,80,375,30),
                        (1075,80,30,400),
                        (1075,460,230,30),
                        (925,530,80,75),
                    ]
        self.spawn_points = [(610,490),(955,495),(1200,500)]
        self.spawn_areas  = [(200,430,300,200),
                             (850,160,200,200),
                             (1000,580,200,200)]
        self.targets = [(390,300),(470,393),
                        (560,630),(1100,660)]
        self.target_mapping = {"fuksi":[1,2,3], "opiskelija":[0]}
        self.special_rule = {"special_areas":[(800,100,300,280),(1030,380,50,80)],"special_targets":[(1100,390),(1050,800)]}

class Areena:
    """ Simple Rectangular Areena map 

    Parameters:

    name: dict
        Dictionary containing name of map in implemented languages
    rects: list
        Rectangles defining the borders of the map
    spawn_points: list
        x,y coordinates of spawn points of Fuksi(People) 
    spawn_areas: list
        Rectangles defining spawn areas of People
    targets: list
        x,y points defining targets of map, these are drawn on screen
    target_mapping: dict
        Dictionary containing spawnarea assigment between different types
        of characters. TODO(?): extend the functionality of this.
    special_rule: dict
        Dictionary containing list of areas (rectangles) and corresponding 
        special target coordinates. Allow for certain areas to be treated
        differently in simulation. Mainly used for areas where characters
        can get stuck.
    """
    name = {"fin":"AREENA",
            "eng":"AREENA",
            "swe":"AREENA"}
    
    def __init__(self) -> None:
        self.rects = [
                        (100,100,20,700),
                        (100,100,1200,20),
                        (1300,100,20,720),
                        (100,800,1200,20),
                    ]
        self.spawn_points = [(600,350)]
        self.spawn_areas  = [(200,200,1000,500)]
        self.targets = [(300,300),(300,600),(1100,600),(1100,300)]
        self.target_mapping = {"fuksi":[0,1,2,3], "opiskelija":[0,1,2,3]}
        self.special_rule = {"special_areas":[],"special_targets":[]}