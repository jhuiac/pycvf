# -*- coding: utf-8 -*-

#import pyffmpeg_audioqueue as audioqueue
import audioqueue
import scipy
import numpy
import itertools
from pycvf.core.errors import pycvf_warning
from pycvf.audio.lib.griffinlim import *


def griffinlimcomputer(gen):
    class GriffinLimAudioReader():
       def __init__(self, niter=5, df=128, di=128//12):
             ww=hamming(df)
             GriffinLim.df=df
             GriffinLim.di=di
             GriffinLim.make_positive=0.5
             self.niter=niter
             gl=GriffinLim(ww=ww)
             #XO=modelinstance.forward(xn)
             #YNA=numpy.abs(XO)
             self.r=None
       def push(reader):
             ##
             ## ok we put all the spectrum in memory
             ## 
             YNA=numpy.array([ x for x in reader])
             self.r=gl.optimize(YNA,iter=self.niter)
             return iter(self)
       def __iter__(self)
             yield self.r
                
    return GriffinLimAudioReader()

    
#   except Exception,e:
#     pycvf_warning("Error while computing spectrum for audiofile :["+str(e)+"]")
#     raise StopIteration,e
      
from pycvf.core import genericmodel
from pycvf.datatypes import audio

class Model(genericmodel.Model):
  def input_datatype(self,x):
       return audio.Spectrum.Datatype
  def output_datatype(self,x):
       return audio.Datatype
  def init_model(self,*args,**kwargs):
       self.processing=[('griffinlim',{'griffinlim':griffinlimcomputer})] 

__call__=Model


