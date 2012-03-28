import sys
import os
import subprocess
from gi.repository import Gtk as gtk
from gi.repository import Gdk
from gi.repository import GObject as gobject
from gi.repository import Notify as pynotify
import time
import threading

import GDocs
import Configuration
import Authentication
import factory
# try:
	
# 	import pynotify
# except:
# 	pass

# try:
#  	import pygtk
#   	pygtk.require("2.0")
# except:
#   	pass
# try:
# 	import gtk
#   	import gtk.glade
# except:
# 	sys.exit(1)

#import gobject

class GUIManager():
	"""Provides an interface to access the GUI functionality
	"""
	
	def __init__(self):
		"""
		"""
		objFactory=factory.Factory()
                
		#get the instances
		self._gdcm=objFactory.get_gdClient_man()
		self._gdam=objFactory.get_gdActions_man()
		self._confMan=objFactory.get_configuration_man()
		self._accMan=objFactory.get_account_man()
		
		
		
		
		


	def show_import_window(self):
		"""Shows the import Google Documents window"""

                window=ImportGDocsWindow(self._gdam,self._confMan)
		#window=MainWindow()

	def show_export_window(self,filePath):
		"""Shows the export Documents window
		"""
		
		window=ExportGDocsWindow(self._gdam,self._confMan,filePath)

	def show_settings_window(self):
		"""Shows the settings window
		"""
		window=SettingsWindow(self._confMan,self._accMan,self._gdcm)



