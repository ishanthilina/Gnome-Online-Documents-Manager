import Authentication

class ConfigurationManager():
    """Provides an interface to access and configure the extension settings
    """
    
    def __init__(self):
        """
        """
        self._am=Authentication.AccountManager()
        

    def get_account(self):
        """Returns the current selected account
        """
        #TODO: Properly implement the functionality to get the 
        #account from a persistence location

        account=self._am.get_accounts().pop()
        return account
