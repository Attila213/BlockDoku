import py
import pygame,math,random,sys,os
import functions as fun
from ANIM.CubeBackground import Background
from ANIM.RemoveCube import RemoveBlock
from pygame.locals import *
import json

mainClock = pygame.time.Clock()
pygame.init()


window = (800,730)
screen = pygame.display.set_mode(window,0,32)

bc = Background(window,screen)
rm = RemoveBlock(screen,20,50,(0, 220, 220))


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

mouse_starter_temp_pos = "None"
hold_mousebutton = False
#Fill-arrays------------------------------------------------------------
fun.fillArray(map,9,9,48,190,10,True)
for i in range(0,3):        
    fun.fillArray(maps[i],5,5,42,60 + i*240,470,False)
    fun.fillArray(maps_cons[i],5,5,42,60 + i*240,470,False)
#-----------------------------------------------------------------------

SCORE = 0

while True:
    success = False
    mouse_on = [[],[],[],[]]
    mx,my = pygame.mouse.get_pos()
    drop = False
    screen.fill((10,17,30))
    
    
    for i in range(3):
        try:
            if mx > maps[i][0][0][1].left and mx < maps[i][0][len(maps[i])-1][1].right and my > maps[i][0][0][1].top and my < maps[i][len(maps[i])-1][0][1]. bottom:
                mouse_on = [fun.checkIndex([mx,my],maps[i]),maps[i],maps_cons[i],map_shapes[i],i]
            if mx > map[0][0][1].left and mx < map[0][8][1].right and my > map[0][0][1].top and my < map[len(map)-1][0][1].bottom:
                mouse_on = [fun.checkIndex([mx,my],map),map]
        except:
            continue

    #QUIT
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()    

    #EVENTS-----------------------------------------------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            #out off range
            
            try:
                if hold_mousebutton == False and mouse_on[1][mouse_on[0][0]][mouse_on[0][1]][0] == "block" and mouse_on[1] != map:

                    #rögízetett egérpozició
                    mouse_starter_temp_pos = [mx,my]
                    
                    mouse_shape_holding = mouse_on[3]
                    map_index = mouse_on[4]
                    
                    #rögzített map
                    starter_map = mouse_on[1]
                    cons_map = mouse_on[2]
                
                    #-----------------------------------------------------------------------     
                    #rögízetett-kattintott x ,y
                    SX = mouse_on[0][0]
                    SY = mouse_on[0][1]     
                    
                    #block és egér közti hely #KELL
                    paddingX = mouse_starter_temp_pos[0]-starter_map[SX][SY][1].x
                    paddingY = mouse_starter_temp_pos[1]-starter_map[SX][SY][1].y
                                
                    #----------------------------------------------------------------------- 
                    
                    hold_mousebutton = True
            except:
                continue
        
        if mouse_on[1] == map and hold_mousebutton == True:
            count =0
            for i in range(len(map)):
                for j in range(len(map)):
                    if(map[i][j][0] == "test"):
                        count +=1;
            
            if count == len(mouse_shape_holding):
                drop = True
                
        if event.type == pygame.MOUSEBUTTONUP:
            if drop == False and hold_mousebutton == True:
                for i in range(5):
                    for j in range(5):
                        if starter_map[i][j][0] == "block":
                            starter_map[i][j][1].x = cons_map[i][j][1].x
                            starter_map[i][j][1].y = cons_map[i][j][1].y
            elif drop == True and hold_mousebutton == True:
                for i in range(len(map)):
                    for j in range(len(map)):
                        if map[i][j][0] == "test":
                            map[i][j][0] = "block"
                starter_map.clear()
                fun.fillArray(starter_map,5,5,42,60 + i*240,470,False)
                
                
                #kijött egy forma vagy egy vonal de lehet egyszerre több is--------------
                del_row=[]
                del_col=[]
                
                j_counter=[]
                #row
                for i in range(len(map)):
                    ic = 0  
                    for j in range(len(map[i])):
                        if map[i][j][0] == "block":
                            ic += 1
                            if ic == 9:
                                del_row.append(i)
                            j_counter.append(j)
                #col
                for i in range(9):
                    c =0
                    for j in j_counter:
                        if j ==i:
                            c +=1
                            if c == 9:
                                del_col.append(i)
                
                #3x3
                
                
                for i in del_col:
                    for j in range(len(map)):
                        map[j][i][0] = "mapL"
                        rm.remove_array.append(map[j][i][1])
                        
                for i in del_row:
                    for j in range(len(map)):
                        map[i][j][0] = "mapL"
                        rm.remove_array.append(map[i][j][1])


                #------------------------------------------------------------
                
                
            hold_mousebutton = False
            
    for i in range(len(map)):
        for j in range(len(map)):
            if map[i][j][0] == "test":
                map[i][j][0] = "mapL"
    
    #DRAW SHAPES------------------------------------------------------------
        
    counter = [[],[],[]]
    for i in range(0,3):
        counter[i] = 0
        for j in range(len(maps[i])):
            for k in range(len(maps[i])):
                if maps[i][j][k][0] == "block":
                    counter[i] += 1
       
    if counter[0] ==0 and counter[1] ==0 and counter[2] ==0: 
        map_shapes.clear()
        for i in range(3):
            fun.clearTable(maps[i],"mapB")    
            rand = random.randint(1,globals["id"])-1
            map_shapes.append((shapes[str(rand)]["pos"]))
    
        for i in range(0,3):     
            maps[i].clear()   
            fun.fillArray(maps[i],5,5,42,60 + i*240,470,False)
            fun.fillArray(maps_cons[i],5,5,42,60 + i*240,470,False)
            
        for i in range(len(map_shapes)):
            for j in map_shapes[i]:
                maps[i][j[0]][j[1]][0] = "block"
    #-----------------------------------------------------------------------
              
    if(hold_mousebutton == True):
        #mozgatás
        for i in range(len(starter_map)):
            for j in range(len(starter_map)):
                if starter_map[i][j][0] == "block":
                    addY = i-SX
                    addX = j-SY
                    
                    starter_map[i][j][1].x = (mx +addX*43) -paddingX      
                    starter_map[i][j][1].y = (my +addY*43)-paddingY

        if mouse_on[1] == map:
            arr = []
            for i in mouse_shape_holding:
                try:
                    if mouse_on[1][mouse_on[0][0]-SX+i[0]][mouse_on[0][1]-SY+i[1]][0] != "block" and mouse_on[0][1]-SY+i[1] >=0 and mouse_on[0][0]-SX+i[0] >=0:   
                        mouse_on[1][mouse_on[0][0]-SX+i[0]][mouse_on[0][1]-SY+i[1]][0]= "test"
                except:
                    continue
    #-----------------------------------------------------------------------
    bc.tick()
    pygame.draw.rect(screen, (10,10,10),pygame.Rect(map[0][0][1].x,map[0][0][1].y,map[0][8][1].right-map[0][0][1].left,map[0][8][1].right-map[0][0][1].left))
    

    fun.drawMap(screen,map)
    
    #TEDD BELE FÜGGVÉNYBE
    for i in range(0,3):
        fun.drawMap(screen,maps[i])
    
    rm.removeAnim()
            
            
    
        
        
    pygame.display.update()