"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
Web: www.blog.ishans.info
Git: https://github.com/ishanthilina/Gnome-Online-Documents-Manager
"""


import unittest
import dbus

import DBusConnector


class DBusConnectorTestCase(unittest.TestCase):
    """Tests the DBusConnector class methods
    """


    def setUp(self):
        """Sets up the test case
        """
        self.connector=DBusConnector.DBusConnector()
        

        
   
    def test_get_dbus_iface(self):
        """
        """
        self.assertIsInstance(self.connector.get_dbus_iface(),dbus.proxies.Interface,"Object types does not match. Expected: <dbus.proxies.Interface>")

    def test_get_dbus_oauth_ifac(self, ):
        """
        """

        self.assertIsInstance(self.connector.get_dbus_oauth_iface("/org/gnome/OnlineAccounts/Accounts/account_1323594572"),dbus.proxies.Interface,"Object types does not match. Expected: <dbus.proxies.Interface>")
        

#test suite
suite = unittest.TestLoader().loadTestsFromTestCase(DBusConnectorTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
