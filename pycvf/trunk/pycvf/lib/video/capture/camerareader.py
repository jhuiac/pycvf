# -*- coding: utf-8 -*-
from pyv4l2 import *
import numpy
from pycvf.lib.video.rgb2bgr import *

#['BGR3', 'RGB3', 'YU12']
class CameraReader:
    def __init__(self,device=None,resolution=None,pixelformat=None,observer=None,inputno=0):
        if not device:
            try:
              device=CameraDevice.List()[0]
            except:
              device=Device.List()[0]                
        self.device=device
        try:
            self.dev=CameraDevice(self.device)
        except:
            self.dev=Device(self.device)
        self.observer=observer
        d=self.dev
        d.SetInput( inputno)
        if (resolution):
            d.SetResolution(resolution[0],resolution[1])
        #d.SetStandard( d.standards['NTSC'] )
        #d.SetField( d.fields['Interlaced'] )
        if(pixelformat):
            self.dev.SetPixelFormat(pixelformat)
        print d.EnumFormats(1)# capture
        d.GetResolutions()
        d.GetPixelFormats()
        d.GetFormat()
        p = self.dev.format.pixelformat
        self.h=self.dev.format.height
        self.w=self.dev.format.width
        self.bgr=False
        self.yuv=0
        self.img=None
        try:
           self.dev.SetPixelFormat('RGB4')
        except:
           pass
        try:
           self.dev.SetPixelFormat('RGB3')
        except:
           pass
        if p == 'RGB4':
            p = 'RGBA'
            self.nc=4
        elif p == 'BGR3':
            p = 'BGR'
            self.nc=3
            self.bgr=True
        elif p == 'RGB3':
            p = 'RGB'
            self.nc=3
        elif p == 'YU12':
            p = 'YU12'
            self.yuv=12
            self.img=numpy.zeros((self.h,self.w,3),dtype=numpy.uint8)
        else:
            raise Exception,"unsupported pixel format :"+p
    def step(self):
        self.dev.Read()
        if (self.yuv):
            y=numpy.ndarray(shape=(self.h,self.w),
                        buffer=self.dev.buffer,dtype=numpy.uint8).copy()
            off=self.h*self.w
            len=(self.h//2)*(self.w//2)
            u=numpy.ndarray(shape=(self.h//2,self.w//2),
                        buffer=self.dev.buffer[off:off+len],dtype=numpy.uint8)
            v=numpy.ndarray(shape=(self.h//2,self.w//2),
                        buffer=self.dev.buffer[off+len:],dtype=numpy.uint8)
            for yy in range(self.h):
                for xx in range(self.w):
                    vv=y[yy,xx]
                    self.img[yy,xx,0]=vv
                    self.img[yy,xx,1]=vv
                    self.img[yy,xx,2]=vv
        else:
            self.img=numpy.ndarray(shape=(self.h,self.w,self.nc),
                        buffer=self.dev.buffer,dtype=numpy.uint8)
        if (self.bgr):
            rgb2bgr(self.img)
        if (self.observer):
            self.observer(self.img.copy())
        return True
    def run(self):
        while self.step():
            pass
