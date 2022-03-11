import imp
from itertools import count
from traceback import print_last
from typing import Any
from numpy import block
import pygame,math,random,sys,os
import functions as fun
from pygame.locals import *
import json

mainClock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((800,730),0,32)
pygame.display.set_caption("BlockDoku")
#-----------------------------------------------------------------------
shapes = fun.loadJson("JSON/shapes",{})
globals = fun.loadJson("JSON/globals",{})

map = []
maps=[[],[],[]]
maps_cons = [[],[],[]]
map_shapes = []
mouse_map_pos = any

drop = False
current_blocks = []

mouse_starter_temp_pos = "None"
hold_mousebutton = False
frame = 0
#Fill-arrays------------------------------------------------------------
fun.fillArray(map,9,9,48,190,10,True)
for i in range(0,3):        
    fun.fillArray(maps[i],5,5,42,60 + i*240,470,False)
    fun.fillArray(maps_cons[i],5,5,42,60 + i*240,470,False)
#-----------------------------------------------------------------------
mouse_on = any

while True:
    
    screen.fill((0,0,0))
    mx,my = pygame.mouse.get_pos()
    frame += 1
    
    
    for i in range(3):
        if mx > maps[i][0][0][1].left and mx < maps[i][0][len(maps[i])-1][1].right and my > maps[i][0][0][1].top and my < maps[i][len(maps[i])-1][0][1]. bottom:
            mouse_on = [fun.checkIndex([mx,my],maps[i]),maps[i]];
        if mx > map[0][0][1].left and mx < map[0][8][1].right and my > map[0][0][1].top and my < map[len(map)-1][0][1].bottom:
            mouse_on = [fun.checkIndex([mx,my],map),map];
    
    #QUIT
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()    

    #-----------------------------------------------------------------------
    if event.type == pygame.MOUSEBUTTONDOWN:
        if hold_mousebutton == False and mouse_on[1][mouse_on[0][0]][mouse_on[0][1]][0] == "block":

            #rögízetett egérpozició
            mouse_starter_temp_pos = [mx,my]
            
            #rögzített map
            starter_map = mouse_on[1]
            
            #a mapon lévő blockok helye
            for i in range(len(starter_map)):
                for j in range(len(starter_map)):
                    if starter_map[i][j][0] =="block":
                        current_blocks.append(maps_cons[i][j][0][1])
            
            #-----------------------------------------------------------------------     
            #rögízetett-kattintott x ,y   őőőőőőőőőőőőőőőőőőőlehet
            SX,SY = fun.checkIndex([mouse_starter_temp_pos[0],mouse_starter_temp_pos[1]],starter_map)
            
            #rögzített tömbelem--
            starter = [starter_map[SX][SY][1].x,starter_map[SX][SY][1].y]
            
            #rögzített block eltolóás
            paddingX = mouse_starter_temp_pos[0]-starter_map[SX][SY][1].x
            paddingY = mouse_starter_temp_pos[1]-starter_map[SX][SY][1].y
            
        
            
            hold_mousebutton = True;
                
    if event.type == pygame.MOUSEBUTTONUP:
        if drop == False and hold_mousebutton == True:
            starter_map[SX][SY][1].x = starter[0]
            starter_map[SX][SY][1].y = starter[1]

            hold_mousebutton = False
            current_blocks.clear()
    #Draw shapes------------------------------------------------------------
    if len(map_shapes) ==0:
        for i in range(3):
            fun.clearTable(maps[i],"mapB")    
            rand = random.randint(1,globals["id"])-1
            map_shapes.append((shapes[str(rand)]["pos"]))
              
    for i in range(len(map_shapes)):
        for j in map_shapes[i]:
            maps[i][j[0]][j[1]][0] = "block"
    #-----------------------------------------------------------------------
          
    #rögzíteni kell a kattintott map összes block alap pozícióját
    
    if(hold_mousebutton == True):
        starter_map[SX][SY][1].x = mx-paddingX
        starter_map[SX][SY][1].y = my-paddingY
        
    #-----------------------------------------------------------------------
    fun.drawMap(screen,map)
    for i in range(0,3):
        fun.drawMap(screen,maps[i])

    pygame.display.update()