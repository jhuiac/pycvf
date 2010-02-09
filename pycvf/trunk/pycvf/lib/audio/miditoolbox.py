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


import midi
import midi.sequencer
try:
    import pypm
except:
    pass

import time
from itertools import ifilter,imap

from pycvf.lib.misc.ireduce import ireduce
import cPickle as pickle

def testmidi1():
    r=midi.midi.read_midifile("/jfli/inputs/karaoke/kar/Bureau/Dutronc_J_._J_aime_les_filles.kar")
    r.get_tempo().tempo
    lt=len(r.tracklist)
    #for t in r.tracklist:
    # les tracks sont justes des listes ordonnees
    timings=map(lambda x:x.tick,r.tracklist[2])
    texts=map(lambda x:x.data.strip(),r.tracklist[2])
    print ''.join(map(lambda x:x.data,r.tracklist[2])).decode('latin1').replace(u'/',u'\n').replace(u'\\',u'\n\n')


class PyPmMidiLazyOutput():
    def __init__(self,dev=3,latency=100):
        print pypm.GetDeviceInfo(dev)
        self.s=pypm.Output(dev, latency)
        basemiditime = pypm.Time()
        basetime=time.time
    def push(self,stamped_event):
        s.Write([stamped_event])



def testmidi2():
    r=midi.midi.read_midifile("/jfli/inputs/karaoke/kar/Bureau/Dutronc_J_._J_aime_les_filles.kar")

    MidiTime = pypm.Time()
    def tryencode(x):
        try:
            st=x.encode_tick()
            return [map(ord,x.encode()[len(st):]),MidiTime+x.tick]
        except:
            return [[],MidiTime+x.tick]


    def tryencode2(x):
        try:
            st=x.encode_tick()
            return [x.encode()[len(st):],MidiTime+x.tick]
        except:
            return ["",MidiTime+x.tick]

    #array(['ControlChangeEvent', 'EndOfTrackEvent', 'NoteOffEvent',
    #       'NoteOnEvent', 'ProgramChangeEvent', 'SetTempoEvent', 'SysExEvent',
    #       'TextMetaEvent', 'TimeSignatureEvent', 'TrackNameEvent']
    l=filter( lambda x:x[0]!=[],map( tryencode, filter(lambda e:(e.type!='TextMetaEvent') and (e.type!='TrackNameEvent')and (e.type!='TimeSignatureEvent')and (e.type!='EndOfTrackEvent'),r.iterevents())))
    for x in range(20,len(l)):
        #s.Write([x])
        print (x,l[x])
        st.Write([l[x]])
        while ((l[x][1]-3000)>pypm.Time()):
            time.sleep(0.1)

    #l=filter( lambda x:x[0]!=[],map( tryencode2, filter(lambda e:(e.type!='TextMetaEvent') and (e.type!='TrackNameEvent')and (e.type!='TimeSignatureEvent')and (e.type!='EndOfTrackEvent'),r.iterevents())))
    #for x in range(len(l)):
    #    #s.Write([x])
    #    print (x,l[x])
    #    s.WriteSysEx(l[x][1],l[x][0])
    #    while ((l[x][1]-3000)>pypm.Time()):
    #        time.sleep(0.1)




def flatmidi(r):
    #(control,program, lasttime, event)
    def transform_context(c,e):
        if (e.type=='ControlChangeEvent'):
            c[0][e.track]=(e.value,c[0][e.track][1])
            c=(c[0],None)
        elif (e.type=='ProgramChangeEvent'):
            c[0][e.track]=(c[0][e.track][0],e.value)
            c=(c[0],None)
        else:
            c=(c[0],[(c[0][e.track], e)])
        return c
    #r=midi.midi.read_midifile("/jfli/inputs/karaoke/kar/Bureau/Dutronc_J_._J_aime_les_filles.kar")
    lentracks=len(r.tracklist)
    context=([  (0,0) ] * lentracks,[])
    return ifilter(lambda x:(x!=None),imap(lambda x:x[1],ireduce(transform_context,r.iterevents(), context )))
