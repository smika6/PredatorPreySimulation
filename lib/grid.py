# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 01:25:02 2020

@author: smika
"""
from lib.sprite import Sprite
import random

class Grid(object):
    
    def __init__(self, pygame, window, HUD_scale, cell_count = 14, width = 2, prey_count = 50, color = (101,101,101)):
        self.pygame = pygame
        self.window = window
        self.HUD_scale = HUD_scale
        self.color = color
        self.width = width
        self.cell_count = cell_count
        self.prey_distribtion = ''
        self.enviornment_complexity = ''
        self.prey = []
        self.obstacles = []
        self.predator = Sprite(pygame, window, 0, 0, 0, 0, 0, 0, color = (0,0,0), name = 'predator')
        self.dead_prey = 0
        self.prey_count = prey_count
        
        #create the dict and populate it as empty
        self.bool_dict = {}
        for x in range(self.cell_count):
            for y in range(self.cell_count):
                self.bool_dict[x,y] = False
        self.sprite_dict = {}
        for x in range(self.cell_count):
            for y in range(self.cell_count):
                self.sprite_dict[x,y] = None
    
    @property
    def elements(self):
        return self.prey + self.obstacles
    
    def empty_cells(self):
        empty = []
        for y in range(0,self.cell_count):
            for x in range(0,self.cell_count):
                if not self.bool_dict[x,y]:
                    empty.append( (x,y) )
        return empty
    
    def update(self):
        
        #constrain
        width, height = self.pygame.display.get_surface().get_size()
        position = (self.predator.x,self.predator.y)
        self.predator.update()
        for element in self.elements:
            if element.x == self.predator.x:
                if element.y == self.predator.y:
                    if element.name == 'obstacle':
                        self.predator.x = position[0]
                        self.predator.y = position[1]
                    if element.name == 'prey':
                        self.prey.remove(element)
                        self.dead_prey = self.dead_prey + 1
        if self.predator.x < 0:
            self.predator.x = 0
        if self.predator.x > self.cell_count-1:
            self.predator.x = self.cell_count-1
        if self.predator.y < 0:
            self.predator.y = 0
        if self.predator.y > self.cell_count-1:
            self.predator.y = self.cell_count-1
        for prey in self.prey:
            prey.update()
        for obstacle in self.obstacles:
            obstacle.update()
    
    def show_boolean_map(self):
        display = ""
        for y in range(self.cell_count):
            for x in range(self.cell_count):
                display = display + str(self.bool_dict[x,y]) + ("  " if not self.bool_dict[x,y] else "   ") #fix for letter length
            display = display + " \n"
        print(display)
    
    def show_sprite_name_map(self):
        display = ""
        for y in range(self.cell_count):
            for x in range(self.cell_count):
                if self.sprite_dict[x,y] == None:
                    display = display + "None\t"
                if isinstance(self.sprite_dict[x,y], Sprite):
                    display = display + self.sprite_dict[x,y].name + "\t"
            display = display + " \n"
        print(display)
                
    
    def simulation_setup(self, prey_distribtion, enviornment_complexity):
        #computation data
        self.prey_distribtion = prey_distribtion
        self.enviornment_complexity = enviornment_complexity
        width, height = self.pygame.display.get_surface().get_size()
        width = width*(1-self.HUD_scale)
        cell_width = width/self.cell_count
        cell_height = height/self.cell_count
        
        #for an even prey distribution
        if prey_distribtion == 'even':
            for y in range(int(round(self.cell_count/2)+1)):
                for x in range(int(round(self.cell_count/2))):
                    if len(self.prey) < self.prey_count:
                        new_prey = Sprite(self.pygame, self.window, 2*x, 2*y, cell_width, cell_height, 0, 0, color=(255,255,255),name='prey')
                        self.prey.append(new_prey)
                        self.bool_dict[2*x,2*y] = True
                        self.sprite_dict[2*x,2*y] = new_prey
        
        #for a random prey distribution
        if prey_distribtion == 'random':
            used = []
            while len(used) < self.prey_count:
                rand_x = random.randint(0, self.cell_count-1)
                rand_y = random.randint(0, self.cell_count-1)
                if (rand_x, rand_y) not in used:
                    if len(self.prey) < self.prey_count:
                        used.append((rand_x,rand_y))
                        new_prey = Sprite(self.pygame, self.window, rand_x, rand_y, cell_width, cell_height, 0, 0, color=(255,255,255),name='prey')
                        self.prey.append(new_prey)
                        self.bool_dict[rand_x,rand_y] = True
                        self.sprite_dict[rand_x,rand_y] = new_prey
        
        #for a clumped prey distribution
        if prey_distribtion == 'clumped':
            clump_size = 4
            distance = 2
            prey_count = self.prey_count
            used = []
            attempts = 0
            retrys = 0
            cutoff = 100
            while len(used) < prey_count*clump_size:
                attempts = attempts + 1
                rand_x = random.randint(0, self.cell_count-2)
                rand_y = random.randint(0, self.cell_count-2)
                not_near_count = 0
                for prev in used:
                    if ((prev[0]-rand_x)**2 + (prev[1]-rand_y)**2)**0.5 > distance:
                        not_near_count = not_near_count + 1
                if not_near_count == len(used):
                    attempts = 0
                    size = clump_size**0.5
                    for a in range(int(round(size))):
                        for b in range(int(round(size))):
                            used.append((rand_x+a,rand_y+b))
                if attempts > cutoff:
                    retrys = retrys + 1
                    used = []
                    if retrys == 3:
                        #print("Unable to resolve clusters distancing within given confinds: reducing prey cluster count")
                        prey_count = prey_count - 1
                        retrys = 0
            for pos in used:
                if len(self.prey) < self.prey_count:
                    new_prey = Sprite(self.pygame, self.window, (pos[0]), (pos[1]), cell_width, cell_height, 0, 0, color=(255,255,255),name='prey')
                    self.prey.append(new_prey)
                    self.bool_dict[pos[0],pos[1]] = True
                    self.sprite_dict[pos[0],pos[1]] = new_prey
        
        #decide the number of obstacles based on input
        number_of_obstacles = 0
        
        if enviornment_complexity == 'moderate':
            number_of_obstacles = 6
        
        if enviornment_complexity == 'complex':
            number_of_obstacles = 12
        
        #populate the obstacles 
        unpopulated_horizontals = []
        unpopulated_verticles = []
        for y in range(0,self.cell_count-1):
            for x in range(0,self.cell_count-1):
                if (not self.bool_dict[x,y] and not self.bool_dict[x+1,y]):
                    unpopulated_horizontals.append( (x,y) )
                if (not self.bool_dict[x,y] and not self.bool_dict[x,y+1]):
                    unpopulated_verticles.append( (x,y) )
        while number_of_obstacles > 0:
            #horizontals
            obstacle_start = random.choice(unpopulated_horizontals)
            obstacle_intercept = False
            obstacle_length = random.randint(2, 4)
            n = 0
            found = False
            while n < obstacle_length and not obstacle_intercept:
                if obstacle_start[0]+n < 10:
                    if not self.bool_dict[obstacle_start[0]+n,obstacle_start[1]]:
                        found = True
                        self.bool_dict[obstacle_start[0]+n,obstacle_start[1]] = True
                        new_obstacle = Sprite(self.pygame, self.window, obstacle_start[0]+n, obstacle_start[1], cell_width, cell_height, 0, 0, (0,0,0),name='obstacle')
                        self.obstacles.append(new_obstacle)
                        self.sprite_dict[obstacle_start[0]+n,obstacle_start[1]] = new_obstacle
                        n = n + 1
                    else:
                        obstacle_intercept = True
                else:
                    obstacle_intercept = True
            if found:
                number_of_obstacles = number_of_obstacles - 1
                found = False
            #verticles
            obstacle_start = random.choice(unpopulated_verticles)
            obstacle_intercept = False
            obstacle_length = random.randint(2, 4)
            n = 0
            found = False
            while n < obstacle_length and not obstacle_intercept:
                if obstacle_start[1]+n < 10:
                    if not self.bool_dict[obstacle_start[0],obstacle_start[1]+n]:
                        found = True
                        self.bool_dict[obstacle_start[0],obstacle_start[1]+n] = True
                        new_obstacle = Sprite(self.pygame, self.window, obstacle_start[0], obstacle_start[1]+n, cell_width, cell_height, 0, 0, color=(0,0,0),name='obstacle')
                        self.obstacles.append(new_obstacle)
                        self.sprite_dict[obstacle_start[0],obstacle_start[1]+n] = new_obstacle
                        n = n + 1
                    else:
                        obstacle_intercept = True
                else:
                    obstacle_intercept = True
            if found:
                number_of_obstacles = number_of_obstacles - 1
                found = False
                
        #spawn the predator
        spawn = random.choice(self.empty_cells())
        self.predator = Sprite(self.pygame, self.window, spawn[0], spawn[1], cell_width, cell_height, 1, 1, color = (255,0,0), name='predator')
        self.bool_dict[spawn[0],spawn[1]] = True
        self.sprite_dict[spawn[0],spawn[1]] = self.predator
        
    
    def render(self, blind_folded):
        width, height = self.pygame.display.get_surface().get_size()
        width = width*(1-self.HUD_scale)
        cell_width = width/self.cell_count
        cell_height = height/self.cell_count
        for x in range(self.cell_count+1):
            self.pygame.draw.line(self.window, self.color, (x*cell_width,0), (x*cell_width,height), self.width)
            self.pygame.draw.line(self.window, self.color, (0,x*cell_height), (width,x*cell_height), self.width)
        if not blind_folded:
            for prey in self.prey:
                prey.render()
        for obstacle in self.obstacles:
            obstacle.render()
        self.predator.render()
    

        
