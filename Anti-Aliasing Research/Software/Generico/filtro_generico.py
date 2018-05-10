'''
Generic Anti-Aliasing algorithm, using canny edge detector and gaussian filter.
Author: Daniel Centeno Einloft
Class: ADSP
Last modification in: 10/06/2017
'''
import cv2
import numpy as np
import copy





frame = cv2.imread("1.png")
canny  = cv2.Canny(frame,0,200)
cv2.imwrite("generico_canny.png",canny)
step = 3

#median = frame
#gauss =  cv2.GaussianBlur(frame,(15,15),0)
#cv2.medianBlur(frame,15,median)




for j in range(0,frame.shape[0]-1):
    for i in range(0, frame.shape[1]-1):
        if(canny[j][i]!=0):
            if((i-step>= 0)and(i+step< frame.shape[1]-1)and(j-step>= 0)and(j+step< frame.shape[0]-1)):
                mat = frame[j-step:j+step,i-step:i+step]
                cv2.medianBlur(mat,7,mat)
                frame[j-step:j+step,i-step:i+step] = mat

print "done!"
cv2.imwrite("generico.png",frame)