from opencv import cv
from opencv import highgui
from pycvf.lib.graphics.imgfmtutils import *
from pycvf.lib.video.rgb2bgr import *

class CameraReader2:
    def __init__(self,device=0,observer=None,bgr=False):
        self.capture = highgui.cvCreateCameraCapture (device)
        if not self.capture:
            raise Exception, "Error opening capture device"
        self.obs=observer
        self.bgr=bgr
    def set_observer(self,obs):
        self.obs=obs
    def copy(self):
        return self
    def step(self):
            frame = highgui.cvQueryFrame (self.capture)
            img=Ipl2NumPyFast(frame)
            if (self.bgr):
                #zs=img.shape
                #img=numpy.array(zip(img[:,:,2].flat,img[:,:,1].flat,img[:,:,0].flat)) ## slow !!!
                rgb2bgr(img) # let use cython
                #img.shape=zs
            if (self.obs):
                self.obs(img)
            return True
    def __getitem__(self,x):
        frame = highgui.cvQueryFrame (self.capture)
        img=Ipl2NumPyFast(frame)
        if (self.bgr):
            rgb2bgr(img) 
        return img
                                                                                                    
    def run(self):
        while self.step():
            pass

#from jfli.video.lazydisplay import *
#l=LazyDisplay()
#from jfli.video.camerareader2 import *
#c=CameraReader2(observer=l.f,bgr=True)
#c.run()

