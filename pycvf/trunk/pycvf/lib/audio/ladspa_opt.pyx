# This file is part of dsptools for python.
# Copyright (C) 2004 Simon Burton <simon@arrowtheory.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


cimport numpy
import numpy
numarray=numpy
include "ladspa.pxi"
tInt8=numpy.int8
tInt16=numpy.int16
tInt32=numpy.int32
tUInt8=numpy.uint8
tUInt16=numpy.uint16
tUInt32=numpy.uint32
tFloat32=numpy.float32
tFloat64=numpy.float64


cdef extern from "Python.h":
  object PyCObject_FromVoidPtr(void *cobj, void (*destruct)(void*))
  void* PyCObject_AsVoidPtr(object)


cdef extern from "numpy/arrayobject.h":
    void *PyArray_DATA(numpy.ndarray arr)

cdef extern from "dlfcn.h":
  enum:
    RTLD_LAZY
    RTLD_NOW
    RTLD_GLOBAL
    RTLD_DEFAULT
    RTLD_NEXT
  void *dlopen(char *filename, int flag)
  char *dlerror()
  void *dlsym(void *handle, char *symbol)
  int dlclose(void *handle)

class Port:
  def __init__(self, ld_object, port_i, sample_rate):
    cdef LADSPA_PortDescriptor d # int
    cdef LADSPA_PortRangeHint rh # struct
    cdef LADSPA_PortRangeHintDescriptor rhd # int
    cdef LADSPA_Descriptor * ld
    ld = <LADSPA_Descriptor*>PyCObject_AsVoidPtr( ld_object )
    self.lpd = ld.PortDescriptors[port_i]
    self.ld = ld_object
    self.name = ld.PortNames[port_i]
#    print "Port.__init__", self.name
    rh = ld.PortRangeHints[port_i]
    ##self.d = d
    ##self.name = name
    self.rhd = rh.HintDescriptor
    if self.is_hint_bounded_below():
      self.lower_bound = rh.LowerBound
      if self.is_hint_sample_rate():
        self.lower_bound = self.lower_bound * sample_rate
    else:
      self.lower_bound = None
    if self.is_hint_bounded_above():
      self.upper_bound = rh.UpperBound
      if self.is_hint_sample_rate():
        self.upper_bound = self.upper_bound * sample_rate
    else:
      self.upper_bound = None
  def __str__(self):
    hints = (
      ( "is_input" , self.is_input() ),
      ( "is_output" , self.is_output() ),
      ( "is_control" , self.is_control() ),
      ( "is_audio" , self.is_audio() ),
      ( "is_hint_bounded_below" , self.is_hint_bounded_below() ),
      ( "is_hint_bounded_above" , self.is_hint_bounded_above() ),
      ( "is_hint_toggled" , self.is_hint_toggled() ),
      ( "is_hint_sample_rate" , self.is_hint_sample_rate() ),
      ( "is_hint_logarithmic" , self.is_hint_logarithmic() ),
      ( "is_hint_integer" , self.is_hint_integer() ),
      ( "is_hint_has_default" , self.is_hint_has_default() ),
      ( "is_hint_default_minimum" , self.is_hint_default_minimum() ),
      ( "is_hint_default_low" , self.is_hint_default_low() ),
      ( "is_hint_default_middle" , self.is_hint_default_middle() ),
      ( "is_hint_default_high" , self.is_hint_default_high() ),
      ( "is_hint_default_maximum" , self.is_hint_default_maximum() ),
      ( "is_hint_default_0" , self.is_hint_default_0() ),
      ( "is_hint_default_1" , self.is_hint_default_1() ),
      ( "is_hint_default_100" , self.is_hint_default_100() ),
      ( "is_hint_default_440" , self.is_hint_default_440() ),
    )
    s = []
    if self.lower_bound is not None:
      s.append( "lower_bound = %s" % self.lower_bound )
    if self.upper_bound is not None:
      s.append( "upper_bound = %s" % self.upper_bound )
    for hint in hints:
      if hint[1]:
        s.append( hint[0] )
    
    s = ", ".join( s )
    return "Port( '%s', %s )" % (self.name,s)
  __repr__ = __str__
  def is_input(self):
    return LADSPA_IS_PORT_INPUT( self.lpd ) != 0
  def is_output(self):
    return LADSPA_IS_PORT_OUTPUT( self.lpd ) != 0
  def is_control(self):
    return LADSPA_IS_PORT_CONTROL( self.lpd ) != 0
  def is_audio(self):
    return LADSPA_IS_PORT_AUDIO( self.lpd ) != 0
  def is_hint_bounded_below(self):
    return LADSPA_IS_HINT_BOUNDED_BELOW(self.rhd) != 0
  def is_hint_bounded_above(self):   
    return LADSPA_IS_HINT_BOUNDED_ABOVE(self.rhd) != 0
  def is_hint_toggled(self):         
    return LADSPA_IS_HINT_TOGGLED(self.rhd) != 0
  def is_hint_sample_rate(self):     
    return LADSPA_IS_HINT_SAMPLE_RATE(self.rhd) != 0
  def is_hint_logarithmic(self):     
    return LADSPA_IS_HINT_LOGARITHMIC(self.rhd) != 0
  def is_hint_integer(self):         
    return LADSPA_IS_HINT_INTEGER(self.rhd) != 0
  def is_hint_has_default(self):     
    return LADSPA_IS_HINT_HAS_DEFAULT(self.rhd) != 0
  def is_hint_default_minimum(self): 
    return LADSPA_IS_HINT_DEFAULT_MINIMUM(self.rhd) != 0
  def is_hint_default_low(self):     
    return LADSPA_IS_HINT_DEFAULT_LOW(self.rhd) != 0
  def is_hint_default_middle(self):  
    return LADSPA_IS_HINT_DEFAULT_MIDDLE(self.rhd) != 0
  def is_hint_default_high(self):    
    return LADSPA_IS_HINT_DEFAULT_HIGH(self.rhd) != 0
  def is_hint_default_maximum(self): 
    return LADSPA_IS_HINT_DEFAULT_MAXIMUM(self.rhd) != 0
  def is_hint_default_0(self):       
    return LADSPA_IS_HINT_DEFAULT_0(self.rhd) != 0
  def is_hint_default_1(self):       
    return LADSPA_IS_HINT_DEFAULT_1(self.rhd) != 0
  def is_hint_default_100(self):     
    return LADSPA_IS_HINT_DEFAULT_100(self.rhd) != 0
  def is_hint_default_440(self):     
    return LADSPA_IS_HINT_DEFAULT_440(self.rhd) != 0

