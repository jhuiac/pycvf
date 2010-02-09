from Bio import Entrez, SeqIO
from pycvf.core import database
from pycvf.datatypes import basics
#from pycvf.datatypes import generator

class DB(database.ContentsDatabase, basics.Label.Datatype):
#generator.Datatype(basics.Label.Datatype)):
  def __init__(self, db="nucleotide", ids=["186972394"],rettype="gb"):
     self.db=db
     self.ids=ids
     self.rettype=rettype     
  def __iter__(self):
      for x in self.ids:
         yield (self[x],x)
  def __getitem__(self,key):
    handle = Entrez.efetch(db=self.db, id=str(key),rettype=self.rettype)
    self.record = SeqIO.read(handle, "genbank")
    handle.close()
    #print dir(record)
    return self.record.seq

__call__=DB
