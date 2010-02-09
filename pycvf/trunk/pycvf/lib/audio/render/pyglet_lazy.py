# -*- coding: utf-8 -*-
import pyglet 

class AudioQueueSource(pyglet.media.StreamingSource) :
    def __init__(self,aq,channels=2, sample_size=16, sample_rate=44100):
        self.aq=aq                                                      
        self.channels=channels                                          
        self.audioformat=pyglet.media.AudioFormat( channels=channels,   sample_size=sample_size, sample_rate=sa
mple_rate)                                                                                                     
        self.audio_format=self.audioformat                                                                     
        self.timestamp=0
        self._duration=float(100*365*24*3600)  #*44100
        self._start_offset = 0
        self._max_offset = self._duration*44100
        self._offset = 0
        self._file=self
        self._data="\0\0"*4096
    def _get_audio_data(self, bytes):
        lensig=bytes//2
        #fratio=self.freq*6.28/44100.
        ar=self.aq.read(lensig//self.channels)
        self._offset+=lensig
        self.timestamp=self._offset
        data=ar.tostring()
        self._data=data
        return pyglet.media.AudioData(data, len(data), self.timestamp, lensig/44100)
    def seek(self, timestamp):
        self._offset=int(timestamp*44100)


class LazyAudioSink:
  def __init__(self,):
       try:
         self.ao=oss.open_audio()
       except:
         self.ao=oss.open('w')
       if (hasattr(self.ao,'stereo')):
         self.ao.stereo(1)
       self.ao.speed(rate)
       if (hasattr(self.ao,'format')):
         self.ao.format(oss.AFMT_S16_LE)
       else:
         self.ao.setfmt(oss.AFMT_S16_LE)
       self.ao.channels(channels)
  def push(self,x):
     ao.write(x[0][1].data)
  def f(self,x):
     ao.write(x[1].data)
     
