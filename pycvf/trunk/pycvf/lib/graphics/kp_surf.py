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
from pycvf.lib.graphics.imgfmtutils import *

def surf(object,as_couple=False):
  xnb=x
  if (xnb.ndim==3):
    xnb=xnb.mean(axis=2)
  if (xnb.dtype!=numpy.int):
    xnb=xnb.astype(numpy.int)
  return numpy.array(sifto(xnb))
  from opencv.cv import cvExtractSURF,CvSeq,cvCreateMemStorage, cvSURFParams
  keypoints,descriptors=cvExtractSURF(xnb,0,cvSURFParams( 500, 1 ) ,0)
  if as_couple:
     return (numpy.array(keypoints),numpy.array(descriptors))
  else:
     return numpy.hstack([numpy.array(keypoints),numpy.array(descriptors)])

#from opencv.highgui import cvLoadImage, CV_LOAD_IMAGE_GRAYSCALE 
#object = cvLoadImage( "/home/tranx/logo_jfli_big.jpg", CV_LOAD_IMAGE_GRAYSCALE )
#object=scipy.lena().astype(numpy.uint8)
#rs=surf(object)
