'''
Super-Sampling Anti-Aliasing algorithm, using OGSS sampling pattern.
Author: Daniel Centeno Einloft
Class: ADSP
Last modification in: 07/06/2017
'''

import cv2
import numpy as np
 
'''
Function that applies a median blur on the image. Returns a blurred pixel.
'''
def median_blur(image,current_height,current_width,frame_res):
	meanB = 0
	meanG = 0
	meanR = 0
	counter = 0
	pixel = []

	for j in range(current_height -frame_res,current_height + frame_res + 1):
		for i in range(current_width -frame_res,current_width +frame_res + 1):
			if((i>= 0)and(i< image.shape[1])and(j>= 0)and(j< image.shape[0])):
				pixel = image[j][i]
				meanB = meanB + pixel[0] 
				meanG = meanG + pixel[1]
				meanR = meanR + pixel[2]
				counter += 1
	if(meanB==0):
		meanB = 1
	if(meanR==0):
		meanR = 1
	if(meanG==0):
		meanG = 1
	#print "(",current_height,",",current_width,") ",meanB,meanG,meanR, counter

	meanB = meanB/counter
	meanG = meanG/counter
	meanR = meanR/counter
	#print "penis"
	return meanB,meanG,meanR

'''
Create the output matrix, that will contain the resulting filtered image.
'''
def create_output_img(frame_res,orig_img): 
	output = np.zeros((orig_img.shape[0]/2,orig_img.shape[1]/2,3), np.uint8)
	return output



############################################################main############################################################
############################################################################################################################

files = "/home/thamior/Desktop/ADSP_projeto_final/Suporte/DarkSouls3/1-frame_SSAA"
output_files = "/home/thamior/Desktop/ADSP_projeto_final/Suporte/1-frame_1_SSAA"
ccc =1638
#for ccc in 

frame = cv2.imread(files + str(ccc)+".png")



frame_res =  2

pixel  = []
ii=0
jj=0

output = create_output_img(frame_res,frame)
for j in range(0,frame.shape[0]-frame_res,frame_res):
	for i in range(0, frame.shape[1]-frame_res,frame_res):
		#print j,i,jj,ii
		pixel = median_blur(frame,j,i,frame_res)
		output[jj][ii] = pixel
		#print ii
		ii += 1
	ii=0
	jj += 1

#cv2.imwrite("output.png",output)
print ccc, "done!" 
cv2.imwrite(output_files + str(ccc)+ ".png",output)
