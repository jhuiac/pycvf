# -*- coding: utf-8 -*-
import numpy
from pycvf.core import database
from pycvf.datatypes import basics
from pycvf.lib.info.hinge_angles import *

def gcd(a,b):
  while (b!=0):
    b,a=a%b,b
  return a

def hinge_enumerate_function(l):
  L=[]
  r=l-1
  for j in range(l):
    for i in range(j):
	if ((i**2+j**2)<=r**2):
	  if (gcd(i,j)==1):
	    for d in range(-int((i**2+j**2)**.5),int((i**2+j**2)**.5)):
	      L.append(HingeAngle(i,j,d).normalized_angle_first_octant())
  L.sort(cmp = lambda x,y:(-1 if (x.__less__(y)) else 1))
  return L

class DB(database.ContentsDatabase):
  def datatype(self):
    return basics.NumericArray.Datatype
  def __init__(self,l=10,x="x"):
    self.L=hinge_enumerate_function(l)
    self.x=x
  def __iter__(self,l=10):
    for x in range(len(self.L)-1):
       yield (numpy.array([self.L[x].x,self.L[x].y,self.L[x].h,getattr(self.L[x+1],self.x)]),x)
  def __getitem__(self,x):
    return (numpy.array([self.L[x].x,self.L[x].y,self.L[x].h,getattr(self.L[x+1],self.x)]),x)


__call__=DB
ContentsDatabase=DB