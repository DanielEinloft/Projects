'''
Super-Sampling Anti-Aliasing algorithm, using HRAA sampling pattern.
Author: Daniel Centeno Einloft
Class: ADSP
Last modification in: 07/05/2017
'''

import cv2
import numpy as np
 
def metodo_2(image,j,i,jj,ii):
	meanB = 0
	meanG = 0
	meanR = 0

	B = float(frame[j][i][0])/255
	G = float(frame[j][i][1])/255
	R = float(frame[j][i][2])/255
	

	B = float(image[j][i+1][0])/255 + B
	G = float(image[j][i+1][1])/255 + G
	R = float(image[j][i+1][2])/255 + R

	B =float(image[j+1][i][0])/255 + B
	G =float(image[j+1][i][1])/255 + G
	R =float(image[j+1][i][2])/255 + R

	B =float(image[j+1][i+1][0])/255 + B
	G =float(image[j+1][i+1][1])/255 + G
	R =float(image[j+1][i+1][2])/255 + R


	B = float(frame[j+2][i][0])/255
	G = float(frame[j+2][i][1])/255
	R = float(frame[j+2][i][2])/255
	

	B = float(image[j+2][i+1][0])/255 + B
	G = float(image[j+2][i+1][1])/255 + G
	R = float(image[j+2][i+1][2])/255 + R

	B =float(image[j+2][i+2][0])/255 + B
	G =float(image[j+2][i+2][1])/255 + G
	R =float(image[j+2][i+2][2])/255 + R

	B =float(image[j+1][i+2][0])/255 + B
	G =float(image[j+1][i+2][1])/255 + G
	R =float(image[j+1][i+2][2])/255 + R

	B =float(image[j][i+2][0])/255 + B
	G =float(image[j][i+2][1])/255 + G
	R =float(image[j][i+2][2])/255 + R


	meanB = (B/9)*255
	meanG = (G/9)*255
	meanR = (R/9)*255


	'''
	B = float(frame[j][i][0])/255
	G = float(frame[j][i][1])/255
	R = float(frame[j][i][2])/255
	

	B = float(image[j][i+1][0])/255 + B
	G = float(image[j][i+1][1])/255 + G
	R = float(image[j][i+1][2])/255 + R

	B =float(image[j+1][i][0])/255 + B
	G =float(image[j+1][i][1])/255 + G
	R =float(image[j+1][i][2])/255 + R

	B =float(image[j+1][i+1][0])/255 + B
	G =float(image[j+1][i+1][1])/255 + G
	R =float(image[j+1][i+1][2])/255 + R

	meanB = (B/4)*255
	meanG = (G/4)*255
	meanR = (R/4)*255
	'''
	return meanB,meanG,meanR

'''
Create the output matrix, that will contain the resulting filtered image.
'''
def create_output_img(frame_res,orig_img): 
	output = np.zeros((orig_img.shape[0]/frame_res,orig_img.shape[1]/frame_res,3), np.uint8)
	return output




############################################################main############################################################
############################################################################################################################

files = "/home/thamior/Desktop/ADSP_projeto_final/Suporte/DarkSouls3/1-frame_SSAA"
output_files = "/home/thamior/Desktop/ADSP_projeto_final/Suporte/1-frame_2_SSAA"
ccc = 1638
#for ccc in 

frame = cv2.imread(files + str(ccc)+".png")


#frame = cv2.imread("frame767.png")
pixel  = []
ii=0
jj=0



output = create_output_img(2,frame)

for j in range(0,frame.shape[0]-1,2):
	for i in range(0, frame.shape[1]-1,2):
		pixel  = metodo_2(frame,j,i,jj,ii)
		output[jj][ii] = pixel
		ii += 1
	ii=0
	jj += 1

#cv2.imwrite("output.png",output)
print ccc, "done!" 
cv2.imwrite(output_files + str(ccc)+ ".png",output)
