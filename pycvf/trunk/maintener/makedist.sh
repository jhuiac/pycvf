#!/bin/bash

test -f setup.py || exit -1

##
## Make distribution
##

python setup.py sdist 
python setup.py sdist --format bztar
#python setup.py bdist 
#python setup.py bdist --format bztar


##
## Link current distribution to current version
##

VERSION=$(echo "import pycvf; print '%s'%(pycvf.__version__,)" | python)

pushd dist
rm -f pycvf-current.tar.gz
ln -s pycvf-$VERSION.tar.gz pycvf-current.tar.gz
popd

##
## Check validity of current version
##