#filter(lambda e: (e.type=='TrackNameEvent')or (e.type=='TimeSignatureEvent')or (e.type=='EndOfTrackEvent') or  (e.type=='SetTempoEvent'),r.iterevents())
#filter(lambda e: (e.type!='TrackNameEvent')and (e.type!='TimeSignatureEvent')and (e.type!='EndOfTrackEvent'),r.iterevents())
#'ControlChangeEvent', 'NoteOffEvent', 'NoteOnEvent',
#       'ProgramChangeEvent',, 'SysExEvent', 'TextMetaEvent'

def testmidi3():
    import midi
    import midi.sequencer
    r=midi.midi.read_midifile("/jfli/inputs/karaoke/kar/Bureau/Dutronc_J_._J_aime_les_filles.kar")
    s=midi.sequencer.sequencer.SequencerWrite()#{'alsa_port_name':'jfliapp','sequencer_stream':True,})
    s.set_nonblock(False)
    s.subscribe_port(128, 1)
    s.stop_sequencer()
    #map( s.data, r.iterevents())
    #s.Write(ChordList)
    #s.event_write(r.tracklist[6][100],tick=True)
    import time
    s.queue_get_tick_time()
    s.start_sequencer()
    s.change_tempo(10)
    for e in r.iterevents() :
        s.event_write(e)#,tick=True)


class SimpleMidiReader:
    def __init__(self,filename,observer=None):
        self.filename=filename
        self.midifile=midi.midi.read_midifile(filename)
        self.observer=observer
        self.cp=self.midifile.iterevents()
    def __iter__(self):
        return self.midifile.iterevents()
    def step(self):
        try:
            x=self.cp.next()
            if (self.observer):
                self.observer(x)
            return True
        except:
            return False
    def run(self):
        while (self.step()):
            pass


class SimpleEMidiReader:
    def __init__(self,observer=None):
        self.filename=None
        self.midifile=None
        self.observer=observer
        self.cp=None
        self.lasttime=0
    def open(self,filename):
        self.filename=filename
        self.midifile=midi.midi.read_midifile(filename)
        self.cp=flatmidi(self.midifile).__iter__()
        self.lasttime=0
    def open_location(self,filename,seekt):
        self.filename=filename
        self.midifile=midi.midi.read_midifile(filename)
        self.cp=flatmidi(self.midifile).__iter__()
        self.lasttime=seekt
        self.seektime(seekt)
    def open_location_s(self,locs):
        filename,seekt=pickle.loads(locs)
        self.filename=filename
        self.midifile=midi.midi.read_midifile(filename)
        self.observer=observer
        self.cp=flatmidi(self.midifile).__iter__()
        self.lasttime=seekt
        self.seektime(seekt)
    def __iter__(self):
        return self.cp
    def seektime(self,t):
        self.cp=ifilter(lambda x:x[0][1].tick>=t, flatmidi(self.midifile).__iter__())
    def step(self):
        try:
            x=self.cp.next()
            try:
                self.lasttime=x[0][1].tick
            except:
                pass
            if (self.observer):
                self.observer(x)
            return True
        except StopIteration:
            return False
    def run(self):
        while (self.step()):
            pass
    def get_cur_location(self):
        return (self.filename,self.lasttime)
    def get_cur_location_s(self):
        return pickle.dumps((self.filename,self.lasttime))
    def set_observer(self,observer):
        self.observer=observer



class SimpleMidiRenderer():
    def __init__(self,port=(128,1)):
        self.s=midi.sequencer.sequencer.SequencerWrite()#{'alsa_port_name':'jfliapp','sequencer_stream':True,})
        self.s.set_nonblock(False)
        self.s.subscribe_port(port[0], port[1])
        self.s.stop_sequencer()
        self.s.queue_get_tick_time()
        self.s.start_sequencer()
    def __del__(self):
        self.s.stop_sequencer()
    def push(self, ev):
        self.s.event_write(ev)

