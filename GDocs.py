"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
"""

import os

import gdata.docs.client

import MyExceptions


class GDClientManager():
    """Handles the creation and authentication of GDocs clients
    """
    
    def __init__(self,confMan):
        """
        """
        self._client = gdata.docs.client.DocsClient(source='Gnome Online Documents Manager')
        self._client.ssl=True
        self._confMan=confMan
        
        #Keep a boolean to verify whether the client has been authenticated or not
        self._is_Authenticated=False
    #
    def authenticate_client(self, account):
        """Authenticates the GDocs client using the Account object passed to it
        
        Arguments:
        - `account`:Authentication.Account
        """

        
        self._CONSUMER_KEY=account.get_consumer_key()
        self._CONSUMER_SECRET=account.get_consumer_secret()
        self._TOKEN=account.get_access_token()
        self._TOKEN_SECRET=account.get_access_token_secret()

        #try to authenticate
        try:
            self._client.auth_token = gdata.gauth.OAuthHmacToken(self._CONSUMER_KEY, self._CONSUMER_SECRET, self._TOKEN,
                                               self._TOKEN_SECRET, gdata.gauth.ACCESS_TOKEN)
        except gdata.client.BadAuthentication:
            exit('Invalid user credentials given.')
        except gdata.client.Error:
            exit('Login Error')

        #Set proxy for the system
        http_proxy=self._confMan.get_proxy()[0]
        https_proxy=self._confMan.get_proxy()[1]
       
        self._confMan.set_proxy(http_proxy,https_proxy)
        self._is_Authenticated=True

    def get_client(self):
        """
        Returns the GDocs client if it has been authenticated
        """
        
        if self._is_Authenticated:
            return self._client
        else:
            raise MyExceptions.CustomException("Client not Authenticated")

    

class GDActionsManager():
    """Controls the interaction with the Google Docs service
    """
    
    def __init__(self, gdcManger):
        """
        
        Arguments:
        - `gdcManger`:
        """
        self._gdcManger = gdcManger

    
    def __create_client(self):
        """Creates a client from GDClientManager
        """
        return self._gdcManger.get_client()


   
    
    def get_all_documents(self):
        """Get and display all resources, using pagination."""
        client=self.__create_client()

        feed = client.GetResources()


        return feed
       
   

    def get_sub_folders(self, entry):
        """Returns all the sub Folders
    
        Arguments:
        - `entry`:gdata.docs.data.Resource (folder)
        """
        
        client=self.__create_client()
       
        subFolders=client.GetResources('https://docs.google.com/feeds/default/private/full'+'/'+entry.resource_id.text+'/contents/-/folder')

        return subFolders

   
    def get_folder_hierarchy(self):
        """Returns the folder hierarchy in Google Docs
        """
        client=self.__create_client()
        
        #Get the folders in root
        rootFolders=client.GetResources('https://docs.google.com/feeds/default/private/full/folder%3Aroot/contents/-/folder')

        #an array to store the root folders with the hierarchy
        folderHierarchy=[]

        #iterate through the root folders
        for rFolder in rootFolders.entry:
            rf=FolderGraphNode(rFolder,self)
            folderHierarchy.append(rf)
            rf.add_children()

        return folderHierarchy

       
        
    
    def download_doc(self, entry,path,format):
        """Downloads a given entry to the path under a given name
        
        Arguments:
        - `entry`:gdata.docs.data.Resource
        - `path`:string - path where the doc should be saved
        - `name`:string - name in which the doc should be saved
        - `format`:String- format to be downloaded
        """
        client=self.__create_client()

        
        client.DownloadResource(entry,path,extra_params={'exportFormat': format})
   
    
    def upload_new_doc(self, path,col,doc_title):
        """Uploads a new document to Google Docs
        
    
        Arguments:
        - `path`:String
        - `Col`:<collection object>
        - `doc_title`:The title of the doc
        """
       

        client=self.__create_client()

        doc = gdata.docs.data.Resource(type='document', title=doc_title)
        media = gdata.data.MediaSource()
        media.SetFileHandle(path, 'application/msword')

        #If a collection has not been defined
        
        if not col:
            
            doc = client.CreateResource(doc,media=media)
            return doc

        doc = client.CreateResource(doc,media=media, create_uri=gdata.docs.client.RESOURCE_UPLOAD_URI+'/'+col.resource_id.text+'/contents')
        
        
        return doc


    def create_collection(self, name):
        """Creates a Collection in Google Docs
    
        Arguments:
        - `name`: name of the collection
        """
        client=self.__create_client()
        col = gdata.docs.data.Resource(type='folder', title=name)
        col= client.CreateResource(col)
        return col

    def update_doc(self, entry,path):
        """Updates a document in the server
    
        Arguments:
        - `entry`: gdata.docs.Resource
        - `path`: String- path to the document
        """
        client=self.__create_client()
        media = gdata.data.MediaSource()
        media.SetFileHandle(path, 'application/msword')

       
        doc=client.UpdateResource(entry,media=media,update_metadata=False,new_revision=True,force=True)
        return doc

    
    def copy_resource_to_collection(self, collection,resource):
        """Copies the given resource to the given collection
    
        Arguments:
        - `collection`: a gdata.resource representing a folder/collection
        - `resource`:a gdata.resource representing a file
        """
        client=self.__create_client()
        client.MoveResource(resource,collection,keep_in_collections=True)
        
    
    def get_doc_data(self, entry):
        """Provides metadata on a given resource
        
        Arguments:
        - `entry`:gdata.docs.data.Resource
        
        """
        
       
        return [entry.GetResourceType(),entry.title.text,entry.resource_id.text]


class FolderGraphNode():
    """A class to setup the folder hierarchy
    """
    
    def __init__(self,folder,gdam):
        """folder: gdata.resource corresponding to a folder
        """
        print folder.title.text
        self._folder=folder
        self._folderHierarchy=[]
        self._gdam=gdam

        #the array to store the children nodes
        self._childrenArray=[]

    def get_folder(self):
        """Returns the gdata.entry folder corresponding to the node
        """
        return self._folder

    def get_children(self):
        """Return the child list
        """
        return self._childrenArray
        
    def add_children(self):
        """Adds children to the node 
    
    Arguments:
    - `child`: A folder node corresponding FolderGraphNode
    """
        

        #iterate through the children
        for child in self._gdam.get_sub_folders(self._folder).entry:
            childNode=FolderGraphNode(child,self._gdam)
            self._childrenArray.append(childNode)
            childNode.add_children()
