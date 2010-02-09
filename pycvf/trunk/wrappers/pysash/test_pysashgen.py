# -*- coding: utf-8 -*-
import os,sys
import pysash as ps
import numpy
import random

normal_sash=False
base=numpy.zeros((1000,),dtype=object)

for i in range(1000):
    base[i]=random.sample(range(20),random.randint(3,6))

def f(l1,l2):
    s1=set(l1)
    s2=set(l2)
    r=1-(float(len(s1.intersection(s2))))/len(s1.union(s2))
    return r
s=ps.GenericSash(f)
s.build(base)

print "built"
#sys.stdin.readline()
   
query=numpy.array([1,2,3]).astype(numpy.float32)
print "query built"
#sys.stdin.readline()
print s.findAllInBall(query,0.5)
print "query done"
#sys.stdin.readline()
print s.getResultIndices()
print s.getResultDists()

