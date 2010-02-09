# -*- coding: utf-8 -*-
import numpy
import random
from itertools import imap #randomvideopatch


def randompatch(i,sz=(48,48)):
  h,w,d=i.shape               
  x=random.randint(0,w-sz[0]) 
  y=random.randint(0,h-sz[1]) 
  return i[y:(y+sz[1]),x:(x+sz[0]),:]

def randompatches(i,np=3,sz=(24,24)):
  return [ randompatch(i,sz) for x in range(np) ]


def anysizerandompatch(i,fromsz=(48,48),tosz=(128,128)):
  h,w,d=i.shape               
  sz=(random.randint(fromsz[0],tosz[0]),random.randint(fromsz[1],tosz[1]) ) 
  x=random.randint(0,w-sz[0]) 
  y=random.randint(0,h-sz[1]) 
  return i[y:(y+sz[1]),x:(x+sz[0]),:]

def anysizerandompatch(i,fromsz=(48,48),tosz=(128,128),rescale=None):
  h,w,d=i.shape               
  sz=(random.randint(fromsz[0],tosz[0]),random.randint(fromsz[1],tosz[1]) ) 
  x=random.randint(0,w-sz[0]) 
  y=random.randint(0,h-sz[1]) 
  if (rescale):
    from pycvf.lib.graphics.rescale import Rescaler2d
    return Rescaler2d(rescale).process(i[y:(y+sz[1]),x:(x+sz[0]),:])
  else:
    return i[y:(y+sz[1]),x:(x+sz[0]),:]


def anysizerandompatches(i,np=3,fromsz=(24,24),tosz=(128,128),rescale=None):
  return [ anysizerandompatch(i,fromsz,tosz,rescale) for x in range(np) ]
  

  

def randomvideopatch(v,sz=(48,48)):
  x=random.randint(0,w-sz[0]) 
  y=random.randint(0,h-sz[1]) 
  return (imap[y:(y+sz[1]),x:(x+sz[0]),:],v)
                                      
def randomvideopatches(v,np=10,sz=(48,48)):
  return [ randomvideopatch(v,sz) for x in range(np) ]
                                      
#def randomvideopatchesfromvideoreader(vr,lenpatch):
#    lenpatch=
#    self.
