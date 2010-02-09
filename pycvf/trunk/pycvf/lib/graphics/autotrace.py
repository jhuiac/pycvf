#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under Lesser GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


from ctypes import *
# using file "/usr/include/autotrace/types.h"
# using file "/usr/include/autotrace/autotrace.h"


try:
  _autotracelib = cdll.LoadLibrary('libautotrace.so')
except:
  _autotracelib = cdll.LoadLibrary('libautotrace.dll')	


try:
  _libc=cdll.msvcrt    
except:
  _libc=CDLL('libc.so.6')
  
class _at_output_opts_type(Structure):
	_fields_ = [
		('dpi', c_int),
	]

at_output_opts_type = _at_output_opts_type

at_real = c_float

class _at_real_coord(Structure):
	_fields_ = [
		('x', at_real),
		('y', at_real),
		('z', at_real),
	]

at_real_coord = _at_real_coord

# enumeration _at_polynomial_degree
AT_LINEARTYPE = 1
AT_QUADRATICTYPE = 2
AT_CUBICTYPE = 3
AT_PARALLELELLIPSETYPE = 4
AT_ELLIPSETYPE = 5
AT_CIRCLETYPE = 6

at_polynomial_degree = c_int

class _at_spline_type(Structure):
	_fields_ = [
		('v', at_real_coord*4),
		('degree', at_polynomial_degree),
		('linearity', at_real),
	]
	def __dict__(self):
		return {'v':((self.v[0].x,self.v[0].y,self.v[0].z ),
		            (self.v[1].x,self.v[1].y,self.v[1].z ), 
			    (self.v[2].x,self.v[2].y,self.v[2].z ),
			    (self.v[3].x,self.v[3].y,self.v[3].z )),
			'degree': self.degree,
			'linearity':   self.linearity
		      }
        def get_degree(self):
            return self.degree
        def get_linearity(self):
            return self.linerarity
        def get_v(self):
                  return ((self.v[0].x,self.v[0].y,self.v[0].z ),
		            (self.v[1].x,self.v[1].y,self.v[1].z ), 
			    (self.v[2].x,self.v[2].y,self.v[2].z ),
			    (self.v[3].x,self.v[3].y,self.v[3].z ))

at_spline_type = _at_spline_type

class _at_color_type(Structure):
	_fields_ = [
		('r', c_ubyte),
		('g', c_ubyte),
		('b', c_ubyte),
	]
        def get_r():
            return self.r
        def get_g():
            return self.g
        def get_b():
            return self.b        

at_color_type = _at_color_type

class _at_spline_list_type(Structure):
	_fields_ = [
		('data', POINTER(at_spline_type)),
		('length', c_uint),
		('clockwise', c_uint),
		('color', at_color_type),
		('open', c_uint),
	]
	def __iter__(self):
		for i in range(self.length):
			yield self.data[i]
	def __dict__(self):
		return {'spline': map(lambda x:x.__dict__(), self), 
	                'clockwise':self.clockwise,
			'color':(self.color.r, self.color.g,self.color.b),
			'open':(self.open)
			}
        def get_spline(self):
            return map(lambda x:x.__dict__(), self)
        def get_clockwise(self):
            return self.clockwise
        def get_open(self):
            return self.open        
        def get_color(self):
            return (self.color.r, self.color.g,self.color.b),      
        def get_perimeter(self):
            it=iter(self)
            p0=po=it.next()
            s=0
            try:
                while True:
                  pi=it.next()
                  pov=po.get_v()
                  piv=pi.get_v()
                  s+=((pov[0][0]-piv[0][0])**2 + (pov[0][1]-piv[0][1])**2)**.5
                  po=pi
            except StopIteration:
                pass
            if (not self.open):
                pi=p0
                pov=po.get_v()
                piv=pi.get_v()                
                s+=((pov[0][0]-piv[0][0])**2 + (pov[0][1]-piv[0][1])**2)**.5
            return s
        def get_perimeter_points(self):
            import numpy
            r=[]
            try:
              for x in self:
                  r.append(x.get_v()[0])
                  
            except StopIteration:
                pass            
            return numpy.array(r)
        def get_pcenter(self):
            return get_perimeter_points(self).mean(axis=0)
        def get_pstd(self):
            return get_perimeter_points(self).std(axis=0)        
        def get_size(self):
            return get_perimeter_points(self).ptp(axis=0)        

at_spline_list_type = _at_spline_list_type

