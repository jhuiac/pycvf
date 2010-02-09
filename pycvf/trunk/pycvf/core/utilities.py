import os, sys, time, random, re, atexit
from pycvf.core.errors import *

class TempDirectory:
    def __init__(self,prefix="pycvf",base=None):
        if (base==None):
            if (sys.platform in ["win32"]):
                base=r"c:\temp"
            else:
                base="/tmp"
        self.base=base
        tmpdirname="%s-%04x-%04x-%04x-%08x"%(prefix,
                                               os.getuid(),
                                               os.getpid(),
                                               int(random.random()*0xFFFFF),
                                               int(time.time() *10 )&0xFFFFFFFF 
                                             )
        self.tmpdirname=os.path.join(base,tmpdirname)
        os.mkdir(self.tmpdirname)
    def get(self):
        return self.tmpdirname
    def __del__(self):
        for f in os.listdir(self.tmpdirname):
            os.unlink(os.path.join([self.tmpdirname,f]))
        os.rmdir(self.tmpdirname)

def removeall_tmp_directories(prefix="pycvf",base=None):
        pycvf_warning("ATEXIT handler doing clean up") 
        if (base==None):
            if (sys.platform in ["win32"]):
                base=r"c:\temp"
            else:
                base="/tmp"
        tmpdirnamere="%s-%04x-%04x-(.*)-(.*)"%(prefix,
                                               os.getuid(),
                                               os.getpid(),
                                             )    
        for f in os.listdir(base):
            if (re.match(tmpdirnamere,f)):
                 tmpdirname=os.path.join(base,f)
                 for f2 in os.listdir(tmpdirname):
                                       os.unlink(os.path.join([tmpdirname,f2]))
                                       os.rmdir(tmpdirname)


                                       
def pycvf_config_var(var_name,default):
    from pycvf.core import settings
    if hasattr(settings,var_name):
        return getattr(settings,var_name)
    return default

atexit.register(removeall_tmp_directories)
