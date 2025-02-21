#       info_tree.py
#
#       Copyright 2011 Hugo Teso <hugo.teso@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import gtk

class InfoWindow(gtk.ScrolledWindow):

    def __init__(self, uicore):
        super(InfoWindow,self).__init__()

        self.uicore = uicore

        self.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.info_tree = InfoTree(self.uicore)

        # Add Textview to Scrolled Window
        self.add(self.info_tree)
        self.show_all()

class InfoTree(gtk.TreeView):
    '''HTML elements TreeView'''

    def __init__(self, core):
        self.store = gtk.ListStore(str, str, str, str, str, str, str, str)
        super(InfoTree,self).__init__(self.store)

        self.uicore = core

        self.set_rules_hint(True)
        self.show_all()

    def create_info_tree(self):

        full_info = self.uicore.full_fileinfo

        # Create the column
        infos = gtk.TreeViewColumn()
        infos.set_title("Extended file information")

        cell = gtk.CellRendererText()
        infos.pack_start(cell, True)
        infos.add_attribute(cell, "text", 0)

        cell = gtk.CellRendererText()
        infos.pack_start(cell, True)
        infos.add_attribute(cell, "text", 1)

        cell = gtk.CellRendererText()
        infos.pack_start(cell, True)
        infos.add_attribute(cell, "text", 2)

        cell = gtk.CellRendererText()
        infos.pack_start(cell, True)
        infos.add_attribute(cell, "text", 3)

        cell = gtk.CellRendererText()
        infos.pack_start(cell, True)
        infos.add_attribute(cell, "text", 4)

        cell = gtk.CellRendererText()
        infos.pack_start(cell, True)
        infos.add_attribute(cell, "text", 5)

        cell = gtk.CellRendererText()
        infos.pack_start(cell, True)
        infos.add_attribute(cell, "text", 6)

        cell = gtk.CellRendererText()
        infos.pack_start(cell, True)
        infos.add_attribute(cell, "text", 7)

        self.treestore = gtk.TreeStore(str, str, str, str, str, str, str, str)

        file_it = self.treestore.append(None, ['File info', '', '', '', '', '', '', ''])
        entry_it = self.treestore.append(None, ['Entry points', '', '', '', '', '', '', ''])

        if full_info.has_key('bin'):
            for info in full_info['bin']:
                if len(info) >= 2:
                    self.treestore.append(file_it, [info[0], info[-1], '', '', '', '', '', ''])

        if full_info.has_key('eps'):
            for ep in full_info['eps']:
                if len(ep) == 2:
                    self.treestore.append(entry_it, [ep[0], ep[1], '', '', '', '', '', ''])

        # Add column to tree
        self.append_column(infos)
        self.set_model(self.treestore)
        self.expand_all()
        #self.collapse_all()

        self.show_all()