class SettingsWindow():
	"""Shows the Settings  window for the system
	"""
	
	def __init__(self,confMan,accMan,gdcm):
		"""
		
                Arguments:
                - `gdam`:GDocs.GDActionsManager
		- `confMan`:Configuration.ConfigurationManager
		-`accMan`:Authentication.AccountManager
		-`gdcm`:GDocs.GDClientManager
                """
		#self._gdam = gdam
		self._confMan=confMan
		self._accMan=accMan
		self._gdcm=gdcm
		

                #load and setup the GUI components

               
		filename = confMan.get_system_path()+"SettingsWindow.glade"
		builder = gtk.Builder()
		builder.add_from_file(filename)
		builder.connect_signals(self)

                #widgets for accounts settings
		self._accountsList=builder.get_object('Combo_AccountsList')
		self._rbFromPersist=builder.get_object('rbFromPersist')
		self._rbFromList=builder.get_object('rbFromList')
		self._cbRememberAcc=builder.get_object('cbRememberAcc')
		self._accLabel=builder.get_object('accLabel')

                #widgets for proxy Settings
		self._tbHttp=builder.get_object('tbHttp')
		self._tbHttps=builder.get_object('tbHttps')
		self._rbNoProxy=builder.get_object('rbNoProxy')
		self._rbSysProxy=builder.get_object('rbSysProxy')
		self._rbCustProxy=builder.get_object('rbCustProxy')
		self._tbHttpPort=builder.get_object('tbHttpPort')
		self._tbHttpsPort=builder.get_object('tbHttpsPort')

                #Set text for the current selected default account
                if self._confMan.get_persisted_account():
			self._accLabel.set_text(self._confMan.get_account().get_email())
		else:
			self._accLabel.set_text('None')


		
	

		#set text for the currently persisted proxy settings
		httpUrl=self._confMan.get_persited_proxy()[0].split(':')[0]
		httpPort=self._confMan.get_persited_proxy()[0].split(':')[1]
		httpsUrl=self._confMan.get_persited_proxy()[1].split(':')[0]
		httpsPort=self._confMan.get_persited_proxy()[1].split(':')[1]
		self._tbHttp.set_text(httpUrl)
		self._tbHttpPort.set_text(httpPort)
		self._tbHttps.set_text(httpsUrl)
		self._tbHttpsPort.set_text(httpsPort)
		
		
		
		accList=gtk.ListStore(str,gobject.TYPE_PYOBJECT )
		
		cell = gtk.CellRendererText()
		self._accountsList.pack_start(cell, True)
		self._accountsList.add_attribute(cell, 'text', 0)
		self._accountsList.set_model(accList)

		#add the accounts to the list
		for accName,accObj in self._accMan.get_accounts().iteritems():
			
			accList.append([accName,accObj])
			#pass
                
		self._accountsList.set_active(0)




		#select the proper account selection method
		if self._confMan.get_persist_active():
			self._rbFromPersist.set_active(True)
			self._accountsList.set_sensitive(False)
			self._cbRememberAcc.set_sensitive(False)

			
		else:
			self._rbFromList.set_active(True)
			self._accountsList.set_sensitive(True)
			self._cbRememberAcc.set_sensitive(True)


		#Show the current proxy usage method
		get_proxy_from=self._confMan.get_proxy_from()

                if get_proxy_from=='none':
			self._rbNoProxy.set_active(True)
		elif get_proxy_from=='file':
			self._rbCustProxy.set_active(True)
		elif get_proxy_from=='system':
			self._rbSysProxy.set_active(True)
                
	
		
	def cb_use_the_acc_selected(self,arg):
		"""Event handler
		"""
	
		self._accountsList.set_sensitive(False)
		self._cbRememberAcc.set_sensitive(False)

	def cb_from_list_selected(self,arg):
		"""Event handler
		"""
		self._accountsList.set_sensitive(True)
		self._cbRememberAcc.set_sensitive(True)

	def ok_but_clicked(self, args):
		"""Action handler for the Ok button
    
		Arguments:
		- `args`:
		"""
		self.apply_but_clicked(args)
		self.destroy_all(args)

	def apply_but_clicked(self, args):
		"""
		
		Arguments:
		- `args`:
		"""
		##Handle Account settings first

                ##if account needs to be loaded from persistence
		if self._rbFromPersist.get_active():
			#if the account is null
                        if self._accLabel.get_text()=='None':
				self.show_error_dlg('Please select a valid account')
				self._rbFromList.set_active(True)
				return
			
			account=self._confMan.get_persisted_account()
			self._confMan.set_account(account)
			self._gdcm.authenticate_client(account)

			#else take it from the list
                elif self._rbFromList.get_active():
			
			account=self._accountsList.get_model()[self._accountsList.get_active()][1]
			self._confMan.set_account(account)
			self._gdcm.authenticate_client(account)

                        #if the settings needs to be persisted
			if self._cbRememberAcc.get_active():
				self._confMan.set_persisted_account(account)
				self._confMan.set_persist_active()
			
                       
                

                ##Handle proxy settings

                #if no proxy is used
                if self._rbNoProxy.get_active():
			self._confMan.set_proxy_type('none')
			self._confMan.set_proxy(None,None)

		#if system proxy is used
		elif self._rbSysProxy.get_active():
			self._confMan.set_proxy_type('system')
			self._confMan.set_proxy(self._confMan.get_proxy()[0],self._confMan.get_proxy()[1])

		#if a custom proxy setting is to be used
		elif self._rbCustProxy.get_active():
			self._confMan.set_proxy_type('file')
			http=self._tbHttp.get_text()+':'+self._tbHttpPort.get_text()
			https=self._tbHttps.get_text()+':'+self._tbHttpsPort.get_text()
			self._confMan.set_proxy(http,https)
			self._confMan.persist_proxy(http,https)


	def show_error_dlg(self, error_string):
		"""This Function is used to show an error dialog when
		an error occurs.
		error_string - The error string that will be displayed
		on the dialog.
		"""
		error_dlg = gtk.MessageDialog(type=gtk.MessageType.ERROR
					      , message_format=error_string
					      , buttons=gtk.ButtonsType.OK)
		error_dlg.run()
		error_dlg.destroy()


	def disable_custom_proxy(self, args):
		"""Disables the custom proxy related widgets
    
    Arguments:
    - `args`:
    """
		self._tbHttp.set_sensitive(False)
		self._tbHttps.set_sensitive(False)
		self._tbHttpPort.set_sensitive(False)
		self._tbHttpsPort.set_sensitive(False)


	def enable_custom_proxy(self, args):
		"""Disables the custom proxy related widgets
    
    Arguments:
    - `args`:
    """
		self._tbHttp.set_sensitive(True)
		self._tbHttps.set_sensitive(True)
		self._tbHttpPort.set_sensitive(True)
		self._tbHttpsPort.set_sensitive(True)


                

	def destroy_all(self,arg):
		"""Destroy everything
		"""
		gtk.main_quit()

		

