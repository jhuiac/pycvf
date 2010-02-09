# -*- coding: utf-8 -*-
import numpy
from pycvf.lib.info.hinge_angles import *

def gcd(a,b):
  while (b!=0):
    b,a=a%b,b
  return a

def hinge_compare_function(l):
  r=l-1
  for j in range(l):
    for i in range(j):
	if ((i**2+j**2)<=r**2):
	  if (gcd(i,j)==1):
	    for d in range(0,int((i**2+j**2)**.5)):
	      ha1=HingeAngle(i,j,d).normalized_angle_first_octant()
	      for j2 in range(l):
		for i2 in range(j):
		    if ((i2**2+j2**2)<=r**2):
		      if (gcd(i2,j2)==1):
			for d2 in range(0,int((i2**2+j2**2)**.5)):
			  if (i,j,d)!=(i2,j2,d2):
			    ha2=HingeAngle(i2,j2,d2).normalized_angle_first_octant()
  		            yield numpy.array([i,j,d,i2,j2,d2,int(ha1.__less__(ha2))])

from pycvf.core import database
from pycvf.datatypes import basics

class DB(database.ContentsDatabase):
  def datatype(self):
    return basics.NumericArray.Datatype
  def __init__(self,l=10):
    self.l=l
  def __iter__(self):
    for x in hinge_compare_function(self.l):
       yield (x,x[:-1])
  def __getitem__(self,a):
    ha1=HingeAngle(a[0],a[1],a[2]).normalized_angle_first_octant()
    ha2=HingeAngle(a[3],a[4],a[5]).normalized_angle_first_octant()
    return numpy.array([a[0],a[1],a[2],a[3],a[4],a[5],int(ha1.__less__(ha2))])

__call__=DB
ContentsDatabase=DB