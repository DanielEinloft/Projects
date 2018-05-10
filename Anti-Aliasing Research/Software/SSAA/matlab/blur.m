%Super-Sampling Anti-Aliasing algorithm, using HRAA sampling pattern.
%Author: Daniel Centeno Einloft and Jean Larrocca.
%Class: ADSP
%Last modification in: 20/06/2017

function [mean_R, mean_G, mean_B] = blur(img,y,x,pstep)

counter = 0;
R= 0.0;
G= 0.0;
B= 0.0;

[yy, xx, ch] = size(img);
% disp(R);
% disp(G);
% disp(B);
% disp(y+pstep);
% disp(x+pstep);
% disp(y- pstep);
% disp(x-pstep);

    for m = (y- pstep):(y+pstep)
		for n = (x-pstep):(x+pstep)
			if((n>=1) && (n<xx) && (m>=1) && (m<yy))
                %disp(img(m,n,1));
                %disp(img(m,n,2));
                %disp(img(m,n,3));
                
                R= double(img(m,n,1))/255+R;
                G= double(img(m,n,2))/255+G;
                B= double(img(m,n,3))/255+B;
                counter = counter +1;
			end;
		end
    end
    mean_R = uint8(R*255/counter);
    mean_G = uint8(G*255/counter);
    mean_B = uint8(B*255/counter);

end