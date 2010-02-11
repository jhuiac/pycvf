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


import numpy, sys
import scipy.stats
from pycvf.core import genericmodel
from pycvf.datatypes import image
from pycvf.datatypes import list as ldt


#def soft_thres(y,thld):
#    x = numpy.abs(y)
#    return numpy.sign(y)*(x >= thld)*(x - thld)

#def hard_thres(y,thld):
#   return (numpy.abs(y) > thld)*y
    
    
def wdenoise(x,tau=-1,mode=0,multiplier=3):
      if (type(x) in [list,tuple]):
	  return map(lambda y:wdenoise(y,tau,mode),x)
      else:
         if (tau=-1):
            tmp=numpy.hstack(reduce( lambda b,n: b+map(lambda y:y.ravel(),filter(lambda y:type(y)==numpy.ndarray,n)) ,x,[]) )             
            tau= multiplier*scipy.stats.median(abs(tmp(:)))/.67;            
         elif(tau=-2),
            tau = multiplier*std(tmp(:));
         if (mode==0):
           x[abs(x)<=tau]=0
           return x
         elif (mode==1):
           x[abs(x)<=tau]=0  
           x[x>tau]-=tau
           x[x<-tau]+=tau
           return x
         else:
           raise ValueError,"Unknown mode"


Model=genericmodel.pycvf_model_function(ldt.Datatype(ldt.Datatype(image.Datatype)),ldt.Datatype(ldt.Datatype(image.Datatype)))(wdenoise)
__call__=Model
                 
