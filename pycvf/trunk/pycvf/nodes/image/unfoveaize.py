# -*- coding: utf-8 -*-

import numpy, sys
from pycvf.core import genericmodel
from pycvf.datatypes import image
from pycvf.datatypes import list as ldt

from pycvf.nodes.image.pyramidalize import pyramidalize

def focus_part_put(img,x,focuspoint=(0.5,0.5),szpart=(32,32)):
  h,w=img.shape[:2]
  by=max(0,int(h*focuspoint[1])-(szpart[1]//2))
  ey=by+min(szpart[1],x.shape[1])
  bx=max(0,(w*focuspoint[0])-(szpart[0]//2))
  ex=bx+min(szpart[0],x.shape[0])
  try:
    img[by:ey,bx:ex]=x
  except:
    pass
  return img

def upscale(img):
  return img.repeat(2,axis=0).repeat(2,axis=1)

class Unfoveaizer:  
  def __init__(self,*args, **kwargs):
    self.args=args
    self.kwargs=kwargs
    self.focus_point=(.5,.5)
  def process(self,x):
    return reduce(lambda b,y:focus_part_put(upscale(b),y), x[1:] , x[0])



Model=genericmodel.pycvf_model_class(ldt.Datatype(image.Datatype),image.Datatype)(Unfoveaizer)
__call__=Model
                 
