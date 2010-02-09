# -*- coding: utf-8 -*-
from pycvf.core.errors import *
import zopencv as zcv
import sys
#from pycvf.lib.graphics.imgfmtutils import *

class OpenCVBackgroundForegroundSeparation:
    def __init__(self,model="fgd",n_gauss=5,bg_threshold=0.7,std_threshold=3.5):
      self.model=model
      if self.model=="gauss":
        self.params = zcv.CvGaussBGStatModelParams();
        self.params.win_size=2;
        self.params.n_gauss=n_gauss;
        self.params.bg_threshold=bg_threshold;
        self.params.std_threshold=std_threshold;
        self.params.minArea=15;
        self.params.weight_init=0.05;
        self.params.variance_init=30;
      else:
        self.params=zcv.CvFGDStatModelParams()
      self.bgmodel=None

    def process(self,videoFrame):
       #videoFrame=videoFrame.mean(axis=2)
       sys.stderr.write("process\n")
       if (not self.bgmodel):
           if self.model=="gauss":
             self.bgmodel = zcv.CvBGStatModel(zcv.cvCreateGaussianBGModel(videoFrame ,self.params))
             sys.stderr.write("minit\n")
           else:
             self.bgmodel = zcv.CvFGDStatModel(zcv.cvCreateFGDStatModel(videoFrame,self.params))
             sys.stderr.write("minit\n")
       else:
          zcv.cvUpdateBGStatModel(videoFrame,self.bgmodel.get_pointer())
       #return videoFrame,videoFrame#
       #pf=zcv.UIplImage(self.bgmodel.prev_frame)
       #zcv.cvCopy(videoFrame,self.bgmodel.prev_frame,0)
       sys.stderr.write(str(("bg/fg", self.bgmodel.background,self.bgmodel.foreground))+"\n")
       bg=zcv.Ipl2NumPyFast(zcv.UIplImage(self.bgmodel.background))
       fg=zcv.Ipl2NumPyFast(zcv.UIplImage(self.bgmodel.foreground))
       return bg,fg 

    def __del__(self):
       zcv.cvReleaseBGStatModel( self.bgmodel );

if __name__=="__main__":
  import pyffmpeg,sys
  vr=pyffmpeg.FFMpegReader()
  vr.open(sys.argv[1])
  obfs=OpenCVBackgroundForegroundSeparation()
  def extract_background(x):
    print "result :", obfs.process(x)
  vr.get_tracks()[0].set_observer(extract_background)
  vr.run()








