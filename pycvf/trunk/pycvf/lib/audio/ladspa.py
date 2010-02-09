from ctypes import *
import os


def PluginSearchDirectory(dir,callbackfct):
    for f in (os.listdir(dir)):
        try:
            lib = cdll.LoadLibrary(dir+"/"+f)
            #lib.Error.restype = ctypes.c_char_p
            #lib.MMap.restype = ctypes.c_void_p
            try:
                ld=lib.ladspa_descriptor
                callbackfct(f,lib,ld)
            except AttributeError:
                print ("%s is not a valid ladspa file"%f)
        except:
            print ("%s is not a ladspa file"%f)

def PluginSearch(callbackfct,dirs=[],defaultdirs=True):
    if (defaultdirs):
        dirs.append("/usr/lib/ladspa")
        if (os.getenv("LADSPA_PATH")):
            dirs+=os.getenv("LADSPA_PATH").split(':')
    for p in dirs:
        PluginSearchDirectory(p,callbackfct)

def PrintListPlugins():
    def print_info(f,lib,ld):
        print (f,ld)
    PluginSearch(print_info)
