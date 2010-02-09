# -*- coding: utf-8 -*-
from pycvf.core.errors import *

import numpy,scipy,scipy.spatial,time


def do_matching(old,new,dist='Euclidean'):
      """
          returns coupling by order of strengthness 
      """
      xres=scipy.spatial.distance.cdist(old,new,dist)
      rsp=xres.copy()
      rsp.sort(axis=1)
      r=[]
      d=[]
      rr=range(xres.shape[0])
      for i in range(xres.shape[0]):
         r.append(rsp[:,0].argmin())
         d.append(rsp[r[-1],0])
         rsp=numpy.vstack([ rsp[:(r[-1]),1:],rsp[(r[-1]+1):,1:]])
         nr=rr[r[-1]]
         del rr[int(r[-1])]
         r[-1]=nr
      return r,d



class SimpleClock:
     def __init__(self):
        self.t=0
     def tick(self):
        self.t+=1
     def get(self):
        return self.t


class GenericTracker:
  minimum_objects_in_scene=1 ## There is always something
  
  class ObjectInScene:
     def __init__(self, **kwargs):
       ##
       ## from_time
       ##
       self.d=kwargs
       self.appeared=True
       self.oldproba=0
       self.proba=0 # some objects are only hypothesis
       self.pos=None # position
       self.pos_prediction=None # position prediction
       self.posh=[] # position history


  def no_movement_prediction_po(self,o, context, newobs):
     """ too simple movement predictor """
    
     return o

  def no_movement_prediction(self, context, newobs):
     return map(lambda o:self.no_movement_prediction_po(o,context,newobs),context)

  def __init__(self,observation_model=None, object_prediction_function=None,similarity_metric=None,sceneclock=None,observer=None,position_extracter=None):
     self.observation_model=observation_model or (lambda x:x)
     self.object_prediction_function=object_prediction_function or self.no_movement_prediction
     self.simpleclock=SimpleClock()
     self.sceneclock=sceneclock or self.simpleclock
     self.observer=observer ## use to detect more events such as scale variation, illumination variation ... 
     self.scene={}
     self.hypothesis=[]
     self.position_extracter=position_extracter or (lambda x:x)
     self.seuil2=0.5
     self.seuil1=0.1
     self.idc=[x for x in range(100)]

  def do_assign_new_in_scene(self,matching,scene,obs):
    print "obs",obs
    for x in range(len(obs )):
        #if ()
           o=self.ObjectInScene()
           o.pos=obs[x]
           o.appeared=True
           self.scene[self.idc.pop()]=o

  def push(self,new_raw_observations):
     ##
     ## This function is regularly called to get new observations
     ##
     new=self.observation_model(new_raw_observations)
     print "new", new
     oldscene=self.object_prediction_function(self.scene,new) ## prediction of the new state
     print "old" ,oldscene
     a1=numpy.array(map(lambda x:x.pos,oldscene))
     a2=numpy.array(map(self.position_extracter,new))
     print a2
     if (a2.shape[0]):
       if (a1.shape[0]):
         r=do_matching(a1,a2)
       else:
         r=[]
       print "r",r
       self.do_assign_new_in_scene(r,a1,a2)
     print "ns",self.scene
     self.make_object_live()
     self.simpleclock.tick()
     time.sleep(0.5)

  def make_object_live(self) :
      ## make appear new object
      for o in self.scene.items():
          if (o[1].appeared):
             o[1].newproba=o[1].oldproba*(o[1].appeared+.5)
          else:
             o[1].newproba=self.oldproba*.5
          if (o[1].oldproba<self.seuil2) and ((o[1].proba*1.5)>self.seuil2):
                self.on_object_disappear(o[1])
  
      
      ## make disappear new object
      print map(lambda o:o[1].proba,self.scene.items())
      to_be_deleted=filter(lambda o:o[1].proba<self.seuil2,self.scene.items())
      to_be_really_deleted=(filter(lambda o:o[1].proba<self.seuil1,self.scene.items()))
      self.scene=dict(filter(lambda o:o[1].proba>=self.seuil1,self.scene.items()))
      for x in to_be_deleted:
         self.on_object_disappear(x[1])
      for x in to_be_really_deleted:
         self.idc.append(x[0])
      
                  

  def on_object_disappear(self,xxx):
     print "object disappeared but no event manager in tracker"
     pycvf_debug(19,"object disappeared but no event manager in tracker")

  def on_new_object_appear(self,xxxx):
     print "object appeared but no event manager in tracker"
     pycvf_debug(19,"new object appeared but no event manager in tracker") 
  
