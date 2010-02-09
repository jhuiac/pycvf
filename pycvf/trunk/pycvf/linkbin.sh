#!/bin/bash

if ! test -d apps; then
  echo "the apps directory does not exist you are probably not in the good directory" 1>&2
  exit -1
fi

if ! test -d core; then
  echo "the core directory does not exist you are probably not in the good directory" 1>&2
  exit -1
fi

if ! test -d nodes; then
  echo "the nodes directory does not exist you are probably not in the good directory" 1>&2
  exit -1
fi


rm -r bin
mkdir bin

for f in $(grep -l "#!/usr/bin/env python" apps/*.py); do
  pa=${f%.py}
  chmod +x $f
  ln -s $PWD/$f bin/pycvf_$(basename $pa)
done

ln -s $PWD/generic_apps/* bin

