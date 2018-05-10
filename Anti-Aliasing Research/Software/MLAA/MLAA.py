#!-*- conding: utf8 -*-

'''
Subpixel Morphological Anti-Aliasing algorithm.
Author: Daniel Centeno Einloft
Class: ADSP
Last modification in: 09/06/2017
'''

import cv2
import numpy as np
import math
import copy
def Validade_Window(j,i,Y):
    if((i-1>= 0)and(i+2< Y.shape[1])and(j-1>= 0)and(j+1< Y.shape[0])):
        return True
    else:
        return False

def neighbours(j,i,Y):
    lumaUp     = Y[j-1][i]
    lumaDown   = Y[j+1][i]
    lumaLeft   = Y[j][i-1]
    lumaRight  = Y[j][i+1]
    lumaCenter = Y[j][i]
    lumaDownLeft  = Y[j+1][i-1]
    lumaUpRight   = Y[j-1][i+1]
    lumaUpLeft    = Y[j-1][i-1]
    lumaDownRight =	Y[j+1][i+1] 
    return lumaUp,lumaDown,lumaLeft,lumaRight,lumaCenter,lumaDownLeft,lumaUpRight,lumaUpLeft,lumaDownRight

def isEdge(j,i,Y):
    if(Validade_Window(j,i,Y)):

        EDGE_THRESHOLD_MIN = 0.26 #lembrar: a escala esta em relacao a 1 e 0 
        EDGE_THRESHOLD_MAX = 0.525  #lembrar: a escala esta em relacao do 1 e 0
        #Direct neighbours of the center pixel of the window

        lumaUp,lumaDown,lumaLeft,lumaRight,lumaCenter,lumaDownLeft,lumaUpRight,lumaUpLeft,lumaDownRight = neighbours(j,i,Y)
        #print "lumaUp,lumaDown,lumaLeft,lumaRight,lumaCenter,lumaDownLeft,lumaUpRight,lumaUpLeft,lumaDownRight"
        #print lumaUp,lumaDown,lumaLeft,lumaRight,lumaCenter,lumaDownLeft,lumaUpRight,lumaUpLeft,lumaDownRight
        # get the max and min values, then calculates the range between them
        LumaMin = min(lumaCenter,min(min(lumaDown,lumaUp),min(lumaLeft,lumaRight)))
        LumaMax = max(lumaCenter,max(max(lumaDown,lumaUp),max(lumaLeft,lumaRight)))
        LumaRange = LumaMax - LumaMin


        #cv2.imwrite("Y.png",Y)


        if(LumaRange < max(EDGE_THRESHOLD_MIN,LumaMax*EDGE_THRESHOLD_MAX)):
            return  0
        else:
            return 1
    else:
        return 0


#issue 2, verificar se esta direitinho os retornos! se ta na posicao certa e nao um a mais/menos

