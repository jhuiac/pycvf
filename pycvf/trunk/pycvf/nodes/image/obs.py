# -*- coding: utf-8 -*-
import numpy, sys
from pycvf.core import genericmodel
from pycvf.datatypes import image
from pycvf.datatypes import basics
from pycvf.lib.info.obs import make_observation

def obs(x,*args,**kwargs):
  return make_observation(*args,**kwargs)(x)

Model=genericmodel.pycvf_model_function(image.Datatype,basics.NumericArray.Datatype)(obs)
__call__=Model
                 
