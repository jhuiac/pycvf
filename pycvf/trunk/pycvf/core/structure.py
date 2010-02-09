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


##############################################################################################################################################################################3
##############################################################################################################################################################################3      
###
### Structure should contain 7 things   
###                                     0) a name
###                                     1) structure iterator (with respect to an instance)
###                                     2) an extractor ( with respect to an instance and a position)
###                                     3) neighborhood (optional,with respect to instance and position)
###                                     4) spatial distance (optional, with respect to some instance)
###                                     5) submodels (optional, submodels autonomous)
###                                     6) submodels (optional,that depends on the neighborhood)
### A Model without structure is an Atomic Model
###
###############################################################################################################################################################################
###############################################################################################################################################################################


class ModelStructure:
  def __init__(self,name,iterator=iter,extractor=lambda m,p:m[p],neighbourhood_f_d=None,distance=None,models=None,conditionalmodels_d=None,weight=1):
     self.name=name
     self.iterator_f=iterator
     self.extrator_f=extractor
     self.neighbourhood_f_d=neighbourhood_f_d or {}
     self.distance_f=distance
     self.models=models or []
     self.cliqueiterator_f_d=clique_iterator_f_d or {}
     self.conditionalmodel=conditionalmodel or []     
     self.weight=weight
  def iterate(self,instance):
     return self.iterator_f(instance)
  def extractor(self,instance,position):
     return self.extractor_f(instance,position) 
  def neighborhood(self,key,instance,position):
     return self.neighbourhood_f_d[key](instance,position)
  def distance(self,e1,e2):
     return self.distance_f(e1,e2)
  def train(self, datas, * args, ** kwargs):
      for x in self.models:
          x.train(datas, *args, **kwargs)
      for y in self.clique_iterator_f_d.values():
          try:
            self.conditionalmodel[y[0]].train(y[1].extract(datas))
          except:
            pass
  def cliques(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).cliques

  def cliques_extract_all(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).extract_all()

  def cliques_extract_all_rec(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).extract_all_rec()

  def cliques_iterate_all(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).iterate_all()

  def cliques_addresses(self,instance,key,*args,**kwargs):
    return eval("self.CliqueSet"+key)(self,instance,*args,**kwargs).addresses()