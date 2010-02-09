# -*- coding: utf-8 -*-
import os,sys
import pysash as ps
import numpy

normal_sash=False
base=numpy.random.random((1000,3)).astype(numpy.float32)

if normal_sash==True:
   s=ps.Sash()
   base=numpy.random.random((100000,3)).astype(numpy.float32)
   s.build(base)
else:
   def f( x,y):
       r=numpy.linalg.norm(x-y)
       return r
   s=ps.GenericSash(f)
   s.build(base)

print "built"
sys.stdin.readline()
   
query=numpy.array([0.3,0.3,0.3]).astype(numpy.float32)
print "query built"
sys.stdin.readline()
print s.findAllInBall(query,0.05)
print "query done"
sys.stdin.readline()
print s.getResultIndices()
print s.getResultDists()

query=numpy.array([0.3,0.3,0.3]).astype(numpy.float32)
print s.findNearest(query)
print s.getResultIndices()
print s.getResultDists()

if normal_sash:
  s.save("test")
  del s

  s=ps.Sash()
  s.build(base,filename="test")
  query=numpy.array([0.3,0.3,0.3]).astype(numpy.float32)
  print s.findAllInBall(query,0.05)
  print s.getResultIndices()
  print s.getResultDists()

  os.remove("test.sash")