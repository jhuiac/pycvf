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


# block with scanline order
def block_extractor(pyr,pos):
    rw1=rh1=1
    rw2=rh2=2
    (l,x,y)=pos
    lm=l+1
    if (lm<len(pyr)):
        rlm=safe_slice_mir(pyr[lm],(y/2)-rh1,(y/2)+rh1+1,(x/2)-rw1,(x/2)+rw1+1).flat
    else:
        rlm=zeros((2*rw1+1),(2*rh1+1)).flat
    rl=safe_slice_mir(pyr[l],y-rh2,y,x-rw2,x+rw2+1).flat
    rl2=safe_slice_mir(pyr[l],y,y+1,x-rw2,x).flat
    return list(rlm) + list(rl) + list(rl2)


def pyrblockextract(pyr, blockextract):
    r=[]
    L=len(pyr)
    for l in range(0,L-1):
        (h,w)=shape(pyr[l])
        for y in range(0,h):
            for x in range(0,w):
                r.append(blockextract(pyr,(l,x,y)))
    return r;


#def pyrblockinject(pyr, blockextract,injector):
#    L=len(pyr)
#    for l in range(0,L-1):
#        (h,w)=shape(pyr[l])
#        for y in range(0,h):
#            for x in range(0,w):
#                injector(blockextract(pyr,(l,x,y)),pyr[l])
#


def pyrblockcreatre(pyr, predictor, blockextract):
    L=len(pyr)
    LR=range(1,L)
    #LR.reverse()
    for l in LR:
        (h,w)=shape(pyr[l])
        for y in range(0,h):
            for x in range(0,w):
                pyr[l][y,x]=predictor(blockextract(pyr,(l,x,y)))
