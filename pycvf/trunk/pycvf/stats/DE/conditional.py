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
import traceback
import numpy
import scipy
import random
import cPickle as pickle
import marshal
  
class RawFiniteStateConditionalModel(object):
    """ conditional model to be used within equation based model such as Bayesian model
        This models supports : 
        * independant sampling upon context
        * this model actually implements different models for each state declared state
        prior= lettres
        evidence=context
    --------------------------------------------------------------------------------------------------------------------------
    PRIOR= ARC/EXT sans le CONTEXT
    EVIDENCE=CONTEXT
    """
    def __init__(self,     project_prior, project_evidence,individual_model_factory, individual_model_class, states=None, from_file=False):
      self.project_prior=project_prior
      self.project_evidence=project_evidence
      self.states=states
      self.no=0
      self.individual_model_factory=individual_model_factory
      self.individual_model_class=individual_model_class
      #if (states!=None):
      self.statedist=numpy.zeros((len(states),))
      self.individual_models=[ individual_model_factory(state) for state in states ]
      #else:
      #  assert(from_file==True)

    def dump(self,f):
        pickle.dump(self.states,f)
        pickle.dump(self.no,f)
        pickle.dump(self.statedist,f)
        try:
          for m in self.individual_models:
               m.dump(f)
        except:
          raise Exception, "error while dumping submodel of  RawFiniteStateConditionalModel" 
    @staticmethod
    def load(f,project_prior, project_evidence,individual_model_factory,individual_model_class,BaseClass=None,nosubload=False, *args, **kwargs):
       if (BaseClass==None):
           BaseClass=RawFiniteStateConditionalModel
       x=BaseClass(
                   project_prior=project_prior, 
                   project_evidence=project_evidence,
                   individual_model_factory=individual_model_factory,
                   individual_model_class=individual_model_class, 
                   states=None, 
                   from_file=(not nosubload),
                   **kwargs
                  )
       print "BaseClass="+str(BaseClass)
       x.states=pickle.load(f)
       x.no=pickle.load(f)
       x.statedist=pickle.load(f)
       if (not nosubload): 
          x.individual_models=[ x.individual_model_class(i).load(f) for i in range(len(x.states))]
       return x
    def test_no_log(self,AandB):
        assert(0)
    def test_log(self,AandB):
        assert(0)
    def test(self,AndB,log=True):
        if (log):
            return self.test_log(AandB)
        else:
            return self.test_no_log(AandB)
    def test_separated(self,A,B,log=True):
      res=[]
      assert(A.shape[0]==B.shape[0])
      for dt0 in range(B.shape[0]) :
         pre=A[dt0]
         ext=B[dt0]
         t=self.test_with_state(pre, ext,log)[0][0] 
         res.append(t)
      return  numpy.vstack([res])
    def train(self,AandBpos,online=True):
        if (AandBpos==None):
           return None
        #print AandBpos
        A=numpy.vstack(map(self.project_prior,AandBpos))
        BL=map(self.project_evidence,AandBpos)
        B=numpy.vstack(BL)
        #print B
        SB=BL[:]
        SB.sort()
        SB=scipy.unique(SB)
        #print SB
        #self.statedist=numpy.zeros((len(self.states),))
        if (online):
          for state in SB:
             C=zip( map(lambda x:(x==state).all(),B), A )
             #tdata=numpy.vstack( reduce( lambda b,x:(x[0]) and (b+[x[1]]) or b , C,[]) )
             tdata=numpy.array( reduce( lambda b,x:(x[0]) and (b+[x[1]]) or b , C,[]) )
             #print state,self.xstates,self.statedist,self.states
             self.statedist[state]+=float(tdata.shape[0])/A.shape[0]
             self.individual_models[state].train(tdata,online=True)
        else:
          for state in SB:
             C=zip( map(lambda x:(x==state).all(),B), A )
             #tdata=numpy.vstack( reduce( lambda b,x:(x[0]) and (b+[x[1]]) or b , C,[]) )
             tdata=numpy.array( reduce( lambda b,x:(x[0]) and (b+[x[1]]) or b , C,[]) )
             self.statedist[state]=float(tdata.shape[0])/Apos.shape[0]
             self.individual_models[state].train(tdata,online=False)
    def train_separated(self,Apos,Bpos, Aneg=None, Bneg=None,online=True):
        if ((Apos==None) or (Bpos ==None)):
           return None
        assert(not(Aneg))
        assert(not(Bneg))
        assert(Apos.shape[0]==Bpos.shape[0])
        A=Apos
        BL=[x for x in Bpos ]
        B=numpy.vstack(BL)
        #print B
        SB=BL[:]
        SB.sort()
        SB=scipy.unique(SB)
        print "SB",SB
        print "APos",A
        self.statedist=numpy.zeros((len(self.states),))
        if (online):
          for state in SB:
             C=zip( map(lambda x:(x==state).all(),B), A )
             #tdata=numpy.vstack( reduce( lambda b,x:(x[0]) and (b+[x[1]]) or b , C,[]) )
             tdata=numpy.array( reduce( lambda b,x:(x[0]) and (b+[x[1]]) or b , C,[]) )
             self.statedist[state]+=float(tdata.shape[0])/Apos.shape[0]
             self.individual_models[state].train(tdata,online=True)
        else:
          for state in SB:
             C=zip( map(lambda x:(x==state).all(),B), A )
             #tdata=numpy.vstack( reduce( lambda b,x:(x[0]) and (b+[x[1]]) or b , C,[]) )
             tdata=numpy.array( reduce( lambda b,x:(x[0]) and (b+[x[1]]) or b , C,[]) )
             self.statedist[state]=float(tdata.shape[0])/Apos.shape[0]
             self.individual_models[state].train(tdata,online=False)


    def test(self,AandB, *args, ** kwargs):
        if (AandBpos==None):
           return None
        A=self.project_prior(AandB)
        BL=self.project_evidence(AandB)
        #B=numpy.vstack(BL)
        SB=BL[:]
        SB.sort()
        SB=scipy.unique(SB)
        RSC=numpy.zeros((AandB.shape[0],))
        for state in SB:
            #tdata=numpy.array(reduce(lambda b,x:((x[1]==state).all()) and (b+[x[0]]) or b, (A,B),[]))
            linesel=numpy.array(map(lambda x:(x==state).all(),B))
            C=zip( linesel, A )
            tdata=numpy.vstack( reduce( lambda b,x:(x[0]) and (b+[x[1]]) or b , C,[]) )
            #print state,tdata
            RS=self.individual_models[state].test(tdata,*args, ** kwargs)
            RSC.put( linesel.nonzero(), RS)
        return RSC



    def test_with_state(self,state,A, *args, ** kwargs):
        #A=numpy.vstack(map(self.project_prior,AandB))
        if (type(state)==int):
          RS=self.individual_models[state].test(A,*args, ** kwargs)
          #print RS
          return RS
        elif (type(state)==numpy.ndarray):       
          #print state[0]   
          SB=state[:]
          SB.sort()
          SB=scipy.unique(SB)
          RSC=numpy.zeros((A.shape[0],))
          for cstate in SB:
            #tdata=numpy.array(reduce(lambda b,x:((x[1]==state).all()) and (b+[x[0]]) or b, (A,B),[]))
            linesel=numpy.array(map(lambda x:(x==cstate).all(),state))
            C=zip( linesel, A )
            tdata=numpy.vstack( reduce( lambda b,x:(x[0]) and (b+[x[1]]) or b , C,[]) )
            #print state,tdata
            RS=self.individual_models[cstate].test(tdata,*args, ** kwargs)
            RSC.put( linesel.nonzero(), RS)

          #RS=numpy.array([self.individual_models[state[si]].test(A[si:(si+1)],*args, ** kwargs) for si in range(state.shape[0])])
          #print RS
          return RSC
        else:
          assert(False)
    def sample(self,n=100, withstate=None, *args, ** kwargs):
        if (withstate ==None):
            import random
            p=random.random()
            withstate=((self.statedist.cumsum()-p)>=0).astype(int).sum()
        return self.individual_models[withstate].sample(n,*args,**kwargs)
    def isample(self,n=100, withstate=None, *args, ** kwargs):
        if (withstate ==None):
            import random
            p=random.random()
            withstate=((self.statedist.cumsum()-p)>=0).astype(int).sum()
        return self.individual_models[withstate].sample(n,*args,**kwargs)
    def random_improve(self,value,withstate=None,amount=0.5, prec=1):
        ###
        ### TODO : Since we have a projection only the really updated part should be upgraded
        ###
        if (not withstate):
          assert(False)
        return self.individual_models[withstate].random_improve(value,amount,prec)
    def memory_cost(self, *args, **kwargs):
        assert(False)
    def cpu_cost(self, *args, **kwargs):
        assert(False)
    
