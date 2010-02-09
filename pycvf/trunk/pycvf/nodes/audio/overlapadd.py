class OverlapAdder(object):
  def __init__(self, filename, channels=1, samplerate=44100):
    self.wf = wave.open(filename, 'w')
    self.wf.setnchannels(CHANNELS)
    self.wf.setframerate(SAMPLER)
    self.wf.setsampwidth(2)
  def push(self,data,make_positive=32768):
    class Reader:
      pass
    reader=Reader()
    return reader

from pycvf.core import genericmodel
from pycvf.datatypes import audio

class Model(genericmodel.Model):
  def input_datatype(self,x):
       return audio.Samples.Datatype
  def output_datatype(self,x):
       return audio.Datatype
  def init_model(self,*args,**kwargs):
       overlapadder=OverlapAdder(*args,**kwargs)
       self.processing=[('overlapadder',{'overlapadder':overlapadder})] 
  
__call__=Model


