# -*- coding: utf-8 -*-
# we assume that we are receiving a video


from pycvf.core.generic_application import *
import numpy
import random


class ArtificialWorld:
   def __init__(self,numboids=5, k=2, noise=2.5,ws=20,Ms=3,ms=0.5):
       self.numboids=numboids
       self.k=k
       self.noise=noise
       self.ws=ws
       self.boidspos=numpy.random.random((numboids,2))*numpy.array([ws,ws])
       self.boidssz=numpy.random.random((numboids,1))*Ms+ms
       self.boidsvel=numpy.random.random((numboids,2))
   def get_obs(self):
       self.boidspos+=self.boidsvel
       self.boidsvel+=numpy.random.random((self.numboids,2))
       self.boidsvel[self.boidsvel>2]=2
       self.boidsvel[self.boidsvel<-2]=-2
       self.boidsvel[self.boidspos>self.ws]=-self.boidsvel[self.boidspos>self.ws]
       self.boidspos[self.boidspos>self.ws]=self.ws
       self.boidsvel[self.boidspos<0]=-self.boidsvel[self.boidspos<0]
       self.boidspos[self.boidspos<0]=0
       o= self.boidspos.take(random.sample(range(self.numboids),self.numboids-self.k),axis=0)+(numpy.random.random((self.numboids-self.k,2))-0.5)*self.noise
       ox=numpy.random.random((self.k,2))*numpy.array([self.ws,self.ws])
       return numpy.vstack([o,ox])




if __name__=="__main__":
  from pycvf.lib.trackers.generictracker import *
  tracker=GenericTracker()
  aw=ArtificialWorld()
  while True:
     tracker.push(aw.get_obs())

