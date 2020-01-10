# -*- coding: utf-8 -*-
# substui.py
# Copyright (C) 2012-2013 Red Hat, Inc.
#
# Authors:
#   Akira TAGOH  <tagoh@redhat.com>
#
# This library is free software: you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gettext
import gi
import re
import sys
from distutils.version import LooseVersion
try:
    from chooserui import FontsTweakChooserUI
except ImportError:
    from fontstweak.chooserui import FontsTweakChooserUI
try:
    from util import FontsTweakUtil
except ImportError:
    from fontstweak.util import FontsTweakUtil
from gi.repository import Easyfc
from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gtk

_ = gettext.gettext

class FontsTweakSubstUI:

    def __init__(self, config, builder, parent):
        self.__initialized = False

        self.config = config
        self.parent_window = parent
        self.remove_subst_button = builder.get_object('remove-subst')
        self.remove_font_button = builder.get_object('remove-font-assigned')
        self.move_up_button = builder.get_object('move-up-subst')
        self.move_down_button = builder.get_object('move-down-subst')
        self.pages = builder.get_object('notebook-subst-pages')
        self.subst_selector = builder.get_object('treeview-selection-subst')
        self.assigned_selector = builder.get_object('treeview-selection-assigned')
        self.subst_view = builder.get_object('treeview-subst-fonts-list')
        self.assigned_view = builder.get_object('treeview-assigned-fonts-list')
        self.subst_view.append_column(Gtk.TreeViewColumn(None, Gtk.CellRendererText(), text=0))
        self.assigned_view.append_column(Gtk.TreeViewColumn(None, Gtk.CellRendererText(), text=0))
        self.subst_view_list = builder.get_object('subst-fonts')
        self.assigned_view_list = builder.get_object('assigned-fonts')
        self.add_dialog = builder.get_object('add-subst-dialog')
        self.add_dialog.set_transient_for(self.parent_window)
        self.add_dialog.set_title(_('Select a font...'))
        self.add_dialog_entry = builder.get_object('combobox-entry')
        self.add_dialog_add_button = builder.get_object('button-add')

        self.listobj = Gtk.ListStore(GObject.TYPE_STRING)
        fonts = Easyfc.Font.get_list(None, None, False)
        if len(fonts) == 0:
            # fontconfig seems not supporting the namelang object
            fonts = Easyfc.Font.get_list(None, None, True)
        for f in fonts:
            iter = self.listobj.append()
            self.listobj.set_value(iter, 0, f)

        chooser_builder = FontsTweakUtil.create_builder('chooser.ui')
        chooser_builder.connect_signals(FontsTweakChooserUI(chooser_builder, self.listobj, self.on_treemodel_filter))
        self.chooser = chooser_builder.get_object('chooser-dialog')
        self.chooser.set_transient_for(self.parent_window)
        self.chooser.set_title(_('Select a font...'))
        self.chooser_view = chooser_builder.get_object('treeview')
        self.chooser_selector = chooser_builder.get_object('treeview-selection')
        self.chooser_view.append_column(Gtk.TreeViewColumn(None, Gtk.CellRendererText(), text=0))

        # check if current icon theme supports the symbolic icons
        for i in ['add-subst', 'remove-subst', 'add-font-assigned', 'remove-font-assigned', 'move-up-subst', 'move-down-subst']:
            icon = builder.get_object(i)
            icon.set_icon_name(FontsTweakUtil.check_symbolic(icon.get_icon_name()))

        for f in self.config.get_subst_family():
            iter = self.subst_view_list.append()
            self.subst_view_list.set_value(iter, 0, f)

        self.on_treeview_selection_subst_changed(self.subst_selector)

        self.__initialized = True

    def on_treemodel_filter(self, model, iter, filter):
        patterns = filter.get_text().split(' ')
        if len(patterns) == 1 and patterns[0] == '':
            return True
        n = model.get_value(iter, 0)
        for p in patterns:
            if re.search(p, n, re.I):
                return True

        return False

    def __treeview_selection_changed(self, widget, no_sel_cb, sel_cb, masked_buttons):
        model, iter = widget.get_selected()
        if iter == None:
            no_sel_cb()
            for w in masked_buttons:
                w.set_sensitive(False)
        else:
            for w in masked_buttons:
                w.set_sensitive(True)
            sel_cb(model, iter)

    def on_treeview_selection_subst_changed(self, widget):
        self.__treeview_selection_changed(widget, lambda: self.pages.set_current_page(1),
                                          lambda model, itr: self.pages.set_current_page(0),
                                          [self.remove_subst_button])
        smodel, siter = widget.get_selected()
        if siter != None:
            subst = smodel.get_value(siter, 0)
            model = self.assigned_view.get_model()
            model.clear()
            for f in self.config.get_substs(subst):
                iter = model.append()
                model.set_value(iter, 0, f.get_family())
                
        self.on_treeview_selection_assigned_changed(self.assigned_selector)

    def on_treeview_selection_assigned_changed(self, widget):
        self.__treeview_selection_changed(widget, lambda: None,
                                          lambda model, itr: None,
                                          [self.remove_font_button, self.move_up_button, self.move_down_button])
        model, iter = widget.get_selected()
        if iter != None:
            if model.iter_previous(iter) == None:
                self.move_up_button.set_sensitive(False)
            else:
                self.move_up_button.set_sensitive(True)
            if model.iter_next(iter) == None:
                self.move_down_button.set_sensitive(False)
            else:
                self.move_down_button.set_sensitive(True)

    def on_add_subst_clicked(self, widget):
        self.add_dialog.show_all()
        resid = self.add_dialog.run()
        self.add_dialog.hide()
        if resid == Gtk.ResponseType.CANCEL:
            return
        name = self.add_dialog_entry.get_text()
        if name == None or len(name) == 0:
            return
        iter = self.add_subst(name)
        if iter == None:
            print("%s has already been added." % name)
        else:
            model = self.subst_view.get_model()
            path = model.get_path(iter)
            self.subst_view.set_cursor(path, None, False)

    def on_remove_subst_clicked(self, widget):
        model, iter = self.subst_selector.get_selected()
        if iter == None:
            return
        n = model.get_value(iter, 0)
        self.config.remove_substs(n)
        try:
            self.config.save()
        except GLib.GError as e:
            if e.domain != 'ezfc-error-quark' and e.code != 6:
                raise
        model.remove(iter)
        self.on_treeview_selection_subst_changed(self.subst_selector)

    def on_add_font_assigned_clicked(self, widget):
        self.chooser.show_all()
        resid = self.chooser.run()
        self.chooser.hide()
        if resid == Gtk.ResponseType.CANCEL:
            return
        model, iter = self.chooser_selector.get_selected()
        if iter == None:
            return
        font = model.get_value(iter, 0)
        iter = self.add_font(font)
        if iter == None:
            print("%s has already been added." % font)
        else:
            model = self.assigned_view.get_model()
            path = model.get_path(iter)
            self.assigned_view.set_cursor(path, None, False)

    def on_remove_font_assigned_clicked(self, widget):
        smodel, siter = self.subst_selector.get_selected()
        if siter == None:
            return
        subst = smodel.get_value(siter, 0)
        model, iter = self.assigned_selector.get_selected()
        if iter == None:
            return
        font = model.get_value(iter, 0)
        self.config.remove_subst(subst, font)
        try:
            self.config.save()
        except GLib.GError as e:
            if e.domain != 'ezfc-error-quark' and e.code != 6:
                raise
        model.remove(iter)
        self.on_treeview_selection_assigned_changed(self.assigned_selector)

    def __update_subst_order(self):
        smodel, siter = self.subst_selector.get_selected()
        if siter == None:
            return
        subst = smodel.get_value(siter, 0)
        model = self.assigned_view.get_model()
        iter = model.get_iter_first()
        a = []
        while iter != None:
            f = model.get_value(iter, 0)
            a.append(f)
            iter = model.iter_next(iter)
        self.config.remove_substs(subst)
        for f in a:
            o = Easyfc.Font()
            o.add_family(f)
            self.config.add_subst(subst, o)
        try:
            self.config.save()
        except GLib.GError as e:
            if e.domain != 'ezfc-error-quark' and e.code != 6:
                raise

    def on_move_up_subst_clicked(self, widget):
        model, iter = self.assigned_selector.get_selected()
        piter = model.iter_previous(iter)
        if piter == None:
            return
        f = model.get_value(iter, 0)
        niter = model.insert_before(piter)
        model.set_value(niter, 0, f)
        model.remove(iter)
        path = model.get_path(niter)
        self.assigned_view.set_cursor(path, None, False)
        self.__update_subst_order()

    def on_move_down_subst_clicked(self, widget):
        model, iter = self.assigned_selector.get_selected()
        niter = model.iter_next(iter)
        if niter == None:
            return
        f = model.get_value(iter, 0)
        newiter = model.insert_after(niter)
        model.set_value(newiter, 0, f)
        model.remove(iter)
        path = model.get_path(newiter)
        self.assigned_view.set_cursor(path, None, False)
        self.__update_subst_order()

    def on_add_subst_dialog_close(self, widget):
        self.add_dialog_entry.set_text('')

    def on_add_subst_dialog_show(self, widget):
        self.add_dialog_entry.set_text('')
        self.add_dialog_entry.grab_focus()

    def add_subst(self, font):
        retval = True
        model = self.subst_view.get_model()
        iter = model.get_iter_first()
        while iter != None:
            f = model.get_value(iter, 0)
            if f == font:
                retval = False
                break
            iter = model.iter_next(iter)
        if retval == True:
            iter = model.append()
            model.set_value(iter, 0, font)
        else:
            iter = None
        return iter

    def add_font(self, font):
        retval = True
        model = self.assigned_view.get_model()
        iter = model.get_iter_first()
        while iter != None:
            f = model.get_value(iter, 0)
            if f == font:
                retval = False
                break
            iter = model.iter_next(iter)
        if retval == True:
            smodel, siter = self.subst_selector.get_selected()
            if siter == None:
                return
            iter = model.append()
            model.set_value(iter, 0, font)
            subst = smodel.get_value(siter, 0)
            o = Easyfc.Font()
            o.add_family(font)
            self.config.add_subst(subst, o)
            try:
                self.config.save()
            except GLib.GError as e:
                if e.domain != 'ezfc-error-quark' and e.code != 6:
                    raise
        else:
            iter = None
        return iter
