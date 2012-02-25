#!/usr/bin/env python

import gtk

class TreeViewListStore:
    def __init__(self):
        window = gtk.Window()
        window.set_default_size(200, 200)
        
        liststore = gtk.ListStore(str)
        treeview = gtk.TreeView(liststore)
        
        liststore.append(["Ubuntu"])
        liststore.append(["Fedora"])
        liststore.append(["Sabayon"])
        liststore.append(["Arch"])
        liststore.append(["Debian"])
        
        column = gtk.TreeViewColumn("Distributions")
        treeview.append_column(column)
        
        cell = gtk.CellRendererText()
        column.pack_start(cell, False)
        column.add_attribute(cell, "text", 0)
        
        window.connect("destroy", lambda w: gtk.main_quit())
        
        window.add(treeview)
        window.show_all()
        
TreeViewListStore()
gtk.main()

