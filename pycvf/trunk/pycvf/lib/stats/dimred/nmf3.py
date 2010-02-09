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
import sys
import numpy
import scipy
from numpy import *
from scipy import *
import random



class TexDoc:
    """
    NMF(Non Negative Matrix Factorization) is a method
    that a aim at matrix at factorizing a positive coefficient matrix $\\mathbf{X}$, 
    into two matrices  the factors W and H must be non-negative., \\mathbf{W} and \\mathbf{H}.
    The matrix $W$ contain the "mixing".
    The matrix $H$ contain the "source".  
    """
    def __init__(self,a):
        pass
    
    def History(self):
        """
        Int their initial paper, Lee & Seung proposed NMF mainly for parts-based decomposition of images. 
        They compared NMF to vector quantization and principal component analysis.
        They showed that although the three techniques may be written as factorizations, they implement different constraints and therefore produce different results.
        """
    def Algorithm(self):
        """
        There are several ways in which the W and H may be found: 
        Original Lee and Seung's updates that are usually referred as the multiplicative update method.
        Other methods have been suggested :
        \begin{itemize}
         \item gradient descent algorithms ;
         \item alternating non-negative least squares; 
         \item projected gradient.
        """
    def BibTex(self):
        """
        Daniel D. Lee and H. Sebastian Seung (2001). 
        "Algorithms for Non-negative Matrix Factorization". 
        Advances in Neural Information Processing Systems 
        13: Proceedings of the 2000 Conference: 556–562, MIT Press.
        """
        
# NMFLAB for Signal Processing written by A. Cichocki and R. Zdunek
# in cooperation with other members of Laboratory for Advanced Brain Signal
# Processing, BSI, RIKEN, Saitama, JAPAN


#
# The toolbox use to keep track of convergence upon many criterion 
# here are the criterion
#


def dist_Fro(Y,Z):
  return numpy.linalg.norm(Y - Z,'fro')

def dist_KL(Y,Z):
  return (Y*log(Y/Z + eps) - Y + Z).sum()

def dist_KL2(Y,Z):
  return (Z*log(Z/Y + eps) + Y - Z).sum()

def dist_Pearson(Y,Z):
   return ( ((Y - Z)**2)/Z ).sum()

def dist_Hellinger(Y,Z):
   return ( (sqrt(Z) - sqrt(Y))**2 ).sum()

def  dist_JS_rel(Y,Z):
   return (2*Y*log(2*Y/(Y + Z) + eps) + Z - Y).sum()

def  dist_JS_rel2(Y,Z):
   return (2*Z*log(2*Z/(Y + Z) + eps) - Z + Y).sum()

def  dist_JS(Y,Z):
   Zy = Y + Z
   return (Y*log(2*Y/Zy + eps) + Z*log(2*Z/Zy + eps) ).sum()

def  dist_AG(Y,Z):
      return (Zy*log(.5*Zy/Y + eps) + Y - Z).sum()

def  dist_AG2(Y,Z):
      return (.5*Zy*log(.5*Zy/sqrt(Y*Z) + eps)).sum()

def  dist_J(Y,Z):
      return ( .5*(Y - Z)*log(Y/Z + eps) ).sum()

def  dist_Chi(Y,Z):
      return ( ((Y + Z)*(Y - Z)**2)/(Y*Z) ).sum()

def  dist_Tria(Y,Z):
      return ( ((Y - Z)**2)/(Y + Z) ).sum()


alldists=[dist_Fro,dist_KL,dist_KL2,dist_Pearson,dist_Hellinger,dist_JS_rel,dist_JS_rel2,dist_JS,dist_AG,dist_AG2,dist_J,dist_Chi,dist_Tria]
eps=1e-48

class DistanceObserver():
    def __init__(self,select_dist=None ):
      self.res=[]
      if selected_dist==None:
         selected_dist=alldists
      self.selected_dist=selected_dist
    def observe(self,Y,A,X):
            Z = A*X + eps
            Z = diag(1./sqrt(var(Z.T)))*Z
            Y = Y + eps
            res.append(map(lambda d:d(Y,Z),self.selected_dist))
                    
                    
def rand(*args):
  return numpy.random.random(args)

def repmat(M,x,y):
  return M.repeat(x,axis=0).repeat(y,axis=1)
                      

def univar(A):
    return dot(A,diag(asarray(sum(A,axis=0)).squeeze()**-1))

