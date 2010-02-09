# -*- coding: utf-8 -*-
import os 
import numpy
import hashlib
from pycvf.core.errors import pycvf_warning
import scipy
from scipy.weave import converters
from scipy.weave import inline

def cimg_code(code,realcode="",prod=False):
    if not prod:
      pycvf_warning("once you finished developping, please add option 'prod=True' to avoid computing a md5 checksum at each call")
    base_install="/usr/"
    base_include=os.path.join(base_install,"include")
    cimg_info={'include_dirs': [base_include,
                              ]
    , 'library_dirs':[base_install+"/lib"]}
    def fct(**context):
      args=[      code+("" if prod else "/* hash : %s */"%(hashlib.md5(realcode).hexdigest(),)), 
                  context.keys()
           ]
      kwargs=dict(
                  support_code="# 1 \"inlinecode\"\n"+realcode,
                  headers=[],
                  libraries=['X11'],
                  include_dirs=cimg_info['include_dirs'],
                  library_dirs=cimg_info['library_dirs'],
                  compiler='gcc',
                  #type_converters = converters.blitz
                 )
           
      assert(not context.has_key("__inlineargs__"))
      context["__inlineargs__"]=args
      context["__inlinekwargs__"]=kwargs
      r= eval("inline(*__inlineargs__,**__inlinekwargs__)",globals(),context)
      context["__inlineargs__"]=None
      return r
    return fct
    

if __name__=="__main__":
  import time
  st=time.clock()
  lena=scipy.lena().reshape(512,512,1).repeat(3,axis=2).astype(numpy.uint8).swapaxes(0,1).copy('F')
  cimg_code("do_test( a_array );",
"""
#include <CImg.h>
using namespace cimg_library;

int do_test(PyArrayObject * npimg ) {
   assert(npimg->nd==3);
   printf("%p %d x %d x %d\\n",npimg->data,npimg->dimensions[1],npimg->dimensions[0],npimg->dimensions[2]);
    CImg<unsigned char> image(npimg->data,npimg->dimensions[1],npimg->dimensions[0],1,npimg->dimensions[2]), visu(500,400,1,3,0);
    image=image.blur(2.5);
    return 0;
}
""",True)(a=lena)
  print "done in ",time.clock()-st, "seconds";

  