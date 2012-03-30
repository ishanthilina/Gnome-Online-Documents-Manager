"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
Web: www.blog.ishans.info
Git: https://github.com/ishanthilina/Gnome-Online-Documents-Manager
"""


import unittest



class GDClientManagerTester(unittest.TestCase):
    """Tests teh GDClientManager class
    """

    def setUp(self):
        """Sets up the test case environment

        """

        import Authentication
        import GDocs
        import gdata.docs.client
        import Configuration
        

       

        self._confMan=Configuration.ConfigurationManager()
        self._gdcManger=GDocs.GDClientManager(self._confMan)
        self._am=Authentication.AccountManager()

        self._gdcm=GDocs.GDClientManager(self._confMan)
        
    
        
        
   


    def test_get_client(self):
        """Tests the get_client method
        """
        import gdata.docs.client
        
        
        account=self._confMan.get_account()

        self._gdcm.authenticate_client(account)

        self.assertIsInstance(self._gdcm.get_client(),gdata.docs.client.DocsClient,"types doesn't match")

class GDActionsManagerTester(unittest.TestCase):
    """Tests the GDActionsManager class
    """

    def setUp(self):
        """Sets up the development environment
        """
        import Authentication
        import GDocs
        import Configuration
        import gdata.docs.client

        self._confMan=Configuration.ConfigurationManager()
        self._am=Authentication.AccountManager()
        self._gdcm=GDocs.GDClientManager(self._confMan)
        self._gdam=GDocs.GDActionsManager(self._gdcm)
       
    
   

        
       
 
    def test_get_folder_hierarchy(self):
        """Tests the get_folder_hierarchy() method
    """
        account=self._confMan.get_account()
        self._gdcm.authenticate_client(account)

        print 'in test method'
        self.assertIsInstance(self._gdam.get_folder_hierarchy(),list,'Type mismatch')
            
        
        
#test suite
suite1 = unittest.TestLoader().loadTestsFromTestCase(GDClientManagerTester)
suite2 = unittest.TestLoader().loadTestsFromTestCase(GDActionsManagerTester)
unittest.TextTestRunner(verbosity=2).run(suite1)
unittest.TextTestRunner(verbosity=2).run(suite2)