#nao esta utilizando a variavel passo com todos os ifs. Mas todos possuem 3 passos 
def detectShape(j,i,Y): #Issue 1: Nao deixar passar das bordas da imagem.
    lumaUp,lumaDown,lumaLeft,lumaRight,lumaCenter,lumaDownLeft,lumaUpRight,lumaUpLeft,lumaDownRight = neighbours(j,i,Y)
    THRESHOLD = 0.15
    #print lumaUp,lumaDown,lumaLeft,lumaRight,lumaCenter,lumaDownLeft,lumaUpRight,lumaUpLeft,lumaDownRight
    steps = 9
    Uflag1 = False
    Uflag2 = False
    Uflag_final = False
    i1= 0
    j1= 0
    i2=0
    j2 = 0
    if(abs(lumaCenter-lumaRight)>=THRESHOLD): #se a diferenca do pixel atual com o pixel da direita, eh uma borda a ser aliased
    	    	#print "netri"
        if(abs(lumaCenter-lumaUpRight)<=THRESHOLD):#4
            #print "4"
            for ii in range(i+1,i+steps+2): #iteracao horizontal
                if((abs(Y[j][ii]-Y[j-1][ii])<=THRESHOLD)and(abs(Y[j][ii]-Y[j][ii-1])>=THRESHOLD)): #condicao de parada para o 4a, |-|
                    i2 = ii - 1#ja atualiza o i2 e i1
                    i1 = i +1
                    for jj in range(j+1,j+steps+1): #iteracao vertical na parte direita do |-|
                        if(abs(Y[jj][i2]-Y[jj][i2+1])<=THRESHOLD):#condicao de parada vertical
                            j2 = jj-1
                            Uflag2 =True
                            break
                    if(Uflag2==False):
                        j2 = j + steps -1
                    for jj in range(j+1,j+steps+1): #iteracao vertical na parte esquerda do |-|
                        if(abs(Y[jj][i1]-Y[jj][i1-1])<=THRESHOLD):#condicao de parada vertical
                            j1 = jj-1
                            Uflag1 =True
                            return "4a",j1,i1,j2,i2
                    if(Uflag1==False):
                        j1 = j + steps -1
                        return "4a",j1,i1,j2,i2
                if((abs(Y[j][ii]-Y[j-1][ii])<=THRESHOLD)and(abs(Y[j][ii]-Y[j][ii-1])<=THRESHOLD)):
                    i2 = ii - 1 # se parou mas nao eh um |-|, ja guarda o valor de i2 para futura utilizacao!nao precisa correr horizontalmente na proxima
                    j2 = j
                    Uflag2=True
                    break
            if(Uflag2==False):
                j2 =j
                i2 = i +steps
            for jj in range(j,j+steps):#+1):
                if((abs(Y[jj][i]-Y[jj][i+1])>=THRESHOLD)and(abs(Y[jj][i+1] - Y[jj+1][i+1])>=THRESHOLD)):#4b, Outro U, so que virado pra direita.
                    j1 = jj
                    for ii in range(i+1,i+steps): #iteracao horizontal de baixo do u de lado
                        if(abs(Y[j1][ii]-Y[j1+1][ii])<=THRESHOLD): #condicao de parada horizontal.
                            i1 = ii-1
                            Uflag1=True
                            return "4b",j1,i1,j2,i2
                    if(Uflag1==False):
                        i1 = i +steps
                        return "4b",j1,i1,j2,i2
                if((abs(Y[jj][i]-Y[jj][i+1])>=THRESHOLD)and(abs(Y[jj][i]-Y[jj+1][i])>=THRESHOLD)): #4c,Z
                    i1 = i
                    j1 = jj
                    return "4c",j1,i1,j2,i2
            i1=i+1
            j1=j + steps - 1
            return "4",j1,i1,j2,i2
        elif((abs(lumaCenter-lumaUp)<=THRESHOLD)and(abs(lumaCenter-lumaDown)>=THRESHOLD)):#2
            #print "2"
            i2= i
            for ii in range(i,i-steps,-1):
                if((abs(Y[j][ii]-Y[j][ii-1])<=THRESHOLD)and(abs(Y[j][ii]-Y[j+1][ii-1])<=THRESHOLD)and(abs(Y[j][ii]-Y[j+1][ii])>=THRESHOLD)): #condicao de parada para o Z
                    j1= j+1
                    i1 =ii
                    for jj in range(j-1,j-steps+1,-1):
                        if(abs(Y[jj][i]-Y[jj][i+1])<=THRESHOLD): #condicao de parada para analise vertical. paraquando for igual (uma iteracao "a mais")
                            j2= jj+1
                            return "2a",j1,i1,j2,i2
                    j2 = j - steps +1 
                    return "2a",j1,i1,j2,i2
           
            #caso nao for um Z, ele sai fora do for e vem pra ca. procura horizontalmente e verticalmente o valor do _|
            j1 = j
            i1 = i - steps+1 #pode ser sobrescrito no for abaixo.
            for ii in range(i,i-steps,-1):
                if(abs(Y[j][ii]-Y[j+1][ii])<=THRESHOLD):
                    i1 = ii+1
                    break
            for jj in range(j-1,j-steps+1,-1):
                if(abs(Y[jj][i]-Y[jj][i+1])<=THRESHOLD): #condicao de parada para analise vertical. paraquando for igual (uma iteracao "a mais")
                    j2= jj+1
                    return "2",j1,i1,j2,i2
            j2 = j - steps +1
            return "2",j1,i1,j2,i2
        elif((abs(lumaCenter-lumaDown)<=THRESHOLD)and(abs(lumaCenter-lumaDownRight)<=THRESHOLD)):#1
            #print "1"
            i1= i+1 #ja atualiza o i1 para o valor correto.
            #iteracao horizontal. Pode resultar em 3 opcoes: 1(normal), 1a (U) ou 1b (Z)
            for ii in range(i+1,i+steps+2): #iteracao horizontal
                if((abs(Y[j][ii]-Y[j+1][ii])<=THRESHOLD)and(abs(Y[j+1][ii-1]-Y[j+1][ii])<=THRESHOLD)): #condicao de parada horizontal para o U. Para um a mais. U detectado!
                    i2 = ii - 1 #i2 ja esta na posicao correta.
                    for jj in range(j-1,j-steps,-1): # analise vertical da direita do u
                        if(abs(Y[jj][i2]-Y[jj][i2+1])<=THRESHOLD): #analisa se chegou no final do U
                            j2 = jj+1 #ja atualiza o j2 para o valor correto
                            Uflag2 = True
                            break
                    if(Uflag2==False):
                        j2 = j-steps+1
                    for jj in range(j-1,j-steps-1,-1): #analise vertical da esquerda do U
                        if(abs(Y[jj][i1]-Y[jj][i1-1])<=THRESHOLD): #analisa se chegou no final do U
                            j1=jj+1
                            Uflag1 = True
                            break
                    if(Uflag1==False):
                        j1 =j -steps+1
                    return "1a",j1,i1,j2,i2

                elif((abs(Y[j][ii]-Y[j+1][ii])<=THRESHOLD)and(abs(Y[j+1][ii-1]-Y[j+1][ii])>=THRESHOLD)):#condicao de parada horizontal! detectou um Z!
                    i2 = ii - 1 #i2 ja esta na posicao correta.
                    j2 = j+1
                    for jj in range(j-1,j-steps-1,-1): #analise vertical da esquerda do Z
                        if(abs(Y[jj][i1]-Y[jj][i1-1])<=THRESHOLD): #analisa se chegou no final do Z
                            j1=jj+1
                            Uflag1 = True
                            break
                    if(Uflag1==False):
                        j1 =j -steps+1
                    return "1b",j1,i+1,j2,i2
            i2 = i+steps
            i1 = i+1
            j2 = j
            for jj in range(j-1,j-steps-1,-1): #analise vertical da esquerda L
                if(abs(Y[jj][i1]-Y[jj][i1-1])<=THRESHOLD): #analisa se chegou no final do L
                    j1=jj+1
                    Uflag1 = True
                    break
            if(Uflag1==False):
                j1 =j -steps+1
            return "1",j1,i1,j2,i2
        elif(abs(lumaCenter-lumaUp)>=THRESHOLD):#3
            #print "3"
            j1 = j
            for jj in range(j+1,j+steps+1): # analisa verticalmente, descendo a imagem. Procura U ou Z
                if((abs(Y[jj][i]-Y[jj][i+1])<=THRESHOLD)and(abs(Y[jj][i]-Y[jj-1][i])>=THRESHOLD)):#condicao de parada para o U
                    j2 = jj -1
                    for ii in range(i-1,i-steps,-1): # analise horizontal na parte de baixo do u                    
                        if(abs(Y[jj][ii]-Y[jj+1][ii])<=THRESHOLD): #analisa vertical se chegou no final do U
                            i2 = ii + 1
                            Uflag2 = True
                            break
                    if(Uflag2==False):
                        i2= i - steps+1
                    for ii in range(i-1,i-steps,-1): # analise horizontal na parte de cima do u                    
                        if(abs(Y[j][ii]-Y[j-1][ii])<=THRESHOLD):
                            i1 = ii+1
                            Uflag1 = True
                            break
                    if(Uflag1==False):
                        i1 = i-steps+1
                    return "3a",j1,i1,j2,i2
                if((abs(Y[jj][i] - Y[jj][i+1])<=THRESHOLD)and(abs(Y[jj][i] - Y[jj-1][i])<=THRESHOLD)): #detectou um formato Z!!
                    j1 = j
                    j2 = jj-1 #atualiza o j2!
                    i2 = i+1
                    #agora procura a  parte horizontal!
                    for ii in range(i-1,i-steps,-1): # analise horizontal na parte de cima do z                    
                        if(abs(Y[j][ii]-Y[j-1][ii])<=THRESHOLD):
                            i1 = ii+1
                            Uflag1 = True
                            break
                    if(Uflag1==False):
                        i1 = i-steps+1
                    return "3b",j1,i1,j2,i2
            #caso nao seja nem U nem Z
            j2 = j +steps -1
            i2 = i
            for ii in range(i-1,i-steps,-1): # analise horizontal na parte de cima do L                   
                if(abs(Y[j][ii]-Y[j-1][ii])<=THRESHOLD):
                    i1 = ii+1
                    Uflag1 = True
                    break
            if(Uflag1==False):
                i1 = i-steps+1
            return "3",j1,i1,j2,i2
        else:
        	return "0",0,0,0,0
    else:
    	return "0",0,0,0,0 


