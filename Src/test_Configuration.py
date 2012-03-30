"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
Web: www.blog.ishans.info
Git: https://github.com/ishanthilina/Gnome-Online-Documents-Manager
"""


import unittest

import Configuration
import Authentication


class ConfigurationManagerTestCase(unittest.TestCase):
    """Tests the ConfigurationManager class methods
    """

    def setUp(self):
	"""Sets up the test case
	"""
	self.confMan=Configuration.ConfigurationManager()
    

    def test_get_persist_active(self):
        """Tests the get_persist_active() method
        
        """
        self.assertIsInstance(self.confMan.get_persist_active(),bool,'Type mismatch')
        
    def test_get_account(self):
        """Tests the get_acccount() method
        """
        self.assertIsInstance(self.confMan.get_account(),Authentication.Account,'Type mismatch')
        
	
        

#test suite
suite = unittest.TestLoader().loadTestsFromTestCase(ConfigurationManagerTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
