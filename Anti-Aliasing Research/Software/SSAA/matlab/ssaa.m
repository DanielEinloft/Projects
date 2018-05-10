%Super-Sampling Anti-Aliasing algorithm, using OGSS and HRAA sampling pattern.
%Author: Daniel Centeno Einloft and Jean Larrocca.
%Class: ADSP
%Last modification in: 23/06/2017


%[x, y, ch] = size(img);

%-------------------------------------Programa Principal ----------------------------------------------------------
clc;
clear;

pstep = 2; %1(off), 2(2x), 4(4x) oversampling

img = imread('2-frame_SSAA0.bmp');
[y, x, ch] = size(img);

R = 0;
G = 0;
B= 0;
mm=1;
nn=1;
output = [];

for m = 1:pstep:y
	for n = 1:pstep:x
        %[R,G,B] = blur(img,m,n,pstep);
        %[R,G,B] = blur(img,m,n,pstep);
        %[R,G,B] = blur2(img,m,n,1);
        [R,G,B] = blur2(img,m,n,2);
        output(mm,nn,1) = R;
        output(mm,nn,2) = G;
        output(mm,nn,3) = B;
        nn = nn+1;
    end
    nn=1;
    mm= mm+1;
end
output = uint8(output);
imshow(output);
%imwrite(output,'resultado_SSAA-1.5.png');
%imwrite(output,'resultado_SSAA-1.png');
%imwrite(output,'resultado_SSAA-2.png');
imwrite(output,'resultado_SSAA-2.5.png');

