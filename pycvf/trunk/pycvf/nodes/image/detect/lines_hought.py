# -*- coding: utf-8 -*-
import math
import numpy
from pycvf.core import genericmodel
from pycvf.datatypes import image
import zopencv

def houghtlines(image):
   block_size = 0
   timage=image.mean(axis=2).astype(numpy.uint8)
   storage = zopencv.cvCreateMemStorage ( block_size )
   pt1=zopencv.CvPoint()
   pt2=zopencv.CvPoint()
   lines = zopencv.cvHoughLines2(timage, storage.get_pointer(), zopencv.CV_HOUGH_STANDARD, 1, zopencv.CV_PI/180, 100, 0, 0 )
   #cvFlip(image)
   BIG=image.shape[0]+image.shape[1]
   resimage=image.copy('C')
   for i in range(min(lines.total,100)):
       line = zopencv.zopencv_pclasses.PointerOnCvPoint2D32f(zopencv.cvGetSeqElem(lines,i));
       rho = line.x;
       theta = line.y;
       a = math.cos(theta)
       b = math.sin(theta)
       x0 = a*rho
       y0 = b*rho
       pt1.x = zopencv.cvRound(x0 + BIG*(-b))
       pt1.y = zopencv.cvRound(y0 + BIG*(a))
       pt2.x = zopencv.cvRound(x0 - BIG*(-b))
       pt2.y = zopencv.cvRound(y0 - BIG*(a))
       color=zopencv.cvScalar(255,0,0,0)
       zopencv.cvLine(resimage, pt1, pt2, color, 1, 1,0 )#zopencv.CV_RGB(255,0,0
   zopencv.cvReleaseMemStorage(storage.get_pointer_on_pointer())
   return resimage
    
Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(houghtlines)
__call__=Model