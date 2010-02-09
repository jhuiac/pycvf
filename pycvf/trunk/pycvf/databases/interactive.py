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
    """
     This database allows you to select interactively which database you want to use.
     Its implementation is really minimal for the moment, but it may act as memo
     when you search of the name of databasse.
    """
    try:
      from pycvf.lib.ui import qt
      from PyQt4.QtGui import QInputDialog
      dbl=dblist()
      r=QInputDialog.getItem(None,"Select a database to use", "Select a database to use",dbl)
      if r[1]:
        r=str(r[0])
      else:
        raise KeyboardInterrupt
    except KeyboardInterrupt:
      raise
    except: 
      dbl=dblist()
      sl=map(lambda x,y:(x,y),range(1,1+len(dbl)),dbl)
      for l in sl: print l
      r=int(sys.stdin.readline())
      r=dbl[r-1]
    return builders.load_force(r)

DB=select_db    
__call__=select_db


