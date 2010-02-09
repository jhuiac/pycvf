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
import sys,numpy

class TexDoc:
    """
    PCA(Principal component analysis) aims at transforming a large number of variables that are likely to be correlated 
    into a smaller number of uncorrelated variables. 
    The resulting first principal component accounts for as much of the variability in the data as possible.
    Each succeeding component accounts for as much of the remaining variability as possible
    """
    def __init__(self,a):
        pass
    
    def History(self):
        """
        PCA was invented in 1901 by Karl Pearson[1]. 
        Pearson, K. (1901). "On Lines and Planes of Closest Fit to Systems of Points in Space" (PDF). Philosophical Magazine 2 (6): 559–572. http://stat.smmu.edu.cn/history/pearson1901.pdf.
        """
    def Algorithm(self):
        """
        PCA involves the calculation of the eigenvalue decomposition of a data covariance matrix (or singular value decomposition of a data matrix).
        To be efficient the data need to have whiten. 
        """
    def InOtherWords(self):
        """PCA is the simplest of the true eigenvector-based multivariate analyses. 
           Often, its operation can be thought of as revealing the internal structure of the data in a way which best explains the variance in the data.
        """
    
    class Formal():
        """
        Principal component analysis 
        """


def PCA(X):
    #x_mean = numpy.asarray( map( numpy.sum, X.T) ) / len( X )
    x_mean = numpy.asarray( X.mean(axis=0) )
    X_ = X - x_mean
    X_t = numpy.dot( X_.T, X_ ) / len(X)
    lam, vec = numpy.linalg.eig( X_t )
    ans = zip( lam, vec.T )
    ans.sort( reverse = True, key=lambda x:x[0] )
    return ans


class IncrementalPCAdimred:
    def __init__(self,id,od,recomputeafter=-1,alwaystrain=False,verbose=True,recomputeafter_increment=lambda x:-1):
        self.id=id
        self.od=od
        self.ld=0 # length data
        if (id!=-1):
          self.x_sum=numpy.zeros((id))        
          self.exj=numpy.zeros((id,id))
        else:
          self.x_sum=numpy.zeros((1))        
          self.exj=numpy.zeros((1,1))
        self.M=None
        self.IM=None
        self.recomputeafter=recomputeafter
        self.recomputeafter_increment=recomputeafter_increment
        self.alwaystrain=alwaystrain
        self.verbose=verbose
    def add_train(self, train): 
        if (self.id==-1):
          self.id=train.shape[1]
          #print self.id
          assert(self.id<1024)
          self.x_sum=numpy.zeros((self.id))        
          self.exj=numpy.zeros((self.id,self.id))
        old=self.ld
        self.ld+=train.shape[0]
        print train.shape, self.x_sum.shape
        self.x_sum+=train.sum(axis=0)
        t=train-(self.x_sum/self.ld)/len(train) 
        #print t.shape
        self.exj+=numpy.dot(t.T,t)
        if ((self.recomputeafter!=-1) and ((old//self.recomputeafter)-(self.ld//self.recomputeafter))):
            self.recompute()
            self.recomputeafter=self.recomputeafter_increment(self.recomputeafter)
        #print self.recomputeafter,self.ld, old, (old//self.recomputeafter)-(self.ld//self.recomputeafter)
        #sys.stderr.write("ld="+str(self.ld))
    def build(self,train):
        self.add_train(train)
    def recompute(self):
        if (self.verbose):
            sys.stderr.write("recomputing PCA...(direct)")
        cov=(self.exj/self.ld)-(numpy.asarray(self.x_sum/self.ld)**2)
        lam, vec = numpy.linalg.eig( cov )
        ans = zip( lam, vec.T )
        ans.sort( reverse = True, key=lambda x:x[0] )
        #return ans
        self.M=numpy.real(numpy.vstack(map(lambda y:y[1],ans[:self.od])))
        if (self.verbose):
            sys.stderr.write("recomputing PCA...(indirect)")        
        self.IM=numpy.real(numpy.asmatrix(numpy.linalg.pinv(self.M)))
        if (self.verbose):
            sys.stderr.write("done...")
    def dimred(self,observations):
        if (self.alwaystrain):
            self.add_train(observations)
        return (self.M*numpy.asmatrix(observations).transpose()).transpose()
    def dimaug(self,simpleobs):
        return (self.IM*numpy.asmatrix(simpleobs).transpose()).transpose()
    def save(self,f):
        import cPickle as pickle
        pickle.dump(self.ld,f)
        pickle.dump(self.x_sum,f)
        pickle.dump(self.exj,f)
        pickle.dump(self.M,f)
        pickle.dump(self.IM,f)
    def load(self,f):
        import cPickle as pickle
        self.ld=pickle.load(f)
        self.x_sum=pickle.load(f)
        self.exj=pickle.load(f)
        self.M=pickle.load(f)
        self.IM=pickle.load(f)
        assert(self.M!=None)
        assert(self.IM!=None)


class PCAdimred():
    def __init__(self,M,k):
        self.meanobs=M.mean(axis=0)
        self.respca=PCA(M)
        self.k=k
        self.M=numpy.vstack(map(lambda y:y[1],self.respca[:self.k]))
        self.IM=numpy.asmatrix(numpy.linalg.pinv(self.M))
    def dimred(self,observations):
        return (self.M*(numpy.asmatrix(observations)-self.meanobs).transpose()).transpose()
    def dimred1(self,observation):
        return (self.M*(numpy.asmatrix(observation)-self.meanobs).transpose()).transpose()
    def dimaug(self,simpleobs):
        #return (self.M.transpose()*numpy.matrix(simpleobs).transpose()).transpose()
        return self.meanobs+((self.IM*numpy.asmatrix(simpleobs).transpose()).transpose())
        #return self.M*simpleobs.transpose()

