#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
try :
  from zopencv import *
  import zopencv_pclasses

  # Global Variables
  class FaceDetector:
      # Parameters for haar detection
      # From the API:
      # The default parameters (scale_factor=1.1, min_neighbors=3, flags=0) are tuned 
      # for accurate yet slow object detection. For a faster operation on real video 
      # images the settings are: 
      # scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING, 
      # min_size=<minimum possible face size
      min_size = cvSize(20,20)
      haar_scale = 1.2
      min_neighbors = 2
      haar_flags = 0
        
      def __init__(self,  cascade_name = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"):
          self.cascade = cvLoadHaarClassifierCascade( cascade_name, cvSize(1,1) );
          if (not self.cascade):
              raise Exception , "Error loading Cv Cascade"
          self.storage = cvCreateMemStorage(0)
    
    
      def detect( self,img ):
        assert( self.cascade )
        #t = cvGetTickCount();
        faces = cvHaarDetectObjects( img, self.cascade, self.storage,
                                         self.haar_scale, self.min_neighbors, self.haar_flags, self.min_size );
        #t = cvGetTickCount() - t;
        #return faces
        print faces
        return map( lambda rct: (rct.x,rct.y,rct.width, rct.height), map(lambda x:zopencv_pclasses.PointerOnCvRect(faces.getSeqElem(x)) ,range(faces.total)))


except ImportError:
  from opencv.cv import *
  from jfli.graphics.imgfmtutils import *


  class FaceDetector:
      min_size = cvSize(20,20)
      haar_scale = 1.2
      min_neighbors = 2
      haar_flags = 0
        
      def __init__(self,  cascade_name = "/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml"):
          self.cascade = cvLoadHaarClassifierCascade( cascade_name, cvSize(1,1) );
          if (not self.cascade):
              raise Exception , "Error loading Cv Cascade"
          self.storage = cvCreateMemStorage(0)
    
    
      def detect( self,img ):
        assert( self.cascade )
        #t = cvGetTickCount();
        faces = cvHaarDetectObjects( NumPy2Ipl( img), self.cascade, self.storage,
                                         self.haar_scale, self.min_neighbors, self.haar_flags, self.min_size );
        #t = cvGetTickCount() - t;
        #return faces
        return map (lambda rct: (rct.x,rct.y,rct.width, rct.height), map(lambda x:r.getSeqElem(x) ,range(faces.total)))
