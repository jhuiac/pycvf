# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# PyCVF
# 2009-2010 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
################################################


import numpy, random,re
from pycvf.core import database
from pycvf.datatypes import basics

class DB(database.ContentsDatabase,basics.NumericArray.Datatype):
  """
    * Returns elements from vector database as a set for doing some learning on it.
  """
  def __init__(self,vdbconstructor, maxelems=None):
     self.vdb=vdbconstructor
     self.maxelems=maxelems
     selfdb=self
     for x in dir(self.vdb()):
        label=re.match("labeling_(.*)",x)
        if (label!=None):
          xlabel=label.group(1)[:]
          print "forwarding labels", label#.group(1)
          def new_labeling(xlabel):
            class Labeling:
              def __init__(selfx,xlabel):
                 selfx.xlabel=xlabel[:]
              @staticmethod
              def datatype():
                from pycvf.datatypes.basics import Label,NumericArray
		return NumericArray.Datatype
              def __iter__(selfx):
                cont=True
                while cont:
                  st=numpy.random.get_state()
                  vdb=self.vdb()
                  labelingf=eval("vdb.labeling_"+selfx.xlabel,{'vdb':vdb})()
                  yield (numpy.vstack([labelingf(x[1]) for x in vdb]),st)
                  if self.maxelems!=None:
                     self.maxelems-=1
                     if self.maxelems<=0:
                         break
              def __getitem__(selfx,st):
                 svst=numpy.random.get_state()      
                 numpy.random.set_state(st)                  
                 vdb=self.vdb()   
                 labelingf=eval("vdb.labeling_"+selfx.xlabel,{'vdb':vdb})()
                 r=numpy.vstack([labelingf[x[1]] for x in vdb]) 
                 numpy.random.set_state(svst)                
                 return r
            return lambda :Labeling(xlabel[:])
          setattr(self,x,new_labeling(xlabel))  
  def __iter__(self):
      cont=True
      while cont:
          st=numpy.random.get_state()
          yield (numpy.vstack([x[0] for x in self.vdb()]),st)
          if self.maxelems!=None:
              self.maxelems-=1
              if self.maxelems<=0:
                  break
  def __getitem__(self,a):
          svst=numpy.random.get_state()      
          numpy.random.set_state(st)
          r=numpy.vstack([x[0] for x in self.vdb()])
          numpy.random.set_state(svst)                
          return r

ContentsDatabase=DB
__call__=DB
