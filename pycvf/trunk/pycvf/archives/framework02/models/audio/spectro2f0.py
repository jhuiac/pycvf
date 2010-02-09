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
from pycvf.nodes import visionmodel_with_segmentation as visionmodel

class Model(visionmodel.MyModel):
  feature='argsort' 
  feature_addvoc={}
  draw_args={'title' : 'Returns F0 according to spectrogram'}
  def init_models(self,basepath):
      self.models.append(CachedModel(SimpleMeanAndVarianceModel,lambda:SimpleMeanAndVarianceModel(),basepath+"fixwindow2f0-mean.mdl"))
#####################################################################################################################################

__call__=Model