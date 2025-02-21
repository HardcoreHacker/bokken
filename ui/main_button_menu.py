#       main_button_menu.py
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
import webbrowser
import lib.bokken_globals as glob

# We need it for the "New" button
import ui.file_dialog as file_dialog

class MenuBar(gtk.Menu):
    '''Main TextView elements'''

    def __init__(self, main):
        super(MenuBar,self).__init__()
        self.main = main
        self.uicore = self.main.uicore

        agr = gtk.AccelGroup()
        self.main.window.add_accel_group(agr)

        actiongroup = gtk.ActionGroup('MainButton')

        # File menu items
        newmenu = gtk.Action('New', None, None, gtk.STOCK_NEW)
        newmenu.connect("activate", self.new_file)

        actiongroup.add_action_with_accel(newmenu, '<Control>N')
        newmenu.set_accel_group(agr)
        newmenu.connect_accelerator()
        newmenuitem = newmenu.create_menu_item()
        self.append(newmenuitem)

        self.manager = gtk.recent_manager_get_default()

        self.recent_menu = gtk.RecentChooserMenu(self.manager)

        self.recentm = gtk.MenuItem('Recent targets')
        self.recentm.set_submenu(self.recent_menu)
        self.recent_menu.connect('item-activated', self.recent_kb)

        self.append(self.recentm)

        smenu = gtk.Menu()

        savem = gtk.ImageMenuItem(gtk.STOCK_SAVE)
        savem.get_children()[0].set_label('Save')
        savem.set_submenu(smenu)

        saves = [
                    ['All', gtk.STOCK_SAVE_AS, 'all'],
                    ['Disassembly', gtk.STOCK_SORT_DESCENDING, 'asm'],
                    ['Hexdump', gtk.STOCK_INDEX, 'hex'],
                    ['Strings', gtk.STOCK_JUSTIFY_CENTER, 'str'],
                ]
        for save in saves:
            savei = gtk.ImageMenuItem(save[1])
            savei.get_children()[0].set_label(save[0])
            savei.connect("activate", self._save, save[2])
            smenu.append(savei)

        self.append(savem)

        sep = gtk.SeparatorMenuItem()
        self.append(sep)

        tmenu = gtk.Menu()

        themem = gtk.ImageMenuItem(gtk.STOCK_SELECT_COLOR)
        themem.get_children()[0].set_label('Themes')
        themem.set_submenu(tmenu)

        themes = ['Classic', 'Cobalt', 'kate', 'Oblivion', 'Tango']
        for theme in themes:
            themei = gtk.MenuItem(theme)
            themei.connect("activate", self._on_theme_change)
            tmenu.append(themei)

        self.append(themem)

        # View Menu
        self.vmenu = gtk.Menu()

        tabsm = gtk.ImageMenuItem(gtk.STOCK_PREFERENCES)
        tabsm.get_children()[0].set_label('Show tabs')
        tabsm.set_submenu(self.vmenu)

        self.append(tabsm)

        sep = gtk.SeparatorMenuItem()
        self.append(sep)

        # Cheatsheet.
        cheat = gtk.Action('Cheat sheet', 'Cheat sheet', None, gtk.STOCK_JUSTIFY_FILL)
        cheat.connect("activate", self.create_cheatsheet_dialog)

        actiongroup.add_action_with_accel(cheat, 'F1')
        cheat.set_accel_group(agr)
        cheat.connect_accelerator()
        cheatitem = cheat.create_menu_item()
        self.append(cheatitem)

        # Help menu.
        helpmenu = gtk.Action('Help', None, None, gtk.STOCK_HELP)
        helpmenu.connect("activate", self.show_wiki)

        actiongroup.add_action_with_accel(helpmenu, '<Control>H')
        helpmenu.set_accel_group(agr)
        helpmenu.connect_accelerator()
        helpmenuitem = helpmenu.create_menu_item()
        self.append(helpmenuitem)

        # About.
        about = gtk.Action('About', None, None, gtk.STOCK_ABOUT)
        about.connect("activate", self.create_about_dialog)

        actiongroup.add_action_with_accel(about, '<Control>A')
        about.set_accel_group(agr)
        about.connect_accelerator()
        aboutitem = about.create_menu_item()
        self.append(aboutitem)

        sep = gtk.SeparatorMenuItem()
        self.append(sep)

        # Quit.
        exit = gtk.Action('Quit', None, None, gtk.STOCK_QUIT)
        exit.connect('activate', self.main.quit)

        actiongroup.add_action_with_accel(exit, '<Control>Q')
        exit.set_accel_group(agr)
        exit.connect_accelerator()
        exititem = exit.create_menu_item()

        self.append(exititem)

    #
    # Functions
    #

    # Private methods
    #

    def delete_view_menu(self):
        for x in self.vmenu.get_children():
            self.vmenu.remove(x)
        self.vmenu.show_all()

    def create_view_menu(self):
        self.nb = self.main.tviews.right_notebook
        for x in self.nb.get_children():
            box = self.nb.get_tab_label(x)
            element = box.get_children()[1].get_text().lower()
            item = gtk.CheckMenuItem("Show " + element)
            if element != 'full info':
                item.set_active(True)
            item.connect("activate", self._on_status_view)
            self.vmenu.append(item)
        self.vmenu.show_all()

    def _on_status_view(self, widget):
        target = widget.get_label().split(' ')[1]
        for x in self.nb.get_children():
            y = self.nb.get_tab_label(x)
            if target in y.get_children()[1].get_text().lower():
                target = x
                break
        if widget.active:
            x.show()
        else:
            x.hide()

    def _on_theme_change(self, widget):
        theme = widget.get_label()
        self.main.tviews.update_theme(theme)

    def show_wiki(self, widget):
        webbrowser.open_new_tab('http://inguma.eu/projects/bokken/wiki')

    def _finish_dasm(self):
        # Used to update tab names after dasm analysis finishes
        self.delete_view_menu()
        self.create_view_menu()

    # New File related methods
    #
    def new_file(self, widget, file=''):
        dialog = file_dialog.FileDialog(file, False)
        resp = dialog.run()
        if resp == gtk.RESPONSE_DELETE_EVENT or resp == gtk.RESPONSE_REJECT:
            dialog.destroy()
        else:
            self.file = dialog.file

            self.main.load_new_file(dialog, self.file)
            dialog.destroy()

    def recent_kb(self, widget):
        """Activated when an item from the recent projects menu is clicked"""

        uri = widget.get_current_item().get_uri()
        # Strip 'file://' from the beginning of the uri
        file_to_open = uri[7:]
        self.new_file(None, file_to_open)

    def create_cheatsheet_dialog(self, widget):

        import cheatsheet_dialog
        self.cheatsheet_dialog = cheatsheet_dialog.CheatsheetDialog()

        return False

    def create_about_dialog(self, widget):
        import ui.about as about

        about_dlg = about.AboutDialog()
        dialog = about_dlg.create_dialog()

        dialog.run()
        dialog.destroy()

    def _get_content(self, type):
        types = {'asm':self.uicore.text_dasm, 'hex':self.uicore.fullhex, 'str':self.uicore.allstrings}
        return types[type]

    def _save(self, widget, data):
        chooser = gtk.FileChooserDialog(title=None,action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        response = chooser.run()

        if response == gtk.RESPONSE_OK:
            all = ['asm', 'hex', 'str']
            filename = chooser.get_filename()
            if data != 'all':
                output = open(filename + '.' + data, 'wb')
                content = self._get_content(data)
                output.write(content)
                output.close()
            else:
                for fmt in all:
                    output = open(filename + '.' + fmt, 'wb')
                    content = self._get_content(fmt)
                    output.write(content)
                    output.close()
        chooser.destroy()