class EMML():
  """  EMML (Kullback-Leibler (EMML))"""
    #       > alphaSa:       parameter of non-linear projection in computation
    #                        of the mixing matrix,
    #       > alphaSx:       parameter of non-linear projection in computation
    #                        of the sources,
  def __init__(self,alphaSa=0,alphaSx=0):
    self.alphaSx=alphaSx
    self.alphaSa=alphaSa
   #(X.*(A'*(Y./(A*X + eps)))).^(1 + alphaSx);
  def update_X(self,Y,A,X):
    return (X*(dot(A.T,(Y/(dot(A,X) + eps)))))**(1 + self.alphaSx)

  def update_A(self,Y,A,X):                    
     A = (A*(dot((Y/(dot(A,X) + eps)),X.T))/asarray(repmat(asmatrix(sum(X,axis=1)),Y.shape[0],1)))**(1 + self.alphaSa)
     return univar(A)
 
  def iter_step(self,k):
        pass  


class ISRA():
  """ ISRA (Frobenius) """
  def __init__(self,regularization_f=1,alphaA=.00001,alphaX=0.00001):
    self.reg_f=regularization_f
    self.alphaX=alphaX
    self.alphaA=alphaA
    self.delta=.1
  def update_X(self,Y,A,X):
    if (self.reg_f==1):
                        psi = 1
    elif (self.reg_f==2):                        
                        # L2 norm
                        psi = X
    elif (self.reg_f==2):                        
                        # Gibbs smoothing 
                        Xp1 = [X[:,-1], X[:,:-2]]
                        Xm1 = [X[:,2:], X[:,1]]
                        psi = tanh((X - Xp1)/self.delta) + tanh((X - Xm1)/self.delta)
                        #Xp2 = [X[:,T-1:T] X[:,1:T-2]];   Xp3 = [X[:,T-2:T] X[:,1:T-3]];  Xp4 = [X[:,T-3:T] X[:,1:T-4]]
                        #Xm2 = [X[:,3:T] X[:,1:2]]; Xm3 = [X[:,4:T] X[:,1:3]];    Xm4 = [X[:,5:T] X[:,1:4]]
                                            
    Yx = numpy.dot(A.T,Y) - self.alphaX*psi
    Yx[Yx <= 0] = 100*eps
    X = X*(Yx/(dot(dot(A.T,A),X) + eps))
    return X
  def update_A(self,Y,A,X):    
     Ya = numpy.dot(X,Y.T) - self.alphaA
     Ya[Ya <= 0] = 100*eps
     A = A*(Ya/(dot(A,dot(X,X.T)).T + eps)).T
     return univar(A)
                
  def iter_step(self,k):
        pass  


    
    #       > alphaA:        regularization parameter for computation of
    #                        the mixing matrix,
    #       > alphaX:        regularization parameter for computation of the sources,
    
                   
class KOMPASS:
   """  Kompass algorithm""" 
   #       > alpha:         parameter "alpha" in the Kompass algorithm,
   def __init__(self,alpha=0.1,eps=1e-9):
      self.eps=eps
      self.alpha=alpha
      
   def iter_step(self,k):
        pass  
      
   def update_X(self,Y,A,X):
      Yx = dot(A,X) + self.eps
      X = X*dot(A.T,(Y*Yx**(self.alpha - 1) ))/(dot(A.T,(Yx**self.alpha)))
      return X
                        
   def update_A(self,Y,A,X):
      Ap = A
      Yx = dot(A,X) + self.eps
      A = A*dot((Y*Yx**(self.alpha - 1)),X.T)/dot((Yx**self.alpha),X.T)
      return univar(A) 

                        
class RALS:
    """  Regularized ALS"""
    def __init__(self,eps=1e-18,big=1e6):
      self.eps=eps
      self.alpha_reg=20.
      self.big=big
    def iter_step(self,k):
      self.alpha_reg = 20*exp(-k/10)
    def update_X(self,Y,A,X):
       X= dot(linalg.pinv(dot(A.T,A) +  self.alpha_reg),dot(A.T,Y))
       X=X.clip(self.eps, self.big)
       return X
    def update_A(self,Y,A,X):               
      Ap = A
      A = dot(Y,dot(X.T,linalg.pinv(dot(X,X.T) + self.alpha_reg)))
      A=A.clip(self.eps, self.big)
      return univar(A)




class FixedXA:
   """ Fixed X/A """
   def __init__(self,true_source_matrix=None,true_mixing_matrix=None ):
     self.true_mixing_matrix=true_mixing_matrix
     self.true_source_matrix=true_source_matrix
   def update_X(self,Y,A,X):                  
     X = self.true_source_matrix + self.eps
     return X
     #nIter_selected = 1000;     # maximum number of Iterations for the selected sample (can be adjusted)
   def update_A(self,Y,A,X):                  
     A = self.true_mixing_matrix + eps
     return univar(A)
     #nIter_selected = 1000;     # maximum number of Iterations for the selected sample (can be adjusted)
   def iter_step(self,k):
        pass  



