#!-*- conding: utf8 -*-

'''
Fast Approximamte Anti-Aliasing algorithm.
Author: Daniel Centeno Einloft
Class: ADSP
Last modification in: 14/05/2017
'''

import cv2
import numpy as np
import math


def Validade_Window(j,i,YCrCb_frame):
	if((i-1>= 0)and(i+1< YCrCb_frame.shape[1])and(j-1>= 0)and(j+1< YCrCb_frame.shape[0])):
		return True
	else:
		return False

def neighbours(j,i,YCrCb_frame):
		lumaUp     = YCrCb_frame[j-1][i]
		lumaDown   = YCrCb_frame[j+1][i]
		lumaLeft   = YCrCb_frame[j][i-1]
		lumaRight  = YCrCb_frame[j][i+1]
		lumaCenter = YCrCb_frame[j][i]
		
		lumaDownLeft  = YCrCb_frame[j+1][i-1]
		lumaUpRight   = YCrCb_frame[j-1][i+1]
		lumaUpLeft    = YCrCb_frame[j-1][i-1]
		lumaDownRight =	YCrCb_frame[j+1][i+1] 
		
		return lumaUp,lumaDown,lumaLeft,lumaRight,lumaCenter,lumaDownLeft,lumaUpRight,lumaUpLeft,lumaDownRight

def isHorizontal(j,i,YCrCb_frame):
	if(Validade_Window(j,i,YCrCb_frame)):
		
		EDGE_THRESHOLD_MIN = 0.0312 #lembrar: a escala esta em relacao a 1 e 0 
		EDGE_THRESHOLD_MAX = 0.125  #lembrar: a escala esta em relacao do 1 e 0

		#Direct neighbours of the center pixel of the window
		lumaUp,lumaDown,lumaLeft,lumaRight,lumaCenter,lumaDownLeft,lumaUpRight,lumaUpLeft,lumaDownRight = neighbours(j,i,YCrCb_frame)
		
		#print lumaUp,lumaDown,lumaLeft,lumaRight,lumaCenter,lumaDownLeft,lumaUpRight,lumaUpLeft,lumaDownRight
		
		# get the max and min values, then calculates the range between them
		LumaMin = min(lumaCenter,min(min(lumaDown,lumaUp),min(lumaLeft,lumaRight)))
		LumaMax = max(lumaCenter,max(max(lumaDown,lumaUp),max(lumaLeft,lumaRight)))
		#print LumaMin, LumaMax
		LumaRange = LumaMax - LumaMin
		#print LumaRange
		if(LumaRange < max(EDGE_THRESHOLD_MIN,LumaMax*EDGE_THRESHOLD_MAX)): # fiz leve modificacao, nao retornei o colorcenter(aka fragcolor). #issue 0
			return  0,0
		
		lumaDownUp   = lumaDown + lumaUp
		lumaLeftRight = lumaLeft + lumaRight

		#print lumaDownUp
		#print lumaLeftRight

		lumaLeftCorners  = lumaDownLeft + lumaUpLeft
		lumaDownCorners  = lumaDownLeft + lumaDownRight
		lumaRightCorners = lumaDownRight + lumaUpRight
		lumaUpCorners    = lumaUpRight + lumaUpLeft

		#print lumaLeftCorners 
		#print lumaDownCorners 
		#print lumaRightCorners
		#print lumaUpCorners   


		edgeHorizontal =  abs(-2.0 * lumaLeft + lumaLeftCorners)  + abs(-2.0 * lumaCenter + lumaDownUp ) * 2.0    + abs(-2.0 * lumaRight + lumaRightCorners)
		edgeVertical =    abs(-2.0 * lumaUp + lumaUpCorners)      + abs(-2.0 * lumaCenter + lumaLeftRight) * 2.0  + abs(-2.0 * lumaDown + lumaDownCorners)	

		if(edgeHorizontal >= edgeVertical): #nao estou retornando frag_color #issue 0
			return 1, LumaRange
		else:
			return 2 ,LumaRange

		    
		#for j in range(j - 1,j + 2):
		#	for i in range(i -1,i + 2):
		#		print "[",j,"][",i,"] ",YCrCb_frame[j][i]
	else:
		return -1,0 #issue 4 tratar caso nao esteja dentro de uma janela de analise (cantos da imagem)

