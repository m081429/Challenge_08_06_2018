# Sample python script

# This script is written in python2 and annotates the input vcf file with

1. Annotates with the most deleterious possibility.
2. Depth of sequence coverage at the site of variation.
3. Number of reads supporting the variant.
4. Percentage of reads supporting the variant versus those supporting reference reads.
5. Allele frequency of variant from Broad Institute ExAC Project API
(API documentation is available here: http://exac.hms.harvard.edu/)
6. Additional optional information from ExAC .

### TASK: Writing a script to annotate a vcf file
### INPUT FILE: VCF FILE ("input.vcf")
### OUTPUT FILE: VCF FILE with new annotations ("output_annotated.vcf")


### a)Python packages Required to run this script
	1)os
	2)argparse
	3)sys
	4)pwd
	5)time
	6)subprocess
	7)re
	8)shutil
	9)pyVEP
	10)requests

### b)SET UP : Installing the python package	
	Setup script to install pyVEP package "setup.sh"

### c) Running the script "run.sh"
	cat run.sh
	PYTHON=`which python`
	#setting the PYTHON PACKAGE DIRECTORY
	export PYTHONPATH=$PYTHONPATH:./PACKAGES1/
	#unit tests
	$PYTHON Python_unittest.py
	#RUNNING THE SCRIPT
	$PYTHON Python_sample.py -i input.vcf -o Annotated.vcf

### d)OUTPUT : 'Annotated.vcf'
	Interpreting the output vcf "Challenge_annotated_out.vcf"
	
#### 	Requirement 1. Annotate with the most deleterious possibility.
	Added VEP most deleterious possibility through VEP API
	"INFO=<ID=VEP_VARIANT_TYPE,Number=A,Type=String,Description="VEP VARIANT TYPE">"
	
####	Requirement 2. Depth of sequence coverage at the site of variation.
	'DP' total depth is already present in the FORMAT field
	
####	Requirement 3. Number of reads supporting the variant.
	'AO' reads supporting variant is already present in the FORMAT field
	
####	Requirement 4. Percentage of reads supporting the variant versus those supporting reference reads.
	Added new format field by extracting reads supporting variant and depth and calculated the percentage
	"##FORMAT=<ID=VP,Number=1,Type=Float,Description="PERCENT NUMBER OF READS SUPPORTING VARIANT to TOTAL NUMBER OF VARIANTS">"
	
####	Requirement 5. Allele frequency of variant from Broad Institute ExAC Project API
	(API documentation is available here: http://exac.hms.harvard.edu/)
	Added new INFO fields EXAC POPULATION FREQUENCY
	'##INFO=<ID=EXAC_POP_FREQ,Number=A,Type=String,Description="EXAC DATABASE POPULATION FREQ INFO(ORDER:ALL POP,European (Non-Finnish),East Asian,Other,African,Latino,South Asian,European (Finnish))">'
	
####	Requirement 6. Additional information from ExAC
	Added new INFO fields EXAC DBSNP RSID, EXAC VARIANT SITE QUALITY SCORE and EXAC VARIANT FILTER VALUE
	'##INFO=<ID=EXAC_RSID,Number=A,Type=String,Description="EXAC DATABASE RSID INFO">'
	'##INFO=<ID=EXAC_SITE_QUALITY,Number=A,Type=String,Description="EXAC DATABASE SITE QUALITY INFO">'
	'##INFO=<ID=EXAC_FILTER_STATUS,Number=A,Type=String,Description="EXAC DATABASE FILTER STATUS INFO">'
	
###  Unit tests:Python_unittest.py
