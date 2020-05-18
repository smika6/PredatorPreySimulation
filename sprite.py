# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 00:21:38 2020

@author: smika
"""
#pretty self explanitory and common
class Sprite(object):
    
    LEFT = True
    RIGHT = False
    
    UP = False
    DOWN = True
    
    STILL = None
    
    def __init__(self, pygame, window, x, y, width, height, x_vel, y_vel, color = (255, 255, 255), name = "Sprite"):
        self.name = name
        self.pygame = pygame
        self.window = window
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.cell_width = width
        self.cell_height = height
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.x_direction = None
        self.y_direction = None
        self.limits = []
        
    def render(self):
        offset = 2
        self.pygame.draw.rect(self.window, self.color, (self.x*self.cell_width+offset+1, self.y*self.cell_height+offset+1, self.width-offset*2, self.height-offset*2) )
    
    def update(self):
        nodiag = True
        if nodiag:
            if self.x_direction and self.x_direction != Sprite.STILL:
                self.x -= self.x_vel
            elif not self.x_direction and self.x_direction != Sprite.STILL:
                self.x += self.x_vel
            elif self.y_direction and self.y_direction != Sprite.STILL:
                self.y += self.y_vel
            elif not self.y_direction and self.y_direction != Sprite.STILL:
                self.y -= self.y_vel
            self.x_direction = Sprite.STILL
            self.y_direction = Sprite.STILL
        else:
            if self.x_direction and self.x_direction != Sprite.STILL:
                self.x -= self.x_vel
            if not self.x_direction and self.x_direction != Sprite.STILL:
                self.x += self.x_vel
            if self.y_direction and self.y_direction != Sprite.STILL:
                self.y += self.y_vel
            if not self.y_direction and self.y_direction != Sprite.STILL:
                self.y -= self.y_vel
            self.x_direction = Sprite.STILL
            self.y_direction = Sprite.STILL
    
    def change_x_direction(self):
        self.x_direction = not (self.x_direction)
    
    def change_y_direction(self):
        self.y_direction = not (self.y_direction)
    
    def set_x_direction(self, direction):
        self.x_direction = direction
    
    def set_y_direction(self, direction):
        self.y_direction = direction
    
    def __str__(self):
        return f"Sprite Object: {self.name} \n    x:{self.x} \n    y:{self.y} \n    width:{self.width} \n    height:{self.height} \n    x_vel:{self.x_vel} \n    y_vel:{self.y_vel} \n    x_direction:{self.x_direction} \n    y_direction:{self.y_direction} \n    color:{self.color} \n    window:{self.window}"