def test_rscm():
     import random
     _len=1
     #m=RawFiniteStateConditionalModel(lambda x:x[1:(1+_len)] ,lambda x:x[0],lambda x: EmModel(_len,2),  range(4) )
     m=RawFiniteStateConditionalModel(lambda x:x[1:(1+_len)] ,lambda x:x[0],lambda x: ParzenModel(_len,1),  range(4) )
     seq=[0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,3,3,2,2,2,1,2,2,2,3,3,1,1,0,0]
     strain=numpy.array([ [x for x in seq[i:(i+_len+1)] ] for i in (range(len(seq)-_len)) ])
     #print strain
     m.train(strain)
     #print m.test(strain)
     print m.test(strain).mean()
     random.shuffle(strain)
     #print m.test(strain)
     print m.test(strain).mean()
     strain=numpy.zeros(strain.shape).astype(int)
     #print m.test(strain)
     print m.test(strain).mean()
     return m

     #print m.sample(5)






class FiniteStateConditionalModel(RawFiniteStateConditionalModel):
  def __init__(self, project_prior, project_evidence,individual_model_factory, individual_model_class, states, check_new=False, *args, ** kwargs):
    self.xstates=states
    self.check_new=check_new
    RawFiniteStateConditionalModel.__init__(self,project_prior, project_evidence,individual_model_factory, individual_model_class ,  range(len(self.xstates)) , *args, **kwargs)
    def wrapped_project_evidence(AandB):
        #print "Wr"
        pe=project_evidence(AandB)
        if (check_new):
          l=list(set(filter(lambda x: x not in self.xstates, pe)))
          #print l
          if (len(l)):
            self.add_states(l)
        return self.xstates.index(pe)
       #return numpy.vstack(map(lambda x:self.xstates.index(x),project_evidence(AandB)))
    self.project_evidence=wrapped_project_evidence
  def add_states(self,states):
      print "new states :", states
      #self.xstates.extend(states)
      self.statedist.resize((len(self.states)+len(states),))
      newmodels=[]
      for state in states:
        newmodels.append(self.individual_model_factory(state))
        self.xstates.append(state)
        self.states.append(len(self.states))
      #print "newstates", self.states
      self.individual_models.extend(newmodels)
      assert(len(self.states)==len(self.xstates))
      #self.states.extend(range(,(len(self.states)+len(newmodels))))
  @staticmethod
  def load(f,project_prior, project_evidence,individual_model_factory,individual_model_class,BaseClass=None, *args, **kwargs):
      if (BaseClass==None):
           BaseClass=FiniteStateConditionalModel
      xstates=pickle.load(f)
      x=RawFiniteStateConditionalModel.load(f,project_prior, project_evidence,individual_model_factory,individual_model_class,BaseClass, *args, **kwargs)
      x.xstates=xstates
      return x  
  def dump(self,f):
      pickle.dump(self.xstates,f)
      RawFiniteStateConditionalModel.dump(self,f)
  def train_separated(self,Apos,Bpos, Aneg=None, Bneg=None,online=True, check_new=None):
     #print "Ts"
     if (check_new==None):
         check_new=self.check_new
     if (check_new):
         l=list(set(filter(lambda x: x not in self.xstates, Bpos)))
         if (len(l)):
           self.add_states(l)
     if  (type(Bneg)!=type(None)):
       Bneg= numpy.array(map(self.xstates.index,Bneg)) 
       if (check_new):
         l=list(set(filter(lambda x: x not in self.xstates, Bpos)))
         if (len(l)):
           self.add_states(l)
     return RawFiniteStateConditionalModel.train_separated(self,Apos,numpy.array(map(self.xstates.index,Bpos)), Aneg, Bneg,online)
  def test_separated(self,A,B,*args,**kwargs):
     return RawFiniteStateConditionalModel.test_separated(self,A,numpy.array(map(self.xstates.index,B)),*args, ** kwargs)


