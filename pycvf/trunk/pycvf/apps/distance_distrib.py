#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycvf.core.generic_application import *
import scipy.stats.kde as kde
import numpy
import pylab

class DistanceDistribApp(IndexUsingApplication):
  class ProgramMetadata(object):
      name="Show Relative Distance Distribution of samples"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  number_query=CmdLineString('n',"numberofneighbors",'number',"name of neighbours","3")  

  @classmethod
  def process(cls,nrels=1,*args,**kwargs):
    nq=int(cls.number_query.value)
    a=map(lambda e:(map(lambda le: map(lambda t:t[1],le) , cls.mdl.process(e[0],processf=lambda x:cls.idx.query([x],nq)))[0]), cls.vdb)
    #print a
    a=numpy.array(a)
    m,M=a.min(),a.max()
    for nn in range(1,nq):
      #print a[:,nn]
      r=kde.gaussian_kde(a[:,nn])
      kdel=numpy.vectorize(r.evaluate)(numpy.arange(m,M,(M-m)/100.))
      print kdel
      #
      pylab.plot(numpy.arange(m,M,(M-m)/100.),kdel)
    pylab.savefig("xx.png")
    pylab.show()

DistanceDistribApp.run(sys.argv[1:])

