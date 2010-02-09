# -*- coding: utf-8 -*-
AUTOINSTALL_MISSING_PACKAGES=True

#Packages = [ "Pyro" ] 

import os,sys,re
from distutils.core import setup
from distutils.extension import Extension
from distutils.core import Command
from Cython.Distutils import build_ext
import numpy.distutils.misc_util as nd


if sys.platform == "Microsoft":
  pass
else:
  pass



CLASSIFIERS = """\
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved :: Gnu Library or Lesser General Public License (LGPL)
Programming Language :: C
Programming Language :: Python
Topic :: Software Development
Topic :: Scientific/Engineering
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

NAME                = 'pycvf'
MAINTAINER          = "pycvf Developers"
MAINTAINER_EMAIL    = "nouvel@nii.ac.jp"
DESCRIPTION         = 'Python Computer Vision Framework'
LONG_DESCRIPTION    = 'Python Computer Vision Framework'
URL                 = "http://pycvf.sourceforge.net/"
DOWNLOAD_URL        = ""
LICENSE             = 'LGPL3'
CLASSIFIERS         = filter(None, CLASSIFIERS.split('\n'))
AUTHOR              = "Bertrand Nouvel"
AUTHOR_EMAIL        = "nouvel@nii.ac.jp"
PLATFORMS           = [ "Linux",  "Unix", "Windows", "Mac" ]
MAJOR               = 0
MINOR               = 0
MICRO               = 11
ISRELEASED          = True
VERSION             = '%d.%d.%d' % (MAJOR, MINOR, MICRO)


# Return the svn version as a string, raise a ValueError otherwise
def svn_version():
    try:
        out = subprocess.Popen(['svn', 'info'], stdout = subprocess.PIPE).communicate()[0]
    except OSError:
        print " --- Could not run svn info --- "
        return ""

    r = re.compile('Revision: ([0-9]+)')
    svnver = None
    for line in out.split('\n'):
        m = r.match(line)
        if m:
            svnver = m.group(1)

    if not svnver:
        raise ValueError("Error while parsing svn version ?")
    return svnver

FULLVERSION = VERSION
if not ISRELEASED:
    FULLVERSION += '.dev'
    # If in git or something, bypass the svn rev
    if os.path.exists('.svn'):
        FULLVERSION += svn_version()


def write_version_py(filename='pycvf/core/version.py'):
    cnt = """
# THIS FILE IS GENERATED FROM PYCVF SETUP.PY
short_version='%(version)s'
version='%(version)s'
release=%(isrelease)s

if not release:
    version += '.dev'
    import os
    svn_version_file = os.path.join(os.path.dirname(__file__),
                                   'pycvf/core','__svn_version__.py')
    if os.path.isfile(svn_version_file):
        import imp
        svn = imp.load_module('pycvf.core.__svn_version__',
                              open(svn_version_file),
                              svn_version_file,
                              ('.py','U',1))
        version += svn.version
"""
    a = open(filename, 'w')
    try:
        a.write(cnt % {'version': VERSION, 'isrelease': str(ISRELEASED)})
    finally:
        a.close()



old_path = os.getcwd()
local_path = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(local_path)
sys.path.insert(0,local_path)

# Rewrite the version file everytime
if os.path.exists('pycvf/core/version.py'): os.remove('pycvf/core/version.py')
write_version_py()

#package_dir={'pycvf':'pycvf'}


def configuration(parent_package='',top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('pycvf',parent_package,top_path)
    config.add_data_files('site.cfg')
    config.make_config_py()
    return config


sys.path=["."]+sys.path

def modify_bashrc(pycvfdir=None):
  if pycvfdir==None:
    pycvfdir=os.path.dirname(__file__)
  f=file(os.path.join(os.environ["HOME"],".bashrc"),"r")
  if (filter(lambda x:re.match("## BEGINING OF PYCVF-CONFIGURATION",x), f.readlines())):
     sys.stderr.write("your .bashrc appears to be already configured, skipping .bashrc configuration...")
     return
  f.close()
  f=file(os.path.join(os.environ["HOME"],".bashrc"),"a")
  f.write("\n")
  f.write("""