class FiniteStateConditionalModelF(RawFiniteStateConditionalModel):
  def __init__(self, project_prior, project_evidence,individual_model_factory, individual_model_class, states, *args, **kwargs):
    self.xstates=states
    RawFiniteStateConditionalModel.__init__(self,project_prior, project_evidence,individual_model_factory, individual_model_class, (states!=None) and range(len(self.xstates)) or None, *args, **kwargs)
    def wrapped_project_evidence(AandB):
       return self.xstates.index(project_evidence(AandB))
    def wrapped_project_prior(AandB):
       return map(self.xstates.index , project_prior(AandB))

       #return numpy.vstack(map(lambda x:self.xstates.index(x),project_evidence(AandB)))
    self.project_evidence=wrapped_project_evidence
    self.project_prior=wrapped_project_prior
  @staticmethod
  def load(f,project_prior, project_evidence,individual_model_factory,individual_model_class,BaseClass=None, *args, **kwargs):
      if (BaseClass==None):
           BaseClass=FiniteStateConditionalModelF
      xstates=pickle.load(f)
      x=RawFiniteStateConditionalModel.load(f,project_prior, project_evidence,individual_model_factory,individual_model_class,BaseClass, *args, **kwargs)
      x.xstates=xstates
      return x
  def dump(self,f):
      pickle.dump(self.xstates,f)
      RawFiniteStateConditionalModel.dump(self,f)
  def train_separated(self,Apos,Bpos, Aneg=None, Bneg=None,online=True):
     if  (type(Aneg)!=type(None)):
       Aneg= numpy.array(map(self.xstates.index,Aneg)) 
     if  (type(Bneg)!=type(None)):
       Bneg= numpy.array(map(self.xstates.index,Bneg)) 
     print Apos
     print Bpos
     print self.xstates
     return RawFiniteStateConditionalModel.train_separated(self, numpy.array(map(self.xstates.index,Apos)) ,numpy.array(map(self.xstates.index,Bpos)) , Aneg,Bneg,online)
  def test_separated(self,A,B,*args,**kwargs):
     return RawFiniteStateConditionalModel.test_separated(self,numpy.array(map(self.xstates.index,A)) ,numpy.array(map(self.xstates.index,B)) ,*args, ** kwargs)


