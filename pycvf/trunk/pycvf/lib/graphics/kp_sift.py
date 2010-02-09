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


# -*- coding: utf-8 -*-
import sys,numpy
import sift as siftm
#import pycudaSift
sifto=siftm.sift

def sift(x,as_couple=False):
  xnb=x
  if (xnb.ndim==3):
    xnb=xnb.mean(axis=2)
  if (xnb.dtype!=numpy.int):
    xnb=xnb.astype(numpy.int)
  ra=numpy.array(sifto(xnb))
  #print "ra=",ra.shape
  if (ra.shape[0]==0):
    sys.stderr.write("Warning SIFT does not return any keypoint, please check img (img size="+str(x.shape)+")")
    #return (numpy.matrix((0,0)),numpy.matrix((0,0)))
    return (None,None)
  if as_couple:
    return ra[:,:6],ra[:,6:]
  else:
    return ra