class _at_spline_list_array_type(Structure):
	_fields_ = [
		('data', POINTER(at_spline_list_type)),
		('length', c_uint),
		('height', c_ushort),
		('width', c_ushort),
		('background_color', POINTER(at_color_type)),
		('centerline', c_uint),
		('preserve_width', c_uint),
		('width_weight_factor', at_real),
	]
	def __iter__(self):
		for i in range(self.length):
			yield self.data[i]
	def __dict__(self):
		return {'splines': map(lambda x:x.__dict__(), self), 
	                'height':self.height,  
			'width':self.width,
			'background_color':self.background_color and (self.background_color.contents.r,self.background_color.contents.g,self.background_color.contents.b) or None,
			'centerline':self.centerline,
			'preserve_width':self.preserve_width,
			'width_weight_factor':self.width_weight_factor
			}
        def get_splines(self):
            return list(self)
        def get_height(self):
            return self.height
        def get_width(self):
            return self.width
        def get_background_color(self):
            return self.background_color and (self.background_color.contents.r,self.background_color.contents.g,self.background_color.contents.b) or None,
        def get_centerliner(self):
            return self.centerline
        def get_preserve_width(self):
            return self.preserve_width
        def get_width_weight_factor(self):
            return self.width_weight_factor
        
        
        
# enumeration _at_msg_type
AT_MSG_FATAL = 1
AT_MSG_WARNING = 2

class _at_bitmap_type(Structure):
	_fields_ = [
		('height', c_ushort),
		('width', c_ushort),
		('bitmap', POINTER(c_ubyte)),
		('np', c_uint),
	]

at_bitmap_type = _at_bitmap_type

class _at_input_opts_type(Structure):
	_fields_ = [
		('background_color', POINTER(at_color_type)),
	]

at_input_opts_type = _at_input_opts_type

class _at_fitting_opts_type(Structure):
	_fields_ = [
		('background_color', POINTER(at_color_type)),
		('color_count', c_uint),
		('corner_always_threshold', at_real),
		('corner_surround', c_uint),
		('corner_threshold', at_real),
		('error_threshold', at_real),
		('filter_iterations', c_uint),
		('line_reversion_threshold', at_real),
		('line_threshold', at_real),
		('remove_adjacent_corners', c_uint),
		('tangent_surround', c_uint),
		('despeckle_level', c_uint),
		('despeckle_tightness', at_real),
		('centerline', c_uint),
		('preserve_width', c_uint),
		('width_weight_factor', at_real),
	]

class _at_coord(Structure):
	_fields_ = [
		('x', c_ushort),
		('y', c_ushort),
	]

at_fitting_opts_type = _at_fitting_opts_type

at_spline_list_array_type = _at_spline_list_array_type

at_string = POINTER(c_char)

at_address = c_void_p

at_coord = _at_coord

at_msg_type = c_int

at_msg_func = POINTER(CFUNCTYPE(None,POINTER(c_char),c_int,c_void_p))

at_input_read_func = POINTER(CFUNCTYPE(at_bitmap_type,POINTER(c_char),POINTER(at_input_opts_type),POINTER(CFUNCTYPE(None,POINTER(c_char),c_int,c_void_p)),c_void_p))

at_output_write_func = POINTER(CFUNCTYPE(c_int,c_void_p,POINTER(c_char),c_int,c_int,c_int,c_int,POINTER(at_output_opts_type),_at_spline_list_array_type,POINTER(CFUNCTYPE(None,POINTER(c_char),c_int,c_void_p)),c_void_p))

at_progress_func = POINTER(CFUNCTYPE(None,c_float,c_void_p))

at_testcancel_func = POINTER(CFUNCTYPE(c_uint,c_void_p))

at_fitting_opts_new = CFUNCTYPE(POINTER(at_fitting_opts_type),)

at_fitting_opts_copy = CFUNCTYPE(POINTER(at_fitting_opts_type),POINTER(at_fitting_opts_type))

at_fitting_opts_free = CFUNCTYPE(None,POINTER(at_fitting_opts_type))

at_input_opts_new = CFUNCTYPE(POINTER(at_input_opts_type),)

at_input_opts_copy = CFUNCTYPE(POINTER(at_input_opts_type),POINTER(at_input_opts_type))

at_input_opts_free = CFUNCTYPE(None,POINTER(at_input_opts_type))

at_output_opts_new = CFUNCTYPE(POINTER(at_output_opts_type),)

at_output_opts_copy = CFUNCTYPE(POINTER(at_output_opts_type),POINTER(at_output_opts_type))

at_output_opts_free = CFUNCTYPE(None,POINTER(at_output_opts_type))

at_bitmap_read = CFUNCTYPE(POINTER(at_bitmap_type),at_input_read_func,at_string,POINTER(at_input_opts_type),at_msg_func,at_address)

at_bitmap_new = CFUNCTYPE(POINTER(at_bitmap_type),c_ushort,c_ushort,c_uint)

at_bitmap_copy = CFUNCTYPE(POINTER(at_bitmap_type),POINTER(at_bitmap_type))

at_bitmap_get_width = CFUNCTYPE(c_ushort,POINTER(at_bitmap_type))

at_bitmap_get_height = CFUNCTYPE(c_ushort,POINTER(at_bitmap_type))

at_bitmap_get_planes = CFUNCTYPE(c_ushort,POINTER(at_bitmap_type))

at_bitmap_free = CFUNCTYPE(None,POINTER(at_bitmap_type))

