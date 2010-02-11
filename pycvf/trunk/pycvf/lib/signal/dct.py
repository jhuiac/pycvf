# -*- coding: utf-8 -*-

import os
import numpy
import scipy.weave

def dct(sig,basefun="dct"):  
  D=numpy.double
  assert(sig.ndim==1)
  assert(sig.dtype==D)
  assert(((sig.shape[0]-1)&(sig.shape[0]))==0),"Must be a power of 2"
  try: 
    sig.data
  except:
    sig=sig.copy('C')
  nr=sig.shape[0]
  J=0
  while (1<<J!=nr):
     J+=1
  #J+=1
  tmp=numpy.ndarray(shape=(4*sig.shape[0]),dtype=D);
  tmp[:nr]=sig
  cd=os.path.dirname(__file__)
  if len(cd)==0:
     cd=os.getcwd()
  scipy.weave.inline( basefun+"(&tmp[0],&tmp[nr],J,&tmp[2*nr]);",['tmp','nr','J'], 
  support_code=file(os.path.join(cd,basefun+'.c')).read() +file(os.path.join(cd,'dht.c')).read(),
  include_dirs= [ cd ] ,
  compiler="gcc", extra_compile_args=["-O3"] )
  return tmp[:nr].copy('C')


def dct_ii(sig):
    return dct(sig,basefun="dct")

def dct_iii(sig):
    return dct(sig,basefun="idct")

def dct_iv(sig,basefun="dct4"):
  D=numpy.double
  assert(sig.ndim==1)
  assert(sig.dtype==D)
  assert(((sig.shape[0]-1)&(sig.shape[0]))==0),"Must be a power of 2"
  try: 
    sig.data
  except:
    sig=sig.copy('C')
  nr=sig.shape[0]
  J=0
  while (1<<J!=nr):
     J+=1
  #J+=1
  wcp=numpy.zeros(shape=(sig.shape[0]),dtype=D); 
  tmp=numpy.ndarray(shape=(8*sig.shape[0]),dtype=D);
  tmp[:nr]=sig
  cd=os.path.dirname(__file__)
  if len(cd)==0:
     cd=os.getcwd()
  scipy.weave.inline( basefun+"(sig,wcp,nr,tmp);",['sig','wcp','nr','tmp','J'], 
  support_code=file(os.path.join(cd,basefun+'.c')).read() +file(os.path.join(cd,'dht.c')).read(),
  include_dirs= [ cd ] ,
  compiler="gcc", extra_compile_args=["-O3"] )
  return wcp

def idst_ii(sig):
    return dct(sig,basefun="dst")

def idst_iii(sig):
    return dct(sig,basefun="idst")