def test_fscm():
     import random
     _len=1
     #m=FiniteStateConditionalModelF(lambda x:x[1:(1+_len)] ,lambda x:x[0],lambda x: EmModel(_len,2),  "abcdef" )
     m=FiniteStateConditionalModelF(lambda x:x[1:(1+_len)] ,lambda x:x[0],lambda x: ParzenModel(1,1),  "abcdef" )
     seq="abababcababccdecdecdecdefabcabcdefabababcdefa"
     strain=numpy.array([ [x for x in seq[i:(i+_len+1)] ] for i in (range(len(seq)-_len)) ])
     #print strain
     m.train(strain)
     print m.test(strain)
     print m.test(strain).mean()
     seq=[x for x in seq]
     random.shuffle(seq)
     strain=numpy.array([ [x for x in seq[i:(i+_len+1)] ] for i in (range(len(seq)-_len)) ])
     print m.test(strain)
     print m.test(strain).mean()
     print m.test(strain).mean()
     return m



class InterpolatedStateConditionalModelSv(FiniteStateConditionalModel):
    def __init__(self, states, k, SearchStructure, project_prior, project_evidence, *args, ** xargs):
      #print states
      if (states!=None):
        #print states
        self.kstates=SearchStructure(states)
      self.k=k
      self.SearchStructure=SearchStructure
      self.real_project_prior=project_prior
      self.real_project_evidence=project_evidence
      FiniteStateConditionalModel.__init__(self,project_prior=project_prior,project_evidence=project_evidence,states=states,*args, **xargs)
    @staticmethod
    def load(f,project_prior, project_evidence,individual_model_factory,individual_model_class,BaseClass=None, *args, **kwargs):
      if (BaseClass==None):
           BaseClass=InterpolatedStateConditionalModelSv
      x=FiniteStateConditionalModel.load(f,project_prior, project_evidence,individual_model_factory,individual_model_class,BaseClass, *args, **kwargs)
      x.kstates=x.SearchStructure(x.xstates)
      return x
    def dump(self,f):
      FiniteStateConditionalModel.dump(self,f)
    def test(self,data):    
      """
         This is an interpolated test among based on nearest neighbor evaluation
      """
      res=[]
      for dt0 in range(data.shape[0]) :
         #print data[dt0].tolist()
         pre=self.real_project_evidence(data[dt0].tolist())
         #xpre=self.project_evidence(data[dt0].tolist())
         ext=self.real_project_prior(data[dt0].tolist())
         #print pre
         knns=self.kstates.query(numpy.array(pre).flat,self.k) ## TODO : the nearest points are not necessarily the most suitable for a this...
         knncoeffs=numpy.array([ (1./(1.+kd)) for kd in knns[0] ])
         knncoeffs/=knncoeffs.sum()
         xl=[]
         for i in range(len(knns[1])):
             t=FiniteStateConditionalModel.test_with_state(self,knns[1][i], ext )[0][0] *knncoeffs[i]
             xl.append(t)
         #print "a",xl,"b",self.test_with_state(knns[1][1], ext ),"t",t
         res.append(reduce(lambda x,y:x+y[0],xl,0) )
         #res.append(sum(xl))
      #print res
      return  numpy.vstack([res])
    def test_with_state(self,stat,tv,*args, **kwargs):
          #if (self.real_project_prior):
          #  stat=self.real_project_evidence([stat])[0]
          #if (self.real_project_prior):
          #  tv=self.real_project_prior(tv)
        print "stat,tv",stat.shape, tv.shape
        knns=self.kstates.query(numpy.array(stat),self.k)
        print knns[0]
        knncoeffs=numpy.array([ (1./(1.+kd)) for kd in knns[0] ])
        knncoeffss=knncoeffs.sum(axis=1).reshape(knns[0].shape[0],1).repeat(self.k,axis=1)
        print knncoeffss.shape
        knncoeffs/=knncoeffss
        #for j in range(knns[1].shape[0]):
        #  print "j",j, knns[1].shape[0], knns[1].shape[1],tv.shape
        #print knns[1]
        r=numpy.array([ FiniteStateConditionalModel.test_with_state(self,knns[1][:,kk], tv) for kk in range(self.k) ])
        print "RRR",r.shape
        r=r.reshape(self.k,knns[0].shape[0]).T
        r*=knncoeffs
        r=r.sum(axis=1)
        print r.shape
        #print "a",xl,"b",self.test_with_state(knns[1][1], ext ),"t",t        
        return numpy.array(r).reshape(tv.shape[0],1)
    def test_separated(self,tdatap, tdatae,log=True):    
      """
         This is an interpolated test among based on nearest neighbor evaluation
      """
      res=[]
      assert(tdatap.shape[0]==tdatae.shape[0])
      for dt0 in range(tdatap.shape[0]) :
         pre=tdatap[dt0]
         ext=tdatae[dt0]
         knns=self.kstates.query(numpy.array(pre).flat,self.k) ## TODO : the nearest points are not necessarily the most suitable for a this...
         knncoeffs=numpy.array([ (1./(1.+kd)) for kd in knns[0] ])
         knncoeffs/=knncoeffs.sum()
         xl=[]
         for i in range(len(knns[1])):
             knnpre=knns[1][i]
             predat=self.test_with_state(knnpre, ext, log )
             #print pre
             #print pre[0]
             #print pre[0][0]
             t=predat[0] *knncoeffs[i]
             xl.append(t)
         if (log):
           res.append(reduce(lambda x,y:x+y,xl,0) )
         else:
           res.append(reduce(lambda x,y:x*y,xl,0) )
      return  numpy.vstack([res])
    def train(self,data, *args, **kwargs):    
      """
        This is a randomized learner : 
            We assign each observation to some nearest neighbor according to some probability
      """
      import random
      resa=[]
      resb=[]
      #print data
      for dt0 in range(data.shape[0]):
         #print data[dt0].tolist()
         pre=self.real_project_evidence(data[dt0].tolist())
         #xpre=self.project_evidence(data[dt0].tolist())
         ext=self.real_project_prior(data[dt0].tolist())
         #print pre
         #print "pre",pre
         #print "ext",ext
         knns=self.kstates.query(numpy.array(pre).flat,self.k) ## TODO : the nearest points are not necessarily the most suitable for a this...
         #print knns[0],knns[1],len(knns[0]),len(knns[1])
         assert(len(knns[0])==len(knns[1]))
         knncoeffs=numpy.array([ (1./(1.+kd)) for kd in knns[0] ])
         knncoeffs/=knncoeffs.sum()
         knncoeffs=knncoeffs.cumsum()
         knncoeffs-=random.random()
         idx=(knncoeffs<=0).astype(int).sum()
         resb.append(knns[1][idx])
         resa.append(ext)
      #print  "resa",resa, "resb" resb
      #FiniteStateConditionalModel.train_separated(self,numpy.array(resa),numpy.array(resb))
      RawFiniteStateConditionalModel.train_separated(self,numpy.array(resa),numpy.array(resb))
    def train_separated(self,pA,pB, *args, **kwargs):    
      """
        This is a randomized learner : 
            We assign each observation to some nearest neighbor according to some probability
      """
      import random
      resa=[]
      resb=[]
      assert(pA.shape[0]==pB.shape[0])
      for dt0 in range(pB.shape[0]):
         pre=pA[dt0]
         ext=pB[dt0]
         #print pre
         #print ext
         #knns=self.kstates.query(numpy.array(pre).flat,self.k) ## TODO : the nearest points are not necessarily the most suitable for a this...
         knns=self.kstates.query(pre,self.k) ## TODO : the nearest points are not necessarily the most suitable for a this...
         #print self.kstates
         knncoeffs=numpy.array([ (1./(1.+kd)) for kd in knns[0] ])
         knncoeffs/=knncoeffs.sum()
         knncoeffs=knncoeffs.cumsum()
         knncoeffs-=random.random()
         idx=(knncoeffs<=0).astype(int).sum()
         assert(len(knns[0])==len(knns[1]))
         resb.append(knns[1][idx])
         resa.append(ext)
      RawFiniteStateConditionalModel.train_separated(self,numpy.array(resa),numpy.array(resb))


