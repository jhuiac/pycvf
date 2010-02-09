# -*- coding: utf-8 -*-
import numpy

def hamming(lw):
   return 0.54-0.46*numpy.cos(numpy.pi*2.*numpy.arange(0,1.,1./lw))

def hamming0(lw):
   return 0.54-0.46*numpy.cos(numpy.pi*2*numpy.arange(0,1.,1./lw))

def hann(lw):
   return 0.5*(1-numpy.cos(numpy.pi*2*numpy.arange(0,1.,1./lw)))

def hann0(lw):
   return 0.5*(1+numpy.cos(numpy.pi*2*numpy.arange(0,1.,1./lw)))

def lanczoc(lw):
   return numpy.sinc(numpy.arange(0,1.,1./lw)*2-1)

def lanczoc0(lw):
   return numpy.sinc(numpy.arange(0,1.,1./lw)*2)

def blackman(lw,alpha=0.16):
   a0=(1-alpha)/2
   a1=1./2.
   a2=alpha/2.
   return a0+a1*numpy.cos(numpy.pi*2*numpy.arange(0,1.,1./lw))+a2*numpy.cos(numpy.pi*4*numpy.arange(0,1.,1./lw))

def gauss(lw,sigma=0.4):
   return numpy.exp(-.5*(numpy.arange(-.5,.5,1./lw)/sigma)**2 )

