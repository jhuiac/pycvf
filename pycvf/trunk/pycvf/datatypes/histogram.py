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

from pycvf.lib.video.render.lazy import LazyDisplay

from pycvf.datatypes import basics

from pycvf.lib.ui.qtdisplay import QtDisplay
from pycvf.structures import spatial
from pycvf.lib.graphics.imgfmtutils import *

import matplotlib.pyplot as pylab
from cStringIO import StringIO 

from matplotlib.backends.backend_agg import FigureCanvasAgg

class Datatype(basics.NumericArray.Datatype):
  ld=None
  content_type="Histogram"
  @classmethod
  def display(cls,x):
     if (not cls.ld):
          cls.ld=LazyDisplay()
     out = StringIO() 
     f=pylab.figure()
     a=f.gca()
     #a.clf()
     a.bars2d(range(len(x)),x)
     out=StringIO()
     f.savefig(out,format="PNG")
     x=PIL2NumPy(PIL.Image.open(out,"PNG"))
     cls.ld.f(x)
  @classmethod
  def get_numpy(cls,x):
     return x
  @staticmethod
  def pylab_display(cls,x):
     pylab.imshow(x)
  @classmethod
  def get_widget(cls,x,*args, **kwargs):
     q=QtDisplay(*args,**kwargs)
     return q
  @classmethod
  def set_widget_value(cls,widget,x):
     out = StringIO() 
     img_dpi=72
     width=400
     height=300
     f=pylab.figure(dpi=img_dpi, figsize=(width/img_dpi, height/img_dpi))
     a=f.gca()
     a.bar(range(len(x)),x,0.5)
     out=StringIO()
     canvas = FigureCanvasAgg(f)
     canvas.draw()
     size = (int(canvas.figure.get_figwidth())*img_dpi, int(canvas.figure.get_figheight())*img_dpi)
     buf=canvas.tostring_rgb()
     im=PIL.Image.fromstring('RGB', size, buf, 'raw', 'RGB', 0, 1)
     x=PIL2NumPy(im)
     widget.f(x)
  