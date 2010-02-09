#!/bin/bash



test -d build || mkdir build
SYS=$(echo "import sys; print sys.platform"|python)
if which uname; then
MACH=$(uname -m)
SYS=$SYS-$MACH
fi
BUILD=build/$SYS

echo $BUILD
test -d $BUILD || mkdir -p $BUILD

#sudo easy_install http://pyffmpeg.googlecode.com/svn/branches/pyffmpeg2-alpha-candidate

#echo "do you want to install PyFFMPEG ? (y/n)"

#svn co http://pyffmpeg.googlecode.com/svn/trunk/newversion_beta/ pyffmpeg
#pushd pyffmpeg
#python setup.py build
#sudo python setup.py install
#popd
#sudo easy_install http://downloads.sourceforge.net/project/python-irclib/python-irclib/0.4.8/python-irclib-0.4.8.tar.gz?use_mirror=jaist


PACKAGE=$1

case $PACKAGE in
 pyffmpeg)
  which git || sudo apt-get install git-core
  git clone "http://github.com/tranx/pyffmpeg.git/" || exit -1
  cd pyffmpeg
  git checkout origin/beta
  python setup.py build_ext -i
  cd ..
  cp pyffmpeg/*.so $BUILD
  ;;
 easyinstalls)
  sudo easy_install flickrapi
  sudo easy_install https://alioth.debian.org/frs/download.php/3126/pymvpa_0.4.3.tar.gz
  sudo easy_install http://www.antlr.org/download/Python//antlr_python_runtime-3.1.tar.gz
  sudo easy_install http://www.mit.edu/~sav/arff/dist/arff-1.0c.tar.gz
  sudo easy_install http://nltk.googlecode.com/files/nltk-2.0b7.zip
  ;;
 itk)
  # http://www.paulnovo.org/repository #ITK
  ;;
 sash)
  (cd pysash; python setup.py build_ext -i ; cd -)
  cp pysash/pysash.so $BUILD
 ;;
 sift)
  (cd pysift; python setup.py build_ext -i ; cd -)
  cp pysift/sift.so $BUILD
 ;; 
 lsh)
  (cd pyslsh; python setup.py build_ext -i ; cd -)
  cp pyslsh/pyslsh.so $BUILD
 ;;
 zopencv)
  #(cd zopencv; ./downloadandbuild.sh; cd -)
  mv zopencv/build_$SYS/* $BUILD
 ;;
 orange)
 mkdir orange
 cd orange;
 svn checkout http://www.ailab.si/svn/orange/trunk/orange
 svn checkout http://www.ailab.si/svn/orange/trunk/source source
 cd source
 make
 cd ..
 cp -a orange *.so ../$BUILD
 cd ..
 ;;
 *)
  echo "Please choose a valid package to install (easyinstalls|itk|sash|lsh|sift|zopencv|pyffmpeg)"
esac