class SimpleEMidiRenderer():
    def __init__(self,port=(128,1)):
        self.s=midi.sequencer.sequencer.SequencerWrite()#{'alsa_port_name':'jfliapp','sequencer_stream':True,})
        self.s.set_nonblock(False)
        self.s.subscribe_port(port[0], port[1])
        self.s.stop_sequencer()
        self.s.queue_get_tick_time()
        self.s.start_sequencer()
    def __del__(self):
        self.s.stop_sequencer()
    def push(self, ev):
        ## should we rewrite the program changes ????
        self.s.event_write(ev[0][1])



def tonotes(m):
    from pycvf.lib.misc.ireduce import ireduce
    def _tonotes(c,n):
        if (n.velocity==0):
            c[0][(n.pitch,n.track)]=n.tick
            return [c[0],None]
        else:
            try:
                r=[n.tick,n.pitch,n.velocity,c[0][(n.pitch,n.track)]-n.tick,n.track]
                c[0][(n.pitch,n.track)]=n.tick
                return [c[0],r]
            except KeyError:
                r=[n.tick,n.pitch,n.velocity,min(m.endoftrack.tick,n.tick+100),n.track]
                c[0][(n.pitch,n.track)]=n.tick
                return [c[0],r]

    l=filter(lambda x:x.type[:4]=="Note", m.iterevents())
    l.reverse()
    l=filter(lambda x:x!=None,map(lambda x:x[1],ireduce(_tonotes,l,[{},None])))
    l.reverse()
    return l


def todnotes(m):
    l=tonotes(m)
    lt=[0]*len(m.tracklist)
    def _dtimenotes(x,n):
        et=n[0]
        nn=n
        nn[0]-=x[0][n[4]]
        x[0][n[4]]=et
        return [x[0],x[1]+[nn]]
    return reduce(_dtimenotes,l,[lt, [] ])[1]


class SimpleNMidiReader:
    def __init__(self,observer=None,tonotes=todnotes):
        self.filename=None
        self.midifile=None
        self.observer=observer
        self.cp=None
        self.lasttime=0
        self.tonotes=tonotes
    def open(self,filename):
        self.filename=filename
        self.midifile=midi.midi.read_midifile(filename)
        self.cp=self.tonotes(self.midifile).__iter__()
        self.lasttime=0
    def open_location(self,filename,seekt):
        self.filename=filename
        self.midifile=midi.midi.read_midifile(filename)
        self.cp=self.tonotes(self.midifile).__iter__()
        self.lasttime=seekt
        self.seektime(seekt)
    def open_location_s(self,locs):
        filename,seekt=pickle.loads(locs)
        self.filename=filename
        self.midifile=midi.midi.read_midifile(filename)
        self.observer=observer
        self.cp=self.tonotes(self.midifile).__iter__()
        self.lasttime=seekt
        self.seektime(seekt)
    def __iter__(self):
        return self.cp
    def seektime(self,t):
        self.cp=ifilter(lambda x:x[0]>=t,self.tonotes(self.midifile) )
    def step(self):
        try:
            x=self.cp.next()
            #try:
            self.lasttime=x[0]
            #except:
            #  pass
            if (self.observer):
                self.observer(x)
            return True
        except StopIteration:
            return False
    def run(self):
        while (self.step()):
            pass
    def get_cur_location(self):
        return (self.filename,self.lasttime)
    def get_cur_location_s(self):
        return pickle.dumps((self.filename,self.lasttime))
    def set_observer(self,observer):
        self.observer=observer


