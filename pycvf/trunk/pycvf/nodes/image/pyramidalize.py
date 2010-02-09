# -*- coding: utf-8 -*-

import numpy, sys
from pycvf.core import genericmodel
from pycvf.datatypes import image
from pycvf.datatypes import list as ldt

def downscale_fast(x):
    return x[::2,::2]

def downscale_bm(x):
    return x.reshape(x.shape[0]//2,2, x.shape[1]//2,2,-1).swapaxes(1,2).reshape(x.shape[0]//2,x.shape[0]//2,4,-1).mean(axis=2)


def pyramidalize(x,ds=downscale_bm,upbound=1):
  s=min(x.shape[0],x.shape[1])
  return reduce(lambda b,n:[ds(b[0])]+b ,range(numpy.log2(s)-(1+upbound)), [x])

Model=genericmodel.pycvf_model_function(image.Datatype,ldt.Datatype(image.Datatype))(pyramidalize)
__call__=Model
                 
