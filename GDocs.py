"""
Author: Ishan Thilina Somasiri
E-mail: ishan@ishans.info
"""


import gdata.docs.client
import MyExceptions
import os

class GDClientManager():
    """Handles the creation, authenitcation of GDocs clients
    """
    
    def __init__(self,confMan):
        """
        """
        self._client = gdata.docs.client.DocsClient(source='yourCo-yourAppName-v1')
        self._client.ssl=True
        self._confMan=confMan
        
        #Keep a boolean to verify whether the client has been authenticated or not
        self._is_Authenticated=False

    def authenticate_client(self, account):
        """Authenticates the GDocs client using the Account object passed to it
        
        Arguments:
        - `account`:
        """

        
        self._CONSUMER_KEY=account.get_consumer_key()
        self._CONSUMER_SECRET=account.get_consumer_secret()
        self._TOKEN=account.get_access_token()
        self._TOKEN_SECRET=account.get_access_token_secret()
        
        try:
            self._client.auth_token = gdata.gauth.OAuthHmacToken(self._CONSUMER_KEY, self._CONSUMER_SECRET, self._TOKEN,
                                               self._TOKEN_SECRET, gdata.gauth.ACCESS_TOKEN)
        except gdata.client.BadAuthentication:
            exit('Invalid user credentials given.')
        except gdata.client.Error:
            exit('Login Error')

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


    #for testing purposes
    def GetAllResourcesSample(self):
        """Get and display all resources, using pagination."""
        client=self.__create_client()

        feed = client.GetResources()


        for entry in feed.entry:
            self.download_doc(entry,'/home/ishan/','name')
            break

    def get_all_documents(self):
        """Get and display all resources, using pagination."""
        client=self.__create_client()

        feed = client.GetResources()


        return feed
       
    def get_all_folders(self):
        """Returns a list of all the folsers in the server
        """
        client=self.__create_client()

        feed = client.GetResources(uri=gdata.docs.client.RESOURCE_FEED_URI+'?showfolders=true')

        folders=[]
        
        for entry in feed.entry:
            if entry.GetResourceType()=='folder':
                folders.append(entry)
                

        return folders

    def get_sub_folders(self, entry):
        """Returns all the sub Folders
    
        Arguments:
        - `entry`:gdata.docs.data.Resource (folder)
        """
        
        client=self.__create_client()
       
        subFolders=client.GetResources('https://docs.google.com/feeds/default/private/full'+'/'+entry.resource_id.text+'/contents/-/folder')

        return subFolders

    #TODO: Implement the functionality correctly
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

        # #store all the folders to iterate
        # folders=[]
        # #to store the folder structure
        # folStruct=[]
        # #print rootFolders
        # ##What happens if there are no sub folders...?
        # for folder in rootFolders.entry:
        #     # print self.get_doc_data(folder)
        #     folders.append(folder)

        # #iterate through all the folders
        # #for folder in folders:
        #     #subFolders=self.get_sub_folders(folder)
        #     #   print folder.title.text

        #     #add the sub folders to the list
        #     #            for subF in subFolders.entry:
        #     #   print subF.title.text
        
        # return folders
        
        

    def download_doc(self, entry,path,format):
        """Downloads a given entry to the path under a given name
        
        Arguments:
        - `entry`:gdata.docs.data.Resource
        - `path`:string
        - `name`:string
        - `format`:String- format to be downloaded
        """
        client=self.__create_client()

        #type of the document
        doc_type=None

        #deterimine the document type
        #TODO- Edit the logic of the code to allow the user to modify the extension
        # if entry.GetResourceType() == 'document':

        #     doc_type=".odt"

        # elif entry.GetResourceType() == 'spreadsheet':
        #     doc_type=".pdf"
            
        # full_path=os.path.join(path,name+doc_type)
        # print full_path
        
        client.DownloadResource(entry,path,extra_params={'exportFormat': format})

    def download_spreadsheet(self, path,entry,format):
        """Downloads the given spreadsheet
    
    Arguments:
    - `path`:String-path to download the spreadsheet
    - `entry`:String - Resource
    - `format`:String- format to be downloaded
    """
        client=self.__create_client()
        client.DownloadResource(entry,path,extra_params={'exportFormat': format})

    def upload_new_doc(self, path,col,doc_title):
        """Uploads a new document to Google Docs
        
    
        Arguments:
        - `path`:String
        - `Col`:<collectio object>
        - `doc_title`:The title of the doc
        """
        #TODO:
        #Add collection selection support
        #Add spreadsheet,presentations upload support

        client=self.__create_client()

        doc = gdata.docs.data.Resource(type='document', title=doc_title)
        media = gdata.data.MediaSource()
        media.SetFileHandle(path, 'application/msword')

        #If a collection has not been defined
        
        if not col:
            
            doc = client.CreateResource(doc,media=media)
            return doc

        doc = client.CreateResource(doc,media=media, create_uri=gdata.docs.client.RESOURCE_UPLOAD_URI+'/'+col.resource_id.text+'/contents')
        # newResource = gdata.docs.data.Resource(path, "document title")

        # media = gdata.data.MediaSource()
        # media.SetFileHandle(path,'application/msword')

        # doc = client.CreateResource(newResource, create_uri=gdata.docs.client.RESOURCE_UPLOAD_URI, media=media,collection=col)

        
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
        - `entry`:
        - `path`: String- path to the document
        """
        client=self.__create_client()
        media = gdata.data.MediaSource()
        media.SetFileHandle(path, 'application/msword')

        # print entry.resource_id.text
        #doc=client.UpdateResource(entry)
        doc=client.UpdateResource(entry,media=media,update_metadata=False,new_revision=True,force=True)
        return doc

    def _get_doc_type(self,entry):
        """Returns the type of the document

        Arguments:
        - `entry`:gdata.docs.data.Resource
            
        """
        print 'Doc type:', entry.GetResourceType()

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
        
        # print '\n'
        # print '=================================================='
        # print 'Doc type:', entry.GetResourceType()
        # print 'Doc name: ', entry.title.text
        # print 'Resource id:', entry.resource_id.text
        # print 'Lables :'
        # for label in entry.GetLabels():
        #     print label,

        # print

        # print
        # print 'Collections (Folders): '

        # for data in entry.InCollections():
        #     for title in  data.GetAttributes(tag='title'):
        #         print title.value

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
