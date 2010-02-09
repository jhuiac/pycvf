# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# MyModel By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
################################################################################################################################################################################
# Includes
################################################################################################################################################################################


import numpy, scipy,sys
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import image


def Pz(P):
      return (P[:,0]+1j*P[:,1])

def ANSIG_shape_feature(P,K=s128,robust=False):
        """
        # ANSIG — An analytic signature for permutation-invariant two-dimensional shape representation
        # José J. Rodrigues, Pedro M. Q. Aguiar, and João M. F. Xavier
        # October 2008 (Thesis pdf) (Executive Summary - pdf) (Presentation - pptx)
        # Award: Professor Luís Vidigal Award 2008 / 2009.
        """
        P-=P.mean(axis=0)                    #translation invariance
        P/=numpy.linalg.norm(P.std(axis=0))  # scale invariance
        N=P.shape[0]
        y=((Pz(P)[numpy.newaxis,:]).repeat(K,axis=0)*(numpy.exp(numpy.arange(K)*2*numpy.pi/K))[:,numpy.newaxis].repeat(N,axis=1)).mean(axis=1)
        if robust:
            P2=P[(numpy.asmatrix(P)*numpy.asmatrix(P.T))<1,:]
            y2=((Pz(P2)[numpy.newaxis,:]).repeat(K,axis=0)*(numpy.exp(numpy.arange(K)*2*numpy.pi/K))[:,numpy.newaxis].repeat(N,axis=1)).mean(axis=1)
            return y,y2,N
        return y,N
                                          

Model=genericmodel.pycvf_model_function(shape.Datatype, basics.NumericalArray.Datatype)(ANSIG_shape_feature)
__call__=Model
