set -x
PYTHON=/usr/local/biotools/python/2.7.10/bin/python
#setting the PYTHON PACKAGE DIRECTORY
export PYTHONPATH=$PYTHONPATH:./PACKAGES1/
#unit tests
$PYTHON Python_unittest.py
#RUNNING THE SCRIPT
$PYTHON Python_sample.py -i input.vcf -o Annotated.vcf
