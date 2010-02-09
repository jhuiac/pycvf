#!/bin/bash

##
## This file is a generator script for ZZOpenCV 0.1
## Tested under Linux x86 and x86_64 Ubuntu 8.04, 8.10 with opencv 1.0 and 1.1
## 
## This file has been written by Bertrand NOUVEL
## Researcher at the JFLI
##
## Copyright CNRS  ## December 2008- February 2009
##

##

##########################################
##### Platform dependant settings
##########################################


SHAREDFX="so"

if [ "$(uname)" == "Darwin" ]; then
  SHAREDFX="dylib"
fi



MODULES="zopencv_core zopencv_highlevel zopencv_lowlevel zopencv_classes zopencv_pclasses zopencv_argck"
DOSTRIP=1
if true; then
if [ "$ZOPENCVPATH" ]; then
## override by environoment
  OPENCVPREFIX=$ZOPENCVPATH
  OCVLIBS="-L $ZOPENCVPATH/lib -L /usr/local/lib -lcv -lcvaux -lhighgui -lml"
  OCVCFLAGS="-I $ZOPENCVPATH/include/opencv -I ."  
else
## GENERIC CONFIGURATION VIA PKG-CONFIG
if [ "$(which pkg-config)" ]; then
  OPENCVPREFIX=$(dirname $(dirname $(pkg-config --cflags-only-I opencv | cut -c 3-)))
  OCVLIBS=$(pkg-config opencv --libs | sed -e "s/-lml//g") 
  OCVCFLAGS=$(pkg-config opencv --cflags) 
else
## STANDARD SETTINGS ?
  OPENCVPREFIX="/usr/local"
  OCVLIBS="-L$OPENCVPREFIX/lib -lcxcore -lcv -lhighgui -lcvaux"
  OCVCFLAGS="-I $OPENCVPREFIX/include -I $OPENCVPREFIX/include/opencv" 
  DARWINNUMPYINC="/Library/Python/2.5/site-packages/numpy/core/include/numpy"
  DARWINNUMPYINC="/System/Library/Frameworks/Python.framework/Versions/2.5/Extras/lib/python/numpy/core/include/"
  CFLAGS="-I $DARWINNUMPYINC"
fi
fi
else
##
## MANUAL CONFIGURATION FOR SPECIFIC SYSTEMS 
##

#  OPENCVPREFIX=/opt/OpenCV-1.0.0/x86_64/
#  OCVLIBS="-L /opt/OpenCV-1.0.0/x86_64/lib -lcv -lcvaux -lhighgui -lml"
#  OCVCFLAGS="-I /opt/OpenCV-1.0.0/x86_64/include/opencv -I ." 
  OPENCVPREFIX=/home/tranx/build/opencvlibraryb/trunk/opencv/
  OCVLIBS="-L /home/tranx/lib -L /usr/local/lib -lcv -lcvaux -lhighgui -lml"
  OCVFLAGS="-I /home/tranx/build/opencvlibraryb/trunk/opencv/include/opencv -I ."
#  OCVCFLAGS="-I /home/tranx/include/opencv -I /home/tranx/build/opencv/include/opencv/ -I ." 
fi

##########################################
##########################################
##########################################

WITHUNDERSCOREHAND="1"
UNDERSCOREHAND="UnDeRsC"
DEFS="-D XXX"


##
## These types are either incomplete either creating loop in our graph...
## They need to be handled explicitely
##