class InterpolatedStateConditionalModelSvF(FiniteStateConditionalModelF):
    def __init__(self, states, k, SearchStructure, project_prior, project_evidence, *args, ** xargs):
      #print states
      if (states!=None):
        #print states
        self.kstates=SearchStructure(states)
      self.k=k
      self.SearchStructure=SearchStructure
      self.real_project_prior=project_prior
      self.real_project_evidence=project_evidence
      FiniteStateConditionalModelF.__init__(self,project_prior=project_prior,project_evidence=project_evidence,states=states,*args, **xargs)
    @staticmethod
    def load(f,project_prior, project_evidence,individual_model_factory,individual_model_class,BaseClass=None, *args, **kwargs):
      if (BaseClass==None):
           BaseClass=InterpolatedStateConditionalModelSv
      x=FiniteStateConditionalModelF.load(f,project_prior, project_evidence,individual_model_factory,individual_model_class,BaseClass, *args, **kwargs)
      x.kstates=x.SearchStructure(x.xstates)
      return x
    def dump(self,f):
      FiniteStateConditionalModelF.dump(self,f)
    def test(self,data):    
      """
         This is an interpolated test among based on nearest neighbor evaluation
      """
      res=[]
      for dt0 in range(data.shape[0]) :
         #print data[dt0].tolist()
         pre=self.real_project_evidence(data[dt0].tolist())
         #xpre=self.project_evidence(data[dt0].tolist())
         ext=self.real_project_prior(data[dt0].tolist())
         #print pre
         knns=self.kstates.query(numpy.array(pre).flat,self.k) ## TODO : the nearest points are not necessarily the most suitable for a this...
         knncoeffs=numpy.array([ (1./(1.+kd)) for kd in knns[0] ])
         knncoeffs/=knncoeffs.sum()
         xl=[]
         for i in range(len(knns[1])):
             t=self.test_with_state(knns[1][i], ext )[0][0] *knncoeffs[i]
             xl.append(t)
         #print "a",xl,"b",self.test_with_state(knns[1][1], ext ),"t",t
         res.append(reduce(lambda x,y:x+y[0],xl,0) )
         #res.append(sum(xl))
      #print res
      return  numpy.vstack([res])
    def test_separated(self,tdatap, tdatae,log=True):    
      """
         This is an interpolated test among based on nearest neighbor evaluation
      """
      res=[]
      assert(tdatap.shape[0]==tdatae.shape[0])
      for dt0 in range(tdatap.shape[0]) :
         pre=tdatap[dt0]
         ext=tdatae[dt0]
         knns=self.kstates.query(numpy.array(pre).flat,self.k) ## TODO : the nearest points are not necessarily the most suitable for a this...
         knncoeffs=numpy.array([ (1./(1.+kd)) for kd in knns[0] ])
         knncoeffs/=knncoeffs.sum()
         xl=[]
         for i in range(len(knns[1])):
             knnpre=knns[1][i]
             predat=self.test_with_state(knnpre, ext, log )
             #print pre
             #print pre[0]
             #print pre[0][0]
             t=predat[0] *knncoeffs[i]
             xl.append(t)
         if (log):
           res.append(reduce(lambda x,y:x+y,xl,0) )
         else:
           res.append(reduce(lambda x,y:x*y,xl,0) )
      return  numpy.vstack([res])
    def train(self,data, *args, **kwargs):    
      """
        This is a randomized learner : 
            We assign each observation to some nearest neighbor according to some probability
      """
      import random
      resa=[]
      resb=[]
      print data
      for dt0 in range(data.shape[0]):
         #print data[dt0].tolist()
         pre=self.real_project_evidence(data[dt0].tolist())
         #xpre=self.project_evidence(data[dt0].tolist())
         ext=self.real_project_prior(data[dt0].tolist())
         #print pre
         #print "pre",pre
         #print "ext",ext
         knns=self.kstates.query(numpy.array(pre).flat,self.k) ## TODO : the nearest points are not necessarily the most suitable for a this...
         print knns[0],knns[1],len(knns[0]),len(knns[1])
         assert(len(knns[0])==len(knns[1]))
         knncoeffs=numpy.array([ (1./(1.+kd)) for kd in knns[0] ])
         knncoeffs/=knncoeffs.sum()
         knncoeffs=knncoeffs.cumsum()
         knncoeffs-=random.random()
         idx=(knncoeffs<=0).astype(int).sum()
         resb.append(knns[1][idx])
         resa.append(ext)
      #print  "resa",resa, "resb" resb
      FiniteStateConditionalModelF.train_separated(self,numpy.array(resa),numpy.array(resb))
    def train_separated(self,pA,pB, *args, **kwargs):    
      """
        This is a randomized learner : 
            We assign each observation to some nearest neighbor according to some probability
      """
      import random
      resa=[]
      resb=[]
      assert(pA.shape[0]==pB.shape[0])
      for dt0 in range(pB.shape[0]):
         pre=pA[dt0]
         ext=pB[dt0]
         knns=self.kstates.query(numpy.array(pre).flat,self.k) ## TODO : the nearest points are not necessarily the most suitable for a this...
         knncoeffs=numpy.array([ (1./(1.+kd)) for kd in knns[0] ])
         knncoeffs/=knncoeffs.sum()
         knncoeffs=knncoeffs.cumsum()
         knncoeffs-=random.random()
         idx=(knncoeffs<=0).astype(int).sum()
         assert(len(knns[0])==len(knns[1]))
         resb.append(knns[1][idx])
         resa.append(ext[0])
      FiniteStateConditionalModelF.train_separated(self,numpy.array(resa),numpy.array(resb))
   

