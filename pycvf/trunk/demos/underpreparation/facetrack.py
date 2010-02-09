# -*- coding: utf-8 -*-
# we assume that we are receiving a video

from pycvf.core.generic_application import *

class FaceTrack(DatabaseUsingApplication):
   ## 
   ##  A detector from an image provide a set of elements with a probability
   ## 
   detector=None
   ##
   ## A tracker keep tracks of what was there or not and tries to find a continuity in the representation
   ##
   tracker=None
   @classmethod
   def process (cls):
     print "processing..."
     from pycvf.lib.video.lazydisplay import LazyDisplay
     ld=LazyDisplay()
     def observe(x):
        #print x
        ld.push((x,0))
        cls.tracker.push(cls.detector.detect(x))
     for x in cls.vdb:
        x[0].set_observer(observe)
        x[0].run()


if __name__=="__main__":
  from pycvf.lib.facedetect.haardetect import *
  from pycvf.lib.trackers.generictracker import *
  FaceTrack.detector=FaceDetector()
  FaceTrack.tracker=GenericTracker()
  FaceTrack.run(sys.argv[1:])