def edge_orientation(j,i,Y,direction):

	lumaUp,lumaDown,lumaLeft,lumaRight,lumaCenter,lumaDownLeft,lumaUpRight,lumaUpLeft,lumaDownRight = neighbours(j,i,Y)

	stepLength = 1
	currentPos = 0
	#seleciona o texel na direcao oposta da borda detectada.
	if(direction==1): #se eh horizontal...
		luma1 = lumaDown
		luma2 = lumaUp
		
		currentPos = i + stepLength*0.5 #nao sei se irei utilizar.... #issue 1
	elif(direction==2): #se eh vertical...
		luma1 = lumaLeft
		luma2 = lumaRight

		currentPos = j + stepLength*0.5 # nao sei se irei utilizar... #issue 1
	
	#print luma1
	#print luma2

	#gradientes da direcao
	gradient1 = luma1 - lumaCenter
	gradient2 = luma2 - lumaCenter
	
	#print gradient1
	#print gradient2	

	#mais brusco
	is1Steepest = False
	if(abs(gradient1) >= abs(gradient2)):
		is1Steepest = True 

	#print is1Steepest
	
	#normaliza de acordo com o FXAA algorito.
	gradientScaled = 0.25*(max(abs(gradient1),abs(gradient2)))
	
	#print gradientScaled 
	
	lumaLocalAverage = 0

	if(is1Steepest):
		stepLength = - stepLength
		lumaLocalAverage = 0.5*(luma1+lumaCenter)
	else:
		lumaLocalAverage = 0.5*(luma2 + lumaCenter)

	#print lumaLocalAverage,stepLength
	return lumaLocalAverage,gradientScaled,stepLength



def get_edge_average(j,i,Y,direction,_uv,stepLength):
	pixel_value = 0

	if(direction==1):
		#print "1-(Y[",j-stepLength,"][",_uv,"] + Y[",j,"][",_uv,"])"
		pixel_value = (Y[j-stepLength][_uv] + Y[j][_uv])/2
	elif(direction==2):
		#print "2-Y[",_uv,"][",i+stepLength,"] + Y[",_uv,"][",i,"]"
		pixel_value = (Y[_uv][i+stepLength] + Y[_uv][i])/2

		
#(Y[j-1][i][0]*0.5 + Y[j+1][i][0]*0.5)*0.5)
#(Y[j-1][i][1]*0.5 + Y[j+1][i][1]*0.5)*0.5)
#(Y[j-1][i][2]*0.5 + Y[j+1][i][2]*0.5)*0.5)
	return True,pixel_value


def edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength):
	offset = 1
	QUALITY =[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8]# ver este vetor.. pode dar segmentation fault depois de 12 iteracoes.... issue 
	uv1 = 0
	uv2 = 0
	if(direction==1):
		uv1 = i - offset
		uv2 = i + offset
	if(direction==2):
		uv1 = j - offset		
		uv2 = j + offset
	
	#print uv1
	#print uv2
	
	end_of_frame1,lumaEnd1 = get_edge_average(j,i,Y,direction,uv1,stepLength)  
	end_of_frame2,lumaEnd2 = get_edge_average(j,i,Y,direction,uv2,stepLength) 
	
	#print end_of_frame1,lumaEnd1
	#print end_of_frame2,lumaEnd2	
	#lidar com o end of frame!!!!!!!!!!!!!!!!!!!!!!11 #issue 2


	lumaEnd1 -= lumaLocalAverage
	lumaEnd2 -= lumaLocalAverage
	
	#print end_of_frame1,lumaEnd1
	#print end_of_frame2,lumaEnd2	
	reached1 = False
	reached2 = False
	
	if(abs(lumaEnd1) >= gradientScaled): reached1 = True
	if(abs(lumaEnd2) >= gradientScaled): reached2 = True
	#print reached1 
	#print reached2 

	reachedBoth = reached1*reached2

	if(reached1!=True): uv1 -= offset
	if(reached2!=True): uv2 += offset
	#print "print",uv1,uv2
	
	#print len(QUALITY)
	for ii in range(2,len(QUALITY)):
		#print "iteracao ",ii," Uv1: ", uv1," Uv2: ",uv2
		if(ii == len(QUALITY)-1):
			QUALITY.append(8)
		if((uv1< 0)or(uv1> 598 )or(uv1> 798 )or(uv2 < 0)or(uv2 > 598)or(uv2 > 798)):
		#if((uv1< 0)or(uv1> 446 )or(uv1> 396 )or(uv2 < 0)or(uv2 > 446)or(uv2 > 396)):	
			uv1 += offset*QUALITY[ii]
			uv2 -= offset*QUALITY[ii]
			#print "cu ",uv1,uv2,lumaEnd1,lumaEnd2
			return uv1,uv2,lumaEnd1,lumaEnd2

		if(reached1!=True):
			end_of_frame1,lumaEnd1 = get_edge_average(j,i,Y,direction,uv1,stepLength)  
			lumaEnd1 -= lumaLocalAverage
			#lidar com o end of frame!!!!!!!!!!!!!!!!!!!!!!11 #issue 2

		if(reached2!=True):
			end_of_frame2,lumaEnd2 = get_edge_average(j,i,Y,direction,uv2,stepLength) 
			lumaEnd2 -= lumaLocalAverage

		
		if(abs(lumaEnd1) >= gradientScaled): reached1 = True
		if(abs(lumaEnd2) >= gradientScaled): reached2 = True

		reachedBoth = reached1*reached2

		if(reached1!=True): uv1 -= offset*QUALITY[ii]
		if(reached2!=True): uv2 += offset*QUALITY[ii]
		
		#print Y.shape[1]-2


		if(reachedBoth==True):
			#print uv1,uv2,lumaEnd1,lumaEnd2
			return uv1,uv2,lumaEnd1,lumaEnd2
			#break	 


def Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2):
	distance1 = 0
	distance2 = 0
	if(direction==1): #fiz leve modificacao aqui... 
		distance1 = i - uv1 
		distance2 = uv2 - i 
	elif(direction==2):
		distance1 = j - uv1
		distance2 = uv2 - j


	#print uv1,uv2,i,j,distance1, direction		
	#print uv1,uv2,i,j,distance2, direction
	
	isDirection1 = False
	if(distance1 < distance2):
		isDirection1 = True #tinha um erro aqui! 
	
	#print isDirection1


	distanceFinal = min(distance1, distance2)
	edgeThickness = distance1 + distance2
	if((distanceFinal == 0)or(edgeThickness==0)):
		return -1
	pixelOffset =  (-distanceFinal/float(edgeThickness)) + 0.5
	
	#print pixelOffset
	
	#a principio esta parte do codigo esta cagando tudo :< 
	isLumaCenterSmaller = False
	if(Y[j][i] < lumaLocalAverage):
		isLumaCenterSmaller = True
	
	#print isLumaCenterSmaller
	correctVariation = False
	#print isLumaCenterSmaller
	#print lumaEnd1,lumaEnd2
	'''
	Super_logic_buffer = False
	if(direction==1):
		if(lumaEnd1 < 0.0):
			Super_logic_buffer =True
		else:
			Super_logic_buffer = False
	else:
		if(lumaEnd2 < 0.0):
			Super_logic_buffer = True
		else:
			Super_logic_buffer = False

	if(Super_logic_buffer != isLumaCenterSmaller):
		correctVariation = True
	else:
		correctVariation = False

	#print correctVariation
	
	finalOffset = 0.0

	if(correctVariation ==True): finalOffset = pixelOffset
	'''
	return pixelOffset



def clamp(n,minn,maxn):
	return max(min(maxn,n),minn)


def Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange):

	SUBPIXEL_QUALITY = 0.75
	lumaUp,lumaDown,lumaLeft,lumaRight,lumaCenter,lumaDownLeft,lumaUpRight,lumaUpLeft,lumaDownRight = neighbours(j,i,Y)

	lumaLeftCorners  = lumaDownLeft + lumaUpLeft
	lumaDownCorners  = lumaDownLeft + lumaDownRight
	lumaRightCorners = lumaDownRight + lumaUpRight
	lumaUpCorners    = lumaUpRight + lumaUpLeft

	lumaDownUp = lumaUp + lumaDown
	lumaLeftRight = lumaLeft + lumaRight

	lumaAverage = (1.0/12.0)*(2.0*(lumaDownUp+lumaLeftRight)+lumaLeftCorners+lumaRightCorners)
	
	subPixelOffset1 = clamp( abs(lumaAverage-lumaCenter)/LumaRange,0.0,1.0)
	#print subPixelOffset1
	subPixelOffset2 = (-2.0*subPixelOffset1+3.0)*subPixelOffset1*subPixelOffset1
	#print subPixelOffset2
	subPixelOffsetFinal = subPixelOffset2*subPixelOffset2*SUBPIXEL_QUALITY
	#print subPixelOffsetFinal

	finalOffset = max(finalOffset,subPixelOffsetFinal)
	#finalOffset = (finalOffset+ subPixelOffsetFinal)/2
	#print finalOffset
	return finalOffset
	
