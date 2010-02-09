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
import scipy.ndimage as scind
import numpy


class Rescaler1d:
    def __init__(self,size):
        self.size=size
    def process(self,img):
        img=numpy.asarray(img)
        #print img.shape
        if (img.ndim==1):
          dmap=numpy.arange(0.,img.shape[0],float(img.shape[0])/self.size[0])
          print img.shape,dmap.shape
          return scind.interpolation.map_coordinates(img,[dmap])
        elif (img.ndim==2):
          return numpy.hstack([self.process(img[l,:]) for l in range(img.shape[0]) ])
        else:
          raise ValueError,  "Unsupported number of dimensions"

class Rescaler2d:
    def __init__(self,size):
        if (len(size)==2):
          self.size=size
          self.mode='S'
        elif (len(size)==3):
          self.size=size[0:2]
          self.mode=size[2]
        else:
          raise ValueError,"invalid rescale"
    def cgrid(self,h,w,dh,dw):
        if (self.mode=='R'):
          return numpy.dstack([numpy.arange(0.,h,float(h)/dh).reshape(dh,1).repeat(dw,axis=1).T,
                             numpy.arange(0.,w,float(w)/dw).reshape(dw,1).repeat(dh,axis=1)])
        elif  (self.mode=='S'):
          ih=(dh*w)/dw
          iw=(dw*h)/dh

          if (ih > h):
            rh=(ih-h)
            #print "rh",rh
            return numpy.dstack([numpy.arange(-(rh/2.),ih-(rh/2.)-0.1,float(ih)/dh).reshape(dh,1).repeat(dw,axis=1).T,
                             numpy.arange(0.,w-0.1,float(w)/dw).reshape(dw,1).repeat(dh,axis=1)])
          else:
            rw=(iw-w)
            #print "rw",rw
            return numpy.dstack([numpy.arange(0,h-0.1,float(h)/dh).reshape(dh,1).repeat(dw,axis=1).T,
                             numpy.arange(-(rw/2.),iw-(rw/2.)-0.1,float(iw)/dw).reshape(dw,1).repeat(dh,axis=1)])
        elif  (self.mode=='T'):
          ih=(dh*w)/dw
          iw=(dw*h)/dh

          if (ih < h):
            rh=(ih-h)
            #print "rh",rh
            #print (-(rh/2.),ih-(rh/2.),float(ih)/dh), (0.,w,float(w)/dw)
            return numpy.dstack([numpy.arange(-(rh/2.),ih-(rh/2.)-0.1,float(ih)/dh).reshape(dh,1).repeat(dw,axis=1).T,
                             numpy.arange(0.,w-0.1,float(w)/dw).reshape(dw,1).repeat(dh,axis=1)])
          else:
            rw=(iw-w)
            #print "rw",rw
            #print (0,h,float(h)/dh), (-(rw/2.),iw-(rw/2.),float(iw)/dw)
            return numpy.dstack([numpy.arange(0,h-0.1,float(h)/dh).reshape(dh,1).repeat(dw,axis=1).T,
                             numpy.arange(-(rw/2.),iw-(rw/2.)-0.1,float(iw)/dw).reshape(dw,1).repeat(dh,axis=1)])
        else:
           raise ValueError,"Wrong rescale mode (R, S or T)"
  

    def process(self,img):
        if (img.ndim==2):
            return scind.interpolation.map_coordinates(img,self.cgrid(img.shape[0],img.shape[1],self.size[0],self.size[1]).T)
        elif (img.ndim==3):
            return numpy.dstack([self.process(img[:,:,l]) for l in range(img.shape[2]) ])
        else:
            raise ValueError, "Unsupported number of dimensions"


