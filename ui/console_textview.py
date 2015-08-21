#       console_textview.py
#       
#       Copyright 2015 Hugo Teso <hugo.teso@gmail.com>
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

import os

import gtk
import pango
import gtksourceview2

class ConsoleTextView(gtk.VBox):
    '''Console TextView elements'''

    def __init__(self, uicore):
        super(ConsoleTextView,self).__init__(False, 1)

        self.uicore = uicore

        #################################################################
        # Interactive Right Textview
        #################################################################

        # Use GtkSourceView to add eye candy :P
        # create buffer
        lm = gtksourceview2.LanguageManager()
        # Add ui dir to language paths
        paths = lm.get_search_path()
        paths.append(os.path.dirname(__file__) + os.sep + 'data' + os.sep)
        lm.set_search_path(paths)
        self.buffer = gtksourceview2.Buffer()
        self.buffer.create_tag("green-background", background="green", foreground="black")
        self.buffer.set_data('languages-manager', lm)
        self.view = gtksourceview2.View(self.buffer)

        # FIXME options must be user selectable (statusbar)
        self.view.set_editable(False)
        #self.view.set_highlight_current_line(True)
        # posible values: gtk.WRAP_NONE, gtk.WRAP_CHAR, gtk.WRAP_WORD...
        self.view.set_wrap_mode(gtk.WRAP_NONE)
        self.view.connect("populate-popup", self._populate_menu)
        
        # setup view
        font_desc = pango.FontDescription('monospace 9')
        if font_desc:
            self.view.modify_font(font_desc)

        self.buffer.set_highlight_syntax(False)
        manager = self.buffer.get_data('languages-manager')
        language = manager.get_language('asm')
        self.buffer.set_language(language)

        self.mgr = gtksourceview2.style_scheme_manager_get_default()

        # Scrolled Window
        self.console_scrolled_window = gtk.ScrolledWindow()
        self.console_scrolled_window.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        self.console_scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.console_scrolled_window.show()
        # Add Textview to Scrolled Window
        self.console_scrolled_window.add(self.view)
        self.pack_start(self.console_scrolled_window, True, True, 0)

        #Always on bottom on change
        self.vajd = self.console_scrolled_window.get_vadjustment()
        self.vajd.connect('changed', lambda a, s=self.console_scrolled_window: self.rescroll(a,s))

        # Comand line entry
        self.exec_entry = gtk.Entry(100)
        self.exec_entry.set_icon_from_stock(1, gtk.STOCK_EXECUTE)
        self.exec_entry.set_icon_tooltip_text(1, 'Execute')
        self.exec_entry.set_text('Radare console: type ? for help')
        self.exec_entry.connect("activate", self.r2_exec)
        self.exec_entry.connect("icon-press", self.r2_exec)
        self.exec_entry.connect('focus-in-event', self._clean, 'in')
        self.exec_entry.connect('focus-out-event', self._clean, 'out')
        self.pack_end(self.exec_entry, False, True, 0)

    def rescroll(self, adj, scroll):
        adj.set_value(adj.upper-adj.page_size)
        scroll.set_vadjustment(adj)

    def r2_exec(self, widget, icon_pos=None, event=None):
        command = self.exec_entry.get_text()
        res = self.uicore.execute_command(command)
        if res and res != '':
            end_iter = self.buffer.get_end_iter()
            self.buffer.insert(end_iter, res + '\n')
        self.exec_entry.set_text('')
        self.exec_entry.grab_focus()

    def add_message(self, msg):
        end_iter = self.buffer.get_end_iter()
        self.buffer.insert(end_iter, ' > ' + msg + '\n')

    def _populate_menu(self, textview, menu):
        opc = gtk.ImageMenuItem((gtk.STOCK_CLEAR))
        opc.get_children()[0].set_label('Clear text')
        menu.prepend(gtk.SeparatorMenuItem())
        menu.prepend(opc)
        opc.connect("activate", self._clear, iter)
        menu.show_all()

    def _clear(self, widget, event):
        self.buffer.set_text('')

    def _clean(self, widget, event, data):
        if data == 'in':
            if widget.get_text() == 'Radare console: type ? for help':
                widget.set_text('')
        elif data == 'out':
            if widget.get_text() == '':
                widget.set_text('Radare console: type ? for help')