#INCOMPLETETYPES="CvGraphEdge CvFeatureTree CvGraphVtx CvFileStorage CvFileNode CvTypeInfo CvSubdiv2DEdge CvQuadEdge2D CvAvgComp CvMatrix3 CvConvexityDefect CvGraphVtx2D CvPOSITObject $UNDERSCOREHAND""IplConvKernelFP $UNDERSCOREHAND""CvPixelPosition8u $UNDERSCOREHAND""CvPixelPosition8s $UNDERSCOREHAND""CvPixelPosition32f"
EXPLICITTYPES="CvBGStatModel CvCapture CvFeatureTree CvFaceTracker CvFileStorage CvGenericHash"
INCOMPLETETYPES="$EXPLICITTYPES CvVoronoiEdge2D CvGraphEdge N6CvEHMM4DOT27_E CvEHMM CvFileNode CvRandState CvGLCM  CvPOSITObject CvVideoWriter Cv3dTrackerCameraInfo Cv3dTrackerCameraIntrinsics Cv3dTracker2dTrackedObject  Cv3dTrackerTrackedObject UIplTileInfo UCvContourScanner CvHidHaarClassifierCascade"
#


FILES="cxerror.h cxtypes.h cxcore.h cvtypes.h cv.h cvaux.h highgui.h" #  cxcore.h cvtypes.h
IGNOREFUNCTIONS="cvSubdiv2DGetEdge cv3dTracker2dTrackedObject cv3dTrackerTrackedObject"

if [ "$ZOPENCVDEST" ]; then
DESTDIR=$ZOPENCVDEST
else
DESTDIR=/usr/local/lib/
fi 


export INCOMPLETETYPES
export EXPLICITTYPES
export IGNOREFUNCTIONS
export FILES

STEPS="1234567"

CMODE=1


##########################################
####### parse commande line arguments
##########################################

CONT=True
while [ "$CONT" ]; do 
case "$1" in
  "-s")
  STEPS=$2
  shift 2
  ;;
  "-p")
  OPENCVPREFIX=$2
  shift 2
  ;;
  "-c++")
  CMODE=""
  shift 1
  ;;
  "-c")
  CMODE="1"
  shift 1
  ;;
  "-m")
  MODULES="$2"
  shift 1
  ;;
  *)
  CONT=""
  ;;
esac
done

echo "STEPS=$STEPS"
echo "OPENCVPREFIX=$OPENCVPREFIX"
echo "CMODE=$CMODE"

###########################################################################
# try to do minimal system check and installation of required softwares
###########################################################################

if !  [ "$(which gccxml)" ]; then
   if [ "$(which apt-get)" ]; then
     echo "system check noticed that you have not installed gcc xml please type :"
     echo "sudo apt-get install gccxml"
     #sudo apt-get install gccxml
     exit -1
   else
   if ! [ "$(which cmake)" ]; then
     echo "cmake is not installed in your system, it is required to install gccxml, please install cmake"
     exit -1
   fi
   echo "installing gcc xml..."
   curl http://archive.ubuntu.com/ubuntu/pool/main/g/gccxml/gccxml_0.9.0+cvs20080525.orig.tar.gz | tar -xvz
   cd gccxml*
   echo "cmake"
   touch GCC/libiberty/xatexit.c
   cmake .
   echo "make"
   make
   echo "admin password is required for installation !"
   echo "sudo make install"
   sudo make install
   fi
fi

cat << EOF | python
import os
try:
  import ctypeslib
except:
  os.system("sudo easy_install ctypeslib")
EOF

##########################################################3
echo "dependencies checked ok"
##########################################################3

ADPATH=""

if [ "$(echo $STEPS|tr -cd 1)" ];then
if [ "$CMODE"  ]; then

echo "#######################################################################"
echo "FORCING C MODE"
echo "#######################################################################"


if [ "$(uname)" == "Darwin" ]; then


test -d tmp  || mkdir tmp
cd tmp
echo -n "" > cvall.h

cat <<EOF >> cvall.h
#define SKIP_INCLUDES 1
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>

#if defined __ICL
    #define CV_ICC   __ICL
#elif defined __ICC
    #define CV_ICC   __ICC
#elif defined __ECL
    #define CV_ICC   __ECL
#elif defined __ECC
    #define CV_ICC   __ECC
#endif

#define CV_SSE2 0

#include <math.h>

//#include <ipl.h>

EOF

for f in $FILES; do
   echo "#include <$f>" >> cvall.h
