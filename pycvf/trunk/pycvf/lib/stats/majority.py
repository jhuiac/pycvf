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
import itertools




##
## Simple majority
## 

class Majority:
   def __init__(self):
      pass
   def majority(self,elm):
      print elm
      raise Exception
   
       
###
### We have a certain number of elements that each elect a certain number of candidates
###   -- We want to select the candidate the match the most the structure
### 



class LocalConsensusMajority:
   def __init__(self,structure_node,structure_edge,nitems):
      self.nitems=nitems
      self.structure_nodes=structure_nodes
      self.structure_edges=structure_edges
   def do_local_votes(self,e):
      ret=self.structure_nodes.apply_map(lambda x:index.getitems(x,self.nitems,with_dist=True).e)
      retidx=strucutres.iterate_all(e)
      return itertools.izip(ret,retidx)
   def edge_proba(self,elm):
       res=strucutres_edges.instantiatel(elm)
       for e in strucutres_edges.iterate_all(elm):
            c=structures_edges.clique(elm)  
            # for each possible source we measure how close are the index of the variables
            r={}
            for k in c:
               r[k[0]]=0
            for p1 in range(len(c)):
                for p2 in range(p1,len(c)):
                   f=(1+distnorm(p[1][1]-p[1][2])) # we make an error of "1" each time there but this is not easy to solve if we want to stay generic
                   r[c[p1][0]]+=f**-1
                   r[c[p2][0]]+=f**-1
            res[e]=r
       return res
   def majority(elm):
       res=strucutres_edges.instantiatel(elm)
       for e in strucutres_edges.iterate_all(elm):
            c=structures_edges.clique(elm)  
            # for each possible source we measure how close are the index of the variables
            r={}
            for k in c:
               r[k[0]]=0
            for p1 in range(len(c)):
                for p2 in range(p2,len(c)):
                   f=(1+distnorm(p[1][1]-p[1][2])) # we make an error of "1" each time there but this is not easy to solve if we want to stay generic
                   r[c[p1][0]]+=f**-1
                   r[c[p2][0]]+=f**-1
            res[e]=r
       return res
      
   
       
      