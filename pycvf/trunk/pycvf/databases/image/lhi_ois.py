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
#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################

import time,random
from pycvf.core import database
from pycvf.lib.video.lazydisplayqt import LazyDisplayQt
from jfli.project_specific.lhi import objects_in_scenes 
from pycvf.datatypes import image

class ContentsDatabase(database.ContentsDatabase):
  def datatype(self):
      return image.Datatype
  def __init__(self,maxcnt=20, categ="human"):
      self.categ=categ
      self.maxcnt=maxcnt
  def __iter__(self):
     i=objects_in_scenes.LHI_objects_in_scenes.object_index()
     for ni in range(self.maxcnt): 
        yield (objects_in_scenes.LHI_objects_in_scenes.objects_in_scene(*(random.sample(i[self.categ],1))[0],otype=self.categ)[0].get_masked_obj(True),None)


