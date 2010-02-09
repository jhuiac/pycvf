# -*- coding: utf-8 -*-
import os,sys

def compute_platform_id():
  if sys.platform in [ "win32","win64"]:
     return sys.platform
  else:
     return sys.platform+"-"+os.uname()[-1]
 
def modify_bashrc(pycvfdir=None):
  xfile=__file__
  if (xfile[0]!=os.path.sep):
    xfile=os.path.join(xfile)
  if pycvfdir==None:
    pycvfdir=os.path.dirname(os.path.dirname(os.path.dirname(xfile)))
  assert(pycvfdir!="")
  HOME=os.path.expanduser("~")
  f=file(os.path.join(HOME,".bashrc"),"r")
  if (filter(lambda x:re.match("## BEGINING OF PYCVF-CONFIGURATION",x), f.readlines())):
     sys.stderr.write("your .bashrc appears to be already configured, skipping .bashrc configuration...")
     return
  f.close()
  HOME=os.path.expanduser("~")  
  f=file(os.path.join(HOME,".bashrc"),"a")
  f.write("\n")
  f.write("""

### BEGINING OF PYCVF-CONFIGURATION 
###

export PATH=$PATH:%PYCVFDIR%%/%pycvf%/%bin
export PYTHONPATH=%PYCVFDIR%:%PYCVFDIR%%/%wrappers%/%build%/%%platform%:$PYTHONPATH

###
### END OF PYCVF-CONFIGURATION 


""".replace("%PYCVFDIR%",pycvfdir).replace("%/%",os.path.sep).replace("%platform%",compute_platform_id()))
  f.close()

def touch_pycvf_settings_py():
    HOME=os.path.expanduser("~")      
    f=open(os.path.join(os.environ["HOME"],".pycvf-settings.py"),"a")
    f.close()
  
if __name__="__main__":
  modify_bashrc()
  touch_pycvf_settings_py()
  