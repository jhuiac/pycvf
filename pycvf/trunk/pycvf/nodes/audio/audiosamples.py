# -*- coding: utf-8 -*-

#import pyffmpeg_audioqueue as audioqueue
import audioqueue
import scipy
import numpy
from pycvf.core.errors import pycvf_warning


class EventReceiver:
  def __init__(self,sample_rate=44100,
                    dest_frame_size=128,
                    dest_frame_overlap=96,
                    tps=30
              ):
       self.audiohq=audioqueue.AudioQueue(limitsz=4) 
       self.audioq=audioqueue.AudioQueue(limitsz=12,
                                         tps=tps,
                                         samplerate=sample_rate,
                                         destframesize=dest_frame_size,
                                         destframeoverlap=dest_frame_overlap,
                                         destframequeue=self.audiohq
                                        )
  def push(self,x):
    self.audioq.push(x)
    
  def get(self):
    x=self.audiohq.get_nowait()
    return x[0]
                                                      
    ## if some data are ready push to 

def audiosample(rdr):
    er=EventReceiver()
    rdr.set_observer(er.audioq.putforce)
    rdr.vr.step()   
    try:
      while True:
        try:
          yield er.get() #audiohq.get_nowait()
        except audioqueue.Queue_Empty:
          rdr.step()
    except StopIteration:
      pass
    except KeyboardInterrupt:
      raise

#   except Exception,e:
#     pycvf_warning("Error while computing spectrum for audiofile :["+str(e)+"]")
#     raise StopIteration,e
      
from pycvf.core import genericmodel
from pycvf.datatypes import audio

class Model(genericmodel.Model):
  def input_datatype(self,x):
       return audio.Datatype
  def output_datatype(self,x):
       return audio.Samples.Datatype
  def init_model(self,*args,**kwargs):
       self.processing=[('audiosamples',{'audiosamples':audiosamples})] 

__call__=Model

if __name__=="__main__":
    from pycvf.core.builders import pycvf_builder
    vdb=pycvf_builder("LF('pycvf.databases.sound_directory','/media/c/music/musique/')")
    r=iter(vdb).next()
    x=audiosamples(r[0])
#    print "x",x
    for a in x:
      print a
