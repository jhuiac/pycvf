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

from pycvf.core.errors import pycvf_debug, pycvf_warning, pycvf_error


class Index(object):
    """
     An index class is class that allows you to associate 
     
     
     keys to list of values/addresses
    """
    def __init__(self,*args,**kwargs):
        """
        This is simply the normal constructor of your index structure
        """
    def add_many(self,keys,values):
        """
           keys and values have to be 2d arrays,
           one vector per row.

           values may be array of object,
           
           while most implementations of keys require arrays of vectors.
        """
    @staticmethod
    def load(filename):
        """
         Load is a static method for loading the index structure and its data.
        """
    def save(self,filename):
        """
          Save allow you to do the opposite of load
        """

    def __getitem__(self,query):
        """
          Syntaxic sugar to next method.
        """

    def getitem(self,query,numelem=1):
        """
         query for the numelem nearest elements to query
        """
    def getitems(self,queries,numelem=1):
        """
         same as previous query except that we do many queries instead of only once
        """
    def keys(self):
        """ return the list of the keys in an index """
    def values(self):
        """ return the list of the values in an index """        
        return iter(self._values) if self._values!= None else []
    def __len__(self):
        """ return the len of an index structure """
    def reset(self):
        """ reset an indexstructure """


__call__=SashIndex
load=SashIndex.load