class Plugin:
  def __init__(self, ld_object, sample_rate ):
    cdef LADSPA_Descriptor * ld
    cdef LADSPA_Handle handle # void *
#    print "Plugin.__init__"
    ld = <LADSPA_Descriptor*>PyCObject_AsVoidPtr(ld_object)
    if ld == NULL:
      raise Exception
    if ld.run_adding != NULL:
      self.run_adding = self.__run_adding
    if ld.set_run_adding_gain != NULL:
      self.set_run_adding_gain = self.__set_run_adding_gain
    handle = ld.instantiate( ld, sample_rate )
    self.handle = PyCObject_FromVoidPtr( handle, NULL )
    self.ld = ld_object
    self.label = ld.Label
    self.name = ld.Name
    self.maker = ld.Maker
    self.copyright = ld.Copyright
    self.sample_rate = sample_rate
    self.ports = []
    for i in range(ld.PortCount):
      port = Port(ld_object, i, sample_rate)
      self.ports.append(port)
  #def __len__(self):
    #return len(self.ports)
  def __getitem__(self,i):
    return self.ports[i]
  def __str__(self):
    return "Plugin("+\
      "  label: '%s' \n" % self.label+\
      "  name: '%s' \n" % self.name+\
      "  maker: '%s' \n" % self.maker+\
      "  copyright: '%s' \n" % self.copyright+\
      ")"
  __repr__ = __str__
  def is_realtime(self):
    cdef LADSPA_Descriptor * ld
    ld = <LADSPA_Descriptor *>PyCObject_AsVoidPtr( self.ld )
    return LADSPA_IS_REALTIME(ld.Properties)
  def is_inplace_broken(self):
    cdef LADSPA_Descriptor * ld
    ld = <LADSPA_Descriptor *>PyCObject_AsVoidPtr( self.ld )
    return LADSPA_IS_INPLACE_BROKEN(ld.Properties)
  def is_hard_rt_capable(self):
    cdef LADSPA_Descriptor * ld
    ld = <LADSPA_Descriptor *>PyCObject_AsVoidPtr( self.ld )
    return LADSPA_IS_HARD_RT_CAPABLE(ld.Properties)
  def connect_port( self, port_idx, numpybuffer ):
    cdef LADSPA_Descriptor * ld
    cdef LADSPA_Handle handle # void *
    ld = <LADSPA_Descriptor *>PyCObject_AsVoidPtr( self.ld )
    handle = PyCObject_AsVoidPtr( self.handle )
    cdef LADSPA_Data* data
    if numpybuffer.dtype != numpy.float32:
      raise TypeError, "need Float32 array"
    #io_buffer =  numpy.ndarray(shape=(len(buffer)),dtype=numpy.float32,data=buffer)#PyArray_DATA(( buffer, tFloat32, NUM_C_ARRAY )
    io_buffer=numpybuffer 
    data = <LADSPA_Data*>PyArray_DATA( io_buffer )
    port = self.ports[port_idx]
    port.io_buffer = io_buffer
    ld.connect_port( handle, port_idx, data )
  def activate( self ):
    cdef LADSPA_Descriptor * ld
    cdef LADSPA_Handle handle # void *
