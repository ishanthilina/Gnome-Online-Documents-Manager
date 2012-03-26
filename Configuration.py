from gi.repository import Gio
import os
import ConfigParser

import Authentication


class ConfigurationManager():
    """Provides an interface to access and configure the extension settings
    """
    
    def __init__(self):
        """
        """

        #TODO: Currently in this class the way to persist acounts and
        #the way to handle their usage status is very primitive. Need
        #to improve this.
        #ex:
        #Bad method- set_persist_active()
        
        self._am=Authentication.AccountManager()
        
        self._scp=ConfigParser.SafeConfigParser()

        #settings file name
        settingsFile='settings.cfg'

        #The file path of the settings file
        self._filePath=os.path.expanduser('~')+'/.'+settingsFile

       #config file to read
        self._scp.read(self._filePath)

        #Currently set account
        self._account=None

        #if there's a persisted setting to use a particular account
        if self._scp.get('acc_info','has_default')=="True":
            accountName=self._scp.get('acc_info','account')

            #if the account is still available in DBus

            if accountName in self._am.get_accounts():
                self._account=self._am.get_accounts()[accountName]
        
        

    def get_persisted_account(self):
        """Returns the current (persisted) default account
        """
       

        #check whether the user has selected a default account
        if self._scp.get('acc_info','has_default')=="True":
            accountName=self._scp.get('acc_info','account')

            return self._am.get_accounts()[accountName]
        
        
        return None

    def set_persisted_account(self, account):
        """Persists the default account
        
        Arguments:
        - `account`:Authentication.Account
        """
        
        self._scp.set('acc_info','account',account.get_email())
        
                
        # Writing our configuration file
        with open(self._filePath, 'wb') as configfile:
            self._scp.write(configfile)

    def set_persist_active(self):
        """Mark the persisted account as active
        """
        self._scp.set('acc_info','has_default','True')
        
                
        # Writing our configuration file
        #TODO - Correct file path
        with open('/home/ishan/4sep/settings.cfg', 'wb') as configfile:
            self._scp.write(configfile)

    def get_persist_active(self):
        """Returns whether the persisted account is marked as active or not 
        """
        if self._scp.get('acc_info','has_default')=='True':
            return True
        else:
            return False

    def get_account(self):
        """Returns the current selected account
        """
        
        return self._account

    def set_account(self, account):
        """Sets the current Account
        
        Arguments:
        - `account`:Authentication.Account
        """
        self._account=account
        

    def get_system_path(self):
        """Returns the path of the place where the python scripts are
        """
        
        return os.path.expanduser('~')+"/"+self._scp.get("file_path","path")

    def set_proxy(self, http,https):
        """
        Sets proxy for the environment of the script
        
        Arguments:
        - `url`:URL of the proxy server
        - `port`:port of the proxy server
        """
        #Set the proxy only if valid arguments are passed
        if http and https:

            
            os.environ['http_proxy']='http://'+http
            os.environ['https_proxy']='https://'+https


        elif not http and not https:
            os.environ['http_proxy']=''
            os.environ['https_proxy']=''
            
       
    def get_proxy(self):
        """Returns the proxy settings as an array 
        Array[0]=http proxy settings
        Array[1]=https proxy settings
        """
        #find out from where to get the proxy settings
        get_proxy_from=str(self._scp.get("proxy_data","get_from"))

        #act accordingly
        
        #get proxy settings from system
        if get_proxy_from=='system':
            
            proxyData=self.__get_sytem_proxy_settings()
            mode=proxyData[0]
            http_proxy=str(proxyData[1])
            https_proxy=str(proxyData[2])
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

    def persist_proxy(self, http,https):
        """
        
        Arguments:
        - `http_url`:
        - `http_port`:
        - `https_url`:
        - `https_port`:
        """

        ##TODO: Add code to remove extra http or https text
        ##ex:
        ##http://http://www.cache.mrt.ac.lk
       
        #self._cp.add_section('proxy_data')
        self._scp.set('proxy_data','http',http)
        self._scp.set('proxy_data','https',https)
                
        # Writing our configuration file
        with open(self._filePath, 'wb') as configfile:
            self._scp.write(configfile)
        
    def set_proxy_type(self, type):
        """Persists the type of proxy that needs to be used
    
    Arguments:
    - `type`:String - none, file, system
    """
        self._scp.set('proxy_data','get_from',type)

        # Writing our configuration file
        with open(self._filePath, 'wb') as configfile:
            self._scp.write(configfile)

    def get_persited_proxy(self):
        """Returns the persisted proxy settings
        """
        http_proxy=self._scp.get("proxy_data","http")
        https_proxy=self._scp.get("proxy_data","https")
        return [http_proxy,https_proxy]

    def get_proxy_from(self):
        """Returns from where the proxy settings are retrieved
        """
        return self._scp.get("proxy_data","get_from")
