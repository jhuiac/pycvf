#!/bin/bash

test -f setup.py || exit -1

VERSION=$(echo "import pycvf; print '%s'%(pycvf.__version__,)" | python)

echo "allowing pycvf to access our screen..."
xhost +SI:localuser:pycvf
echo "copying file to pycvf"
sudo cp dist/pycvf-current.tar.gz ~pycvf
echo "creating file"
cat << EOF > /tmp/pycvf-runscript.sh
rm -r lib/python/pycvf-*
rm -r pycvf-$VERSION
tar -xvzf pycvf-current.tar.gz
cd pycvf-$VERSION
export PYTHONPATH=
echo "installing"
python setup.py build_py -c -O1 --home ~pycvf
python setup.py install -O1 --home ~pycvf
#rm -r  ~/lib/python/pycvf/models
#ln -s ~/lib/python/pycvf/framework02/models  ~/lib/python/pycvf/models
#ln -s ~/lib/python/pycvf/framework02/apps ~/lib/python/pycvf/apps
echo "install done"
export PYTHONPATH=~/lib/python/ 
cd pycvf 
cd apps
echo "running dbshow"
python model_features_print.py  
EOF
chmod +x /tmp/pycvf-runscript.sh
echo "copying script"
sudo cp /tmp/pycvf-runscript.sh ~pycvf
echo "running script"
sudo -u pycvf  bash -c "HOME=~pycvf;cd;./pycvf-runscript.sh"