done
cd ..

else


test -d tmp  || mkdir tmp
cd tmp
echo -n "" > cvall.h
for f in $FILES; do
   echo "#include <$f>" >> cvall.h
done
cd ..
fi


for i in  $OPENCVPREFIX/include/opencv/*.h tmp/cvall.h ;do
   echo "gcc $DEFS -I $OPENCVPREFIX/include/opencv -E -o _$(basename $i) $i"
   gcc $DEFS $ADPATH -I $OPENCVPREFIX/include/opencv -E -o _$(basename $i) $i

   if [ "$WITHUNDERSCOREHAND" ]; then
      sed  -e "s/lambda/Lambda/g" -e 's/_Ipl/UIpl/g'  -e "s/_Cv/UCv/g" < _$(basename $i) > __$(basename $i)
      mv __$(basename $i) _$(basename $i)
   fi
   echo 'extern "C" {' > $(basename $i)
   echo "#include \"_$(basename $i)\"" >> $(basename $i)
   echo '}' >> $(basename $i)
done



else

echo "#######################################################################"
echo "C++ MODE"
echo "#######################################################################"


test -d tmp  || mkdir tmp
cd tmp
echo -n "" > cvall.h
for f in $FILES; do
   echo "#include <$f>" >> cvall.h
done
cd ..


for i in  $OPENCVPREFIX/include/opencv/*.h tmp/cvall.h ;do
   echo "g++ $DEFS -I $OPENCVPREFIX/include/opencv -E -o $(basename $i) $i"
   g++ $DEFS $ADPATH -I $OPENCVPREFIX/include/opencv -E -o $(basename $i) $i
   
   if [ "$WITHUNDERSCOREHAND" ]; then
 #    sed  -e "s/lambda/Lambda/g" -e 's/_Ipl/UIpl/g'  -e "s/_Cv/UCv/g"  -e "s/__builtin_*\([^ );]*\)\([ ]*\)(\([^)]*\))//g" -e "s/__builtin_ia32\([^ ]*\)//g"  < $(basename $i) > _$(basename $i)
      sed  -e "s/lambda/Lambda/g" -e 's/_Ipl/UIpl/g'  -e "s/_Cv/UCv/g"  < $(basename $i) > _$(basename $i)
      mv _$(basename $i) $(basename $i)
   fi
done

fi


fi

if [ "$(echo $STEPS|tr -cd 2)" ];then

echo "#######################################################################"
echo "Converting to XML"
echo "#######################################################################"

ADPATH=""


if [ "$CMODE"  ]; then
for f in cvall.h; do
  bf=${f%.h}
  gccxml --gccxml-compiler gcc --gccxml-cxxflags -fpermissive -fpermissive $ADPATH -I. $DEFS $f -fxml=$bf.xml
  grep -v Converter $bf.xml > $bf.xml.tmp
  mv $bf.xml.tmp $bf.xml
done
else
for f in cvall.h; do
  bf=${f%.h}
  gccxml --gccxml-compiler gcc --gccxml-cxxflags -fpermissive -fpermissive $ADPATH -I. $DEFS $f -fxml=$bf.xml
  grep -v Converter $bf.xml > $bf.xml.tmp
  mv $bf.xml.tmp $bf.xml
done
fi

fi



if [ "$(echo $STEPS|tr -cd 3)" ];then
echo "#######################################################################"
echo "Converting to Cython and fixing buggy declarations"
echo "#######################################################################"

#(

#for t in $INCOMPLETETYPES; do
#   echo "ctypedef void $t"
#done

#echo

#for f in $FILES; do
#python /usr/bin/xml2cython.py -l${f%.h} $f cvall.xml | grep -v "^Item not handled"| grep -v "^Struct member not handled"| grep -v "^Argument not handled"
#done
#
#) | egrep -v -e "^[^I \t]+[A-Z][^ ]*$" | sed -e "s/lambda/__LaMbDa__/g" > zopencv.pyx
echo -n > zopencv_core.pyx

rm cv.xml
ln -s cvall.xml cv.xml

cat << EOF >> zopencv_core.pyx
SHRT_MAX=32767
EOF

#python dodefs.py | sed -e "s/lambda/__LaMbDa__/g" >> zopencv_core.pyx || exit -1
python dodefs.py >> zopencv_core.pyx  || exit -1

cat << EOF >> zopencv_core.pyx
def CV_MAKETYPE(depth,cn):
	return ((depth) + (((cn)-1) << CV_CN_SHIFT))
EOF



for f in $FILES;do
egrep -e "^#define( +)[A-Za-z]([0-9A-Za-z_]*) " $OPENCVPREFIX/include/opencv/$f | sed -e 's%//.*%%g' -e 's%/\*.*\*/%%g' -e 's%/\*.*%%g'| cut -d ':' -f 2 | cut -d ' ' -f 2- | tr '\t' ' '| sed -e "s/\ \ */ /g"|grep -v -w int | sed -e "s/^ //" -e "s/ /=/" -e  "s/\([0-9][0-9]*\.[0-9]*\)f/\1/g"  | egrep -v -w -e "EXIT|cvPseudoInverse|cvMean|CV_WHOLE_ARR|CV_IS_CONT_MAT|cvSlice" | egrep -v '[g-wy-z]' >> zopencv_core.pyx
done


