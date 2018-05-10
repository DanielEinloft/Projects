%Super-Sampling Anti-Aliasing algorithm, using OGSS sampling pattern.
%Author: Daniel Centeno Einloft and Jean Larrocca.
%Class: ADSP
%Last modification in: 22/06/2017

function [mean_R, mean_G, mean_B] = blur2(img,y,x,pstep)

R= 0.0;
G= 0.0;
B= 0.0;

[yy, xx, ch] = size(img);

if((x+pstep<xx) && (y+pstep<yy))
        R= (double(img(y,x,1))/255 +double(img(y+1,x,1))/255 +double(img(y,x+1,1))/255+double(img(y+1,x+1,1))/255)+ double(img(y+2,x,1))/255 + double(img(y+2,x+1,1))/255 + double(img(y+2,x+2,1))/255 + double(img(y,x+2,1))/255 + double(img(y+1,x+2,1))/255;
        G= (double(img(y,x,2))/255 +double(img(y+1,x,2))/255 +double(img(y,x+1,2))/255+double(img(y+1,x+1,2))/255)+  double(img(y+2,x,2))/255 + double(img(y+2,x+1,2))/255 + double(img(y+2,x+2,2))/255  +double(img(y,x+2,2))/255 + double(img(y+1,x+2,2))/255;
        B= (double(img(y,x,3))/255 +double(img(y+1,x,3))/255 +double(img(y,x+1,3))/255+double(img(y+1,x+1,3))/255)+  double(img(y+2,x,3))/255 + double(img(y+2,x+1,3))/255 + double(img(y+2,x+2,3))/255 + double(img(y,x+2,3))/255 + double(img(y+1,x+2,3))/255;
    
    
        mean_R = uint8(R*255/9);
        mean_G = uint8(G*255/9);
        mean_B = uint8(B*255/9);
%       R= (double(img(y,x,1))/255 +double(img(y+1,x,1))/255 +double(img(y,x+1,1))/255+double(img(y+1,x+1,1))/255);
%       G= (double(img(y,x,2))/255 +double(img(y+1,x,2))/255 +double(img(y,x+1,2))/255+double(img(y+1,x+1,2))/255);
%       B= (double(img(y,x,3))/255 +double(img(y+1,x,3))/255 +double(img(y,x+1,3))/255+double(img(y+1,x+1,3))/255);  
%       mean_R = uint8(R*255/4);
%       mean_G = uint8(G*255/4);
%       mean_B = uint8(B*255/4);
else
    mean_R = img(y,x,1);
    mean_G = img(y,x,2);
    mean_B = img(y,x,3);
end;