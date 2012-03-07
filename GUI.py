import sys
import GDocs
import Configuration
import os
import gobject
try:
 	import pygtk
  	pygtk.require("2.0")
except:
  	pass
try:
	import gtk
  	import gtk.glade
except:
	sys.exit(1)


class GUIManager():
	"""Provides an interface to access the GUI functionality
	"""
	
	def __init__(self):
		"""
		"""
		#TODO: Find an elegant way to do this.
		self._confMan=Configuration.ConfigurationManager()
		account=self._confMan.get_account()
		self._gdcm=GDocs.GDClientManager()
		self._gdam=GDocs.GDActionsManager(self._gdcm)
		self._gdcm.authenticate_client(account)


	def show_import_window(self):
		"""Shows the import Google Documents window"""

                window=ImportGDocsWindow(self._gdam,self._confMan)
		#window=MainWindow()

	def show_export_window(self):
		"""Shows the export Documents window
		"""
		window=ExportGDocsWindow(self._gdam,self._confMan)
		

class ExportGDocsWindow():
	"""Shows the export  Google Docs windows
	"""
	
	def __init__(self, gdam,confMan):
		"""
		
                Arguments:
                - `gdam`:GDocs.GDActionsManager
		- `confMan`:Configuration.ConfigurationManager
                """
		self._gdam = gdam
		self._confMan=confMan

                #load and setup the GUI components

               
		filename = confMan.get_system_path()+"ExportGDocsWindow.glade"
		builder = gtk.Builder()
		builder.add_from_file(filename)
		builder.connect_signals(self)
		
		self._FolderTreeView=builder.get_object('FolderTreeView')

		col_name=gtk.TreeViewColumn('')
		col_name.set_resizable(True)
		self._FolderTreeView.append_column(col_name)

                self._folderList=gtk.TreeStore( gobject.TYPE_STRING,
                                         gobject.TYPE_BOOLEAN,gobject.TYPE_PYOBJECT )

                renderer=gtk.CellRendererToggle()
		renderer.set_property('activatable', True)
		renderer.connect( 'toggled', self.col1_toggled_cb, self._folderList )
		#renderer.set_sensitive(True)

                col_select=gtk.TreeViewColumn('Folder Name',renderer)
		col_select.add_attribute(renderer, "active", 1)
	
		col_select.set_resizable(True)
		self._FolderTreeView.append_column(col_select)

		
	
		self._FolderTreeView.set_model(self._folderList)

                #add folder data
		folders=self._gdam.get_folder_hierarchy()

                for folder in folders:
			print folder.title.text
			self._folderList.append(None,(folder.title.text,None,folder))
			
			#p= FolderList.append(None, ('1',None))
			#	FolderList.append(p, ('2',None))

                cell = gtk.CellRendererText()
		cell.set_property( 'editable', True )
		col_select.pack_start(cell,False)
		col_select.add_attribute(cell,"text",0)

	def upload(self):
		"""Upload a doc to Google docs upon GUI call
		"""
		#TODO: Add multi folder support
		folders=self.get_selected_folders()
		
		
                
	def col1_toggled_cb( self, cell, path, model ):
		"""
		Sets the toggled state on the toggle button to true or false.
		"""
		

		model[path][1] = not model[path][1]

		return
	
	def get_selected_folders(self):
		"""Returns the selected folders as a list
		"""
		selected=[]

                for folder in self._folderList:
		
			if  folder[1]:
				selected.append(folder[2])
			

		return selected

	def destroy_all(self,arg):
		"""Destroy everything
		"""
		gtk.main_quit()

		
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
		
		self._DocTreeView=builder.get_object('DocTreeView')
		self._entry_fileSaveLocation=builder.get_object('fileSaveLocation')
		

                
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
                DocList=gtk.ListStore(str,str,str,str)
		self._DocTreeView.set_model(DocList)

                ##stores the dictionary of Gdocs sentries
		self._entryList={}
		
		for doc in self._gdam.get_all_documents().entry:
			data= self._gdam.get_doc_data(doc)
			#print dir(data)
			
			DocList.append([data[0],data[1],"Folder",data[2]])
			#print doc.resource_id
			#TODO: There's a more elegant way to do this
			#http://faq.pygtk.org/index.py?req=show&file=faq13.015.htp
			self._entryList[doc.resource_id.text]=doc
			

			#itr=DocList.append([1,'2','3'])
		#DocList.insert_after(itr,[2,"2",'2'])
		#DocList.append(["1","2","3","R_ID"])
		

                cell = gtk.CellRendererText()
		col_type.pack_start(cell,False)
		col_type.add_attribute(cell,"text",0)

                self._but_save=builder.get_object('but_save')
		#self._but_save.set_visible(False)

	def destroy_all(self,arg):
		"""Destroy everything
		"""
		gtk.main_quit()

	

	def on_set_save_location(self,arg1,arg2,arg3):
		"""
		"""
		# print type(arg1)
		# print type(arg2)
		# print type(arg3)
		# print (DocumentsSaveAsWindow())
		dialog_buttons = (gtk.STOCK_CANCEL
					, gtk.RESPONSE_CANCEL
					, gtk.STOCK_SAVE
					, gtk.RESPONSE_OK)
		file_dialog = gtk.FileChooserDialog(title="Select Save Location"
				, action=gtk.FILE_CHOOSER_ACTION_SAVE
				, buttons=dialog_buttons)
		filter = gtk.FileFilter()
		filter.set_name("*.odt")
		filter.add_pattern("*.odt")
		file_dialog.add_filter(filter)

                result = ""
		if file_dialog.run() == gtk.RESPONSE_OK:
			result = file_dialog.get_filename()
			
		file_dialog.destroy()
	
		self._entry_fileSaveLocation.set_text(result)

	def on_save_button(self,arg1 ):
		"""Saves the given Doc
		"""
		filePath=self._entry_fileSaveLocation.get_text()
		if len(filePath)==0:
			self.show_error_dlg("File path is empty")
			return
		treeModel=self._DocTreeView.get_selection().get_selected_rows()[0]
		path=self._DocTreeView.get_selection().get_selected_rows()[1]
		#print path[0]
		iter=treeModel.get_iter(path[0])
		resourceID= treeModel.get_value(iter,3)

                
		
		self._gdam.download_doc(self._entryList[resourceID],filePath)

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
		os.system("soffice "+self._entry_fileSaveLocation.get_text())
		self.destroy_all(None)

	def show_error_dlg(self, error_string):
		"""This Function is used to show an error dialog when
		an error occurs.
		error_string - The error string that will be displayed
		on the dialog.
		"""
		error_dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR
					      , message_format=error_string
					      , buttons=gtk.BUTTONS_OK)
		error_dlg.run()
		error_dlg.destroy()


class Test(object):
	"""
    """
	
	def __init__(self):
		"""
        """
	
		filename = "/home/ishan/4sep/Test.glade"
		builder = gtk.Builder()
		builder.add_from_file(filename)
		builder.connect_signals(self)
		#builder.get_object('window1').hide()


	
	def destroy_all(self,arg):
		"""Destroy everything
		"""
		gtk.main_quit()
	




if __name__ == "__main__":

        guiM=GUIManager()
	
	if (len(sys.argv) > 1):
		if( sys.argv[1] == 'import' ):
		
	        	guiM.show_import_window()
		
		elif( sys.argv[1] == 'export' ):

		        print 'save'
	        	guiM.show_export_window()
	
	#
	#t=Test()
	gtk.main()
