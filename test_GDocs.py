"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
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
        

       

        
        self._gdcManger=GDocs.GDClientManager()
        self._am=Authentication.AccountManager()

        self._gdcm=GDocs.GDClientManager()
    
        
        
    #     self._gdcm.set_proxy("http://cache.mrt.ac.lk","3128")


    def test_get_client(self):
        """Tests the get_client method
        """
        import gdata.docs.client
        
        account=self._am.get_accounts().pop()

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
        import gdata.docs.client
        self._am=Authentication.AccountManager()
        self._gdcm=GDocs.GDClientManager()
        self._gdam=GDocs.GDActionsManager(self._gdcm)
    
    def test_file_download(self):
        """Tests the file download functionality
        """
        
        account=self._am.get_accounts().pop()

        
        
        # self._gdcm.set_proxy("http://cache.mrt.ac.lk","3128")
        self._gdcm.authenticate_client(account)
        #self._gdam.GetAllResourcesSample()
        

        
       
    def test_upload_new_doc(self):
        """Tests the upload_doc() method
        """
        import gdata.docs.data
        
        account=self._am.get_accounts().pop()

        self._gdcm.authenticate_client(account)
        #self._gdcm.set_proxy("http://cache.mrt.ac.lk","3128")


        #col=self._gdam.get_all_folders().pop()
        col=None
        # print col.title.text

        print 'Uploading doc'
        doc=self._gdam.upload_new_doc('/home/ishan/up.odt',col,"My testing upload")
        print 'updating doc'
        self._gdam.update_doc(doc,'/home/ishan/ddd.odt')
        #self.assertIsInstance(doc,gdata.docs.data.Resource,"Class type does not match.")

    def test_get_all_folders(self):
        """Tests the get_all_folders() method
        """
        account=self._am.get_accounts().pop()

        self._gdcm.authenticate_client(account)

        # for folder in self._gdam.get_all_folders():
        #     print folder.title.text
        
#test suite
suite1 = unittest.TestLoader().loadTestsFromTestCase(GDClientManagerTester)
suite2 = unittest.TestLoader().loadTestsFromTestCase(GDActionsManagerTester)
unittest.TextTestRunner(verbosity=2).run(suite1)
unittest.TextTestRunner(verbosity=2).run(suite2)
