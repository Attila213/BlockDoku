from calendar import c
from turtle import color, st
import pygame,math,random,sys,os
import functions as fun
import json
from json.decoder import JSONDecodeError
from threading import Thread
mainClock = pygame.time.Clock()


pygame.init()
#----------------------------------------------------------------------
def loadJson(filename,value):
    
    arr = any
    try:
        with open(filename+".json","r") as f:
            try:
                arr=json.load(f)
            except:
                arr = value
    except:
        writeJson(filename,value)
        with open(filename+".json","r") as f:
            arr=json.load(f)
    return arr

def writeJson(filename,arr):
    with open(filename+".json", 'w') as outfile:
        json.dump(arr, outfile)

def CubeAni(size,res,pos,mode,screen):
    col = pos[0] 
    row = pos[1] 

    
    x = map[col][row][1].right-(map[col][row][1].right-map[col][row][1].left)/2
    y = map[col][row][1].top-(map[col][row][1].top-map[col][row][1].bottom)/2
    
    frame = 0
    
    if mode == "mapB":
        map[col][row][0] = mode
        
    while(size != res):
        frame += 1
        
        if(frame == 700):
            if size > res:
                size -= 1
            if size < res:
                size += 1
            frame = 0
            
        if mode != "mapB" and size == res:
            map[col][row][0] = mode
        
                
        pygame.draw.polygon(screen,(0, 255, 140),((x-size,y-size),(x+size,y-size),(x+size,y+size),(x-size,y+size)))
        

#----------------------------------------------------------------------
click_enabled = True
num = "";
temp = []
map = []
fun.fillArray(map,5,5,40,300,200,(100,100,100))
#----------------------------------------------------------------------

screen = pygame.display.set_mode((800,730),0,32)

while True:
    mx,my = pygame.mouse.get_pos()
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            #CLEAR--------------------------------------
            for i in range(5):
                for j in range(5):
                    if map[i][j][0] == "test":
                        map[i][j][0] = "mapB"    
            #-------------------------------------------
            col,row = fun.checkIndex((mx,my),map);
            
            if [col,row] in temp:
                temp.remove([col,row])
            else:
                temp.append([col,row])

            pos = [col,row]
            
            if map[col][row][0] == "mapB":
                x = Thread(target=CubeAni, args=(0,20,pos,"block",screen))
                x.start()
            elif map[col][row][0] == "block":
                x = Thread(target=CubeAni, args=(20,0,pos,"mapB",screen))
                x.start()
                
              
            
        if event.type == pygame.KEYDOWN: 
            shapes = loadJson("JSON/shapes",{})
            globals=loadJson("JSON/globals",{"id":0}) 
            #Show pieces
            if event.key == pygame.K_RETURN:

                if num == "":    
                    for i in range(globals["id"]):    
                        print(i,shapes[str(i)]["pos"])
                    print()
                else:
                    #CLEAR--------------------------------------
                    for i in range(5):
                        for j in range(5):
                            if map[i][j][0] == "test":
                                map[i][j][0] = "mapB"    
                    #-------------------------------------------
                    try:
                        for i in shapes[str(num)]["pos"]:
                            map[i[0]][i[1]][0] = "test"
                            
                    except:
                        print("IndexOutOfRange: "+ num)    
                num = ""
                         
            #Insert datas to JSON
            if event.key == pygame.K_COMMA:
                file_writing_permission = True

                #check if is there any shape like this one----------------------
                for i in range(globals["id"]):
                    j = shapes[str(i)]["pos"]
                    
                    if len(j) == len(temp):
                        counter = 0
                        for t in temp:
                            if t in j:
                                counter += 1
                        if counter == len(j):
                            file_writing_permission = False
                            print("PERMISSION DENIED")

                    
                if file_writing_permission == True and (len(temp) > 0):
                    
                    #-----------------CLEAR------------------
                    for i in range(5):
                        for j in range(5):
                            map[i][j][0] = "mapB"
                    #----------------------------------------

                    shapes[globals["id"]] ={}
                    shapes[globals["id"]]["pos"] = temp
      
                    globals["id"] += 1
                    #Json write-----------------------------
                    
                    writeJson("JSON/globals",globals)
                    writeJson("JSON/shapes",shapes)
                    temp.clear()
            
            if event.key == pygame.K_0:
                num += "0"
                print(num)
            if event.key == pygame.K_1:
                num += "1"
                print(num)
            if event.key == pygame.K_2:
                num += "2"
                print(num)
            if event.key == pygame.K_3:
                num += "3"
                print(num)
            if event.key == pygame.K_4:
                num += "4"
                print(num)
            if event.key == pygame.K_5:
                num += "5"
                print(num)
            if event.key == pygame.K_6:
                num += "6"
                print(num)
            if event.key == pygame.K_7:
                num += "7"
                print(num)
            if event.key == pygame.K_8:
                num += "8"
                print(num)
            if event.key == pygame.K_9:
                num += "9"
                print(num)
            if event.key == pygame.K_BACKSPACE:
                num = num[:-1]
                print(num)
                
            if event.key == pygame.K_DELETE:
                keys_list = list(shapes)
                key = keys_list[int(num)]
                shapes.pop(key)
                
                   
                #Reset ID-s---------------------------------------
                new_shapes = {}
                counter =0
                for i in range(globals["id"]):
                    try:
                        new_shapes[counter] = {}
                        new_shapes[counter]["pos"] = shapes[str(i)]["pos"]
                    except:
                        continue
                    counter += 1
                globals["id"] = counter
                num = ""
                #-------------------------------------------------
                
                shapes = new_shapes
                writeJson("JSON/globals",globals)
                writeJson("JSON/shapes",shapes)

    fun.drawMap(screen,map)
    mainClock.tick(120)
    pygame.display.update()