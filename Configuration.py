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

       #config file to read
        self._scp.read('settings.cfg')
        

    def get_account(self):
        """Returns the current selected account
        """
        #TODO: Properly implement the functionality to get the 
        #account from a persistence location

        #check whether the user has selected a default account
        if self._scp.get('acc_info','has_default')=="True":
            accountName=self._scp.get('acc_info','account')

            return self._am.get_accounts()[accountName]
        
        
        return None

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
        #Set the proxy only if valid arguments are passed
        if url and port:
        
            os.environ['http_proxy']=url+":"+port
            os.environ['https_proxy']=url+":"+port

    def get_proxy(self, ):
        """Returns the proxy settings as an array 
        Array[0]=http proxy settings
        Array[1]=https proxy settings
        """
        #find out from where to get the proxy settings
        get_proxy_from=self._scp.get("proxy_data","get_from")

        #act accordingly

        #get proxy settings from system
        if get_proxy_from=='system':
            proxyData=self.__get_sytem_proxy_settings()
            mode=proxyData[0]
            http_proxy=proxyData[1]
            https_proxy=proxyData[2]
            #if the system has manually/automatically set the proxy settings
            if mode!='none':
                return [http_proxy,https_proxy]
            #if the system uses a direct connection
            else:
                return [None,None]
        
        elif get_proxy_from=='file':
             http_proxy=self._scp.get("proxy_data","http")
             https_proxy=self._scp.get("proxy_data","https")
             return [http_proxy,https_proxy]

        #If no proxy is used 
        return [None,None]
       
    def __get_sytem_proxy_settings(self):
        """Get system proxy settings."""
        mode=Gio.Settings.new('org.gnome.system.proxy').get_string('mode')
        
        http_settings = Gio.Settings.new('org.gnome.system.proxy.http')
        http_host = http_settings.get_string('host')
        http_port = str(http_settings.get_int('port'))

        https_settings = Gio.Settings.new('org.gnome.system.proxy.https')
        https_host = https_settings.get_string('host')
        https_port = str(https_settings.get_int('port'))
        
        # if http_settings.get_boolean('use-authentication'):
        #     username = http_settings.get_string('authentication_user')
        #     password = http_settings.get_string('authentication_password')
        # else:
        #     username = password = None
        return [mode,http_host+":"+http_port,https_host+":"+https_port]   

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
        
