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

class IterReader():
   def __init__(self,i,a=None,observer=None):
      self.i=i
      self.a=a
      self.observer=observer
      self.c=0
   def step(self):
          o=self.i.next()
          if (self.observer):
            self.observer(o)
          self.c+=1
   def get_current_address(self):
      return (self.a,self.c)
   def set_observer(self,observer):
      self.observer=observer
   def run(self):
      try:
        while True:
          self.step()
      except StopIteration:
          return
      