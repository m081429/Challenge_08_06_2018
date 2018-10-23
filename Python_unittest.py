#!/usr/local/biotools/python/2.7.10/bin/python3
__author__ = "Naresh Prodduturi"
__email__ = ""
__status__ = "Dev"
############################################################################
####Unit tests #############################################################
##Version: 1.0 #############################################################
##Date: 10/22/2018##########################################################
############################################################################

import unittest
from Python_sample import *

class Tests_Sample(unittest.TestCase):
 
	def setUp(self):
		pass
	
	'''Tests to test VEP API'''
	def test_1_VEP_Most_sever_conse(self):
		self.assertEqual(VEP_Most_sever_conse("1","36937059","A","G"),'synonymous_variant')
    
	def test_2_VEP_Most_sever_conse(self):
		self.assertEqual(VEP_Most_sever_conse("1","27688633","G","A"),'missense_variant')
		
	def test_3_VEP_Most_sever_conse(self):
		self.assertNotEqual(VEP_Most_sever_conse("1","36937059","A","G"),'missense_variant')

	'''Tests to test EXAC_REST_API API'''
	def test_1_EXAC_REST_API(self):
		Exac_rsid="rs116517080"
		Exac_site_quality="5626257.9"
		Exac_filter_status="PASS"
		Exac_pop_freq="0.0165102162664,0.025,0.0,0.013,0.004,0.01,0.002,0.016"
		expected_output=[Exac_rsid,Exac_site_quality,Exac_filter_status,Exac_pop_freq]
		self.assertEqual(EXAC_REST_API("1","14107932","C","T"),expected_output)
    
	'''Tests to test EXAC_REST_API API'''
	def test_2_EXAC_REST_API(self):
		Exac_rsid="rs1046331"
		Exac_site_quality="187610745.12"
		Exac_filter_status="PASS"
		Exac_pop_freq="0.825572198329,0.845,0.716,0.838,0.93,0.802,0.757,0.817"
		expected_output=[Exac_rsid,Exac_site_quality,Exac_filter_status,Exac_pop_freq]
		self.assertEqual(EXAC_REST_API("1","14143003","A","G"),expected_output)
	
	def calc_read_supp_var(self):
		self.assertEqual(calc_read_supp_var(30,60),0.500)
 
if __name__ == '__main__':
	unittest.main()