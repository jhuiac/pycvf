#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
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


# -*- coding: utf-8 -*-

import re, os, math, random, time,sys, traceback, datetime
from pycvf.nodes.sequencereader import *
from pycvf.lib.midi.miditoolbox import *

default_databasedir="/databases/karaoke/col1"

from pycvf.core import database
class ContentsDatabase(database.ContentsDatabase):
  CONTENT_TYPE="midinotes"
  def __init__(self,databasedir=default_databasedir):
     self.databasedir=databasedir
     
  def __iter__(self):
    allmidis=[]
    for xdir in [ self.databasedir ]:
        try:
            if (xdir[-1]!='/'): xdir+='/'
            allmidis.extend(filter(lambda x:re.match("(.*).(mid|kar)",x,re.I), map(lambda x:xdir+x,os.listdir(xdir))))
        except:
            pass
    random.shuffle(allmidis)
    try:
        for filename in allmidis:
          midireader=SimpleEMidiReader(filename)
          midireader.open(filename)
          yield (midireader,filename)
          #yield SequenceReader(u'\n'.join(xs[bl:-1]),a=x)
    except StopIteration:
        pass
  @staticmethod
  def display(elr):
     render=SimpleEMidiRenderer()
     elr.set_observer(render.push)
     elr.run()


          

#def readmidifile(filename, winprec=0.3,winpost=0.3):
#    midireader=SimpleEMidiReader(filename)
#    midireader.open(filename)
#    tempo=float(midireader.midifile.get_tempo().tempo)
#    winprec=int(tempo*winprec)
#    winpost=int(tempo*winpost)
#    #midireader.set_observer(xev)
#    #midireader.run()
#    #sev=filter(lambda ev:type(ev)==midi.midi.TextMetaEvent,midireader.midifile.iterevents())
#    alltxtevs=map(lambda x:( x.data, x.track,  x.tick),filter(lambda x:x.data[0]!='@',filter(lambda ev:type(ev)==midi.midi.TextMetaEvent,midireader.midifile.iterevents())))
#    cev={}
#    cev['s']=0
#    cev['l']=[]
#    cev['t']=''
#    lev=[]
#    for x in alltxtevs:
#        cev['l'].append(x)
#        cev['e']=x[2]
#        x0=x[0].strip('\x00')
#        cev['t']+=re.match('([^ \\n\\/\\?!\\\\.;,]*)([ \\n\\/\\?!\\\\.;,]*)(.*)',x0).group(1).lower()
#        while (re.match('([^ \\n\\?!\\/\\\\.;,]*)([ \\n\\?!\\/\\\\.;,])(.*)',x0)):
#            lev.append(cev)
#            cev={}
#            cev['s']=x[2]
#            cev['e']=x[2]
#            cev['l']=[x]
#            x0=re.match('([^ \\n\\?!\\/\\\\.;,]*)([ \\n\\?!\\/\\\\.;,])(.*)',x0).group(3).lower()
#            cev['t']=re.match('([^ \\n\\/\\?!\\\\.;,]*)([ \\n\\/\\?!\\\\.;,]*)(.*)',x0).group(1).lower()
#    lev.append(cev) 
#    m=map(lambda x:(x['t'],x['s']-winprec, x['e']-winpost,[]),filter(lambda x:len(x['t'])>0,lev))
#    class xevreader:
#        def __init__(self,m,tempo):
#            self.m=m
#            self.memorizeev=numpy.zeros((128,))
#            self.lasttick=0
#            self.tempo=tempo
#        def f(self,ev):
#            daev=ev[0][1]
#            t=daev.tick
#            if (type(daev)==midi.midi.NoteOnEvent):
#                self.memorizeev[daev.pitch]+=float(daev.velocity)/127.
#            elif (type(daev)==midi.midi.NoteOffEvent):
#                self.memorizeev[daev.pitch]/=4.
#            self.memorizeev*=0.25**(float(t-self.lasttick)/tempo) 
#            self.lasttick=daev.tick
#            for k in range(len(self.m)):
#                if ((self.m[k][1]<=t )  and (t< self.m[k][2])):
#                    self.m[k][3].append(ev)
#    xevr=xevreader(m,tempo)
#    midireader.set_observer(xevr.f)
#    midireader.run()
#    m=xevr.m
#    return m