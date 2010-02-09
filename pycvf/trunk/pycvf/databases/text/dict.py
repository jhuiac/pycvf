import dictclient

def listdb(*args,**kwargs):
    c=dictclient.Connection(*args,**kwargs)
    return c.getdbdescs()

def getdbc(serverargs=[],db="littre"): 
    c=dictclient.Connection(*serverargs)
    return dictclient.Database(c,db)

def get_definitions(serverargs=[],db="littre",query="test"):
     dbc=getdbc(serverargs,db) 
     return dbc.define('jour')[0].defstr
    
from pycvf.core import database
from pycvf.datatypes import basics
 
class DB(database.ContentsDatabase,basics.Label.Datatype):
    def __init__(self, querydb, db="littre", serverargs=[]):
       self.querydb=querydb
       self.db=db
       self.dbc=getdbc(serverargs,db) 
    def __iter__(self):
       for i in self.querydb:
            defs=self.dbc.define(i[0])
            for j in range(len(defs)):
               yield (defs[j].defstr, (i,j))
    def __getitem__(self,x):
            defs=self.dbc.define(x[0])
            return defs[x[1]].defstr
        

__call__=DB
ContentsDatabase=DB