def totab(m):
    from pycvf.lib.misc.ireduce import ireduce
    def _tonotes(c,n):
        if (n.velocity==0):
            c[0][(n.pitch,n.track)]=n.tick
            return [c[0],None]
        else:
            try:
                r=((n.tick,n.pitch),(c[0][(n.pitch,n.track)],n.pitch),n.velocity,n.track)
                c[0][(n.pitch,n.track)]=n.tick
                return [c[0],r]
            except KeyError:
                r=((n.tick,n.pitch),(min(midireader.midifile.endoftrack.tick,n.tick+100),n.pitch),n.velocity,n.track)
                c[0][(n.pitch,n.track)]=n.tick
                return [c[0],r]
    l=filter(lambda x:x.type[:4]=="Note", m.iterevents())
    l.reverse()
    l=filter(lambda x:x!=None,map(lambda x:x[1],ireduce(_tonotes,l,[{},None])))
    l.reverse()
    return l

def partialtab(m,tfrom,tto):
    t=totab(m)
    return filter(lambda x: (x[0][0]<tto) and (x[1][0]>=tfrom), t)


from reportlab.lib.units import cm
from reportlab.pdfgen.pycanvas import Canvas
from reportlab.lib.pagesizes import *
from reportlab.lib.pagesizes import A4
(A4w,A4h)=A4
A4L=(A4h,A4w)


def draw_tab(midi,filename,pagesize=A4L,encoding='latin1',tickperpages=8000):
    pal=[ (0,0,0),(0,0,1),(0,1,0),(1,0,0),(0,1,1),(1,1,0),(1,0,1),(0.5,0.5,0.5),(0,0,0.5),(0,0.5,0),(0.5,0,0)
         ,(0.5,0,0.5),(0,0.5,0.5),(0.5,0.5,0),(1,0,0.5),(0,0.5,1),(0.5,0,1),(0,1,0.5),(1,0.5,0),(0.5,0,1),(1,1,0.5),(1,0.5,1),
         (0.5,1,1),(1,1,0.5),(1,0.5,1),(0.5,1,1),(1,0.5,0.5),(0.5,0.5,1),(0.5,0.5,1),(0.5,1,0.5),(1,0.5,0.5),(0.5,0.5,1) ]
    canvas=Canvas(filename,pagesize=pagesize)
    canvas.setTitle("sampletab");
    leftmargin,bottommargin,rightmargin,topmargin=(1*cm,1*cm,1*cm,1*cm)
    L=pagesize[0]
    l=pagesize[1]
    leftstart,bottomstart,rightend,topend=(leftmargin,bottommargin,L-rightmargin,l-topmargin)
    hspace=rightend-leftstart
    vspace=topend-bottomstart
    eot=midireader.midifile.endoftrack.tick
    dtime=tickperpages
    for page in range(math.ceil(eot/tickperpages)):
        btime=page*tickperpages
        etime=btime+dtime
        for i in partialtab(midi,btime,etime):
            canvas.setLineWidth(i[2]*5./128.)
            canvas.setStrokeColorRGB(*pal[i[3]])
            canvas.line(leftstart+(max(i[0][0]-btime,0)*hspace/dtime),bottomstart+(i[0][1]*vspace/128),
                        leftstart+(min(i[1][0]-btime,etime-btime)*hspace/dtime),bottomstart+(i[1][1]*vspace/128))
        canvas.setStrokeColorRGB(0,0,0)
        canvas.setFont("Helvetica", 4)
        for e in filter(lambda x:(x.type=="TextMetaEvent") and (x.tick>=btime) and (x.tick<etime) ,midi.iterevents()):
            print e.data.decode(encoding)
            canvas.drawString(leftstart+((e.tick-btime)*hspace/dtime),2.1*cm, e.data.decode(encoding))
        canvas.showPage()
    canvas.save()


#
#     time.sleep(0.01)
#
#
#    r.tracklist[6][100]
#
#
#    findtextrack()
#    snd_seq_subscribe_port()
#snd_seq_set_input_buffer_size(...)
#
#    snd_seq_set_output_buffer_size(...)
#snd_seq_system_info(...)
#    snd_seq_set_client_name(...)
# snd_seq_open(...)

## we define a virtual sequencer that knows at each moment which are the notes on
## and which are the notes off
