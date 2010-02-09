from zopencv_core import *
import zopencv_classes
from zopencv_classes import *
from zopencv_highlevel import *
import zopencv_pclasses as pointers

##
## hmm le probleme de les declarer ici ce ne sont pas les types de retour des fonctions
##

class CvSeq(zopencv_classes.CvSeq):
  def iter(cvseq,typ):
    for x in range(cvseq.total):
      yield typ(cvseq.getSeqElem(x))

class CvPoint(zopencv_classes.CvPoint):
    def __tuple__(self):
        return (self.x,self.y)
