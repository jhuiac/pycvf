# -*- coding: utf-8 -*-
import sys
import os
import stat

import pycvf.core.database
from pycvf.core import settings
from pycvf.core import builders

def dblist():
     r=[]
     for x in globals().values():
        try:
          if issubclass(x,pycvf.core.database.ContentsDatabase):
             r.append(x)
        except:
          pass
     dbl=settings.PYCVF_DATABASE_PATH.split(':')
     for p in dbl:
        if (p):
          for x in os.listdir(builders.pycvf_builder(p[:-1]).__path__[0]):
            if (x[-3:]==".py") and (x!="__init__.py"):
              r.append(p+x[:-3])
            elif ("." not in x):
              dj=os.path.join(builders.pycvf_builder(p[:-1]).__path__[0],x)
              if (stat.S_ISDIR(os.stat(dj)[0])):
                try:
                  os.stat(os.path.join(dj,"__init__.py"))
                  builders.load_force(p+x)                  
                  dbl.append(p+x+".")
                except OSError:
                  pass
     return r


def select_db():
    dbl=dblist()
    sl=map(lambda x,y:(x,y),range(1,1+len(dbl)),dbl)
    for l in sl: print l
    r=int(sys.stdin.readline())
    return builders.load_force(dbl[r])
    
__call__=select_db
