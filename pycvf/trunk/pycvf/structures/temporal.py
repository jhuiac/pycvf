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
from pycvf.nodes.structure import ModelStructure

class TemporalStructure(ModelStructure):
  def iterate(self,instance):
     return range(len(instance))
  def extractor(self,instance,pos):
     return instance[pos]
  def distance(self,x1,x2):
     return abs(x1-x2)
