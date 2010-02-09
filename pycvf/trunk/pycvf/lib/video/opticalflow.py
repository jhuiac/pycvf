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
import zopencv as zcv
import numpy
from pycvf.lib.graphics.colortransforms import *


class OpticalFlowHS:
    def __init__(self,size,use_previous=0,lambdav=20, maxiter=10, eps=0.0001):
        self.use_previous=use_previous
        self.lambdav=lambdav
        self.imgprev=None
        self.imgvelx=numpy.ndarray(shape=(size[0],size[1]),dtype=numpy.float32)
        self.imgvely=numpy.ndarray(shape=(size[0],size[1]),dtype=numpy.float32)
        self.maxiter=maxiter
        self.eps=eps
    def push(self,imgcurr):
        if (self.imgprev==None):
            self.imgprev=imgcurr.copy()
        assert(self.imgprev.shape==imgcurr.shape)
        criteria=zcv.cvTermCriteria( zcv.CV_TERMCRIT_EPS+zcv.CV_TERMCRIT_ITER,self.maxiter,self.eps)
        zcv.cvCalcOpticalFlowHS( self.imgprev, imgcurr, self.use_previous, self.imgvelx, self.imgvely, self.lambdav, criteria );
        self.imgprev=imgcurr.copy()
        return numpy.dstack([self.imgvelx,self.imgvely])


class OpticalFlowBM:
    def __init__(self,size,use_previous=0,blocksize=(8,8),shiftsize=(8,8),maxrange=(8,8),bfc=0):
        self.use_previous=use_previous
        self.blocksize=zcv.cvSize(blocksize[0],blocksize[1])
        self.shiftsize=zcv.cvSize(shiftsize[0],shiftsize[1])
        self.maxrange=zcv.cvSize(maxrange[0],maxrange[1])
        self.imgprev=None
        self.imgvelx=numpy.ndarray(shape=((size[0]-bfc*blocksize[1])//shiftsize[1],(size[1]-bfc*blocksize[0])//shiftsize[0]),dtype=numpy.float32)
        self.cvimgvelx=zcv.NumPy2CvMatFast(self.imgvelx)
        self.imgvely=numpy.ndarray(shape=((size[0]-bfc*blocksize[1])//shiftsize[1],(size[1]-bfc*blocksize[0])//shiftsize[0]),dtype=numpy.float32)
        self.cvimgvely=zcv.NumPy2CvMatFast(self.imgvely)
    def push(self,imgcurr):
        if (self.imgprev==None):
            self.imgprev=imgcurr.copy()
        assert(self.imgprev.shape==imgcurr.shape)
        zcv.cvCalcOpticalFlowBM( self.imgprev, imgcurr, self.blocksize, self.shiftsize,  self.maxrange,self.use_previous,self.cvimgvelx, self.cvimgvely );
        self.imgprev=imgcurr.copy()
        return numpy.dstack([self.imgvelx,self.imgvely])




class OpticalFlowLK:
    def __init__(self,size,use_previous=0,winsize=(7,7)):
        self.use_previous=use_previous
        self.winsize=zcv.cvSize(winsize[0],winsize[1])
        self.imgprev=None
        self.imgvelx=numpy.ndarray(shape=(size[0],size[1]),dtype=numpy.float32)
        self.cvimgvelx=zcv.NumPy2CvMatFast(self.imgvelx)
        self.imgvely=numpy.ndarray(shape=(size[0],size[1]),dtype=numpy.float32)
        self.cvimgvely=zcv.NumPy2CvMatFast(self.imgvely)
    def push(self,imgcurr):
        if (self.imgprev==None):
            self.imgprev=imgcurr.copy()
        assert(self.imgprev.shape==imgcurr.shape)
        zimp=zcv.NumPy2CvMatFast(self.imgprev)
        zimc=zcv.NumPy2CvMatFast(imgcurr)
        zcv.cvCalcOpticalFlowLK(zimp , zimc , self.winsize, self.cvimgvelx, self.cvimgvely );
        self.imgprev=imgcurr.copy()
        return numpy.dstack([self.imgvelx,self.imgvely])



class OpticalFlowPyrLk:
    def __init__(self,size,use_previous=1,lambdav=1):
        self.use_previous=use_previous
        self.lambdav=lambdav
        self.imgprev=None
        self.imgvel=numpy.ndarray(shape=(2,size[0],size[1]),dtype=numpy.float32)
    def push(self,imgcurr):
        if (not self.imgprev):
            self.imgprev=imgcurr
        assert(self.imgprev.shape==imgcurr.shape)
        prevpyr=NumPy2XIplFast(self.imgprev)
        currpyr=NumPy2XIplFast(imgcurr)
        prevfeatures=NumPy2XIplFast(self.imgprev)
        currfeatures=NumPy2XIplFast(imgcurr)
        count=0
        criteria=zcv.cvTermCriteria( zcv.CV_TERMCRIT_EPS+zcv.CV_TERMCRIT_ITER,10,1.0)
        velx=NumPy2XIplFast(self.imgvel[0])
        vely=NumPy2XIplFast(self.imgvel[1])
        zcv.cvCalcOpticalFlowPyrLK( self.imgprev, imgcurr, self.use_previous, velx, vely, self.lambdav, criteria );
        self.imgprev=imgcurr
        return self.imgvel


def polarflow(a):
    from scipy import angle
    b=a[:,:,0]+1j*a[:,:,1]
    return numpy.dstack([(angle(b)+(2*numpy.pi))%(2*numpy.pi),abs(b)])

def flow2rgb(a):
    # transform flow into polar coordinates : map phase to hue, and strengh to saturation (or intensity)
    #pf=polarflow(a)
    b=a[:,:,0]+1j*a[:,:,1]
    x=(numpy.angle(b)/6.28*255.).astype(numpy.uint8)
    y=(abs(b)/2).astype(numpy.uint8)  #*255.
    #print x.min(), x.max(), y.min(), y.max()
    #x=numpy.ones(tuple(list(pf.shape[0:2])+[1]))
    z=numpy.ones(tuple(list(a.shape[0:2])+[1]))*127
    t=numpy.dstack([x,y,z]).astype(numpy.uint8).copy('C')
    #print t.shape
    return hsv2rgb(t)#.swapaxes(0,2).copy()

if __name__ == '__main__':
    #from pycvf.lib.video import camerareader2
    from pycvf.lib.video import camerareader
    from pycvf.lib.video.render.lazy as lazydisplay
    #from pycvf.lib.video import lazydisplayqt as lazydisplay
    #c=camerareader2.CameraReader2()
    c=camerareader.CameraReader("/dev/video1")
    print "A"
    class GetSizeInfo:
        def __init__(self):
            self.size=None
        def f(self,i):
            #print i
            self.size=i.shape
    getsizeinfo=GetSizeInfo()
    c.observer=getsizeinfo.f
    print "B"
    c.step()
    c.step()
    print getsizeinfo.size
    print "?"
    l=lazydisplay.LazyDisplay()
    print "Cm"
    #of=OpticalFlowLK( (getsizeinfo.size[0], getsizeinfo.size[1]),winsize=(5,5))
    #of=OpticalFlowLK( (256, 256),winsize=(5,5))
    of=OpticalFlowBM( (256, 256) )
    #of=OpticalFlowHS((256,256))
    print "done"
    
    #of=OpticalFlowHS((getsizeinfo.size[0], getsizeinfo.size[1]))
    c.observer=lambda i:l.f(flow2rgb(numpy.array(of.push(i[:256,:256,1].astype(numpy.uint8)))))
    while (True):
       c.step()

