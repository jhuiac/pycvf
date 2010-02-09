# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# MyModel By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
################################################################################################################################################################################
# Includes
################################################################################################################################################################################


###
###


from pycvf.core import genericmodel
from pycvf.nodes.datatypes import image
import numpy,scipy,scipy.ndimage

F1=numpy.array([[0,1,0],[1,1,1],[0,1,0]])

def gradient_magnitude(img):
    g=scipy.gradient(img)
    return scipy.abs(g[0]+1j*g[1])
    
def skeletize(img):
    dt=numpy.float32
    if (img.ndim==3):
      img=img.mean(axis=2)
    ximg=img.max()-img
    dimg=scipy.ndimage.distance_transform_edt(ximg)
    mimg1=scipy.ndimage.maximum_filter(dimg,size=(3,3))
    mimg2=scipy.ndimage.maximum_filter(dimg,size=(3,1))    
    mimg3=scipy.ndimage.maximum_filter(dimg,size=(1,3))
    mimg4=scipy.ndimage.maximum_filter(dimg,footprint=F1)
    img=(((dimg-mimg1)==0).astype(dt))
    img+=(((dimg-mimg2)==0).astype(dt))
    img+=(((dimg-mimg3)==0).astype(dt))
    img+=(((dimg-mimg4)==0).astype(dt))    
    img*=ximg
    #img*=dimg
    return img

def cgradient(img):
    r=gradient(img)
    return r[0]+1j*r[1]

def V(y,x):
    return numpy.array([y,x])

def latecki_ssm(img):
    ba,bb,bc=numpy.roll(img,1,axis=0),img,numpy.roll(img,-1,axis=0)
    aa,ab,ac=numpy.roll(ba,-1,axis=1),numpy.roll(bb,-1,axis=1),numpy.roll(bc,-1,axis=1)
    ca,cb,cc=numpy.roll(ba,1,axis=1),numpy.roll(bb,1,axis=1),numpy.roll(bc,1,axis=1)
    s=numpy.zeros(img.shape)
    s+=ab*V(0,-1)+ba*V(-1,0)+cb*V(0,1)+bc*V(1,0)
    return max(0,s)

def skeletize_latecki(img,gaussian_filter):
    # http://www.cis.temple.edu/~latecki/Papers/icip__SSM07.pdf
    dt=numpy.float32
    if (img.ndim==3):
      img=img.mean(axis=2)
    img=img.astype(dt)
    img/=img.max()      
    gimg=scipy.ndimage.gaussian_filter(img,2)
    ximg=img.max()-img
    dimg=scipy.ndimage.distance_transform_edt(ximg)
    #
    # now let's compute f
    fimg=1-scipy.abs(scipy.convolve(cgradient(gimg),dimg))
    #
    # and now compute its gradient
    u0,v0=scipy.gradient(fimg)
    #
    # now we do diffusion

    
    ##
    # now we apply SSM map
    gvf=diffuse_gradient_vector
    
    #
    # then we do particular point detection
    mimg1=scipy.ndimage.maximum_filter(dimg,size=(3,3))
    img=(((dimg-mimg1)==0).astype(dt))
    img*=ximg
    return img

class Model(genericmodel.Model):
        def input_datatype(self,x):
            assert(isinstance(x,image.Datatype) or issubclass(x,image.Datatype))
            return image.Datatype
        def output_datatype(self,x):
            return image.Datatype
        def init_model(self,variant="",*args,**kwargs):
                 self.processline='src|skeletize'
                 f=eval("skeletize"+variant)
                 self.context['skeletize']=lambda x:(f(x,*args,**kwargs))

__call__=Model
