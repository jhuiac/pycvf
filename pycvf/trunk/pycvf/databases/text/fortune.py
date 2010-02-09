from pycvf.core import database
from pycvf.core import settings
from pycvf.datatypes import basics
import os

FORTUNEPATH=( "/usr/share/games/fortunes" if not hasattr(settings,"FORTUNEPATH") else settings.FORTUNEPATH)  

class DB(database.ContentsDatabase,basics.Label.Datatype):
    def __init__(self, filename):
        self.f=file(os.path.join(FORTUNEPATH,filename)+".u8")
        p=""
        r=[]
        for l in self.f.readlines():
            if (l.strip()!='%'):
               p+=l.decode('utf8')
            else:
               r.append(p)
               p=""
        self.r=r
    def __iter__(self):
            for i in range(len(self.r)):
               yield (self.r[i], i)
    def __getitem__(self,x):
            return self.r[i]
        

__call__=DB
ContentsDatabase=DB