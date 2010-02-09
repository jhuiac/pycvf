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

# 
# Datatype used for interdependant datas
#

def Datatype(*dts):
  class DatatypeT:
    content_type="Tuple"
    @classmethod
    def display(cls,x):
      c=0
      for dt in dts:
        dt.display(x[c])
        c+=1
    @classmethod
    def get_shape_1(cls,x):
      return map(lambda i:dts[i].get_shape_1(x[i]),range(len(dts)))
    @classmethod
    def get_shape_many(cls,x):
      return (len(x),)+tuple(map(lambda i:dt1.get_shape_1(x[0][i]), range(len(dts))))
    @classmethod
    def get_obs_shape_1(cls,x):
      return (dt1.get_obs_shape_1(x[0])+dt2.get_obs_shape_1(x[1]))
    @classmethod
    def get_obs_shape_many(cls,x):
      return (dt1.get_obs_shape_1(x[0][0])+dt2.get_obs_shape_1(x[0][1]))
    @classmethod
    def make_obs_1(cls,x):
      return numpy.hstack([ dt1.make_obs_1(x[0]) , dt1.make_obs_1(x[1])   ] )
    @classmethod
    def make_obs_many(cls,x):
      return numpy.hstack([ dt1.make_obs_many(x[0]) , dt1.make_obs_many(x[1])   ] )
    @classmethod
    def decode_obs_1(cls,x):
      return numpy.hstack([ dt1.make_obs_1(x[0]) , dt1.make_obs_1(x[1])   ] )
    @classmethod
    def decode_obs_many(cls,x):
      return numpy.hstack([ dt1.make_obs_many(x[0]) , dt1.make_obs_many(x[1])   ] )
    @classmethod
    def get_numpy(cls,x):
      return numpy.array([dt1.get_numpy(x[0]),dt2.get_numpy(x[1])])   
    @classmethod
    def get_numpy(cls,x):
      return numpy.array([dt1.get_numpy(x[0]),dt2.get_numpy(x[1])])
    @staticmethod
    def pylab_display(cls,x):
      assert(False)
    @classmethod
    def get_widget(cls,*args):
      from PyQt4.QtGui import QWidget
      class QCoupledWidget(QWidget): 
         def __init__(self,parent,*args):
           self.wi=[ dts[i].get_widget(parent) for i in range(len(dts)) ]
      qw=QCoupledWidget(*args)
      return qw
    @classmethod
    def set_widget_value(cls,widget,x):
      for i in range(len(dts)):
         dts[i].set_widget_value(widget.wi[i],x[i])
    @classmethod
    def get_typerelated_structures(cls):
        return { }
    @classmethod
    def get_default_structure(cls):
       return None

  return DatatypeT