def test_ufscm():
     import random
     from scipy.spatial.kdtree import  KDTree
     #import pycvf.indexes.smallindexes import SmallContinuousMultiDimIndex
     _len=3
     k=2
     L=[ x for x in numpy.ndindex((2,2,2,2,2,2)) ]
     #print L
     m=InterpolatedStateConditionalModelSv(
            L,
            k,
            KDTree,
            project_prior=lambda x:x[_len:_len+1] ,
            project_evidence=lambda x:x[0:_len],
            individual_model_factory=lambda x: HistogramModel(bins=(5,5),base=(-2,-2), delta=(2,2) )  # Em2Model(2,2)
       )
     seq=[ (numpy.cos(alpha),numpy.sin(alpha)) for alpha in numpy.arange(0,6.28,0.05) ]
     strain=numpy.array([ [x for x in seq[i:(i+_len+1)] ] for i in (range(len(seq)-_len)) ])
     #print strain
     m.train(strain)
     #print m.test(strain)
     #print m.test(strain).mean()
     #print "/X"
     strainb=numpy.random.random(strain.shape).astype(int)
     print m.test(strainb)
     print m.test(strainb).mean()

     seq=[ (numpy.cos(alpha),numpy.sin(-alpha)) for alpha in numpy.arange(0,6.28,0.05) ]
     strain=numpy.array([ [x for x in seq[i:(i+_len+1)] ] for i in (range(len(seq)-_len)) ])
     print m.test(strain)
     print m.test(strain).mean()
     strain=numpy.random.random(strain.shape).astype(int)
     print m.test(strain)
     print m.test(strain).mean()
     return m

