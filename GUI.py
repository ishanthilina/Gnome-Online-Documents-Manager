import sys
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


class MainWindow:
        """This is an Hello World GTK application"""

        def __init__(self):
		
                # #Set the Glade file
                # self.gladefile = "hello.glade"  
	        # self.wTree = gtk.glade.XML("1.glade") 
		
		# #Get the Main Window, and connect the "destroy" event
		# self.window = self.wTree.get_widget("MainWindow")
		# if (self.window):
		# 	self.window.connect("destroy", gtk.main_quit)
                #text.insertString( cursor, "in class\n", 0 )
                #load the 1.glade
                filename = "/home/ishan/4sep/1.ui"
		builder = gtk.Builder()
		builder.add_from_file(filename)
		builder.connect_signals(self)
		#comment the following lines
		window=builder.get_object('window')
		window.show_all()

	def on_buttonGenerate_clicked(self, widget):
		print "You clicked the button"

if __name__ == "__main__":
	hwg = MainWindow()
	gtk.main()
