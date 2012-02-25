#!/usr/bin/env python

import gtk

class TreeViewTreeStore:
    def __init__(self):
        window = gtk.Window()
        window.set_default_size(200, 200)
        
        treestore = gtk.TreeStore(str)
        treeview = gtk.TreeView(treestore)
        
        ubuntu = treestore.append(None, ["Ubuntu"])
        treestore.append(ubuntu, ["http://www.ubuntu.com/"])
        fedora = treestore.append(None, ["Fedora"])
        treestore.append(fedora, ["http://fedoraproject.org/"])
        treestore.append(None, ["Sabayon"])
        treestore.append(None, ["Arch"])
        debian = treestore.append(None, ["Debian"])
        treestore.append(debian, ["http://www.debian.org/"])
        
        column = gtk.TreeViewColumn("Distributions")
        treeview.append_column(column)
        
        cell = gtk.CellRendererText()
        column.pack_start(cell, False)
        column.add_attribute(cell, "text", 0)
        
        window.connect("destroy", lambda w: gtk.main_quit())
        
        window.add(treeview)
        window.show_all()
        
TreeViewTreeStore()
gtk.main()