#    print "Plugin.activate", self.label
    ld = <LADSPA_Descriptor *>PyCObject_AsVoidPtr( self.ld )
    handle = PyCObject_AsVoidPtr( self.handle )
    if ld.activate != NULL:
      ld.activate( handle )
#    print "Plugin.activate: done"
  def run( self, sample_count ):
    cdef LADSPA_Descriptor * ld
    cdef LADSPA_Handle handle # void *
    ld = <LADSPA_Descriptor *>PyCObject_AsVoidPtr( self.ld )
    handle = PyCObject_AsVoidPtr( self.handle )
    ld.run( handle, sample_count )
  def __run_adding( self, sample_count ):
    cdef LADSPA_Descriptor * ld
    cdef LADSPA_Handle handle # void *
    ld = <LADSPA_Descriptor *>PyCObject_AsVoidPtr( self.ld )
    handle = PyCObject_AsVoidPtr( self.handle )
    if ld.run_adding == NULL:
      raise Exception, "Internal error: plugin has no run_adding method !"
    ld.run_adding( handle, sample_count )
  def __set_run_adding_gain( self, gain ):
    cdef LADSPA_Descriptor * ld
    cdef LADSPA_Handle handle # void *
    ld = <LADSPA_Descriptor *>PyCObject_AsVoidPtr( self.ld )
    handle = PyCObject_AsVoidPtr( self.handle )
    if ld.run_adding == NULL:
      raise Exception, "Internal error: plugin has no set_run_adding_gain method !"
    ld.set_run_adding_gain( handle, gain )
  def deactivate( self ):
    cdef LADSPA_Descriptor * ld
    cdef LADSPA_Handle handle # void *
#    print "Plugin.deactivate", self.label
    ld = <LADSPA_Descriptor *>PyCObject_AsVoidPtr( self.ld )
    handle = PyCObject_AsVoidPtr( self.handle )
    if ld.deactivate != NULL:
      ld.deactivate( handle )
#    print "Plugin.deactivate: done"
  def cleanup( self ):
    cdef LADSPA_Descriptor * ld
    cdef LADSPA_Handle handle # void *
#    print "Plugin.__del__", self.name
    ld = <LADSPA_Descriptor *>PyCObject_AsVoidPtr( self.ld )
    handle = PyCObject_AsVoidPtr( self.handle )
    ld.cleanup( handle )

class Lib:
  def __init__(self,name):
    cdef void*handle
    cdef char*error
    cdef LADSPA_Descriptor_Function get_ld
    cdef LADSPA_Descriptor * ld
    cdef object ld_object
    
    self.name = name
    for d in ladspapath:
        try:
            if d[-1]!='/':
                d+='/'
            xname = d+name+".so"
            os.stat(xname)
            break;
        except:
            pass
        
    name=xname
    os.stat(name)
#    print "finding handle", name
    handle = dlopen( name, RTLD_NOW )
    if handle == NULL:
      raise Exception, dlerror()
    #print "got handle", name
    self.handle = PyCObject_FromVoidPtr(handle,NULL)
  
    get_ld = <LADSPA_Descriptor_Function>dlsym( handle, "ladspa_descriptor" )
    error = dlerror()
    if error != NULL:
      raise Exception, error
  
    self.plugins = []
    #print len(self.plugins)
    i = 0
    while 1:
#      print "get_ld", i
      ld = get_ld(i)
      if ld == NULL:
        break
#      print "   OK:", i
      ld_object = PyCObject_FromVoidPtr(ld,NULL) 
      plugin = Plugin( ld_object, 44100 )
      self.plugins.append( plugin )
      i = i + 1
#    print "done"
  def __len__(self):
    return len(self.plugins)
  def __getitem__(self, i):
    return self.plugins[i]
  def __str__(self):
    return "Lib: %s: %s"%( self.name, self.plugins )
  def __del__(self):
#    print "Lib.__del__", self.name
    cdef void*handle
    for plugin in self.plugins:
      plugin.cleanup()
    del self.plugins
    handle = PyCObject_AsVoidPtr( self.handle )
    if dlclose(handle) != 0:
      raise Exception, dlerror()
#    print "Lib.__del__: done"

#install_backtrace()

import os
#import time

# XX: check LADSPA_PATH environment variable
if os.environ.has_key("LADSPA_PATH"):
  ladspapath = os.environ["LADSPA_PATH"].split(":")
else:
  ladspapath = ["/usr/local/lib/ladspa/","/usr/lib/ladspa"]#,"/opt/ladspa/lib"]
libs = []
for path in ladspapath:
  try:
    for name in os.listdir( path ):
      if name.endswith(".so"):
        libs.append( name[:-3] )
  except OSError:
    pass
#print "libs", libs

#libs = []
#for name in plugins:
  ##print "Lib",name
  #libs.append( Lib(name) )

#plugins = 

if 0:
  lib = Lib("sine")
  print lib.plugins



