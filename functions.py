import pygame,math,random,sys,os
from pygame import display
from pygame.locals import *
import json

def fillArray(arr,length,width,size,pad_horizontal,pad_verical,color):
    size = size;
    border = size +1;
    for i in range(width):
        arr1 = []
        for j in range(length):
            if(color == True):
                arr1.append(["mapL",pygame.Rect(pad_horizontal+(j*border),pad_verical+(i*border),size,size)])
            else:
                arr1.append(["mapB",pygame.Rect(pad_horizontal+(j*border),pad_verical+(i*border),size,size)])
    
        arr.append(arr1)

def drawMap(surf,arr):
    for sor in arr:
        for oszlop in sor:
            if oszlop[0] == "mapD":
                pygame.draw.rect(surf,(150,150,150),oszlop[1])
            elif oszlop[0] == "mapL":
                pygame.draw.rect(surf,(100,100,100),oszlop[1])
            elif oszlop[0] == "block":
                pygame.draw.rect(surf,(0, 255, 140),oszlop[1])
            elif oszlop[0] == "test":
                pygame.draw.rect(surf,(247, 5, 227),oszlop[1])

def checkIndex(pos,arr):
    row = -1
    col = -1
    for i in range(len(arr)):
        for j in range(len(arr)):
            if pos[0] >= arr[i][j][1].left and pos[0] <= arr[i][j][1].right and pos[1] >= arr[i][j][1].top and pos[1] <= arr[i][j][1].bottom:
                col = j
                row = i
                
            
    return row,col
            
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

def clearTable(arr,block):
    for i in range(len(arr)):
        for j in range(len(arr)):
            arr[i][j][0] = block
        
