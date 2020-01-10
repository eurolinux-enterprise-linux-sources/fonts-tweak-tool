# -*- coding: utf-8 -*-
# util.py
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
import os.path
import string
from collections import OrderedDict
try:
    from fontstweak import FontsTweakConst
except ImportError:
    from fontstweak.fontstweak import FontsTweakConst
from gi.repository import Gtk

def N_(s):
    return s

class FontsTweakUtil:

    @classmethod
    def find_file(self, uifile):
        path = os.path.dirname(os.path.realpath(__file__))
        f = os.path.join(path, 'data', uifile)
        if not os.path.isfile(f):
            f = os.path.join(path, '..', 'data', uifile)
        if not os.path.isfile(f):
            f = os.path.join(FontsTweakConst.UIPATH, uifile)
        return f

    @classmethod
    def create_builder(self, uifile):
        builder = Gtk.Builder()
        builder.set_translation_domain(FontsTweakConst.GETTEXT_PACKAGE)
        builder.add_from_resource('/org/tagoh/fonts-tweak-tool/' + uifile)
        return builder

    @classmethod
    def get_language_list(self, default):
        dict = OrderedDict()
        if default == True:
            dict[''] = N_('Default')
        try:
            fd = open(self.find_file('locale-list'), 'r')
        except:
            raise RuntimeError("Unable to open locale-list")

        while True:
            line = fd.readline()
            if not line:
                break
            try:
                tokens = string.split(line)
            except AttributeError:
                tokens = line.split()
            lang = str(tokens[0]).split('.')[0].replace('_', '-')
            try:
                dict[lang] = string.join(tokens[3:], ' ')
            except AttributeError:
                dict[lang] = ' '.join(tokens[3:])

        return dict

    @classmethod
    def check_symbolic(self, name):
        theme = Gtk.IconTheme.get_default()
        if not theme.has_icon(name):
            return name.replace('-symbolic', '')
        return name

