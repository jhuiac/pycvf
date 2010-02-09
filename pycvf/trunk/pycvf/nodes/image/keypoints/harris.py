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
from pycvf.datatypes import image
import numpy,scipy,scipy.ndimage


def harris(I):
    """ Harris Corner Detector """
    Ix,Iy = scipy.gradient(I)
    H11 = Ix*Ix
    H12 = Ix*Iy
    H22 = Iy*Iy
    return (H11*H22 - H12**2) 

def harris_smooth(I,alpha=0.04,si=1):
    """ Harris Corner Detector """
    def imsmooth(I,si):
        return scipy.ndimage.gaussian_filter(I,si)
    Ix,Iy = scipy.gradient(I)
    H11 = imsmooth(Ix*Ix, si)
    H12 = imsmooth(Ix*Iy, si)
    H22 = imsmooth(Iy*Iy, si)
    return (H11*H22 - H12**2) - alpha*(H11+H22)**2


def showkkp(im,nb=100, *args,**kwargs):
   ags=scipy.argsort(harris(im,*args,**kwargs).ravel())[-nb:]
   im=im[:,:,numpy.newaxis].repeat(3,axis=2)
   im/=im.max()
   for p in ags:
     y,x=p//im.shape[1],p%im.shape[1]
     im[max(0,y-1):y+1,max(0,x-1):x+1,0]=1
     im[max(0,y-1):y+1,max(0,x-1):x+1,1]=0
     im[max(0,y-1):y+1,max(0,x-1):x+1,2]=0
   pyplot.imshow(im)

class Model(genericmodel.Model):
        def input_datatype(self,x):
            assert(isinstance(x,image.Datatype) or issubclass(x,image.Datatype))
            return image.Datatype
        def output_datatype(self,x):
            return image.Datatype
        def init_model(self,variant="",*args,**kwargs):
                 self.processline='src|harris'
                 f=eval("harris"+variant)
                 self.context['harris']=lambda x:(f(x,*args,**kwargs))

__call__=Model
