"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
"""


import unittest
import Configuration



class ConfigurationManagerTestCase(unittest.TestCase):
    """Tests the ConfigurationManager class methods
    """

    def setUp(self):
	"""Sets up the test case
	"""
	self.confMan=Configuration.ConfigurationManager()
    

    def test_persist_proxy(self):
	"""Tests the get_proxy method	
	"""
	
	self.confMan.persist_proxy('1','2','3','4')
	self.assertEqual(['1:2','3:4'],self.confMan.get_proxy(),'Proxy values does not match')

    
        

#test suite
suite = unittest.TestLoader().loadTestsFromTestCase(ConfigurationManagerTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
