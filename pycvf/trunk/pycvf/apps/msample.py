# -*- coding: utf-8 -*-
  ##############
  # To be cleaned a littled bit ...
  ##############
# -*- coding: utf-8 -*-
import sys
from pycfg.core.generic_application import *
import time
import cPickle as pickle
from pycvf.lib.graphics.imgfmtutils import NumPy2PIL
from pycvf.lib.graphics.colortransforms import hsv2rgb


class MSamplerApp(ModelUsingApplication):
  class ProgramMetadata(object):
      name="PyCvF Application"
      version="0.1"
      license="GPLv3"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  def do_record2(self,x):
    NumPy2PIL(x.astype(numpy.uint8)).save("/tmp2/sampler-o-%s.png"%(str(time.time())))

  def do_record(self,x):
    pickle.dump(x,file("/tmp2/sampler-%s.pcl"%(str(time.time()),),"wb"),protocol=2)
    print "dr"
    xo=x[0].reshape(91,123,3).astype(numpy.uint8)
    NumPy2PIL(xo).save("/tmp2/sampler-%s.png"%(str(time.time())))
    xo[0]=0

  @classmethod
  def process(cls, * args, **kwargs):
     submdl=mdl.get_by_cname(modelpart.value)
     print submdl
     print submdl.structures
     substruct=submdl.structures.values()[0]
     print "substruct", substruct
     for e in vdb:
       substructshp=substuct.get_shape(e[0])
       print "shape",substructshp



MSamplerApp.run(sys.argv[1])


