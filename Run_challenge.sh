PYTHON=python
#setting the PYTHON PACKAGE DIRECTORY
export PYTHONPATH=$PYTHONPATH:./PACKAGES/
#RUNNING THE SCRIPT
$PYTHON Challenge.py -i Challenge_data.vcf -o Challenge_annotated_out.vcf
