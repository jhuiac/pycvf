# -*- coding: utf-8 -*-
from pycvf.core.generic_application import *

class SimpleRetexturizerApp(IndexUsingApplication):
  class ProgramMetadata(object):
      name="Simple Resynthetizer Application"
      version="0.1"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  number_query=CmdLineString('n',"numberofneighbors",'number',"name of neighbours","3")  
  modelpart=CmdLineString(None,"modelpart","modelpath","specified within the mode where the structure is to be extracted","//")

     
  @classmethod
  def process(cls, * args, **kwargs):
    submdl=mdl.get_by_cname(modelpart.value)
    print submdl
    cls.mdl.print_tree()
    class Recomposer:
       def __init__(self):
          self.shp=None
          self.si=None
       def reset(self):
          self.shp=None
          self.si=structure.instantiate()
       def process(self,data):
          self.shape=None
       def get(self):
          return si.recomposeall(self.si)
    recomposer=Recomposer()
    for e in cls.vdb:
       recomposer.reset()
       cls.mdl.process_path([e[0]],[e[1]],cls.modelpart.value,recomposer.process)
       print recomposer.get()
       
if __name__=='__main__':
    SimpleRetexturizerApp.run(sys.argv[1:])


# python build_index.py  --db imagepatches  --dbargs '"db":"image_directory","dbargs":"\"path\":\"/databases/VisionTexture/VisTex/Images/Scenes/GrassLand\"" --model "image.lbp" -s "xxx.idx"
# python build_index.py  --db:"image_directory" -dbargs '"path":"/databases/VisionTexture/VisTex/Images/Scenes/GrassLand" \
#                        --model "#M('naive')
#                                " *{'patches':S('patches',(16,16))}"
#                                " |{'#patches':MS("image.lbp")" -s "xxx.idx"

# python resynthmap.py   --db "image_directory"