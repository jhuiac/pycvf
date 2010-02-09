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
##
## The new model builder is based on autoimp
##

import sys

#sys.path

from autoimp import *

def model_build(xstr, vdb,suppargs):
  print "loading model ...",xstr
  if (type(xstr) in [ str ]):
     suppargs=eval('{'+suppargs+'}')
  res=eval(xstr.replace('@',"'/',vdb,**suppargs"))
  res.init()
  return res
