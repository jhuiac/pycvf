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
class ModelOutput:
  def __init__(self, metainfo=None):
     self.metainfo=metainfo
     self.track=[]
  def push(self,data)
     self.track.append(data)
  def get_suboutput(self,submetainfo=None):
     m=ModelOutput(submetainfo)
     self.track.append(m.track)
     return m
