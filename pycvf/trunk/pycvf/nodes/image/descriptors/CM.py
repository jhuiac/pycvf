from pycvf.core.builders import *
from pycvf.core import autoimp
autoimp._import_all()
pycvf=autoimp.pycvf

def Model(self,subdivide=(3,3),moments=[1,2,3],colorlayers=1):
  m0=pycvf.nodes.image.exploded_transform(pycvf.structures.spatial.Subdivide(subdivide+(1,)*colorlayers) , pycvf.nodes.image.moments(moments,colorlayers))
  m0=m0|free('numpy.vstack(map(lambda y:y[0],x)).ravel()'
  return m0

__call__=Model