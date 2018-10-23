#!/usr/local/biotools/python/2.7.10/bin/python3
__author__ = "Naresh Prodduturi"
__email__ = ""
__status__ = "Dev"

import os
import argparse
import sys
import pwd
import time
import subprocess
import re
import shutil
from pyVEP import VEP
import requests

def argument_parse():
	'''Parses the command line arguments'''
	parser=argparse.ArgumentParser(description='')
	parser.add_argument("-i","--input",help="input vcf file",required="True",type=input_file_validity)
	parser.add_argument("-o","--output",help="output txt file",required="True")
	return parser

def input_file_validity(file):
	'''Validates the input files'''
	if os.path.exists(file)==False:
		raise argparse.ArgumentTypeError( '\nERROR:Path:\n'+file+':Does not exist')
	if os.path.isfile(file)==False:
		raise argparse.ArgumentTypeError( '\nERROR:File expected:\n'+file+':is not a file')
	if os.access(file,os.R_OK)==False:
		raise argparse.ArgumentTypeError( '\nERROR:File:\n'+file+':no read access ')
	return file

def main():
	abspath=os.path.abspath(__file__)
	words = abspath.split("/")
	'''reading the config filename'''
	parser=argument_parse()
	arg=parser.parse_args()
	'''Reading inputfile'''
	input_vcf=arg.input
	'''output file'''
	output_vcf=arg.output
	'''Varible initialization'''
	exac_pop_list=["European (Non-Finnish)", "East Asian", "Other", "African", "Latino", "South Asian", "European (Finnish)"]
	header_add_flag=1
	'''Reading vcf file'''
	fobj = open(input_vcf)
	myfile = open(output_vcf, mode='wt')
	'''iterating through input vcf file'''
	for record in fobj:
		record = record.strip()
		'''identifying the header section of vcf file'''
		if record.startswith('#'):
			'''identifying the start of format section and add new annotation tags'''
			if record.startswith('##FORMAT') and header_add_flag==1:
				header_add_flag=0
				str_header='##INFO=<ID=VEP_VARIANT_TYPE,Number=A,Type=String,Description="VEP VARIANT TYPE">'
				myfile.write(str_header+"\n")
				str_header='##INFO=<ID=EXAC_RSID,Number=A,Type=String,Description="EXAC DATABASE RSID INFO">'
				myfile.write(str_header+"\n")
				str_header='##INFO=<ID=EXAC_SITE_QUALITY,Number=A,Type=String,Description="EXAC DATABASE SITE QUALITY INFO">'
				myfile.write(str_header+"\n")
				str_header='##INFO=<ID=EXAC_FILTER_STATUS,Number=A,Type=String,Description="EXAC DATABASE FILTER STATUS INFO">'
				myfile.write(str_header+"\n")
				str_header='##INFO=<ID=EXAC_POP_FREQ,Number=A,Type=String,Description="EXAC DATABASE POPULATION FREQ INFO(ORDER:ALL POP,European (Non-Finnish),East Asian,Other,African,Latino,South Asian,European (Finnish))">'
				myfile.write(str_header+"\n")
				str_header='##FORMAT=<ID=VP,Number=1,Type=Float,Description="PERCENT NUMBER OF READS SUPPORTING VARIANT to TOTAL NUMBER OF VARIANTS">'
				myfile.write(str_header+"\n")
				myfile.write(record+"\n")
			else:
				myfile.write(record+"\n")
		else:
			'''spliting the record to words'''
			list_record=record.split("\t")
			list_ALT = list_record[4].split(',')
			record_CHROM = list_record[0]
			record_POS = list_record[1]
			record_REF = list_record[3]
			record_FORMAT = list_record[8]
			'''spliting the format string'''
			list_FORMAT = record_FORMAT.split(':')
			'''identify total depth DP and num reads variant AO'''
			index_DP=list_FORMAT.index("DP")
			index_AO=list_FORMAT.index("AO")
			list_vep_variant_type = []
			list_var_num_reads_alt = []
			list_var_freq_perc = []
			list_exac_rsid = []
			list_exac_site_quality = []
			list_exac_filter_status = []
			list_exac_pop_freq = []
			'''iterating through each alternate allele'''
			for alt in list_ALT:
				'''preparing string to call VEP API'''
				str_temp = record_CHROM+" "+record_POS+" . "+record_REF+" "+alt+" . . ."
				'''identifying complex variants'''
				if len(record_REF)>1 and len(alt)>1:
					str_most_severe_consequence = "NA"
				else:
					'''calling the VEP API'''
					print(str_temp)
					vep_obj = VEP(str_temp, 'grch37')
					'''extracting most deleterious possibility'''
					str_most_severe_consequence = vep_obj[0]['most_severe_consequence']
					print(str_most_severe_consequence)
					sys.exit(1)
				'''preparing string to call EXAC REST API'''
				str_temp = 'http://exac.hms.harvard.edu/rest/variant/variant/'+record_CHROM+"-"+str(record_POS)+"-"+record_REF+"-"+str(alt)
				resp = requests.get(str_temp)
				if resp.status_code != 200:
					'''This means something went wrong'''
					raise ApiError('GET /tasks/ {}'.format(resp.status_code))
				'''Getting response from exac in to json object'''	
				json_resp_exac = resp.json()
				Exac_rsid=""
				Exac_site_quality=""
				Exac_filter_status=""
				Exac_pop_freq_list=[]
				'''Identifysing if requested variant is in exac DB'''
				if 'pop_acs' in json_resp_exac:
					'''extracting various exac values for the variant'''
					Exac_pop_freq_list.append(str(json_resp_exac['allele_freq']))
					Exac_rsid=str(json_resp_exac['rsid'])
					Exac_site_quality=str(json_resp_exac['site_quality'])
					Exac_filter_status=str(json_resp_exac['filter'])
					'''calculating various population freq'''
					for pop in exac_pop_list:
						if str(json_resp_exac['pop_ans'][pop]) == "0":
							Exac_pop_freq_list.append("0")
						else:		
							Exac_pop_freq_list.append(str(round(float(json_resp_exac['pop_acs'][pop])/float(json_resp_exac['pop_ans'][pop]),3)))
				else:
					Exac_pop_freq_list.append("NA")
					Exac_rsid="NA"
					Exac_site_quality="NA"
					Exac_filter_status="NA"
				'''Combining various pop freqs'''	
				Exac_pop_freq=str.join(",",Exac_pop_freq_list)
				list_vep_variant_type.append(str_most_severe_consequence)
				list_exac_rsid.append(Exac_rsid)
				list_exac_site_quality.append(Exac_site_quality)
				list_exac_filter_status.append(Exac_filter_status)
				list_exac_pop_freq.append(Exac_pop_freq)
			'''Combining exac values from each alternate allele'''	
			str_vep_variant_type=str.join(',',list_vep_variant_type)
			str_exac_rsid=str.join(',',list_exac_rsid)
			str_exac_site_quality=str.join(',',list_exac_site_quality)
			str_exac_filter_status=str.join(',',list_exac_filter_status)
			str_exac_pop_freq=str.join(',',list_exac_pop_freq)
			'''Writing annotations to output vcf file'''
			list_record[7]=list_record[7]+';VEP_VARIANT_TYPE='+str_vep_variant_type+';EXAC_RSID='+str_exac_rsid+';EXAC_SITE_QUALITY='+str_exac_site_quality+';EXAC_FILTER_STATUS='+str_exac_filter_status+';EXAC_POP_FREQ='+str_exac_pop_freq
			list_record[8]=list_record[8]+':VP'
			'''iterating through each sample in the vcf file for each variant'''
			for samp_index in range(9,len(list_record)):
				list_temp_samp=list_record[samp_index].split(':')
				'''total depth'''
				dp_temp_samp=float(list_temp_samp[index_DP])
				'''Num reads supporting variants'''
				ao_temp_samp=list_temp_samp[index_AO]
				list_ao_temp_samp = ao_temp_samp.split(',')
				list_temp_alt=[]
				'''calculating freq percentage for each allele'''
				for temp_alt in list_ao_temp_samp:
					vp_temp_samp=str(round(100*(float(temp_alt)/dp_temp_samp),3))
					list_temp_alt.append(vp_temp_samp)
				vp_temp_samp=str.join(',',list_temp_alt)	
				list_record[samp_index]=list_record[samp_index]+':'+vp_temp_samp
			'''combining the new values to record and writing to output vcf file'''	
			record=str.join("\t",list_record)
			myfile.write(record+"\n")
	fobj.close()
	myfile.close()
	
if __name__ == "__main__":
	main()
                     