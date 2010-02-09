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

class PseudoReader():
   def __init__(self,o,a=None,observer=None):
      self.o=o
      self.co=o
      self.a=a
      self.observer=observer
   def step(self):
      if (self.co!=None):
        if (self.observer):
          self.observer(self.co)
        r=self.co
        self.co=None 
        return r
      raise StopIteration
   def get_current_address(self):
      return self.a
   def set_observer(self,observer):
      self.observer=observer
   def run(self):
      try:
        while True:
          self.step()
      except StopIteration:
          return
      