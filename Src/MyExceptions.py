"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
Web: www.blog.ishans.info
Git: https://github.com/ishanthilina/Gnome-Online-Documents-Manager
"""


class CustomException(Exception):
    """
    Class to create custom exceptions
    """
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)