def create_weights():
    smoothing_matrix = []
    L_matrix = []
    L_matrix.append([0.5,0,0,0,0,0,0,0,0]) #validado
    L_matrix.append([0.75,0.25,0,0,0,0,0,0,0]) #validado
    L_matrix.append([0.82,0.50,0.18,0,0,0,0,0,0]) #validado
    L_matrix.append([0.85,0.70,0.37,0.12,0,0,0,0,0]) #validado
    L_matrix.append([0.90,0.8,0.51,0.4,0.25,0,0,0,0]) #validado
    L_matrix.append([0.94,0.82,0.56,0.46,0.35,0.2,0,0,0])
    L_matrix.append([0.94,0.80,0.50,0.46,0.4,0.30,0.15,0,0])
    L_matrix.append([0.95,0.85,0.7,0.60,0.5,0.35,0.20,0.12,0])
    L_matrix.append([0.96,0.80,0.75,0.60,0.51,0.41,0.35,0.24,0.15])
    
    U_matrix = []
    U_matrix.append([0.75,0,0,0,0,0,0,0,0])
    U_matrix.append([0.50,0.50,0,0,0,0,0,0,0])
    U_matrix.append([0.70,0.50,0.7,0,0,0,0,0,0])#3
    U_matrix.append([0.75,0.25,0.25,0.75,0,0,0,0,0]) 
    U_matrix.append([0.8,0.6,0.4,0.6,0.8,0,0,0,0])#5

    U_matrix.append([0.82,0.50,0.18,0.18,0.50,0.82,0,0,0])


    U_matrix.append([0.85,0.65,0.35,0.15,0.35,0.65,0.85,0,0])
    U_matrix.append([0.9,0.75,0.52,0.30,0.30,0.52,0.75,0.9,0])
    U_matrix.append([0.92,0.77,0.55,0.43,0.3,0,15,0,3,0.43,0.55,0.77,0.92])



    Z_matrix = []
    #Z_matrix.append([0.3,0.40,0,0,0,0]) #1 0 #validado
    Z_matrix.append([0.5,0.80,0,0,0,0,0,0,0,0]) #1 0 #validado
    Z_matrix.append([0.35,0.35,0,0,0,0,0,0,0,0]) #21 #validado
    Z_matrix.append([0.4,0.85,0.9,0.4,0,0,0,0,0,0]) #32 #validado
    Z_matrix.append([0.25,0.75,0.75,0.25,0,0,0,0,0,0]) #43 #validado

    Z_matrix.append([0.20,0.53,0.74,0.74,0.53,0.20,0,0,0,0]) #54 #validado

    Z_matrix.append([0.18,0.50,0.82,0.82,0.50,0.18,0,0,0,0]) #65 #validado

    Z_matrix.append([0.15,0.41,0.65,0.84,0.84,0.65,0.41,0.15,0,0]) #76 #validado

    Z_matrix.append([0.10,0.29,0.55,0.88,0.88,0.55,0.29,0.10,0,0]) #65 #validado
    Z_matrix.append([0.18,0.50,0.82,0.82,0.50,0.18,0,0,0,0]) #65 #validado




    smoothing_matrix.append(L_matrix)
    smoothing_matrix.append(U_matrix)
    smoothing_matrix.append(Z_matrix)
    return smoothing_matrix


