"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
Web: www.blog.ishans.info
Git: https://github.com/ishanthilina/Gnome-Online-Documents-Manager
"""



import dbus


class DBusConnector():
    """Handles the interaction with the Gnome Online Accounts DBus service
    """
    
    def __init__(self):
        """
        """
        pass
        
    def get_dbus_iface(self):
        """Returns an interface to access the methods in Gnome Online Accounts DBus service
        """
        bus = dbus.SessionBus()
        proxy = bus.get_object('org.gnome.OnlineAccounts',
                           '/org/gnome/OnlineAccounts')
        #create an interface
        iface=dbus.Interface(proxy, dbus_interface='org.freedesktop.DBus.ObjectManager')
        

        return iface

    def get_dbus_oauth_iface(self, account):
        """Returns the interface for OAuth data access for the given account using DBus
        
        Arguments:
        - `account`:String
        """
        bus = dbus.SessionBus()
        accProxy=bus.get_object('org.gnome.OnlineAccounts',
                           account)
        #create an interface
        oauthIface=dbus.Interface(accProxy, dbus_interface='org.gnome.OnlineAccounts.OAuthBased')
        
        
        return oauthIface
