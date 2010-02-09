# -*- coding: utf-8 -*-

import numpy, sys
from pycvf.core import genericmodel
from pycvf.datatypes import image
from pycvf.datatypes import list as ldt

from pycvf.nodes.image.pyramidalize import pyramidalize

def focus_part(x,focuspoint=(0.5,0.5),szpart=(32,32)):
  h,w=x.shape[:2]
  by=int(h*focuspoint[1])-(szpart[1]//2)
  ey=by+szpart[1]
  bx=(w*focuspoint[0])-(szpart[0]//2)
  ex=bx+szpart[0]
  return x[by:ey,bx:ex]

class Foveaizer:  
  def __init__(self,*args, **kwargs):
    self.args=args
    self.kwargs=kwargs
    self.focus_point=(.5,.5)
  def process(self,x):
    r=map(lambda xi:focus_part(xi,self.focus_point), pyramidalize(x,*self.args,**self.kwargs))
    return r



Model=genericmodel.pycvf_model_class(image.Datatype,ldt.Datatype(image.Datatype))(Foveaizer)
__call__=Model
                 