class ExportGDocsWindow():
	"""Shows the export  Google Docs windows
	"""
	
	def __init__(self, gdam,confMan,filePath):
		"""
		
                Arguments:
                - `gdam`:GDocs.GDActionsManager
		- `confMan`:Configuration.ConfigurationManager
                """
		self._gdam = gdam
		self._confMan=confMan
		#set the file path properly
		self._filePath=filePath[7:]
		
		
		 
                if filePath=='':
			self.show_error_dlg('Save the file before uploading')
			sys.exit()

                #load and setup the GUI components

               
		filename = confMan.get_system_path()+"ExportGDocsWindow.glade"
		builder = gtk.Builder()
		builder.add_from_file(filename)
		builder.connect_signals(self)
		
		self._FolderTreeView=builder.get_object('FolderTreeView')
		self._mainWindow=builder.get_object('mainWindow')
		
		
		#self._FolderTreeView.
		self._tbUploadName=builder.get_object('uploadName')

                ##show the window before loading content
		#threading.Thread(gtk.main())
                

                #get the file name from the file path
		fName=filePath.split('.')[-2].split('/')[-1]+'.'+filePath.split('.')[-1]
		self._tbUploadName.set_text(fName)

		col_name=gtk.TreeViewColumn('')
		col_name.set_resizable(True)
		self._FolderTreeView.append_column(col_name)

		self._folderList=gtk.TreeStore( gobject.TYPE_STRING,gobject.TYPE_BOOLEAN,gobject.TYPE_PYOBJECT )
		#self._folderList=gtk.TreeStore( gobject.TYPE_BOOLEAN,gobject.TYPE_STRING,gobject.TYPE_PYOBJECT )
                renderer=gtk.CellRendererToggle()
		renderer.set_property('activatable', True)
		#renderer.set_property('width',20)
		renderer.connect( 'toggled', self.col1_toggled_cb, self._folderList )
		#renderer.set_sensitive(True)

                colFolder=gtk.TreeViewColumn('Folder Name',renderer)
		colFolder.add_attribute(renderer, "active", 1)
	
		colFolder.set_resizable(True)
		self._FolderTreeView.append_column(colFolder)

                #notifications
		notified=False
                if pynotify.init("Gnome Google Documents Manager"):
			n = pynotify.Notification.new("Gnome Google Documents Manager", "\n Your Google Documents folders list is being retrieved. Please wait.","dialog-information")
			n.set_timeout(5)
			n.show()
			notified=True
		
	

                self._FolderTreeView.set_model(self._folderList)

                self._mainWindow.get_root_window().set_cursor(Gdk.Cursor(Gdk.CursorType.WATCH))
		

                #add folder data
		fHierarchy=self._gdam.get_folder_hierarchy()
		
                parent=None
                for folder in fHierarchy:

                       
                        
			#array to store the items linearly
			folderList=[]
			#add the root folder
                        folderList.append([None,folder])

                        #set the parent to null
			parentNode=None
			#add it to the GUI list
			
			

			while len(folderList)>0:
				#get the next element in the folderList
				child=folderList.pop(0)
				#add the item to GUI
				parentNode=self._folderList.append(parentNode,(child[1].get_folder().title.text,None,child[1].get_folder()))
				#parentNode=self._folderList.append(parentNode,(child[1].get_folder(),None,child[1].get_folder().title.text))
				#iterate through its children and add them to folderList
				for entry in child[1].get_children():
					folderList.append([parentNode,entry])
					 
			
		
		

		#If a notification has been raised
		if notified:
			n.close()
                
		cell = gtk.CellRendererText()
		cell.set_property( 'editable', True )
		#cell.set_property('height',20)
		colFolder.pack_start(cell,False)
		colFolder.add_attribute(cell,"text",0)

		self._mainWindow.get_root_window().set_cursor(Gdk.Cursor(Gdk.CursorType.ARROW))
		
	def add_children_to_list(self, folder,parent):
		"""Adds a folder to the GUI ListStore
    
		Arguments:
		- `folder`: folder that should be added to the list
		- `parent`: gui parent of that folder
		"""
		#add each child to the tree
		for child in folder.get_children():
			parentNode=self._folderList.append(parent,(child.get_folder().title.text,None,child.get_folder()))
			#add the children of this folder
			#self.add_children_to_list(folder,parentNode)
                

	def upload(self,arg1):
		"""Upload a doc to Google docs upon GUI call
		"""

                #Set the curosr to busy
		self._mainWindow.get_root_window().set_cursor(Gdk.Cursor(Gdk.CursorType.WATCH))
		print 'ssss'
		folders=self.get_selected_folders()

                

                #upload to the first selected folder
		doc=self._gdam.upload_new_doc(self._filePath,None,self._tbUploadName.get_text())

                #copy to the other resources
		for folder in folders:
			self._gdam.copy_resource_to_collection(folder,doc)
		
		self._mainWindow.get_root_window().set_cursor(Gdk.Cursor(Gdk.CursorType.ARROW))
                
	def col1_toggled_cb( self, cell, path, model ):
		"""
		Sets the toggled state on the toggle button to true or false.
		"""
		

		model[path][1] = not model[path][1]
		

		return

        def _add_children(self, iter,results):
		"""Adds the children of the iterator entry 
		
		Arguments:
		- `iter`: an iterator
		-`results`: an array to store the results
		"""

               
		

                #check whether this entry is selected
		if self._folderList[iter][1]:
			results.append(self._folderList[iter][2])
			
				
		#if this entry has children
		if self._folderList.iter_has_child(iter):
			self._add_children(self._folderList.iter_children(iter),results)
		
		
	
	def get_selected_folders(self):
		"""Returns the selected folders as a list
		"""
		#to store the selected items
		selected=[]
		
		
                rootIter=self._folderList.get_iter_first()
		#	path=self._folderList.get_path(iter)


                
                while rootIter!=None:
			#if the entry has been selected
			if  self._folderList[rootIter][1]:
				selected.append(self._folderList[rootIter][2])
				

			#check for selected children
			if self._folderList.iter_has_child(rootIter):
				
				self._add_children(self._folderList.iter_children(rootIter),selected)
                                
			#select the next entry
			rootIter=self._folderList.iter_next(rootIter)	

               
			

                
		return selected

	def destroy_all(self,arg):
		"""Destroy everything
		"""
		gtk.main_quit()

	def show_error_dlg(self, error_string):
		"""This Function is used to show an error dialog when
		an error occurs.
		error_string - The error string that will be displayed
		on the dialog.
		"""
		error_dlg = gtk.MessageDialog(type=gtk.MessageType.ERROR
					      , message_format=error_string
					      , buttons=gtk.ButtonsType.OK)
		error_dlg.run()
		error_dlg.destroy()

		