at_splines_new = CFUNCTYPE(POINTER(at_spline_list_array_type),POINTER(at_bitmap_type),POINTER(at_fitting_opts_type),at_msg_func,at_address)

at_splines_new_full = CFUNCTYPE(POINTER(at_spline_list_array_type),POINTER(at_bitmap_type),POINTER(at_fitting_opts_type),at_msg_func,at_address,at_progress_func,at_address,at_testcancel_func,at_address)

at_splines_write = CFUNCTYPE(None,at_output_write_func,c_void_p,at_string,POINTER(at_output_opts_type),POINTER(at_spline_list_array_type),at_msg_func,at_address)

at_splines_free = CFUNCTYPE(None,POINTER(at_spline_list_array_type))

at_color_new = CFUNCTYPE(POINTER(at_color_type),c_ubyte,c_ubyte,c_ubyte)

at_color_copy = CFUNCTYPE(POINTER(at_color_type),POINTER(at_color_type))

at_color_equal = CFUNCTYPE(c_uint,POINTER(at_color_type),POINTER(at_color_type))

at_color_free = CFUNCTYPE(None,POINTER(at_color_type))

at_input_get_handler = CFUNCTYPE(at_input_read_func,at_string)

at_input_get_handler_by_suffix = CFUNCTYPE(at_input_read_func,at_string)

at_input_list_new = CFUNCTYPE(POINTER(POINTER(c_char)),)

at_input_list_free = CFUNCTYPE(None,POINTER(POINTER(c_char)))

at_input_shortlist = CFUNCTYPE(POINTER(c_char),)

at_output_get_handler = CFUNCTYPE(at_output_write_func,at_string)

at_output_get_handler_by_suffix = CFUNCTYPE(at_output_write_func,at_string)

at_output_list_new = CFUNCTYPE(POINTER(POINTER(c_char)),)

at_output_list_free = CFUNCTYPE(None,POINTER(POINTER(c_char)))

at_output_shortlist = CFUNCTYPE(POINTER(c_char),)

at_version = CFUNCTYPE(POINTER(c_char),c_uint)

at_home_site = CFUNCTYPE(POINTER(c_char),)

##
##
##

at_bitmap_new=at_bitmap_new(("at_bitmap_new",_autotracelib))
at_output_get_handler_by_suffix=at_output_get_handler_by_suffix(("at_output_get_handler_by_suffix",_autotracelib))
at_bitmap_free=at_bitmap_free(("at_bitmap_free",_autotracelib))
at_fitting_opts_new=at_fitting_opts_new(("at_fitting_opts_new",_autotracelib))
at_output_opts_new=at_output_opts_new(("at_output_opts_new",_autotracelib))
at_splines_new=at_splines_new(("at_splines_new",_autotracelib))
at_splines_write=at_splines_write(("at_splines_write",_autotracelib))
at_splines_free=at_splines_free(("at_splines_free",_autotracelib))


import numpy

#xxx=0

def NumPy2AtBitmap(im):
	global xxx
	from pycvf.lib.misc.hack import rwbuffer_at
	#atbm=at_bitmap_type()
	atbm=at_bitmap_new(im.shape[1],im.shape[0],(len(im.shape)==3) and (im.shape[2]) or 1)
	numpy.ndarray(buffer=rwbuffer_at(cast(pointer(atbm.contents.bitmap),POINTER(c_ulong)).contents.value,atbm.contents.width*atbm.contents.height*atbm.contents.np ),shape=(atbm.contents.width,atbm.contents.height,atbm.contents.np),dtype=numpy.uint8)[:,:,:]=im.reshape(im.shape[1],im.shape[0],(len(im.shape)==3) and (im.shape[2]) or 1)
	return atbm


class AutoTrace:
	class AutoTraceResult(object):
		def __init__(self,splines):
			self.splines=splines
		def __del__(self,):
			at_splines_free(self.splines)
		def __iter__(self):
		       return iter(self.splines.contents)
		def __dict__(self):
		       return self.splines.contents.__dict__()
                def get_object(self):
                    return self.splines.contents
	def __init__(self):
		self.opts = at_fitting_opts_new()
	        self.output_opts = at_output_opts_new()
	def trace(self,img):
		ab=NumPy2AtBitmap(img)
		splines = at_splines_new(ab, 
	                         self.opts, 
		     	         at_msg_func(),  
				 at_address())	
		at_bitmap_free(ab)
		return AutoTrace.AutoTraceResult(splines)				 
        def output(self,filename,tracing):
		a=at_output_get_handler_by_suffix(c_char_p(filename.split('.')[-1]))
		b=_libc.fopen(filename,"wb")
	        at_splines_write(a,b,"",self.output_opts,
				tracing.splines,
				at_msg_func(),
				at_address()
				)	
		_libc.fclose(b)                                
				 
if __name__=="__main__":
	import scipy
	
	xl=scipy.lena().astype(numpy.uint8).reshape(512,512,1)
	at=AutoTrace()
	at.opts.contents.despeckle_level=10
	print at.trace(xl).__dict__()

				