def get_pixel_value(j,i,Y,frame,finalOffset,stepLength):
	#print "get pxel"
	jj=j
	ii=i
	bufferOffset = 0
	pixel = []
	teste = []
	if(direction==1):
		if(finalOffset >0):
			bufferOffset = math.ceil(finalOffset)
			jj = int(bufferOffset*stepLength)
			#((frame[j-jj][i][0]*finalOffset + frame[j][i][0]*(1-finalOffset))/2 + (frame[j][i-1][0]*0.5 + frame[j][i+1][0]*0.5)/2 ) 
			pixel.append((frame[j-jj][i][0]*finalOffset + frame[j][i][0]*(1-finalOffset))*0.5 + (frame[j][i-1][0]*0.5 + frame[j][i+1][0]*0.5)*0.5 )
			pixel.append((frame[j-jj][i][1]*finalOffset + frame[j][i][1]*(1-finalOffset))*0.5 + (frame[j][i-1][1]*0.5 + frame[j][i+1][1]*0.5)*0.5 ) 
			pixel.append((frame[j-jj][i][2]*finalOffset + frame[j][i][2]*(1-finalOffset))*0.5 + (frame[j][i-1][2]*0.5 + frame[j][i+1][2]*0.5)*0.5 ) 

			#pixel.append(frame[j-jj][i][0]*finalOffset + frame[j][i][0]*(1-finalOffset))
			#pixel.append(frame[j-jj][i][1]*finalOffset + frame[j][i][1]*(1-finalOffset))
			#pixel.append(frame[j-jj][i][2]*finalOffset + frame[j][i][2]*(1-finalOffset))
	elif(direction==2):
		if(finalOffset >0):
			bufferOffset = math.ceil(finalOffset)
			ii = int(bufferOffset*stepLength) 
			pixel.append(((frame[j][i+ii][0]*(finalOffset) + frame[j][i][0]*(1-finalOffset))*0.5 + (frame[j-1][i][0]*0.5 + frame[j+1][i][0]*0.5)*0.5))
			pixel.append(((frame[j][i+ii][1]*(finalOffset) + frame[j][i][1]*(1-finalOffset))*0.5 + (frame[j-1][i][1]*0.5 + frame[j+1][i][1]*0.5)*0.5))
			pixel.append(((frame[j][i+ii][2]*(finalOffset) + frame[j][i][2]*(1-finalOffset))*0.5 + (frame[j-1][i][2]*0.5 + frame[j+1][i][2]*0.5)*0.5))


			#pixel.append(frame[j][i+ii][0]*(finalOffset) + frame[j][i][0]*(1-finalOffset))
			#pixel.append(frame[j][i+ii][1]*(finalOffset) + frame[j][i][1]*(1-finalOffset))
			#pixel.append(frame[j][i+ii][2]*(finalOffset) + frame[j][i][2]*(1-finalOffset))
	
#	if(len(pixel)!=0):
#		if(pixel[0]<50 or pixel[1] <50 or pixel[2]<50):
#			pixel[0] = pixel[0]- pixel[0]/3
#			pixel[1] = pixel[1]- pixel[1]/3
#			pixel[2] = pixel[2]- pixel[2]/3
	#print "len:",len(pixel)
	#teste.append(float(pixel[0])/255)
	#teste.append(float(pixel[1])/255)
	#teste.append(float(pixel[2])/255)

	
	#print "[",j,"][",i,"]:", teste
	return pixel


#################################################
####################main#########################
#################################################
frame = cv2.imread("frame767.png")
#frame = cv2.imread("22.png")
#output = np.zeros((frame.shape[0],frame.shape[1],3), np.uint8)
output = frame
YCrCb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2YCR_CB)
Y,Cr,Cb = cv2.split(YCrCb_frame)
Y = Y/255.0 #normalize Y channel



Horizontal = np.zeros((Y.shape[0],Y.shape[1],1), np.uint8)
Vertical = np.zeros((Y.shape[0],Y.shape[1],1), np.uint8)
pixel = []

for j in range(1,frame.shape[0]-1):
	for i in range(1, frame.shape[1]-1):
		#print j,",",i
		pixel = frame[j][i]
		direction,LumaRange = isHorizontal(j,i,Y)
		if(direction==1):
			Horizontal[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,frame,finalOffset,stepLength)
				#output[j][i] = pixel
				if(len(pixel)!=0):
					output[j][i] = pixel
		elif(direction==2):
			Vertical[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,frame,finalOffset,stepLength)
				if(len(pixel)!=0):
					output[j][i] = pixel
		#else:
		#	output[j][i] = frame[j][i]
cv2.imwrite("output1.png",output)			

