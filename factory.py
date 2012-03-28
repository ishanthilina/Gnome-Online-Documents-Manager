"""

"""
import GDocs
import Configuration
import Authentication

class Factory():
    """Creates instances of required classes and returns them
    """

    
    def __init__(self):
        """
        """

        #Create instances of all the classes
	self._confMan=Configuration.ConfigurationManager()
	self._gdcm=GDocs.GDClientManager(self._confMan)
	self._gdam=GDocs.GDActionsManager(self._gdcm)
	self._accMan=Authentication.AccountManager()


        account=self._confMan.get_account()
	self._gdcm.authenticate_client(account)




    def get_configuration_man(self):
	"""Returns an instance of the ConfigurationManager class
	"""
	return self._confMan
    


    def get_gdClient_man(self):
	"""Returns an instance of the GDClientManager class
	"""
	return self._gdcm

    def get_gdActions_man(self):
	"""Returns an instances of the GDActionsManager class
	"""
	return self._gdam

    def get_account_man(self):
	"""Returns an instance of the AccountManager class
	"""
	return self._accMan
