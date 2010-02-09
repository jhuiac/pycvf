#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pandac.PandaModules import loadPrcFileData
loadPrcFileData("", "fullscreen 1")
from pandac.PandaModules import *
import sys,os,re, stat
import direct.directbase.DirectStart
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
import numpy
import pickle
from pycvf.core.errors import *
from pycvf.core.generic_application import *
from pycvf.lib.ui.panda import picker
from pycvf.lib.graphics.imgfmtutils import NumPy2PIL
from pycvf.indexes import load_index
import scipy

cmr12 = loader.loadFont('cmr12.egg')
 
class World(DirectObject):
    def enable_picking(self):
        self.lastHiliteObj = []

        def setHiliteCol(pickObj):
          pickObj.setScale(2)
          self.lastHiliteObj.append(pickObj)

        def setNormCol():
          self.lastHiliteObj[0].setScale(1)
          self.lastHiliteObj.pop()

        def hiliteTask(task):
          if self.lastHiliteObj != []:
              setNormCol()
          if base.mouseWatcherNode.hasMouse() == True:
            m=base.mouseWatcherNode.getMouse()
            if self.mousepicker.getObjectHit(m) != None:
                setHiliteCol(self.mousepicker.getPickedObj())
         
          return Task.cont           
        taskMgr.add(hiliteTask,'hiliteTask')

    def explore_nn(self,entry):
        app=self.app
        print "QUERY=", entry
        keys=app.mdl.process_path([entry[0]],[entry[1]],app.key.value,lambda x:x)
        keys=numpy.array(keys)
        xxx=map(lambda y:map(lambda x:(app.vdb[x[0][0]],x[0][0],x[1]),y),app.idx.getitems(keys,self.nq))
        #print xxx        

        ### our main node
        self.iconwheel = render.attachNewNode(PandaNode("iconwheel"))
        ## a card maker will create planes for us
        cm=CardMaker('')

        cm.setFrame(-5,5,-5,5)       

        self.ld=xxx[0]
        lld=len(self.ld)         

        self.iconwheelMovement = self.iconwheel.hprInterval(50,Point3(360,0,0))                          
        MAXR=10
        for y in range(lld):
             nn = self.iconwheel.attachNewNode(cm.generate())
             nnr = self.iconwheel.attachNewNode(cm.generate()) 
             nn.setColor(1,0,0,1)
             nnr.reparentTo(nn)
             nnr.setH(180)
             nnr.setColor(1,1,1,1)
             texth = TextNode('hicond%04d'%(y,))
             texth.setText(unicode(self.ld[y][2]).encode('utf8'))
             texth.setTextColor(0,0,0,1)
             textb = TextNode('bicond%04d'%(y,))
             textb.setText(unicode(self.ld[y][2]).encode('utf8'))
             textb.setTextColor(0,0,0,1)
             tnpb = self.iconwheel.attachNewNode(textb)
             tnph = self.iconwheel.attachNewNode(texth)
             z=numpy.exp(1j*numpy.pi*2*(y%MAXR)/min(lld,MAXR))
             z*=3*min(lld,MAXR)*min(10,(self.ld[y][2]/1000.))
             w2=texth.getWidth()/2
             nn.setPos(numpy.real(z),numpy.imag(z) , (y//MAXR)*8)
             tnpb.reparentTo(nnr)
             tnph.reparentTo(nnr)
             tnpb.setPos(-w2,0 ,-3)
             tnph.setPos(-w2,0 ,3)
             texfilename=os.tmpnam()+".jpg"
             img=NumPy2PIL(255-self.ld[y][0][:,:,0])
             img.save(texfilename)
             tex=loader.loadTexture(texfilename)
             nn.setTexture(tex)
             nnr.setTexture(tex)
             os.remove(texfilename)
             nn.setTag("action",str(pickle.dumps((-1,(self.ld[y][0],self.ld[y][1])))))
             nn.lookAt(base.camera)
             self.nn = self.iconwheel.hprInterval(0,Point3(0,0,0)) 
             self.mousepicker.makePickable(nn)
        self.iconwheelMovement.loop()                    
        base.camera.reparentTo(render)
        base.camera.setPos(30,-45,26)
        base.camera.lookAt(0,0,0)


    def resetscene(self):
        self.iconwheel.removeNode()
        del self.iconwheel

    #def gotodir(self,dirname):
        #self.resetscene()
        #self.opendir(dirname)

    #def goup(self):
        #self.gotodir(os.path.join(self.curdir,".."))

    def __init__(self):
        ##  basic settings
        self.movieid=0
        self.curdir=( os.getcwd() if len(sys.argv)<2 else sys.argv[1])
        base.setBackgroundColor(0,0,0,1)
        base.camLens.setNearFar(1.0,10000)
        base.camLens.setFov(75)

        self.icontex={} ## this is our tecture cache
        self.mousepicker=picker.Picker()
        self.lastClicked=None
        self.accept('escape',sys.exit)
#        self.accept('u',self.goup)
        self.accept("mouse1", self.click)
        self.accept("mouse1-up", self.release_click) 
        self.enable_picking()

    def click(self):
      #print "click" ,self.lastHiliteObj[0].ls()#, self.lastHiliteObj[0].getName(),self.lastHiliteObj[0].listTags(),self.lastHiliteObj[0].getKey()#,self.lastHiliteObj[0].getPythonTag()
      if len(self.lastHiliteObj):
         self.lastClicked=self.lastHiliteObj[0]
     
    def release_click(self):
      #print "click rel"  ,self.lastHiliteObj 
      if len(self.lastHiliteObj) and (self.lastHiliteObj[0]==self.lastClicked):
         action=pickle.loads(self.lastClicked.getTag("action"))
         if action[0]:
           if action[0]==-1:
              self.resetscene()
              self.explore_nn(action[1])




class SimpleIndexQueryApp(IndexUsingApplication):
  class ProgramMetadata(object):
      name="3d Nearest Neighbors Explorer based on PANDA"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      license="GPLv3"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  number_query=CmdLineString('n',"numberofneighbors",'number',"name of neighbours","3")  
  key=CmdLineString(None,"key","modelpath","specified within the model what should be used as key when indexing","/")
  delay=CmdLineString("i","interval","interval","wait for specified interval in-between entries","0")                            
  #block=CmdLineString('b',"block",'number',"do block-queries","1")

  @classmethod
  def process(cls,nrels=1,*args,**kwargs):
    w=World()
    cls.idx=load_index.__call__((cls.idx.root_class if hasattr(cls.idx,"root_class") else cls.idx.__class__),cls.index_filename)
    w.app=cls
    w.nq=int(cls.number_query.value)
    idb=iter(cls.vdb)
    w.explore_nn(idb.next())
    run()
    w.app=None
       
#t=Texture()
#i=PNMImage(512,512)
#t.load(i)
#l=scipy.lena()[:,:,numpy.newaxis].repeat(3,axis=2).astype(numpy.uint8).copy('C')
#t.setRamImage(ConstPointerToArrayUnsignedChar(l.data))
#print dir(t)
#print cvMgr.listVariables()
SimpleIndexQueryApp.run(sys.argv[1:])


