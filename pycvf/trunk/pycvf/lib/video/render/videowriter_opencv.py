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


from pycvf.lib.graphics.zopencv import *
import ctypes

def CV_FOURCC(c1,c2,c3,c4):
   return ctypes.c_int(((ord(c1) & 255) + ((ord(c2) & 255)<<8) + ((ord(c3) & 255)<<16) + ((ord(c4) & 255)<<24))).value


#CV_FOURCC('P','I','M','1')    = MPEG-1 codec
#CV_FOURCC('M','J','P','G')    = motion-jpeg codec (does not work well)
#CV_FOURCC('M', 'P', '4', '2') = MPEG-4.2 codec
#CV_FOURCC('D', 'I', 'V', '3') = MPEG-4.3 codec
#CV_FOURCC('D', 'I', 'V', 'X') = MPEG-4 codec
#CV_FOURCC('U', '2', '6', '3') = H263 codec
#CV_FOURCC('I', '2', '6', '3') = H263I codec
#CV_FOURCC('F', 'L', 'V', '1') = FLV1 codec


class CvVideoWriter:
   def __init__(self,fname,fps = 25,frameW = 320,frameH  = 200, codec="MJPG", isColor=1):
       self.writer=cvCreateVideoWriter(fname,
                                       CV_FOURCC(codec[0],codec[1],codec[2],codec[3]),
                                       fps,
                                       cvSize(frameW,frameH),
                                       isColor)
   def push(self,img):
        cvWriteFrame(self.writer,img.copy('C')) 
   def __del__(self):
       pass
        #cvReleaseVideoWriter(self.writer)

# import pycvf.lib.video.cvvideowriter as cvw; cvw.CvVideoWriter("/tmp/out1.avi")
if __name__ == "__main__":
  import numpy,scipy
  from pycvf.lib.graphics.rescale import Rescaler2d
  rsc=Rescaler2d((320,200))
  c=CvVideoWriter("/tmp/test.mpg")
  ib=scipy.lena().reshape((512,512,1)).repeat(3,axis=2)
  for i in range(100):
    print "Frame ",i
    ib[:,:,0]=i*3
    c.push(rsc.process(ib).astype(numpy.uint8))
  
  