###
### BEGINING OF PYCVF-CONFIGURATION 
###

export PATH=$PATH:%PYCVFDIR%/pycvf/bin
export PYTHONPATH=%PYCVFDIR%:%PYCVFDIR%/wrappers/build/%platform%:$PYTHONPATH

###
### END OF PYCVF-CONFIGURATION 
###

""".replace("%PYCVFDIR%",pycvfdir).replace("%platform%",sys.platform+"-"+os.uname()[-1]))
  f.close()


class ConfigureBashRCCommand(Command):
  description = """ Setup your bashrc so that you can use PYCVF as developper """

  user_options = []
  def initialize_options(self):
    return {}
  def finalize_options(self):
    return {}
  def run(self,*args,**kwargs):
    modify_bashrc()
    
class PyCVFInstallCommand(Command):
  description = """ Command doing all what we can for you to have an easy install. """

  user_options = []
  def initialize_options(self):
    return {}
  def finalize_options(self):
    return {}
  def run(self,*args,**kwargs):
    assert False,"Not yet implemented"

class InstallDatabaseCommand(Command):
  """ Install various databases on your system """
  description = """ Install various databases on your system """

  user_options = []
  def initialize_options(self):
    return {}
  def finalize_options(self):
    return {}
  def run(self,*args,**kwargs):
    import pycvf.maintenance.downloaddbs
    pycvf.maintenance.downloaddbs.main()

setup(      #entry_points = {
            # "distutils.commands": [
            #      "install_databases = pycvf.generics_apps.downloaddbs:install_databases"
            # ]
            #},
            cmdclass={
              "install_databases":InstallDatabaseCommand, 
              "configure_bashrc":ConfigureBashRCCommand,
              'build_ext': build_ext,
              'pycvf_install':PyCVFInstallCommand,
            },
            packages=['pycvf', 'pycvf.core', 'pycvf.nodes', 'pycvf.lib','pycvf.lib.graphics',   'pycvf.lib.video',
                      'pycvf.lib.info','pycvf.lib.misc','pycvf.lib.stats', 'pycvf.lib.ui' , 'pycvf.lib.ui.qt', 'pycvf.databases',
                     'pycvf.framework02', 'pycvf.framework01', 'pycvf.framework03',
                     'pycvf.framework03.models',
                     'pycvf.framework02.models', 
                     'pycvf.framework02.models.datatypes', 
                     'pycvf.framework02.models.structures',                      
                     'pycvf.framework02.models.image',                                           
                     'pycvf.framework02.models.audio',                                                                
                     'pycvf.framework02.models.basics',                                                                                     
                     'pycvf.framework01.models',
                     'pycvf.framework01.apps',  'pycvf.framework02.apps'
                     ],
#            package_dir=package_dir,
            name=NAME,
            maintainer=MAINTAINER,
            maintainer_email=MAINTAINER_EMAIL,
            description=DESCRIPTION,
            long_description=LONG_DESCRIPTION,
            url=URL,
            download_url=DOWNLOAD_URL,
            license=LICENSE,
            classifiers=CLASSIFIERS,
            author=AUTHOR,
            author_email=AUTHOR_EMAIL,
            platforms=PLATFORMS,
            version     =VERSION,
            ext_modules = [   
#                   Extension("lib.stats.histogram", ["lib/stats/histogram.pyx"]),
                   Extension("pycvf.lib.misc.hack", ["pycvf/lib/misc/hack.pyx"], include_dirs=nd.get_numpy_include_dirs()),
                   Extension("pycvf.lib.video.rgb2bgr", ["pycvf/lib/video/rgb2bgr.pyx"], include_dirs=nd.get_numpy_include_dirs()),
                 ]


    )
