"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
"""

import DBusConnector
import re
import uno

import unohelper

class Account():
    """A class to store account details
    """
    
    def __init__(self, consumer_key, consumer_secret, access_token,access_token_secret,email):
        """
        
        Arguments:
        - `consumer_key`:String
        - `consumer_secret`:String
        - `access_token`:String
        - `access_token_secret`:String
        - `email`:String
        """
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token = access_token
        self._access_token_secret = access_token_secret
        self._email=email
        

    def get_consumer_key(self ):
        """returns the consumer key of the account
        """
        return self._consumer_key


    def get_consumer_secret(self):
        """returns the consumer secret of the account
        """
        return self._consumer_secret
        
    def get_access_token(self):
        """returns the access token of the account
        """ 
        return self._access_token
        
    def get_access_token_secret(self):
        """returns the access token secret of the account
        """ 
        return self._access_token_secret

    def get_email(self):
        """Returns the email of the account
        """
        return self._email
        

class AccountManager(unohelper.Base):
    """Manages the accounts that are available to the extension
    """
    
    def __init__(self):
        """
        """
 
        pass

    def get_accounts(self):
        """Returns the available accounts in Gnome Online Accounts manager
        """

        #To store the accounts
        accounts_arr=[]
        
        #get the accounts interaface from DBus
        iface=DBusConnector.DBusConnector().get_dbus_iface()

        #get the account information
        objects= iface.GetManagedObjects()

        #get all the accounts stored
        for entry in objects:
            test=re.search("/org/gnome/OnlineAccounts/Accounts", entry)
            if test:
                #get the OAuth details
                email= objects[entry]['org.gnome.OnlineAccounts.Account']['Identity'].encode('utf8')
                consumer_key=objects[entry]['org.gnome.OnlineAccounts.OAuthBased']['ConsumerKey'].encode('utf8')
                consumer_secret=objects[entry]['org.gnome.OnlineAccounts.OAuthBased']['ConsumerSecret'].encode('utf8')

                #get other important OAuth info
                oauth_iface=DBusConnector.DBusConnector().get_dbus_oauth_iface(entry)
                access_token= oauth_iface.GetAccessToken()[0].encode('utf8')
                access_token_secret=oauth_iface.GetAccessToken()[1].encode('utf8')

                #Create an account
                cl=Account(consumer_key,consumer_secret , access_token, access_token_secret,email )
                accounts_arr.append(cl)

 
        return accounts_arr


        
    
