# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Video Database for Training
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
################################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################
from pycvf.core import database
from pycvf.datatypes import basics
import numpy, random

#########################################################################################################################################
# Create the ContentsDatabase Object
#########################################################################################################################################
from pycvf.lib.ontology import ystockquote

class DB(database.ContentsDatabase,basics.NumericVector.Datatype):
   def __init__(self, symbol, datefrom, dateend):
       self.symbol=symbol
       self.datefrom=datefrom
       self.dateend=dateend
       self.data=ystockquote.get_historical_prices(symbol,datefrom,dateend)
   def __iter__(self):
       c=1
       for l in self.data[1:]:
           yield (numpy.array(map(float,l[1:])),((self.symbol),l[0],c))
           c+=1
   def __getitem__(self,key):
       assert(self.symbol==key[0])
       return map(float,self.data[key[2]][1:])
   def __len__(self):
      return self.data.shape[0]

# Framework 2 compatibility
ContentsDatabase=DB
__call__=DB
