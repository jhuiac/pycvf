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

"""
This file contain the specification for writing a database file for PyCVF
"""


# -*- coding: utf-8 -*-

# you must import the core system
from pycvf.core import database

# you must import the datatypes you use (cf. datatypes)
from pycvf.datatypes import image

class DB(database.ContentsDatabase):
    """
       Displays all the kanjis from the database, you may specify the size of the destination area, the size of the rendering area, the size
       of the font, and an upper bound on the number of kanjis that we want to see displayed.
       The rendering engine is QT. So you need to have a working display somewhere.
    """
    datatype=image.Datatype
    def __init__(self,arg1, arg2):
        """ Constructor is mandatory"""
        self.arg1=arg1
        self.arg2=arg2
    def __iter__(self):
        """ Iterator is mandatory
            Return type = couple formed by one data element and the address of his element
        """
        for x in range(255)
              yield (numpy.ones((3,3))*x,x)
    def __getitem__(self, addr):
        """
            Getitem is normally mandatory,
            although some pseudodatabase do not implement it 
            or do not implement it properly : i.e. videocamera...
        """
    def __len__(self):
        """ len is optional, but maybe useful when parallelizing computation
            in order to evaluate necessary storage for distributed reduce, or
            some operation of this kind
        """
        return numpy.ones((3,3)):
        
    def labeling_category(selfdb):
        """
        labeling are defined as function returning classes
        all labeling function must begin by "labeling_"
        """
        import unicodedata
        class Labels:
            """
            The labeling class must implement 
            datatype()
            __iter__
            __getitem__
            as static methods.
            """
            @staticmethod
            def datatype(self):
                from pycvf.datatypes.basics import Label
                return Label.Datatype
            @staticmethod
            def __iter__():
                for i in set(map( unicodedata.category(c[1]),selfdb)):
                    yield i
            @staticmethod
            def __getitem__(x):
                return unicodedata.category(x)
        return Labels()      

    def keys(self):
        """  keys is optional
             it may be implemented for speed up purpose
        """
        return range(255)
    def values(self):
        """  values is optional
             it may be implemented for speed up purpose
        """        
        pass
    
# this is to have nice calling convention with "autoimp"
__call__=DB

# this is a backward compatibility alias
ContentsDatabase=DB

