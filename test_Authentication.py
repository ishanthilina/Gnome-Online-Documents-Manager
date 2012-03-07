"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
"""


import unittest


class AccountTestCase(unittest.TestCase):
    """Tests the Account class methods
    """

    def setUp(self):
        """
        """
        import Authentication
        #setup a dummy account
        self._account=Authentication.Account("Key","Secret","Acc_tok","Acc_tok_sec","email")
        
    
    def test_get_consumer_key(self):
       """Test get_consumer_key() method
       """
       
       self.assertEqual("Key",self._account.get_consumer_key(),"Consumer Keys don't match")
      
      
       

    def test_get_consumer_secret(self):
        """Test get_consumer_secret() method
        """
        self.assertEqual("Secret",self._account.get_consumer_secret(),"Consumer secrets don't match")

    def test_get_access_token(self):
        """Tests the get_access_token() method
        """
        self.assertEqual("Acc_tok",self._account.get_access_token(),"Access tokens don't match")

    def test_get_access_token_secret(self):
        """Tests the get_access_token_secret() method
        """
        self.assertEqual("Acc_tok_sec",self._account.get_access_token_secret(),"Access token secrets don't match")

    def test_get_email(self):
        """Tests the get_email() method
        """
        self.assertEqual("email",self._account.get_email(),"Email does not match")


class AccountManagerTestCase(unittest.TestCase):
    """Tests the AccountManager class
    """

    def setUp(self):
        """Sets up the test case environment
        """
        import Authentication
        self._am=Authentication.AccountManager()
        
    def test_get_accounts(self):
        """Tests the get_accounts() method
        """
       
        
        self.assertIsInstance(self._am.get_accounts(),dict,"Not an array of Account classes")
        
        
        
        
#Test suite
AccountTestSuite = unittest.TestLoader().loadTestsFromTestCase(AccountTestCase)
AccountManagerTestSuite = unittest.TestLoader().loadTestsFromTestCase(AccountManagerTestCase)
unittest.TextTestRunner(verbosity=2).run(AccountTestSuite)
unittest.TextTestRunner(verbosity=2).run(AccountManagerTestSuite)