def smooth_edge(smoothing_matrix,j,i,tipo,j1,i1,j2,i2,orig_matrix, result_matrix):
    img_buffer = copy.deepcopy(orig_matrix)
    if(tipo=='1'):
        V = j-j1+1
        H= i2 - i
        c1 = 0
        c2 = 0
 
        for jj in range(j,j1-1,-1):
            if((result_matrix[jj][i1][0])==(img_buffer[jj][i1][0])and((result_matrix[jj][i1][1])==(img_buffer[jj][i1][1]))and((result_matrix[jj][i1][2])==(img_buffer[jj][i1][2]))):
                buff = smoothing_matrix[0][V-1][c1]*orig_matrix[jj][i] + (1- smoothing_matrix[0][V-1][c1])*orig_matrix[jj][i1]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[jj][i1] = buff
                #else:
                    #print j,i," tipo:",tipo
            c1+=1

        for ii in range(i1,i2+1):
            if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                buff = smoothing_matrix[0][H-1][c2]*orig_matrix[j+1][ii] + (1- smoothing_matrix[0][H-1][c2])*orig_matrix[j][ii]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
            c2+=1
    elif(tipo=="1a"):
        V1 = j-j1+1
        V2 = j -j2+1
        H= i2 - i
        c1 = 0
        c2 = 0
        c3 = 0

        for jj in range(j,j1-1,-1):
            if((result_matrix[jj][i1][0])==(img_buffer[jj][i1][0])and((result_matrix[jj][i1][1])==(img_buffer[jj][i1][1]))and((result_matrix[jj][i1][2])==(img_buffer[jj][i1][2]))):
                buff = smoothing_matrix[0][V1-1][c1]*orig_matrix[jj][i] + (1- smoothing_matrix[0][V1-1][c1])*orig_matrix[jj][i1]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[jj][i1]= buff
                #else:
                    #print j,i," tipo:",tipo
            c1+=1

        for jj in range(j,j2-1,-1):          
            if((result_matrix[jj][i2][0])==(img_buffer[jj][i2][0])and((result_matrix[jj][i2][1])==(img_buffer[jj][i2][1]))and((result_matrix[jj][i2][2])==(img_buffer[jj][i2][2]))):
                buff = smoothing_matrix[0][V2-1][c2]*orig_matrix[jj][i2+1] + (1- smoothing_matrix[0][V2-1][c2])*orig_matrix[jj][i2]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[jj][i2]=buff
                #else:
                    #print j,i," tipo:",tipo
            c2+=1
        for ii in range(i1,i2+1):
            if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                buff = smoothing_matrix[1][H-1][c3]*orig_matrix[j+1][ii] + (1- smoothing_matrix[1][H-1][c3])*orig_matrix[j][ii]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
            c3+=1
    elif(tipo=="1b"):
        V = j-j1+1
        H=i2 - i
        _H = float(H)/2
        c1 = 0
        c2 = 0
        if H%2 != 0:
            _H = int(_H)
            for ii in range(i1,i1+_H+1):
                if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                    buff = smoothing_matrix[2][H-1][c1]*orig_matrix[j][ii] + (1- smoothing_matrix[2][H-1][c1])*orig_matrix[j+1][ii]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[j][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
                c1+= 1
            for ii in range(i1+_H,i2+1):
                if((result_matrix[j+1][ii][0])==(img_buffer[j+1][ii][0])and((result_matrix[j+1][ii][1])==(img_buffer[j+1][ii][1]))and((result_matrix[j+1][ii][2])==(img_buffer[j+1][ii][2]))):
                    buff = smoothing_matrix[2][H-1][c1]*orig_matrix[j+1][ii] + (1- smoothing_matrix[2][H-1][c1])*orig_matrix[j][ii]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[j+1][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
                c1+= 1
        else:
            _H = int(_H)
            for ii in range(i1,i1+_H):
                if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                    buff = smoothing_matrix[2][H-1][c1]*orig_matrix[j][ii] + (1- smoothing_matrix[2][H-1][c1])*orig_matrix[j+1][ii]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[j][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
                c1+= 1
            for ii in range(i1+_H,i2+1):
    
                if((result_matrix[j+1][ii][0])==(img_buffer[j+1][ii][0])and((result_matrix[j+1][ii][1])==(img_buffer[j+1][ii][1]))and((result_matrix[j+1][ii][2])==(img_buffer[j+1][ii][2]))):
                    buff = smoothing_matrix[2][H-1][c1]*orig_matrix[j+1][ii] + (1- smoothing_matrix[2][H-1][c1])*orig_matrix[j][ii]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[j+1][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
                c1+= 1


        for jj in range(j,j1-1,-1):
            if((result_matrix[jj][i1][0])==(img_buffer[jj][i1][0])and((result_matrix[jj][i1][1])==(img_buffer[jj][i1][1]))and((result_matrix[jj][i1][2])==(img_buffer[jj][i1][2]))):
                buff = smoothing_matrix[0][V-1][c2]*orig_matrix[jj][i] + (1- smoothing_matrix[0][V-1][c2])*orig_matrix[jj][i1]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[jj][i1] = buff
                #else:
                    #print j,i," tipo:",tipo
            c2+=1
    elif(tipo=="2"):
        V = j - j2 +1
        H = i-i1 +1
        c1 = 0
        c2 = 0
        for jj in range(j,j2-1,-1):
            if((result_matrix[jj][i][0])==(img_buffer[jj][i][0])and((result_matrix[jj][i][1])==(img_buffer[jj][i][1]))and((result_matrix[jj][i][2])==(img_buffer[jj][i][2]))):
                buff = smoothing_matrix[0][V-1][c1]*orig_matrix[jj][i+1] + (1- smoothing_matrix[0][V-1][c1]*orig_matrix[jj][i])
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[jj][i]=buff
                #else:
                    #print j,i," tipo:",tipo
            c1+=1
        for ii in range(i,i1-1,-1):
            if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                buff = smoothing_matrix[0][H-1][c2]*orig_matrix[j+1][ii] + (1- smoothing_matrix[0][H-1][c2]*orig_matrix[j][ii])
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j][ii]=buff
                #else:
                    #print j,i," tipo:",tipo
            c2+=1
    elif(tipo=="2a"):
        H=i-i1+1
        _H = float(H)/2
        c1 = 0
        c2 = 0
        if H%2 != 0: #impar
            _H = int(_H)
            for ii in range(i1,i1+_H+1):
                if((result_matrix[j+1][ii][0])==(img_buffer[j+1][ii][0])and((result_matrix[j+1][ii][1])==(img_buffer[j+1][ii][1]))and((result_matrix[j+1][ii][2])==(img_buffer[j+1][ii][2]))):
                    buff = smoothing_matrix[2][H-1][c1]*orig_matrix[j+1][ii] + (1- smoothing_matrix[2][H-1][c1])*orig_matrix[j][ii]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[j+1][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
                c1+= 1    

            for ii in range(i1+_H,i+1):
                if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                    buff = smoothing_matrix[2][H-1][c1]*orig_matrix[j][ii] + (1- smoothing_matrix[2][H-1][c1])*orig_matrix[j+1][ii]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[j][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
                c1+= 1        
        else: #par
            _H = int(_H)
            for ii in range(i1,i1+_H):
                if((result_matrix[j+1][ii][0])==(img_buffer[j+1][ii][0])and((result_matrix[j+1][ii][1])==(img_buffer[j+1][ii][1]))and((result_matrix[j+1][ii][2])==(img_buffer[j+1][ii][2]))):
                    buff = smoothing_matrix[2][H-1][c1]*orig_matrix[j+1][ii] + (1- smoothing_matrix[2][H-1][c1])*orig_matrix[j][ii]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[j+1][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
                c1+= 1    

            for ii in range(i1+_H,i+1):
                if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                    buff = smoothing_matrix[2][H-1][c1]*orig_matrix[j][ii] + (1- smoothing_matrix[2][H-1][c1])*orig_matrix[j+1][ii]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[j][ii] =buff
                #else:
                    #print j,i," tipo:",tipo
                c1+= 1     
    elif(tipo =="3"):
        V = j2 - j +1
        H = i-i1 +1
        c1 =0
        c2 =0
        for jj in range(j,j2+1):
            if((result_matrix[jj][i][0])==(img_buffer[jj][i][0])and((result_matrix[jj][i][1])==(img_buffer[jj][i][1]))and((result_matrix[jj][i][2])==(img_buffer[jj][i][2]))):
                buff = smoothing_matrix[0][V-1][c1]*orig_matrix[jj][i+1] + (1- smoothing_matrix[0][V-1][c1])*orig_matrix[jj][i]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[jj][i] = buff
                #else:
                    #print j,i," tipo:",tipo
            c1+=1
        for ii in range(i,i1-1,-1):
            if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                buff = smoothing_matrix[0][H-1][c2]*orig_matrix[j-1][ii] + (1- smoothing_matrix[0][H-1][c2]*orig_matrix[j][ii])
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j][ii]= buff
                #else:
                    #print j,i," tipo:",tipo
            c2+=1
    elif(tipo=="3a"):
        V = j2-j+1
        H1 = i-i1 +1
        H2 = i-i2 +1
        c1 =0
        c2 =0
        c3 = 0
        for ii in range(i,i1-1,-1):
            if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                buff = smoothing_matrix[0][H1-1][c1]*orig_matrix[j-1][ii] + (1- smoothing_matrix[0][H1-1][c1]*orig_matrix[j][ii])

                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j][ii]  =buff
                #else:
                    #print j,i," tipo:",tipo
            c1+=1

        for ii in range(i,i2-1,-1):
            if((result_matrix[j2][ii][0])==(img_buffer[j2][ii][0])and((result_matrix[j2][ii][1])==(img_buffer[j2][ii][1]))and((result_matrix[j2][ii][2])==(img_buffer[j2][ii][2]))):
                buff = smoothing_matrix[0][H2-1][c2]*orig_matrix[j2+1][ii] + (1- smoothing_matrix[0][H2-1][c2]*orig_matrix[j2][ii])
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j2][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
            c2+=1


        for jj in range(j,j2+1):
            if((result_matrix[jj][i][0])==(img_buffer[jj][i][0])and((result_matrix[jj][i][1])==(img_buffer[jj][i][1]))and((result_matrix[jj][i][2])==(img_buffer[jj][i][2]))):
                buff = smoothing_matrix[1][V-1][c3]*orig_matrix[jj][i+1] + (1- smoothing_matrix[1][V-1][c3])*orig_matrix[jj][i]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[jj][i] = buff
                #else:
                    #print j,i," tipo:",tipo
            c3+=1
    elif(tipo =="3b"):
        H = i-i1 +1
        V = j2 -j+1
        c1= 0
        c2 = 0
        _V = float(V)/2
        if(V%2 != 0): #impar
           _V = int(_V)
           for jj in range(j,j+_V+1):
                if((result_matrix[jj][i][0])==(img_buffer[jj][i][0])and((result_matrix[jj][i][1])==(img_buffer[jj][i][1]))and((result_matrix[jj][i][2])==(img_buffer[jj][i][2]))):
                    buff = smoothing_matrix[2][V-1][c1]*orig_matrix[jj][i] + (1- smoothing_matrix[2][V-1][c1])*orig_matrix[jj][i+1]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[jj][i] = buff
                    #else:
                        #print j,i," tipo:",tipo
                c1+= 1

           for jj in range(j+_V, j2+1):
               if((result_matrix[jj][i+1][0])==(img_buffer[jj][i+1][0])and((result_matrix[jj][i+1][1])==(img_buffer[jj][i+1][1]))and((result_matrix[jj][i+1][2])==(img_buffer[jj][i+1][2]))):
                    buff = smoothing_matrix[2][V-1][c1]*orig_matrix[jj][i+1] + (1- smoothing_matrix[2][V-1][c1])*orig_matrix[jj][i]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[jj][i+1] =buff
                    #else:
                        #print j,i," tipo:",tipo
               c1+= 1    

        else: #par
           _V = int(_V)
           for jj in range(j,j+_V):
                if((result_matrix[jj][i][0])==(img_buffer[jj][i][0])and((result_matrix[jj][i][1])==(img_buffer[jj][i][1]))and((result_matrix[jj][i][2])==(img_buffer[jj][i][2]))):
                    buff = smoothing_matrix[2][V-1][c1]*orig_matrix[jj][i] + (1- smoothing_matrix[2][V-1][c1])*orig_matrix[jj][i+1]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[jj][i] = buff
                    #else:
                        #print j,i," tipo:",tipo
                c1+= 1

           for jj in range(j+_V, j2+1):
               if((result_matrix[jj][i+1][0])==(img_buffer[jj][i+1][0])and((result_matrix[jj][i+1][1])==(img_buffer[jj][i+1][1]))and((result_matrix[jj][i+1][2])==(img_buffer[jj][i+1][2]))):
                   buff = smoothing_matrix[2][V-1][c1]*orig_matrix[jj][i+1] + (1- smoothing_matrix[2][V-1][c1])*orig_matrix[jj][i]
                   if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                       result_matrix[jj][i+1] = buff
                   #else:
                       #print j,i," tipo:",tipo
               c1+= 1    
        
        for ii in range(i,i1-1,-1):
            if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                buff = smoothing_matrix[0][H-1][c2]*orig_matrix[j-1][ii] + (1- smoothing_matrix[0][H-1][c2]*orig_matrix[j][ii])
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
            c2+=1
    elif(tipo =="4"):
    	V = j1 - j +1
    	H = i2 - i
    	c1 = 0
    	c2 = 0
        for jj in range(j,j1+1):
            if((result_matrix[jj][i+1][0])==(img_buffer[jj][i+1][0])and((result_matrix[jj][i+1][1])==(img_buffer[jj][i+1][1]))and((result_matrix[jj][i+1][2])==(img_buffer[jj][i+1][2]))):
                buff = smoothing_matrix[0][V-1][c1]*orig_matrix[jj][i] + (1- smoothing_matrix[0][V-1][c1])*orig_matrix[jj][i-1]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[jj][i+1] = buff
                #else:
                    #print j,i," tipo:",tipo
            c1+=1
        for ii in range(i+1,i2+1):
            if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                buff = smoothing_matrix[0][H-1][c2]*orig_matrix[j-1][ii] + (1- smoothing_matrix[0][H-1][c2])*orig_matrix[j][ii]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
            c2+=1
    elif(tipo=="4a"):
    	V1 = j1 -j +1
    	V2 = j2 - j +1
    	H  = i2 - i1 +1 
    	c1 = 0
    	c2 = 0
    	c3 = 0
        for jj in range(j,j1+1):
            if((result_matrix[jj][i+1][0])==(img_buffer[jj][i+1][0])and((result_matrix[jj][i+1][1])==(img_buffer[jj][i+1][1]))and((result_matrix[jj][i+1][2])==(img_buffer[jj][i+1][2]))):
                buff= smoothing_matrix[0][V1-1][c1]*orig_matrix[jj][i] + (1- smoothing_matrix[0][V1-1][c1])*orig_matrix[jj][i-1]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[jj][i+1] = buff
                #else:
                    #print j,i," tipo:",tipo
            c1+=1

        for jj in range(j,j2+1):
            if((result_matrix[jj][i2][0])==(img_buffer[jj][i2][0])and((result_matrix[jj][i2][1])==(img_buffer[jj][i2][1]))and((result_matrix[jj][i2][2])==(img_buffer[jj][i2][2]))):
                buff = smoothing_matrix[0][V2-1][c2]*orig_matrix[jj][i2+1] + (1- smoothing_matrix[0][V2-1][c2])*orig_matrix[jj][i2]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[jj][i2] = buff
                #else:
                    #print j,i," tipo:",tipo
            c2+=1

        for ii in range(i1,i2+1):
            if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                buff = smoothing_matrix[1][H-1][c3]*orig_matrix[j-1][ii] + (1- smoothing_matrix[1][H-1][c3])*orig_matrix[j][ii]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j][ii] = buff
                #else:
                   #print j,i," tipo:",tipo
            c3+=1
    elif(tipo =="4b"):
        V =  j1 -j +1
        H1 = i1 - i
        H2 = i2 - i
    	c1 =0
    	c2 =0
    	c3 = 0


        for ii in range(i+1,i1+1):
            if((result_matrix[j1][ii][0])==(img_buffer[j1][ii][0])and((result_matrix[j1][ii][1])==(img_buffer[j1][ii][1]))and((result_matrix[j1][ii][2])==(img_buffer[j1][ii][2]))):
                buff = smoothing_matrix[0][H1-1][c1]*orig_matrix[j1+1][ii] + (1- smoothing_matrix[0][H1-1][c1])*orig_matrix[j1][ii]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j1][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
            c1+=1


        for ii in range(i+1,i2+1):
            if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                buff = smoothing_matrix[0][H2-1][c2]*orig_matrix[j-1][ii] + (1- smoothing_matrix[0][H2-1][c2])*orig_matrix[j][ii]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j][ii] = buff
                #else:
                    #print j,i," tipo:",tipo
            c2+=1

        for jj in range(j,j1+1):
            if((result_matrix[jj][i+1][0])==(img_buffer[jj][i+1][0])and((result_matrix[jj][i+1][1])==(img_buffer[jj][i+1][1]))and((result_matrix[jj][i+1][2])==(img_buffer[jj][i+1][2]))):
                buff = smoothing_matrix[1][V-1][c3]*orig_matrix[jj][i] + (1- smoothing_matrix[1][V-1][c3])*orig_matrix[jj][i-1]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[jj][i+1] =buff
                #else:
                    #print j,i," tipo:",tipo
            c3+=1
    elif(tipo == "4c"):
        V= j1-j+1
        H = i2 - i
        c1 =0
        c2 = 0
        _V = float(V)/2
        if(V%2 != 0): #impar
            _V = int(_V)
            for jj in range(j,j+_V+1):
                    if((result_matrix[jj][i+1][0])==(img_buffer[jj][i+1][0])and((result_matrix[jj][i+1][1])==(img_buffer[jj][i+1][1]))and((result_matrix[jj][i+1][2])==(img_buffer[jj][i+1][2]))):
                        buff = smoothing_matrix[2][V-1][c1]*orig_matrix[jj][i+1] + (1- smoothing_matrix[2][V-1][c1])*orig_matrix[jj][i]
                        if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                            result_matrix[jj][i+1] = buff
                        #else:
                            #print j,i," tipo:",tipo
                    c1+= 1
    
            for jj in range(j+_V, j1+1):
                   if((result_matrix[jj][i][0])==(img_buffer[jj][i][0])and((result_matrix[jj][i][1])==(img_buffer[jj][i][1]))and((result_matrix[jj][i][2])==(img_buffer[jj][i][2]))):
                    buff = smoothing_matrix[2][V-1][c1]*orig_matrix[jj][i] + (1- smoothing_matrix[2][V-1][c1])*orig_matrix[jj][i+1]
                    if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                        result_matrix[jj][i] = buff
                    #else:
                        #print j,i," tipo:",tipo
                   c1+= 1
        else: #par
            _V = int(_V)
            for jj in range(j,j+_V):
                    if((result_matrix[jj][i+1][0])==(img_buffer[jj][i+1][0])and((result_matrix[jj][i+1][1])==(img_buffer[jj][i+1][1]))and((result_matrix[jj][i+1][2])==(img_buffer[jj][i+1][2]))):
                        buff = smoothing_matrix[2][V-1][c1]*orig_matrix[jj][i+1] + (1- smoothing_matrix[2][V-1][c1])*orig_matrix[jj][i]
                        if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                            result_matrix[jj][i+1] - buff
                        #else:
                           #print j,i," tipo:",tipo
                    c1+= 1
    
            for jj in range(j+_V, j1+1):
                   if((result_matrix[jj][i][0])==(img_buffer[jj][i][0])and((result_matrix[jj][i][1])==(img_buffer[jj][i][1]))and((result_matrix[jj][i][2])==(img_buffer[jj][i][2]))):
                       buff = smoothing_matrix[2][V-1][c1]*orig_matrix[jj][i] + (1- smoothing_matrix[2][V-1][c1])*orig_matrix[jj][i+1]
                       if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                           result_matrix[jj][i] = buff
                       #else:
                            #print j,i," tipo:",tipo
                   c1+= 1
        for ii in range(i+1,i2+1):
            if((result_matrix[j][ii][0])==(img_buffer[j][ii][0])and((result_matrix[j][ii][1])==(img_buffer[j][ii][1]))and((result_matrix[j][ii][2])==(img_buffer[j][ii][2]))):
                buff = smoothing_matrix[0][H-1][c2]*orig_matrix[j-1][ii] + (1- smoothing_matrix[0][H-1][c2])*orig_matrix[j][ii]
                if((buff[0]>0)and(buff[1]>0)and(buff[2]>0)):
                    result_matrix[j][ii] =buff
                #else:
                    #print j,i," tipo:",tipo
            c2+=1
    
    return result_matrix

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------X----------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------normal---------------------------------------------------------------------------
 




#################################################
####################main#########################
#################################################

smoothing_matrix = create_weights()
#frame = cv2.imread("mlaa-teste.png")
#frame = cv2.imread("mlaa-teste (1).png")
#frame = cv2.imread("1.png")
##frame = cv2.imread("morphological.png")
#frame = cv2.imread("morphological - Copia.png")
frame = cv2.imread("1.png")
#frame = cv2.imread("tipo2.png")
#frame = cv2.imread("tipo3.png")
#frame = cv2.imread("tipo4.png")

canny  = cv2.Canny(frame,0,100)
cv2.imwrite("canny.png",canny)
output = frame
YCrCb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2YCR_CB)
Y,Cr,Cb = cv2.split(YCrCb_frame)
cv2.imwrite("Y.png",Y)

Y = Y/255.0 #normalize Y channel

Edges = np.zeros((Y.shape[0],Y.shape[1],1), np.uint8)
pixel = []


#img = cv2.imread("output.png")
#buff = img[270][409]
#print buff
#if((buff[0]>100)and(buff[1]>100)and(buff[2]>100)):
#    print "banana!"

counter =0 
for j in range(1,frame.shape[0]-10):
    for i in range(1, frame.shape[1]-10):
        if(canny[j][i]!=0):
            #Edges[j][i]=255
            #print "que coisa"
            tipo,j1,i1,j2,i2 = detectShape(j,i,Y)
            #print tipo,j1,i1,j2,i2
            if(tipo != "0"):
                #frame_buff = cv2.imread("frame767.png")
                output = smooth_edge(smoothing_matrix,j,i,tipo,j1,i1,j2,i2,frame,output)
                #cv2.imwrite("output"+str(counter)+".png",output)
                counter+=1
#cv2.imwrite("edges.png", Edges)

cv2.imwrite("output.png",output)

'''
print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#isEdge(4,5,Y)
#detectShape(4,5,Y)
#j= 7
#i = 7
#print "posicao inicial:(",j,",",i,")"
#
#tipo,j1,i1,j2,i2 = detectShape(j,i,Y)
#print tipo,j1,i1,j2,i2
#output = smooth_edge(smoothing_matrix,j,i,tipo,j1,i1,j2,i2,frame,output)
#
#cv2.imwrite("output.png",output)


j=  11#12
i =  13 # 23
tipo,j1,i1,j2,i2 = detectShape(j,i,Y)
print tipo,j1,i1,j2,i2
frame = cv2.imread("zzzzz.png")
output = smooth_edge(smoothing_matrix,j,i,tipo,j1,i1,j2,i2,frame,output)
cv2.imwrite("output.png",output)
'''
 