class ASYM_ALPHAD:
   """ Asymmetric alpha-divergence """
   def __init__(self):
       self.alpha=0.1
       self.omegaX=1
       self.omegaY=1
   def iter_step(self,k):
        pass     
   def update_X(self,Y,A,X):
            gamma_m = sum(A,axis=0)
            Z = dot(A,X) + eps
            Q = (1/self.alpha)*((Y/Z)**self.alpha - 1)
            return (X*exp(dot(diag(self.omegaX/gamma_m),(dot(A.T,Q)))))**(1 + self.alphaS)     
   def update_A(self,Y,A,X):
            Ap = A;        
            gamma_T = (sum(X,axis=1)).T
            Z = A*X + eps;
            Q = (1/self.alpha)*((Y/Z)**self.alpha - 1)
            A = A*exp(dot(Q,dot(X.T,diag(self.omegaA/gamma_T))))
            return univar(A) 


class EG_BASE(object):
   """ EG_DKL """
   def __init__(self,omegaX=1., omegaA=1.,alphaS=0):
       self.omegaX=omegaX
       self.omegaA=omegaA
       self.alphaS=alphaS
   def computeQ(self,Y,A,X):
       assert(False)                
   def update_X(self,Y,A,X):  
            gamma_m = sum(A,axis=0)
            Z = dot(A,X) + eps
            Q = self.computeQ(Y,A,X,Z)
            dom=diag(self.omegaX*asarray(gamma_m.squeeze()**-1))
            return (X*exp(dot(dom,dot(A.T,Q))))**(1 + self.alphaS) 
   def update_A(self,Y,A,X):  
            Ap = A        
            gamma_T = (sum(X,axis=1)).T
            Z = dot(A,X) + eps
            Q = self.computeQ(Y,A,X,Z)
            dam=diag(self.omegaA*asarray(gamma_T.squeeze()**-1))
            A = A*exp(dot(Q, dot(X.T,dam)))
            return univar(A) 
                     

class EG_DKL(EG_BASE):
   """ EG_DKL """                      
   def computeQ(self,Y,A,X,Z):
      return log(Y/Z + eps)
                  

class EG_RAG(EG_BASE):
   """ EG_RAG """                      
   def computeQ(self,Y,A,X,Z):
      return log(2*Y/(Z + Y) + eps);
                  
      
class EG_SAG(EG_BASE):
   """ EG_SAG """                      
   def computeQ(self,Y,A,X,Z):
      return log(2*sqrt(Y*Z)/(Z + Y) + eps) + (Y - Z)/Z ;


class EG_DJ(EG_BASE):
   """ EG_DJ """                      
   def computeQ(self,Y,A,X,Z):
      return .5*log(Y/Z + eps) + .5*(Y - Z)/Z ;
        
class EG_RJS(EG_BASE):
   """ EG_RJS """                      
   def computeQ(self,Y,A,X,Z):
      return (Y - Z)/(Y + Z) ;
        

class EG_DRJS(EG_BASE):
   """ EG_DRJS """                      
   def computeQ(self,Y,A,X,Z):
      return 2*log(.5*(Y + Z)/Z) + (Z - Y)/(Y + Z);
            
class EG_SJS(EG_BASE):
   """ EG_RJS """                      
   def computeQ(self,Y,A,X,Z):
      return log(.5*(Y + Z)/Z + eps) 
        
                    
class EG_TRI(EG_BASE):
   """ EG_TRI """                      
   def computeQ(self,Y,A,X,Z):
      return (2*Y/(Y + Z))**2 - 1 
        
class EG_BE(EG_BASE):
   """ EG_BE """                      
   def __init__(self,alpha_BE=1,*args, **xargs):
       EG_BASE.__init__(self, *args, **xargs)
       self.alpha_BE=alpha_BE
   def computeQ(self,Y,A,X,Z):
      return self.alpha_BE*log((Y + self.alpha_BE*Z)/((1 + self.alpha_BE)*Z) + eps)
        
class PINV:         
    def __init__(self,*args , ** kwargs):
        pass
    def iter_step(self,k):
      pass
    def update_X(self,Y,A,X):
      return dot(linalg.pinv(A),Y)             
    def update_A(self,Y,A,X):     
       A = dot(Y,linalg.pinv(X.T).T)  
       return univar(A)         

    