##
## from this we may learn a multiscale model
##


class DynamicallyInterpolatedStateConditionalModelSv(InterpolatedStateConditionalModelSv):
    def usemodel(self,sv):
       return self.statedistributionmodel(sv)
    def neighboring(self,sv):
       self.kstates.query(sv,ball)  	
    def relative_information(self,nv,sv):
        ##
        testpoints=map(lambda x:(sv+x)/2,neighborpos)
        testpoints=reduce(lambda x,y:x+y+model_from_state(y).sample()  ,testpoints, []) 
        return self.dist(model_from_state(sv)(testpoints), model_from_state(nv)(testpoints)) ## we compute the distance in-between the estimates of one model and another model 
    def usefulness(self,sv):
        """ 
        An information is useful if it has some practical impact on the way we take decision, and cannot be sumamrized by any other information
        """
        return self.usemodel(sv)*[ self.relative_information(sv,nv)  for nv in self.neighboring(sv)]
    def suggest_new_point(self):
	## return a random point acording to statedistributionmodel
        return self.statedistributionmodel(sv).sample(1)
    def update(self,data):
      ## maybe one may remove useless nodes ??
      usevect=[self.usefulness(x) for x in self.xstates]
      mostuseless=argmin(uservect)
      ## maybe one may insert new nodes ?
      ##
      ## Let's create a new tree
      ## 
      pass

  




####
####
####