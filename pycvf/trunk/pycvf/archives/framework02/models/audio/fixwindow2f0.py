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

import re, os, math, random, time,sys, traceback, time, logging
import scipy,pylab,scipy.ndimage

from pycvf.lib.stats.models import *

####################################################################################################################################
from pycvf.core import genericmodel 

class Model(genericmodel.GenericModel):
  feature='src|fft|abs|argsort' 
  feature_addvoc={}
  draw_args={'title' : 'position of maxima in FFT spectrum'}
  def init_models(self,basepath):
      self.models.append(CachedModel(SimpleMeanAndVarianceModel,lambda:SimpleMeanAndVarianceModel(),basepath+"fixwindow2f0-mean.mdl"))

__call__=Model

#####################################################################################################################################