class AlternateAlgorithm():
    def __init__(self,listalgos):
        self.algos=listalgos
    def update_X(self, *args):
        return random.choice(self.algos).update_X(*args)
    def update_A(self, *args):
        return random.choice(self.algos).update_A(*args)

class Initializer1():
    def __init__(self, Y,r,*args, **kwargs):
        m,T=Y.shape
        self.m=m
        self.r=r
        self.T=T
        self.m_sx = numpy.matrix([x for x in range(m)])
        self.r_sx = numpy.matrix([x for x in range(r)])
        self.T_sx = numpy.matrix([x for x in range(T)])
    def get_initA(self, * args, **kwargs):
            Ainit= abs(repmat(.1*sin(2*pi*.1*self.m_sx.T),1,self.r) 
                                   + repmat(.1*cos(2*pi*.1*self.r_sx),self.m,1) + repmat(cos(2*pi*.471*self.m_sx.T),1,self.r) + repmat(sin(2*pi*.471*self.r_sx),self.m,1))
            return Ainit/Ainit.max()
    def get_initX(self, *args, **kwargs):
            Xinit= abs(repmat(.1*sin(2*pi*.1*self.r_sx.T),1,self.T) + repmat(.1*cos(2*pi*.1*self.T_sx),self.r,1) + repmat(cos(2*pi*.471*self.r_sx.T),1,self.T) + repmat(sin(2*pi*.471*self.T_sx),self.r,1))
            return Xinit/Xinit.max()
            

class Initializer0():
    def __init__(self, Y ,r,*args, **kwargs):
        m,T=Y.shape
        self.m=m
        self.r=r
        self.T=T
    def get_initA(self, * args, **kwargs):
        return rand(self.m,self.r)
            
    def get_initX(self, *args, **kwargs):
        return rand(self.r,self.T)


class InitializerPinv():
    def __init__(self, Y ,r,*args, **kwargs):
        m,T=Y.shape
        self.Y=Y
        self.PA= rand(m,r)
        self.PX= rand(r,T)
        
    def get_initA(self, * args, **kwargs):
        A = dot(self.Y,linalg.pinv(self.PX.T).T)  
        return univar(A)         
            
    def get_initX(self, *args, **kwargs):
        return dot(linalg.pinv(self.PA),self.Y)
            
            
class InitializerD():
    def __init__(self,*args, **kwargs):
        self.i0=Initializer0(*args, ** kwargs)
        self.i1=Initializer1(*args, ** kwargs)
        self.i2=InitializerPinv(*args, ** kwargs)
    def get_initA(self,k):
        if ( k==0 ): return self.i1.get_initA()
        elif ( k==1 ): return self.i2.get_initA()
        else: return self.i0.get_initA()
        
    def get_initX(self,k):
        if ( k ==0 ): return self.i1.get_initX()
        elif ( k ==1 ): return self.i2.get_initX()
        else: return self.i0.get_initX()


