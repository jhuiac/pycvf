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
import cPickle as pickle

class PersistentObject(object):
  dirty=True
  @classmethod
  def load(cls,self,filename):
    r=pickle.load(file(filename))
    r.po_filename=filename
    r.dirty=False
    return r
  def save(self):
    if self.dirty:
      self.dirty=False
      pickle.dump(self,file(self.po_filename,"w"))
  def set_filename(self,filename):
      self.po_filename=filename
  def __del__():
    self.save()
