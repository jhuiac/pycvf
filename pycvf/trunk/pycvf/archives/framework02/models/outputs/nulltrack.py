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
  def __init__(self, trkfilename, metainfo):
     self.track=NullTrack(meta=map(lambda x: x[2],self.observed_features))
  def push(self,data):
     pass
  def get_suboutput(self,submetainfo=None):
     m=ModelOutput(submetainfo)
     return m