#types=$(grep "cdef struct" zopencv_core.pyx | tr -d ':' | cut -d ' ' -f 3)
#for types

#cat zopencvbase.pyx



#sed -e 's/'$UNDERSCOREHAND'/_/g'  -e "/CImage/d" -e "/set_preprocess_func/d" -e "/cvvAddSearchPath/d" -e "/cvvConvertImage/d" < zzopencv_core.tpy > zzopencv_core.py


#cat << EOF >> zzopencv_core.py
#IplImage=_IplImage
#def CV_MAKETYPE(depth,cn):
#  return ((depth) + (((cn)-1) << CV_CN_SHIFT))
#def zImage(img):
#	return zopencv_core.NumPy2ZIplFast(img)
#def zMat(x):
#	return zopencv_core.NumPy2ZCvMatFast(x)
#EOF


#for f in $FILES;do
#egrep -e "^#define( +)[A-Za-z]([0-9A-Za-z_]*) " $OPENCVPREFIX/include/opencv/$f | sed -e 's%//.*%%g' -e 's%/\*.*\*/%%g' -e 's%/\*.*%%g'| cut -d ':' -f 2 | cut -d ' ' -f 2- | tr '\t' ' '| sed -e "s/\ \ */ /g"|grep -v -w int | sed -e "s/^ //" -e "s/ /=/" -e  "s/\([0-9][0-9]*\.[0-9]*\)f/\1/g" | egrep -v -w -e "EXIT|cvPseudoInverse|cvMean|CV_WHOLE_ARR|CV_IS_CONT_MAT|cvSlice" >> zzopencv_core.py
#done

#mv zzopencv.py zzopencv.tpy
#egrep -v -e "CImage|set_preprocess_func|set_postprocess_func|cvvAddSearchPath|cvvConvertImage" < zzopencv_core.tpy > zzopencv_core.py



fi


## it seems that it is not actually required to go C++ here...
CMODE=0

if [ "$(echo $STEPS|tr -cd 4)" ];then

if [ "$CMODE" ]; then
echo "#######################################################################"
echo "Cythoning to C"
echo "#######################################################################"
else
echo "#######################################################################"
echo "Cythoning to C++"
echo "#######################################################################"
fi

DEBUGNAMES="-e 's/declarations.CvLeeParameters/int/g' -e 's/CvLeeParameters/int/g'"
DEBUGNAMES=""
cat zopencv_core.pyx | sed $DEBUGNAMES -e 's/__darwin_size_t/size_t/g' | grep -v CV_LEE |grep -v "ctypedef int int" | grep -v "enum int" > zopencv_core.pyxtmp
cat <<EOF | sed -e "s/    /@/g"|tr '@' '\t'>> zopencv_core.pyxtmp

