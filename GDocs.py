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
    
    def __init__(self):
        """
        """
        self._client = gdata.docs.client.DocsClient(source='yourCo-yourAppName-v1')
        
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

        self._is_Authenticated=True

    def get_client(self):
        """
        Returns the GDocs client if it has been authenticated
        """
        
        if self._is_Authenticated:
            return self._client
        else:
            raise MyExceptions.CustomException("Client not Authenticated")

    def set_proxy(self, url,port):
        """
        Sets proxy for the environment of the script
        
        Arguments:
        - `url`:URL of the proxy server
        - `port`:port of the proxy server
        """
        
        os.environ['http_proxy']=url+":"+port
        os.environ['https_proxy']=url+":"+port

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
       


    def download_doc(self, entry,path,name):
        """Downloads a given entry to the path under a given name
        
        Arguments:
        - `entry`:gdata.docs.data.Resource
        - `path`:string
        - `name`:string
        """
        client=self.__create_client()

        #type of the document
        doc_type=None

        #deterimine the document type
        #TODO- Edit the logic of the code to allow the user to modify the extension
        if entry.GetResourceType() == 'document':

            doc_type=".odt"

        elif entry.GetResourceType() == 'spreadsheet':
            doc_type=".xls"
            
        full_path=os.path.join(path,name+doc_type)
        print full_path
        
        client.DownloadResource(entry,full_path)

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



        doc = client.CreateResource(doc,media=media, collection=col)
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
        

    def _get_doc_type(self,entry):
        """Returns the type of the document

        Arguments:
        - `entry`:gdata.docs.data.Resource
            
        """
        print 'Doc type:', entry.GetResourceType()
        

    def get_doc_data(self, entry):
        """Provides metadata on a given resource
        
        Arguments:
        - `entry`:gdata.docs.data.Resource
        
        """
        
        
        # print 'Doc type:', entry.GetResourceType()
        # print 'Doc name: ', entry.title.text
        # print 'Resource id:', entry.resource_id
        # print 'Lables :'
        # for label in entry.GetLabels():
        #     print label,

        # print

        # print
        # print 'Collections (Folders): '

        # for data in entry.InCollections():
        #     for title in  data.GetAttributes(tag='title'):
        #         print title.value

        return [entry.GetResourceType(),entry.title.text]


