from turtle import Screen
import pygame
from pygame.locals import *
pygame.init()

class RemoveBlock:
    sizeoriginal = 0
    sizecountback = 0
    speed = 0
    frame = 0
    color = any
    remove_array = []
    
    screen = any
    
    def __init__(self,screen,size,speed,color):
        self.sizeoriginal = size;
        self.sizecountback = size;

        self.speed = speed
        self.color = color
        self.screen = screen
        
    def removeAnim(self):
        for block in self.remove_array:
            x = block.right-(block.right-block.left)/2
            y = block.top-(block.top-block.bottom)/2
        
            if self.sizecountback > 0 and len(self.remove_array) > 0:
                self.frame += 1
                if(self.frame == self.speed):
                    self.sizecountback -=1
                
                    self.frame = 0
                
            pygame.draw.polygon(self.screen,self.color,((x-self.sizecountback,y-self.sizecountback),(x+self.sizecountback,y-self.sizecountback),(x+self.sizecountback,y+self.sizecountback),(x-self.sizecountback,y+self.sizecountback)))
            
            if self.sizecountback == 0:
                self.remove_array.clear()
                self.sizecountback = self.sizeoriginal
                
            