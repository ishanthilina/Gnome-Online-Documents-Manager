"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
Web: www.blog.ishans.info
Git: https://github.com/ishanthilina/Gnome-Online-Documents-Manager
"""


import re

import uno
import unohelper

import DBusConnector

class Account():
    """A class to store account details
    """
    
    def __init__(self, consumerKey, consumerSecret, accessToken,accessTokenSecret,email):
        """
        
        Arguments:
        - `consumerKey`:String
        - `consumerSecret`:String
        - `accessToken`:String
        - `accessToken_secret`:String
        - `email`:String
        """
        self._consumerKey = consumerKey
        self._consumerSecret = consumerSecret
        self._accessToken = accessToken
        self._accessTokenSecret = accessTokenSecret
        self._email=email
        

    def get_consumer_key(self ):
        """returns the consumer key of the account
        """
        return self._consumerKey


    def get_consumer_secret(self):
        """returns the consumer secret of the account
        """
        return self._consumerSecret
        
    def get_access_token(self):
        """returns the access token of the account
        """ 
        return self._accessToken
        
    def get_access_token_secret(self):
        """returns the access token secret of the account
        """ 
        return self._accessTokenSecret

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

        #dictionary to store the accounts
        accounts_dic={}
        
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
                consumerKey=objects[entry]['org.gnome.OnlineAccounts.OAuthBased']['ConsumerKey'].encode('utf8')
                consumerSecret=objects[entry]['org.gnome.OnlineAccounts.OAuthBased']['ConsumerSecret'].encode('utf8')

                #get other important OAuth info
                oauth_iface=DBusConnector.DBusConnector().get_dbus_oauth_iface(entry)
                accessToken= oauth_iface.GetAccessToken()[0].encode('utf8')
                accessTokenSecret=oauth_iface.GetAccessToken()[1].encode('utf8')

                #Create an account
                cl=Account(consumerKey,consumerSecret , accessToken, accessTokenSecret,email )
                accounts_dic[email]=cl

 
        return accounts_dic


        
    
