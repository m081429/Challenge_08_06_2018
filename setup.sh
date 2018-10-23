set -x
PYTHON=/usr/local/biotools/python/2.7.10/bin/python
PIP=/usr/local/biotools/python/2.7.10/bin/pip
#create package directory
mkdir PACKAGES1
#getting the source code
git clone https://github.com/kantale/pyVEP.git
tar -zcvf pyVEP.tar.gz pyVEP
#installing the package
$PIP install -t ./PACKAGES1 pyVEP.tar.gz
#clean up
rm pyVEP.tar.gz
rm -rf pyVEP/
