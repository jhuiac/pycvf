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

def surf(x,as_couple=False):
  xnb=x
  if (xnb.ndim==3):
    xnb=xnb.mean(axis=2)
  if (xnb.dtype!=numpy.uint8):
    xnb=xnb.astype(numpy.uint8)
  #from opencv.cv import cvExtractSURF,CvSeq,cvCreateMemStorage, cvSURFParams
  #keypoints,descriptors=cvExtractSURF(xnb,0,cvSURFParams( 500, 1 ) ,0)
  import zopencv
  from zopencv import cvExtractSURF,cvSURFParams
  params=cvSURFParams(500,1)
  print dir(params)
  #cvSURFParams( 500, 1 )
  #CvArr * img,CvArr * mask,CvSeq * * keypoints,CvSeq * * descriptors,CvMemStorage * storage,CvSURFParams params,int useProvidedKeyPts)
  keypoints=zopencv.zopencv_pclasses.PointerOnCvSeq(0)
  descriptors=zopencv.zopencv_pclasses.PointerOnCvSeq(0)
  storage = zopencv.cvCreateMemStorage ( 0 )
  cvExtractSURF(xnb,0,keypoints.get_pointer_on_pointer(), descriptors.get_pointer_on_pointer() , storage, params ,0)
  print "SURF OUTPUT=",keypoints.total, descriptors.total
  keypoints=map(lambda x:zopencv.zopencv_pclasses.PointerOnCvPoint(keypoints.getSeqElem(x)) ,range(keypoints.total))
  descriptors=map(lambda x:zopencv.zopencv_pclasses.PointerOnCvPoint(descriptors.getSeqElem(x)) ,range(descriptors.total))
  zopencv.cvReleaseMemStorage(storage.get_pointer_on_pointer())
  if as_couple:
     return (numpy.array(keypoints),numpy.array(descriptors))
  else:
     return numpy.hstack([numpy.array(keypoints),numpy.array(descriptors)])

#from opencv.highgui import cvLoadImage, CV_LOAD_IMAGE_GRAYSCALE 
#object = cvLoadImage( "/home/tranx/logo_jfli_big.jpg", CV_LOAD_IMAGE_GRAYSCALE )
#object=scipy.lena().astype(numpy.uint8)
#rs=surf(object)
