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

#class SequenceReader():
   #def __init__(self,o,a=None,observer=None):
      #self.o=o
      #self.a=a
      #self.observer=observer
      #self.i=0
   #def step(self):
      #try:
          #if (self.observer):
           #self.observer(self.o[self.i])
          #r=self.o[self.i]
          #self.i+=1
          #return r
      #except IndexError:
         #raise StopIteration
   #def get_current_address(self):
      #return (self.a,self.i)
   #def set_observer(self,observer):
      #self.observer=observer
   #def run(self):
      #try:
        #while True:
          #self.step()
      #except StopIteration:
          #return
      

class SequenceReader():
   def __init__(self,o,a=None,observer=None,len=None):
      self.o=o
      self.a=a
      self.observer=observer
      self.i=0
      self.len=len
   def copy(self):
       return SequenceReader(self.o,self.a)
   def step(self):
      try:
          r=self.o.next()
          if (self.observer):
           self.observer(r)
          self.i+=1
          return r
      except IndexError:
         raise StopIteration
   def get_current_address(self):
      return (self.a,self.i)
   def set_observer(self,observer):
      self.observer=observer
   def run(self):
      try:
        while True:
          self.step()
      except StopIteration:
          return
   def __len__(self):
     return self.len