for j in range(1,output.shape[0]-1):
	for i in range(1, output.shape[1]-1):
		#print j,",",i
		pixel = output[j][i]
		direction,LumaRange = isHorizontal(j,i,Y)
		if(direction==1):
			Horizontal[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				#output[j][i] = pixel
				if(len(pixel)!=0):
					output[j][i] = pixel
		elif(direction==2):
			Vertical[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				if(len(pixel)!=0):
					output[j][i] = pixel
cv2.imwrite("output2.png",output)			
'''
for j in range(1,output.shape[0]-1):
	for i in range(1, output.shape[1]-1):
		#print j,",",i
		pixel = output[j][i]
		direction,LumaRange = isHorizontal(j,i,Y)
		if(direction==1):
			Horizontal[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				#output[j][i] = pixel
				if(len(pixel)!=0):
					output[j][i] = pixel
		elif(direction==2):
			Vertical[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				if(len(pixel)!=0):
					output[j][i] = pixel
cv2.imwrite("output3.png",output)			

for j in range(1,output.shape[0]-1):
	for i in range(1, output.shape[1]-1):
		#print j,",",i
		pixel = output[j][i]
		direction,LumaRange = isHorizontal(j,i,Y)
		if(direction==1):
			Horizontal[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				#output[j][i] = pixel
				if(len(pixel)!=0):
					output[j][i] = pixel
		elif(direction==2):
			Vertical[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				if(len(pixel)!=0):
					output[j][i] = pixel
cv2.imwrite("output4.png",output)	


for j in range(1,output.shape[0]-1):
	for i in range(1, output.shape[1]-1):
		#print j,",",i
		pixel = output[j][i]
		direction,LumaRange = isHorizontal(j,i,Y)
		if(direction==1):
			Horizontal[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				#output[j][i] = pixel
				if(len(pixel)!=0):
					output[j][i] = pixel
		elif(direction==2):
			Vertical[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				if(len(pixel)!=0):
					output[j][i] = pixel
cv2.imwrite("output5.png",output)	

for j in range(1,output.shape[0]-1):
	for i in range(1, output.shape[1]-1):
		#print j,",",i
		pixel = output[j][i]
		direction,LumaRange = isHorizontal(j,i,Y)
		if(direction==1):
			Horizontal[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				#output[j][i] = pixel
				if(len(pixel)!=0):
					output[j][i] = pixel
		elif(direction==2):
			Vertical[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				if(len(pixel)!=0):
					output[j][i] = pixel
cv2.imwrite("output6.png",output)	

for j in range(1,output.shape[0]-1):
	for i in range(1, output.shape[1]-1):
		#print j,",",i
		pixel = output[j][i]
		direction,LumaRange = isHorizontal(j,i,Y)
		if(direction==1):
			Horizontal[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				#output[j][i] = pixel
				if(len(pixel)!=0):
					output[j][i] = pixel
		elif(direction==2):
			Vertical[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				if(len(pixel)!=0):
					output[j][i] = pixel
cv2.imwrite("output7.png",output)	

for j in range(1,output.shape[0]-1):
	for i in range(1, output.shape[1]-1):
		#print j,",",i
		pixel = output[j][i]
		direction,LumaRange = isHorizontal(j,i,Y)
		if(direction==1):
			Horizontal[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				#output[j][i] = pixel
				if(len(pixel)!=0):
					output[j][i] = pixel
		elif(direction==2):
			Vertical[j][i] = 255
			direction,LumaRange = isHorizontal(j,i,Y)
			lumaLocalAverage,gradientScaled,stepLength = edge_orientation(j,i,Y,direction)
			uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(j,i,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
			finalOffset = Estimating_offset(j,i,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
			if(finalOffset!=-1):
				finalOffset = Subpixel_AntiAliasing(j,i,Y,finalOffset,LumaRange)
				pixel = get_pixel_value(j,i,Y,output,finalOffset,stepLength)
				if(len(pixel)!=0):
					output[j][i] = pixel
cv2.imwrite("output8.png",output)	
'''

#for i in range(1, frame.shape[1]):
#	print output[j][i][0]

cv2.imwrite("horizontal.png",Horizontal)
cv2.imwrite("vertical.png", Vertical)

#jj= 6
#ii= 3
#direction,LumaRange = isHorizontal(jj,ii,Y)
#lumaLocalAverage,gradientScaled,stepLength = edge_orientation(jj,ii,Y,direction)
#uv1,uv2,lumaEnd1,lumaEnd2 =edge_lenght(jj,ii,Y,direction,lumaLocalAverage,gradientScaled,stepLength)
#finalOffset = Estimating_offset(jj,ii,Y,direction,uv1,uv2,lumaLocalAverage,lumaEnd1,lumaEnd2)
#finalOffset = Subpixel_AntiAliasing(jj,ii,Y,finalOffset,LumaRange)
#pixel = get_pixel_value(jj,ii,Y,frame,finalOffset,stepLength)
#
#print pixel