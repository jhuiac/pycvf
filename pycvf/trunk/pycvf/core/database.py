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

from pycvf.core.errors import pycvf_warning
import itertools

class ContentsDatabase(object):
  def values(self):
    return itertools.imap(lambda x:x[0], self)
  def keys(self):
    return itertools.imap(lambda x:x[1], self)
  def datatype(self):
      pycvf_warning("You are using a old style database... Please implement 'datatype' for specifying the datatype type")
      return self
  def labeling_default(selfdb):
    class Labels:
            @staticmethod
            def datatype(x):
                from pycvf.datatypes.basics import Label
                return Label.Datatype
            @staticmethod
            def __iter__():
                for i in selfdb:
                    yield c[1]
            @staticmethod
            def __getitem__(x):
                return x
    return Labels()
  def labeling_plus(selfdb):
    class Labels:
            @staticmethod
            def datatype(x):
                from pycvf.datatypes.basics import Label
                return Label.Datatype
            @staticmethod
            def __iter__():
                for i in selfdb:
                    yield 1
            @staticmethod
            def __getitem__(x):
                return 1
    return Labels()
  def labeling_minus(selfdb):
    class Labels:
            @staticmethod
            def datatype(x):
                from pycvf.datatypes.basics import Label
                return Label.Datatype
            @staticmethod
            def __iter__():
                for i in selfdb:
                    yield -1
            @staticmethod
            def __getitem__(x):
                return -1
    return Labels()
  def labeling_zero(selfdb):
    class Labels:
            @staticmethod
            def datatype(x):
                from pycvf.datatypes.basics import Label
                return Label.Datatype
            @staticmethod
            def __iter__():
                for i in selfdb:
                    yield 0
            @staticmethod
            def __getitem__(x):
                return 0
    return Labels()
      

