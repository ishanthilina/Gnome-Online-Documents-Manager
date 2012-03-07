import Authentication
import os
import ConfigParser

class ConfigurationManager():
    """Provides an interface to access and configure the extension settings
    """
    
    def __init__(self):
        """
        """
        self._am=Authentication.AccountManager()
        
        self._scp=ConfigParser.SafeConfigParser()

       
        self._scp.read('settings.cfg')
        

    def get_account(self):
        """Returns the current selected account
        """
        #TODO: Properly implement the functionality to get the 
        #account from a persistence location

        account=self._am.get_accounts().pop()
        return account

    def get_system_path(self):
        """Returns the path of the place where the python scripts are
        """
        
        return os.path.expanduser('~')+"/"+self._scp.get("file_path","path")

    def set_proxy(self, url,port):
        """
        Sets proxy for the environment of the script
        
        Arguments:
        - `url`:URL of the proxy server
        - `port`:port of the proxy server
        """
        
        os.environ['http_proxy']=url+":"+port
        os.environ['https_proxy']=url+":"+port

    def get_proxy(self, ):
        """Returns the proxy settings as an array 
        Array[0]=http proxy settings
        Array[1]=https proxy settings
        """
        
        
        http_proxy=self._scp.get("proxy_data","http")
        https_proxy=self._scp.get("proxy_data","https")

        return [http_proxy,https_proxy]

    def persist_proxy(self, http_url,http_port,https_url,https_port):
        """
        
        Arguments:
        - `http_url`:
        - `http_port`:
        - `https_url`:
        - `https_port`:
        """

       
        #self._cp.add_section('proxy_data')
        self._scp.set('proxy_data','http',http_url+':'+http_port)
        self._scp.set('proxy_data','https',https_url+':'+https_port)
                
        # Writing our configuration file
        with open('settings.cfg', 'wb') as configfile:
            self._scp.write(configfile)
        
