"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
Web: www.blog.ishans.info
Git: https://github.com/ishanthilina/Gnome-Online-Documents-Manager
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
	print self.confMan.get_proxy()
	#self.assertEqual(['1:2','3:4'],self.confMan.get_proxy(),'Proxy values does not match')

    def test_get_system_path(self):
	"""Tests the get_system_path() method
	"""
	print self.confMan.get_system_path()

    def test_get_account(self):
	"""Returns the google account the user has selected
	
	"""
	print self.confMan.get_account()
	
        

#test suite
suite = unittest.TestLoader().loadTestsFromTestCase(ConfigurationManagerTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