##,Index_norm, true_mixing_matrix, true_source_matrix, montecarlo_on, alterning_steps,restart_montecarlo_on,AL,Y_true,type_alg_A, type_alg_X, max_restart, regularization_f,no_Iter,alphaSa,alphaSx,alphaA,alphaX,alpha
def nmf(Y,nbdimsrc, algox=None, algoa=None, observer=None, Initializer=InitializerD, distance=dist_KL,nbiter = 500, nbiter_preview = 30 ,nbiterperstep=5 ,nbcandidates=10, epsil_normA = 1e-44,AL=1,convergence_criterion_reached=lambda x:False,  ** kwargs  ):
    """
    # nbiter_preview
    #nbiter maximum number of Iterations for the selected sample (can be adjusted)
    #
    # Non-negative Matrix Factorization (NMF) based on the basic Lee-Seung algorithms
    #
    # [A,X]=nmf_Lee_Seung(...)
    #       produces mixing matrix A of dimension [m by nbdimsrc],
    #       and source matrix X of dimension [nbdimsrc by T], for the linear mixing model: AX = Y,
    #       where Y is an observation matrix [m by T].
    # Note: > m: number of sensors,
    #       > nbdimsrc: number of sources,
    #       > T: number of samples,
    #
    # INPUTS:
    #       > AL:            mixing matrix estimaed from the preceeding layer,
    #       > Y_true:        the first layer mixed signals (mixtures),
    #       > max_restart:   number of restarts,
    #       > no_Iter:       number of inner Iterations,
    # nbiter = 500     # maximum number of Iterations for the selected sample (can be adjusted)
    # nbiter_preview = 30 # maximum number of Iterations for each random sample
    # epsil_normA = 1e-44 # tolerance for alternating
    #
    # OUTPUTS:
    #       > A:               estimated mixing matrix,
    #       > X:               estimated source matrix,
    #
    # #########################################################################
    """
       
    if (algox==None):
        algox=EMML()
        
    if (algoa==None):
        algoa=EMML()
    # test for negative values in Y
    if (Y.min() < 0):
        sys.stderr.write('Some matrix entries are changed from negative to small positive')
        Y[Y< 0] = eps
       
    Y_true=Y
       
    if (min(sum(Y,axis=1)) == 0):
        raise Exception,'All rows must contain at least one non null element'
        
    initializer=Initializer(Y,nbdimsrc)

    d_outer_temp = scipy.Infinity
    nr_best = -1
    
    # candiate selection
    for candidateno in range(nbcandidates):
        A=asarray(initializer.get_initA(candidateno))
        A = dot(A,diag(asarray(sum(A,axis=0)).squeeze()**-1))        # Normalization of initial guess
        X=asarray(initializer.get_initX(candidateno))

        Z = asarray(AL*asmatrix(dot(A,X)))
        d_outer_p = distance(Y_true,Z)

        
        for k in range(nbiter_preview):
            alpha_reg = 20*exp(-k/10)
            epsil = 0
            # generalized divergence-reducing NMF Iterations (main algorithm)
            for t in range(1,nbiterperstep):
                X=algox.update_X(Y,A,X)
                A=algoa.update_A(Y,A,X)
        Z = asarray(AL*asmatrix(dot(A,X)))
        d_outer = distance(Y_true,Z)

        if ((d_outer-d_outer_p)>0.00001):
           sys.stderr.write('Warning process is not converging :  (%f -> %f)\n'%( d_outer_p,d_outer ))

        
        if ((candidateno == 0) or (d_outer < d_outer_temp)):
            A_best = A.copy()
            X_best = X.copy()
            d_outer_temp = d_outer; 
            nr_best = candidateno
               
                      
        sys.stderr.write('Candidate %d, distance = %e\n'%(candidateno, d_outer))
           
   
    # main loop
    A = A_best
    X = X_best 
    d_outer_p=scipy.Infinity      
    for k in range(nbiter):
       for t in range(1,nbiterperstep):
                X=algox.update_X(Y,A,X)
                A=algoa.update_A(Y,A,X)

       if observer:
                observer(Y,A,X,k)
                        
       Z = asarray(AL*asmatrix(dot(A,X)))
       d_outer = distance(Y_true,Z)
       if (convergence_criterion_reached(d_outer)):
           break
       if ((d_outer-d_outer_p)>0.00001):
           sys.stderr.write('Warning process is not converging :  (%f -> %f)\n'%( d_outer_p,d_outer ))
       d_outer_p=d_outer
                   
    sys.stderr.write('Final distance = %e\n'%( d_outer))
    # One-Variance scaling
    X[X <= 0] = eps
    return (A,X, d_outer)
    

#abs(numpy.array([ nmf3.nmf(numpy.random.random((10,10)),4,algox=nmf3.EG_DJ(), algoa=nmf3.EG_DKL(),nbiter=100,nbiter_preview=8)[2] for x in range(20) ])).mean()
#abs(numpy.array([ nmf3.nmf(numpy.random.random((10,10)),4,algox=nmf3.AlternateAlgorithms([nmf3.EG_DJ(), nmf3.EG_DKL()]), algoa=nmf3.AlternateAlgorithms([ nmf3.EG_DKL(),nmf3.EMML()]) ,nbiter=100,nbiter_preview=8)[2] for x in range(20) ])).mean()


class NMFdimred():
    def __init__(self,M,k, *args, ** kwargs):
        self.res=nmf(asarray(M),k, *args, ** kwargs)
        self.M=linalg.pinv(self.res[1])  #self.res[1].T
#        self.IM=numpy.matrix(numpy.linalg.pinv(self.M))
        self.IM=self.res[1]
    def dimred(self,observations):
        return dot(observations,self.M)
    def dimaug(self,simpleobs):
        return dot(simpleobs,self.IM)
    def save(self,file):
        import cPickle as pickle
        pickle.dump(f,self.M)
        pickle.dump(f,self.IM)
    def load(self,file):
        import cPickle as pickle
        self.M=pickle.load(f)
        self.IM=pickle.load(f)
    