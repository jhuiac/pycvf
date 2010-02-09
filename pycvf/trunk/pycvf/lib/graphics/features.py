#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


import scipy
import scipy.stats
import numpy

def lbp(img):
    res=[]
    timg=img
    for i in [ (0,1), (1,1), (0,-1),(0,-1),(1,-1),(1,-1),(0,1), (0,1)  ]:
      timg=numpy.roll(timg,i[1],axis=i[0])
      res+=[timg>=img]
    return numpy.dstack(res)

def lbph(img):
  r=numpy.matrix([128,64,32,16,8,4,2,1])*numpy.asmatrix(numpy.array(lbp(img)).reshape(scipy.prod(img.shape),8)).astype(int).T
  f=scipy.stats.histogram(r,numbins=256,defaultlimits=(0,256))[0]
  return f/f.sum()
  
#def hog(img):
    
    
    
#function [bm bv] = anna_BinMatrix(A,E,G,angle,bin)
## anna_BINMATRIX Computes a Matrix (bm) with the same size of the image where
## (i,j) position contains the histogram value for the pixel at position (i,j)
## and another matrix (bv) where the position (i,j) contains the gradient
## value for the pixel at position (i,j)
##                
##IN:
##    A - Matrix containing the angle values
##    E - Edge Image
##   G - Matrix containing the gradient values
##    angle - 180 or 360%   
##   bin - Number of bins on the histogram 
##    angle - 180 or 360
##OUT:
##    bm - matrix with the histogram values
##   bv - matrix with the graident values (only for the pixels belonging to
##   and edge)
#
#[contorns,n] = bwlabel(E);  
#X = size(E,2);
#Y = size(E,1);
#bm = zeros(Y,X);
#bv = zeros(Y,X);
#
#nAngle = angle/bin;
#
#for i=1:n
#    [posY,posX] = find(contorns==i);    
#    for j=1:size(posY,1)
#        pos_x = posX(j,1);
#        pos_y = posY(j,1);
#        
#        b = ceil(A(pos_y,pos_x)/nAngle);
#        if b==0, bin= 1; end
#        if G(pos_y,pos_x)>0
#            bm(pos_y,pos_x) = b;
#            bv(pos_y,pos_x) = G(pos_y,pos_x);                
#        end
#    end
#end

    
def phogDescriptor(bh,bv,L,bin):
  """
  %               
  %IN:
  %    bh - matrix of bin histogram values 
  %    bv - matrix of gradient values 
  %   L - number of pyramid levels
  %   bin - number of bins
  %
  %OUT:
  %    p - pyramid histogram of oriented gradients (phog descriptor)
  """

  p = []
  # level0
  for b in range(bin):
     ind = bh==b;
     p.append(bv(ind).sum())
  cella = 1
  for l in range(L):
    x = bh.shape[1]//(1<<l)
    y = bh.shape[0]//(1<<l)
    xx=0
    yy=0
    while xx+x<=bh.shape[1]:
        while yy +y <=bh.shape[0]: 
            bh_cella = []
            bv_cella = []
            bh_cella = bh[yy:yy+y,xx:xx+x]
            bv_cella = bv[yy:yy+y,xx:xx+x]
            
            for b in range(bin):
                ind = bh_cella==b;
                p.append(bv_cella(ind).sum())
            end 
            yy = yy+y
        
        cella = cella+1
        yy = 0
        xx = xx+x
   
  if p.sum()!=0:
    p = p/sum(p)
  return p

    
def phog(img,bin,angle,L):
  if img.sum()>100:
     E = edge(G,'canny');
     GradientX,GradientY = gradient(img)
     GradientYY = gradient(GradientY)
     Gr = sqrt((GradientX*GradientX)+(GradientY*GradientY));          
     index = GradientX == 0;
     GradientX[index] = 1e-5;
            
     YX = GradientY/GradientX;
     if angle == 180:
          A = ((atan(YX)+(pi/2))*180)/pi
     if angle == 360:
          A = ((atan2(GradientY,GradientX)+pi)*180)/pi
                                
     bh,bv = anna_binMatrix(A,E,Gr,angle,bin);
  else:
     bh = zeros(size(I,1),size(I,2));
     bv = zeros(size(I,1),size(I,2)); 
  p = phogDescriptor(bh,bv,L,bin);
  return p
