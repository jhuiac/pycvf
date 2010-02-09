# -*- coding: utf-8 -*-
from pylsh import MPLSHIndex
import sys,numpy

sys.stderr.write("a\n")
sys.stderr.flush()
a=numpy.random.random((3200,5))
a=a.astype(numpy.float32)

sys.stderr.write("b\n")
sys.stderr.flush()
i=MPLSHIndex(a)

sys.stderr.write("c\n")
sys.stderr.flush()
i.build()
  
sys.stderr.write("d : about tot do one query\n")
sys.stderr.flush()

# when too far away bins don't match
queryv=numpy.array([[2,2,2,2,-2],[.5,.5,.5,.5,.5],[1,1,1,1,-1],[.5,.5,.5,.5,.5]],dtype=numpy.float32) 
xres=i.query(queryv,5,1) # 20?

sys.stderr.write("e\n")
sys.stderr.flush()
print xres

import scipy.spatial
md=scipy.spatial.distance.cdist(a,queryv)
print md.argsort(axis=0)[:6,:].T
md.sort(axis=0)
print md[:6,:].T**2