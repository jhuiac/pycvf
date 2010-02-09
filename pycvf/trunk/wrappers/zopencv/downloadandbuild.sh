#!/bin/bash

if test -d opencv; then
cd opencv
svn up || true
else
svn co https://opencvlibrary.svn.sourceforge.net/svnroot/opencvlibrary/trunk/opencv
cd opencv
fi

cmake .
make || exit -1

cd ..

SYS=build_$(echo "import sys; print sys.platform"|python)
if which uname; then
MACH=$(uname -m)
SYS=$SYS-$MACH
fi

echo $SYS
test -d $SYS || mkdir -p $SYS

export ZOPENCVDEST=$SYS
export ZOPENCVPATH=opencv

ln -sf /usr/bin/g++-4.1 g++
ln -sf /usr/bin/gcc-4.1 gcc

PATH=$PWD:$PATH ./build.sh