class ImportGDocsWindow():
	"""Shows the import Google Docs windows
	"""
	
	def __init__(self, gdam,confMan):
		"""
		
                Arguments:
                - `gdam`:GDocs.GDActionsManager
		- `confMan`:Configuration.ConfigurationManager
                """
		self._gdam = gdam

                #load and setup the GUI components

                #TODO: Create a good way to get the file locations.From the
		#ConfigurationManager may be?
		filename = confMan.get_system_path()+"ImportGDocsWindow.glade"
		builder = gtk.Builder()
		builder.add_from_file(filename)
		builder.connect_signals(self)

                #get widgets from the glade file
		self._DocTreeView=builder.get_object('DocTreeView')
		self._entry_fileSaveLocation=builder.get_object('fileSaveLocation')
		self._mainWindow=builder.get_object('mainWindow')
		self._cbListDocs=builder.get_object('cbListDocs')
		self._cbListSpreadsheets=builder.get_object('cbListSpreadsheets')
		self._cbListPresentations=builder.get_object('cbListPresentations')

                #set window size
		self._mainWindow.set_default_size(100,100)
                
		col_type=gtk.TreeViewColumn('Type')
		col_type.set_resizable(True)
		self._DocTreeView.append_column(col_type)

                col_name=gtk.TreeViewColumn('Name',gtk.CellRendererText(),text=1)
		col_name.set_resizable(True)
		self._DocTreeView.append_column(col_name)

                col_folders=gtk.TreeViewColumn('In Folders',gtk.CellRendererText(),text=2)
		col_folders.set_resizable(True)
		self._DocTreeView.append_column(col_folders)

                #The last str is to store the resource_id
                self._docList=gtk.ListStore(str,str,str,gobject.TYPE_PYOBJECT)
		self._DocTreeView.set_model(self._docList)

                #notifications
		notified=False
                if pynotify.init("Gnome Google Documents Manager"):
			n = pynotify.Notification.new("Gnome Google Documents Manager", "\n Your Google Documents list is being downloaded. Please wait.","dialog-information")
			#n.set_timeout()
			n.show()
			notified=True
		

		self._mainWindow.get_root_window().set_cursor(Gdk.Cursor(Gdk.CursorType.WATCH))
                        
		for doc in self._gdam.get_all_documents().entry:

                        #list only if the doc is a document/spreadsheet/presentation

                        if doc.GetResourceType() in ['document','spreadsheet','presentation']:
				
				data= self._gdam.get_doc_data(doc)
			
				#Get collection info
				collectionList=None
				for entry in doc.InCollections():
					for title in entry.GetAttributes(tag='title'):
						if not collectionList:
							collectionList=''
							collectionList+=title.value+','
							
							
				if collectionList:
				#remove the last comma
					collectionList=collectionList[0:len(collectionList)-1]

				collectionList=str(collectionList)
			
				self._docList.append([data[0],data[1],collectionList,doc])
				#print doc.resource_id
				#TODO: There's a more elegant way to do this
				#http://faq.pygtk.org/index.py?req=show&file=faq13.015.htp
			
			

				#itr=DocList.append([1,'2','3'])
				#DocList.insert_after(itr,[2,"2",'2'])
				#DocList.append(["1","2","3","R_ID"])

				#If a notification has been raised
		if notified:
			n.close()
		
                cell = gtk.CellRendererText()
		col_type.pack_start(cell,False)
		col_type.add_attribute(cell,"text",0)

                self._but_save=builder.get_object('but_save')
		#self._but_save.set_visible(False)



                #select the default entry in the list
		self._DocTreeView.get_selection().select_path(0)
		

                self._mainWindow.get_root_window().set_cursor(Gdk.Cursor(Gdk.CursorType.ARROW))
                
	def destroy_all(self,arg):
		"""Destroy everything
		"""
		gtk.main_quit()

	

	def on_set_save_location(self,arg1,arg2,arg3):
		"""
		"""
		

		

                

                
		dialog_buttons = (gtk.STOCK_CANCEL
					, gtk.ResponseType.CANCEL
					, gtk.STOCK_SAVE
					, gtk.ResponseType.OK)
		file_dialog = gtk.FileChooserDialog(title="Select Save Location"
				, action=gtk.FileChooserAction.SAVE
				, buttons=dialog_buttons)

                # filter = gtk.FileFilter()
		# filter.set_name("*.odt")
		# filter.add_pattern("*.odt")
		# file_dialog.add_filter(filter)

                # filter = gtk.FileFilter()
		# filter.set_name("*.doc")
		# filter.add_pattern("*.doc")
		# file_dialog.add_filter(filter)

		##set the default name
		treeModel=self._DocTreeView.get_selection().get_selected_rows()[0]
		path=self._DocTreeView.get_selection().get_selected_rows()[1]
		
		iter=treeModel.get_iter(path[0])
		resource= treeModel.get_value(iter,3)

                #if this is a doc
		if resource.GetResourceType()=='document':
			file_dialog.set_current_name(resource.title.text+'.odt')
		#if this is a spreadsheet
		elif resource.GetResourceType()=='spreadsheet':
			file_dialog.set_current_name(resource.title.text+'.ods')
		#if this is a presentation
		elif resource.GetResourceType()=='presentation':
			file_dialog.set_current_name(resource.title.text+'.ppt')
		

                

                result = ""
		if file_dialog.run() == gtk.ResponseType.OK:
			result = file_dialog.get_filename()
			
		file_dialog.destroy()
	
		self._entry_fileSaveLocation.set_text(result)

	def on_save_button(self,arg1 ):
		"""Saves the given Doc
		"""

		#Set the curosr to busy
		#time.sleep(10)
		#print 'Hi'
		#self._mainWindow.get_root_window().set_cursor(Gdk.Cursor(Gdk.CursorType.WATCH))
		#self._mainWindow.set_cursor(Gdk.Cursor(Gdk.CursorType.WATCH))
		#print 'Chathu'
                
		filePath=self._entry_fileSaveLocation.get_text()
		#file extension
		ext=filePath.split('.')[-1]
		
		
                #if the extension is not set
		if not ext:
			self.show_error_dlg("File extension is not set")
			return

                #if file path is not set
		if len(filePath)==0:
			self.show_error_dlg("File path is empty")
			return

		#get the selected resource
                treeModel=self._DocTreeView.get_selection().get_selected_rows()[0]
		path=self._DocTreeView.get_selection().get_selected_rows()[1]
		#print path[0]
		iter=treeModel.get_iter(path[0])
		resource= treeModel.get_value(iter,3)

                #if this is a doc
		if resource.GetResourceType()=='document':
			#if the extension matches
			if ext in ['doc','odt','rtf']:
				self._gdam.download_doc(resource,filePath,ext)
			else:
				self.show_error_dlg("Wrong file type. Supported file types are doc,odt,rtf")
		#if this is a spreadsheet
		elif resource.GetResourceType()=='spreadsheet':
			#if the extension matches
			if ext in ['xls','ods']:
				#TODO:deprecated method. replace with download_doc
				self._gdam.download_doc(resource,filePath,ext)
			else:
				self.show_error_dlg('Wrong file type.Supported file types are xls,doc')
		#if this is a presentation
		elif resource.GetResourceType()=='presentation':

                        #if the extension matches
			if ext in ['ppt','pptx']:
				#TODO:deprecated method. replace with download_doc
				self._gdam.download_doc(resource,filePath,ext)
			else:
				self.show_error_dlg('Wrong file type. Supported file types include pptx')
		
		#self._mainWindow.get_root_window().set_cursor(Gdk.Cursor(Gdk.CursorType.ARROW))

	def on_save_n_open_button(self, arg1):
		"""Saves the given doc and opens it in Libre office
    
		Arguments:
		- `arg1`:
		"""
		filePath=self._entry_fileSaveLocation.get_text()
		if len(filePath)==0:
			self.show_error_dlg("File path is empty")
			return
		self.on_save_button(arg1)

		subprocess.Popen(['soffice', self._entry_fileSaveLocation.get_text()])
		#os.system("soffice "+self._entry_fileSaveLocation.get_text())
		self.destroy_all(None)

	def show_error_dlg(self, error_string):
		"""This Function is used to show an error dialog when
		an error occurs.
		error_string - The error string that will be displayed
		on the dialog.
		"""
		error_dlg = gtk.MessageDialog(type=gtk.MessageType.ERROR
					      , message_format=error_string
					      , buttons=gtk.ButtonsType.OK)
		error_dlg.run()
		error_dlg.destroy()


	def list_docs_cb_toggled(self, args):
		""" Gets called when listing option check box is toggle
    
		Arguments:
		- `args`:
		"""
		#the new model to store the tree data
		newModel=gtk.ListStore(str,str,str,gobject.TYPE_PYOBJECT)

		#iterate through the default model
		iter=self._docList.get_iter_first()

                while iter:

                        #if this entry is a document
			if self._docList.get_value(iter,0)=='document':
				#if documents should be added to the list
				if self._cbListDocs.get_active():
					newModel.append([self._docList.get_value(iter,0),self._docList.get_value(iter,1),self._docList.get_value(iter,2),self._docList.get_value(iter,3)])

			#if this entry is a spreadsheet
			if self._docList.get_value(iter,0)=='spreadsheet':
				#if documents should be added to the list
				if self._cbListSpreadsheets.get_active():
					newModel.append([self._docList.get_value(iter,0),self._docList.get_value(iter,1),self._docList.get_value(iter,2),self._docList.get_value(iter,3)])

			#if this entry is a presentation
			if self._docList.get_value(iter,0)=='presentation':
				#if documents should be added to the list
				if self._cbListPresentations.get_active():
					newModel.append([self._docList.get_value(iter,0),self._docList.get_value(iter,1),self._docList.get_value(iter,2),self._docList.get_value(iter,3)])
			
			iter=self._docList.iter_next(iter)

		self._DocTreeView.set_model(newModel)


if __name__ == "__main__":

        guiM=GUIManager()
	
	if (len(sys.argv) > 1):
		if( sys.argv[1] == 'import' ):
		
	        	guiM.show_import_window()
		
		elif( sys.argv[1] == 'export' ):

		        filePath=sys.argv[2]
			
	        	guiM.show_export_window(filePath)

		elif( sys.argv[1] == 'settings' ):

		        
	        	guiM.show_settings_window()
	
	#
	#t=Test()
	gtk.main()
