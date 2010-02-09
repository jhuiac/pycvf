# -*- coding: utf-8 -*-
### For a deterministic reader, reads in-between two time codes (Maybe used to implement slice in other readers...)
from pycvf.core.errors import pycvf_warning

class SubsequenceReader:
    def __init__(self,reader, addrfrom, addrto):
        self.reader=reader
        self.addrfrom=addrfrom
        self.addrto=addrto
        self.fno=0
    def get_tracks(self):
        return self.reader.get_tracks()
    def copy(self):
        return SubsequenceReader(self.reader.copy(),self.addrfrom,self.addrto)
    def set_observer(self,observer):
        self.reader.set_observer(observer)
    def step(self):
        if (self.fno==0):
          try:
            self.reader.seek_to(self.addrfrom)
          except Exception, e:
            pycvf_warning("Subsequence Reader : Unable to seek : the result may be invalid ! reason :"+str(e))          
            import traceback, sys
            if (hasattr(sys,"last_traceback")):
              traceback.print_tb(sys.last_traceback)
            else:
              traceback.print_tb(sys.exc_traceback)
        if (self.reader.get_current_address()[1]>=self.addrto):
            raise StopIteration
        self.reader.step()
        self.fno+=1
    def get_current_address(self):
        r=self.reader.get_current_address()        
    def __len__(self):
      return self.addrto-self.addrfrom
    def rewind(self):
      self.fno=0
    def seek_to(self,pos):
      if (pos>=len(self)):
         raise ValueError
      self.fno=pos
      self.reader.seek_to(self.addrfrom+pos)
    def __getitem__(self,addr):
       if (addr>=len(self)):
         raise ValueError
       self.fno=addr
       r=self.reader[self.addrfrom+addr]
       self.fno+=1
       return r
    def run(self):
        try:
           while True:
              self.step()
        except StopIteration:
           pass


