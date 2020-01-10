# -*- coding: utf-8 -*-
# propui.py
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

class FontsTweakPropUI:

    def __init__(self, config, builder, parent):
        self.__initialized = False

        self.updating = False
        self.config = config
        self.parent_window = parent
        self.remove_button = builder.get_object('remove-font')
        self.pages = builder.get_object('notebook-properties-pages')
        self.selector = builder.get_object('treeview-selection')
        self.view = builder.get_object('treeview-prop-fonts-list')
        self.view.append_column(Gtk.TreeViewColumn(None, Gtk.CellRendererText(), text=0))
        self.view_list = builder.get_object('fonts-list')
        self.check_subpixel_rendering = builder.get_object('checkbutton-subpixel-rendering')
        self.check_embedded_bitmap = builder.get_object('checkbutton-embedded-bitmap')
        self.combobox_subpixel_rendering = builder.get_object('combobox-subpixel-rendering')
        self.combobox_hintstyle = builder.get_object('combobox-hintstyle')
        self.radio_no_hinting = builder.get_object('radiobutton-no-hinting')
        self.radio_hinting = builder.get_object('radiobutton-hinting')
        self.radio_autohinting = builder.get_object('radiobutton-autohinting')
        self.check_embedded_bitmap.set_sensitive(False)
        self.features_frame = builder.get_object('frame-features')
        self.features_frame.set_sensitive(False)
        self.features_view = builder.get_object('treeview-features-list')
        self.features_view.append_column(Gtk.TreeViewColumn(None, Gtk.CellRendererText(), text=0))
        self.features_selector = builder.get_object('treeview-selection-features')
        self.features_list = builder.get_object('features-list')
        self.enable_feature_tags = False

        try:
            ezfcver = Easyfc.version()
            if LooseVersion(ezfcver) > LooseVersion('0.10'):
                self.check_embedded_bitmap.set_sensitive(True)
            if LooseVersion(ezfcver) > LooseVersion('0.11'):
                self.features_frame.set_sensitive(True)
                self.enable_feature_tags = True
        except AttributeError:
            pass

        # check if current icon theme supports the symbolic icons
        add_icon = builder.get_object('add-font')
        add_icon.set_icon_name(FontsTweakUtil.check_symbolic(add_icon.get_icon_name()))
        del_icon = builder.get_object('remove-font')
        del_icon.set_icon_name(FontsTweakUtil.check_symbolic(del_icon.get_icon_name()))

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

        for f in self.config.get_fonts():
            iter = self.view_list.append()
            self.view_list.set_value(iter, 0, f.get_family())

        self.on_treeview_selection_changed(self.selector)

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

    def on_treeview_selection_changed(self, widget):
        model, iter = widget.get_selected()
        if iter == None:
            self.pages.set_current_page(1)
            self.remove_button.set_sensitive(False)
        else:
            font = model.get_value(iter, 0)
            for f in self.config.get_fonts():
                if f.get_family() == font:
                    x = f.get_subpixel_rendering()
                    if x != Easyfc.FontSubpixelRender.NONE:
                        self.check_subpixel_rendering.set_active(True)
                        self.combobox_subpixel_rendering.set_active(x - 1)
                    else:
                        self.check_subpixel_rendering.set_active(False)
                        self.combobox_subpixel_rendering.set_active(0)
                    self.check_embedded_bitmap.set_active(f.get_embedded_bitmap())
                    h = f.get_hinting()
                    ah = f.get_autohinting()
                    style = f.get_hintstyle()
                    if style == Easyfc.FontHintstyle.UNKNOWN:
                        style = Easyfc.FontHintstyle.NONE
                    if not h and not ah:
                        self.radio_no_hinting.set_active(True)
                    elif h and not ah:
                        self.radio_hinting.set_active(True)
                    elif not h and ah:
                        self.radio_autohinting.set_active(True)
                    self.combobox_hintstyle.set_active(style - 1)
                    if self.enable_feature_tags:
                        model = self.features_view.get_model()
                        model.clear()
                        for n in f.get_available_features():
                            iter = model.append()
                            model.set_value(iter, 0, n)
                        feat = f.get_features()
                        iter = model.get_iter_first()
                        self.updating = True
                        while iter != None:
                            f = model.get_value(iter, 0)
                            if f in feat:
                                self.features_selector.select_iter(iter)
                            iter = model.iter_next(iter)
                        self.updating = False

            self.pages.set_current_page(0)
            self.remove_button.set_sensitive(True)

    def on_add_font_clicked(self, widget):
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
            model = self.view.get_model()
            path = model.get_path(iter)
            self.view.set_cursor(path, None, False)

    def on_remove_font_clicked(self, widget):
        model, iter = self.selector.get_selected()
        if iter == None:
            return
        font = model.get_value(iter, 0)
        self.config.remove_font(font)
        try:
            self.config.save()
        except GLib.GError as e:
            if e.domain != 'ezfc-error-quark' and e.code != 6:
                raise
        model.remove(iter)
        self.on_treeview_selection_changed(self.selector)

    def on_checkbutton_subpixel_rendering_toggled(self, widget):
        mode = Easyfc.FontSubpixelRender.UNKNOWN
        if widget.get_active():
            self.combobox_subpixel_rendering.set_sensitive(True)
            model = self.combobox_subpixel_rendering.get_model()
            iter = self.combobox_subpixel_rendering.get_active_iter()
            mode = model.get_value(iter, 1)
        else:
            self.combobox_subpixel_rendering.set_sensitive(False)
            mode = Easyfc.FontSubpixelRender.NONE
        self.__apply_changes(lambda o: o.set_subpixel_rendering(mode))

    def on_checkbutton_embedded_bitmap_toggled(self, widget):
        self.__apply_changes(lambda o: o.set_embedded_bitmap(widget.get_active()))

    def on_radiobutton_no_hinting_toggled(self, widget):
        self.combobox_hintstyle.set_sensitive(not widget.get_active())
        if not widget.get_active():
            return
        self.__apply_changes(lambda o: o.set_hinting(False) == o.set_autohinting(False))

    def on_radiobutton_hinting_toggled(self, widget):
        if not widget.get_active():
            return
        self.__apply_changes(lambda o: o.set_hinting(True) == o.set_autohinting(False))

    def on_radiobutton_autohinting_toggled(self, widget):
        if not widget.get_active():
            return
        cb = (lambda o: o.set_hinting(False) == o.set_autohinting(True))
        self.__apply_changes(cb)
        self.on_combobox_hintstyle_changed(self.combobox_hintstyle)

    def on_combobox_subpixel_rendering_changed(self, widget):
        model = widget.get_model()
        iter = widget.get_active_iter()
        if iter == None:
            return
        rgba = model.get_value(iter, 1)
        self.__apply_changes(lambda o: o.set_subpixel_rendering(rgba))

    def on_combobox_hintstyle_changed(self, widget):
        model = widget.get_model()
        iter = widget.get_active_iter()
        if iter == None:
            return
        hintstyle = model.get_value(iter, 1)
        self.__apply_changes(lambda o: o.set_hintstyle(hintstyle))

    def __remove_feature(self, o):
        for f in o.get_features():
            o.remove_feature(f)

    def __add_feature(self, o, featlist):
        for f in featlist:
            o.add_feature(f)

    def on_treeview_selection_features_changed(self, widget):
        if self.updating:
            return
        model, pathlist = widget.get_selected_rows()
        if len(pathlist) == 0:
            self.__apply_changes(self.__remove_feature)
        else:
            feat = []
            for p in pathlist:
                iter = model.get_iter(p)
                feat.append(model.get_value(iter, 0))
            self.__apply_changes(self.__add_feature, feat)

    def __apply_changes(self, cb, *args):
        model, iter = self.selector.get_selected()
        if iter == None:
            return
        font = model.get_value(iter, 0)
        for f in self.config.get_fonts():
            if f.get_family() == font:
                cb(f, *args)
                break
        try:
            self.config.save()
        except GLib.GError as e:
            if e.domain != 'ezfc-error-quark' and e.code != 6:
                raise

    def add_font(self, font):
        retval = True
        model = self.view.get_model()
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
            o = Easyfc.Font()
            o.set_family(font)
            self.config.add_font(o)
        else:
            iter = None
        return iter
