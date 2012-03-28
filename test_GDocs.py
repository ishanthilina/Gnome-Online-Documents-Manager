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
        
    
        
        
    #     self._gdcm.set_proxy("http://cache.mrt.ac.lk","3128")


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
       
    
    def test_file_download(self):
        """Tests the file download functionality
        """
        
        account=self._confMan.get_account()

        
        
        # self._gdcm.set_proxy("http://cache.mrt.ac.lk","3128")
        self._gdcm.authenticate_client(account)
        #self._gdam.GetAllResourcesSample()
        

        
       
    def test_upload_new_doc(self):
        """Tests the upload_doc() method
        """
        import gdata.docs.data
        
        account=self._confMan.get_account()

        self._gdcm.authenticate_client(account)
        #self._gdcm.set_proxy("http://cache.mrt.ac.lk","3128")


        #col=self._gdam.get_all_folders().pop()
        #self._gdam.get_doc_data(col)
        col=None
        # print col.title.text

        print 'Uploading doc'
        #doc=self._gdam.upload_new_doc('/home/ishan/up.odt',col,"My testing upload")
        #print 'updating doc'
        #self._gdam.update_doc(doc,'/home/ishan/ddd.odt')
        #self.assertIsInstance(doc,gdata.docs.data.Resource,"Class type does not match.")

    def test_get_all_folders(self):
        """Tests the get_all_folders() method
        """
        account=self._confMan.get_account()

        self._gdcm.authenticate_client(account)

        #for folder in self._gdam.get_all_folders():
        #   print folder.title.text
            #self._gdam.get_sub_folders(folder)

    def test_get_folder_hierarchy(self):
        """Tests the g
    """
        account=self._confMan.get_account()
        self._gdcm.authenticate_client(account)

        print 'in test method'
        for entry in  self._gdam.get_folder_hierarchy():
            print entry.get_folder().title.text
        
        
#test suite
suite1 = unittest.TestLoader().loadTestsFromTestCase(GDClientManagerTester)
suite2 = unittest.TestLoader().loadTestsFromTestCase(GDActionsManagerTester)
unittest.TextTestRunner(verbosity=2).run(suite1)
unittest.TextTestRunner(verbosity=2).run(suite2)
