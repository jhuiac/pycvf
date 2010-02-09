# -*- coding: utf-8 -*-
import direct.directbase.DirectStart
#for the events
from direct.showbase import DirectObject
#for collision stuff
from pandac.PandaModules import *
from direct.task import Task


class Picker(DirectObject.DirectObject):
   def __init__(self):
      #setup collision stuff
      ## ok the detection collision engine
      ## the traverser has for goal to check at all the objects for knowing if there a collision
      self.picker= CollisionTraverser()
      self.picker.showCollisions(render)
      ## an event queue this is were we record the collision that have occured
      self.queue=CollisionHandlerQueue()
      ## The object that will cause the event
      self.pickerNode=CollisionNode('mouseRay')
      self.pickerNode.setFromCollideMask(GeomNode.getDefaultCollideMask())
      self.pickerRay=CollisionRay()
      self.pickerNode.addSolid(self.pickerRay)

      ## and we attach it to the camera
      self.pickerNP = camera.attachNewNode(self.pickerNode)
      self.picker.addCollider(self.pickerNP, self.queue)

      #self.pickerNP=camera.attachNewNode(self.pickerNode)
      ##  We will do select with normally collidable objects
      #




      #this holds the object that has been picked
      self.pickedObj=None

   #this function is meant to flag an object as being somthing we can pick
   def makePickable(self,newObj):
      newObj.setTag('pickable','true')

   #this function finds the closest object to the camera that has been hit by our ray
   def getObjectHit(self, mpos): #mpos is the position of the mouse on the screen
      self.pickedObj=None #be sure to reset this
      self.pickerRay.setFromLens(base.camNode, mpos.getX(),mpos.getY())
      self.picker.traverse(render)
      if self.queue.getNumEntries() > 0:
         #print self.queue,self.queue.getNumEntries()
         self.queue.sortEntries()
         self.pickedObj=self.queue.getEntry(0).getIntoNodePath()

         parent=self.pickedObj#.getParent()
         self.pickedObj=None

         while parent != render:
            if parent.getTag('pickable')=='true':
               self.pickedObj=parent
               return parent
            else:
               parent=parent.getParent()
      return None

   def getPickedObj(self):
         return self.pickedObj


if __name__=="__main__":
  mousePicker=Picker()
  HILITECOL = Vec4(0.7,1,0.7,1)
  NORMCOL = Vec4(1,1,1,1)

  #load thest models
  panda=loader.loadModel('panda')
  teapot=loader.loadModel('teapot')
  box=loader.loadModel('box')

  #put them in the world
  panda.reparentTo(render)
  panda.setPos(camera, 0, 100,0)
  panda.setColor(NORMCOL)

  teapot.reparentTo(render)
  teapot.setPos(panda, -30, 0, 0)
  teapot.setColor(NORMCOL)

  box.reparentTo(render)
  box.setPos(panda, 30,0,0)
  box.setColor(NORMCOL)

  mousePicker.makePickable(panda)
  mousePicker.makePickable(teapot)
  mousePicker.makePickable(box)

  lastHiliteObj = []

  def setHiliteCol(pickObj):
    pickObj.setColor(HILITECOL)
    lastHiliteObj.append(pickObj)

  def setNormCol():
    lastHiliteObj[0].setColor(NORMCOL)
    lastHiliteObj.pop()

  def hiliteTask(task):
    if lastHiliteObj != []:
        setNormCol()

    if base.mouseWatcherNode.hasMouse() == True:
        if mousePicker.getObjectHit(base.mouseWatcherNode.getMouse()) != None:
            setHiliteCol(mousePicker.getPickedObj())

    return Task.cont           

  taskMgr.add(hiliteTask,'hiliteTask')
  run()