EOF

mv zopencv_core.pyxtmp zopencv_core.pyx

if [ "$CMODE" ]; then
for m in $MODULES; do 
echo "$m"
cython -I . $m.pyx || exit -1
done
else
cython --cplus -I . zopencv.pyx || exit -1
fi


fi


if [ "$CMODE" ]; then
COMPILER=gcc
else
COMPILER=g++
fi

#COMPILER=icc

CFLAGS="$CFLAGS -fomit-frame-pointer -fPIC"


if [ "$(echo $STEPS|tr -cd 5)" ];then
echo "##################################################################################################"
echo "Compiling Python Module... (It requires lot of memory and about 10 minutes on a modern computer!!)"
echo "##################################################################################################"


rm *.h *.hpp

mkdir build

for f in $FILES;do
  sed  -e "s/lambda/Lambda/g" -e 's/_Ipl/UIpl/g'  -e "s/_Cv/UCv/g" < $OPENCVPREFIX/include/opencv/$f > build/$f
done


#cat <<EOF > zopencv.c
##include "cvall.h"
#EOF
## avoid reincluding already used includes
#(grep '#' build/cvall.h | grep include |  cut -d  '"' -f 2 |sort|uniq | while read p; do grep '#define' $p | head --lines=1 ; done )>> zopencv.c
#sed -e 's/struct CvSize/CvSize/g' < zopencv.t | grep -v '#include "cvall.h"' >> zopencv.c



for f in $MODULES; do
mv $f.c $f.t
sed -e 's/struct CvSize/CvSize/g' < $f.t  >> $f.c
echo "$COMPILER $CFLAGS -fPIC -I build -c $(python-config --cflags) $OCVCFLAGS  $f.c"
$COMPILER $CFLAGS -fPIC -I build -c $(python-config --cflags) $OCVCFLAGS  $f.c 2>&1 | tee zopencv.gccerrs
done


fi

if [ "$(echo $STEPS|tr -cd 6)" ];then
echo "#######################################################################"
echo "Linking"
echo "#######################################################################"

cat <<EOF >  vdefs.c 
#include <stdlib.h>
void * cvMorphContours=abort;
void * cvCalcContoursCorrespondence=abort;
void * _ZN2cv15groupRectanglesERNS_6VectorINS_5Rect_IiEEEEid =abort;
void * cvCalcOpticalFlowFarneback=abort;
EOF

case $(uname) in
  "Darwin")
#   libtool -dynamic -flat_namespace -lSystem -compatibility_version 0.1 -current_version 0.1 -o zopencv.dylib -undefined suppress zopencv.o
echo "THIS PART IS TO BE UPDATED / DEBUGED"
gcc -c vdefs.c
libtool -dynamic -lSystem -compatibility_version 0.1 -current_version 0.1 -o zopencv.dylib zopencv.o vdefs.o -L/usr/local/lib -lcxcore -lcvaux -lcv -lhighgui -lml $(python-config --libs) 
;;
   *)
for f in $MODULES; do   
  echo "$COMPILER -I build $(python-config --libs) $OCVLIBS -shared -o $f.$SHAREDFX $f.o vdefs.c "
  $COMPILER -I build $(python-config --libs) $OCVLIBS -shared -o $f.$SHAREDFX $f.o  vdefs.c -lswscale -lavcodec -lavformat
  if [ "$DOSTRIP" ] ; then
      strip $f.$SHAREDFX
  fi 
done
;;
esac

fi


if [ "$(echo $STEPS|tr -cd 7)" ];then
echo "#######################################################################"
echo "Installing into directory $DESTDIR..."
echo "#######################################################################"

ln -s $PWD/zopencv.py $DESTDIR
ln -s $PWD/zopencv_*.$SHAREDFX $DESTDIR

fi
