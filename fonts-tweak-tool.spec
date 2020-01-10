Name: fonts-tweak-tool
Version: 0.3.2
Release: 1%{?dist}
Summary: Tool for customizing fonts per language

Group: User Interface/Desktops
License: LGPLv3+
URL: https://bitbucket.org/tagoh/%{name}/
Source0: https://bitbucket.org/tagoh/%{name}/downloads/%{name}-%{version}.tar.bz2

BuildRequires: desktop-file-utils
BuildRequires: intltool
BuildRequires: python-devel
BuildRequires: gobject-introspection-devel glib2-devel
Requires: libeasyfc-gobject >= 0.12.1
Requires: pygobject3
Requires: gtk3
Requires: hicolor-icon-theme

%description
fonts-tweak-tool is a GUI tool for customizing fonts per language on desktops
using fontconfig.

%prep
%setup -q
%configure --disable-static

%build
make %{?_smp_mflags}

%install
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications fonts-tweak-tool.desktop
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="/usr/bin/install -p"

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.{la,so}
rm -f $RPM_BUILD_ROOT%{_datadir}/gir-*/FontsTweak-*.gir

%find_lang %{name}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc README COPYING AUTHORS NEWS
%{_bindir}/%{name}
%{python_sitelib}/fontstweak
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_libdir}/libfontstweak-resources.so.0*
%{_libdir}/girepository-*/FontsTweak-*.typelib

%changelog
* Wed Jul 31 2013 Akira TAGOH <tagoh@redhat.com> - 0.3.2-1
- New upstream release.

* Thu Apr 18 2013 Akira TAGOH <tagoh@redhat.com> - 0.3.1-1
- New upstream release.
  - Fix a crash. (#952983)

* Fri Mar 29 2013 Akira TAGOH <tagoh@redhat.com> - 0.3.0-1
- New upstream release.

* Tue Feb 26 2013 Akira TAGOH <tagoh@redhat.com> - 0.2.0-1
- New upstream release.
  - Improve UI (#909769)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Akira TAGOH <tagoh@redhat.com> - 0.1.5-1
- New upstream release.
  - Updated translations (#816378)

* Tue Dec 18 2012 Akira TAGOH <tagoh@redhat.com> - 0.1.4-1
- New upstream release.
  - Fix file writing issue when the classification filter is turned off.
    (#886330)

* Sat Nov 24 2012 Akira TAGOH <tagoh@redhat.com> - 0.1.2-1
- New upstream release
  - Fix broken icons issue on non-GNOME desktops (#879140)

* Wed Nov 21 2012 Akira TAGOH <tagoh@redhat.com> - 0.1.1-3
- Fix a typo

* Wed Nov 21 2012 Akira TAGOH <tagoh@redhat.com> - 0.1.1-2
- clean up and improve the spec file.

* Mon Oct 22 2012 Akira TAGOH <tagoh@redhat.com> - 0.1.1-1
- New upstream release.
  - Drop the unnecessary warnings (#859455)

* Wed Sep 19 2012 Akira TAGOH <tagoh@redhat.com> - 0.1.0-1
- New upstream release.

* Mon Aug 06 2012 James Ni <kent.neo@gmail.com> - 0.0.8-1
- Apply pull request from tagoh

* Tue Jul 24 2012 James Ni <kent.neo@gmail.com> - 0.0.7-1
- Fixed rhbz#838871, Apply button is always clickable
- Fixed rhbz#838854, existing settings in .i18n isn't reflected to initial value
- Fixed rhbz#838865, Unable to remove language in GTK Language Order tab
- Fixed rhbz#838850 - empty language added to .i18n

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 James Ni <jni@redhat.com> - 0.0.6-1
- Implement pango_language feature and bug fix

* Tue Mar 20 2012 James Ni <jni@redhat.com> - 0.0.5-1
- Fix issue of 'UnicodeWarning: Unicode equal comparison failed'

* Mon Mar 19 2012 James Ni <jni@redhat.com> - 0.0.4-1
- Bug fix and feature enhancement

* Thu Feb 23 2012 James Ni <jni@redhat.com> - 0.0.3-1
- Fix the issue of spec file

* Fri Feb 17 2012 James Ni <jni@redhat.com> - 0.0.2-3
- Fix the issue of spec file

* Wed Feb 08 2012 James Ni <jni@redhat.com> - 0.0.2-2
- Fix the issue of spec file

* Tue Feb 07 2012 James Ni <jni@redhat.com> - 0.0.2-1
- Update the licenses file and modify the spec file

* Mon Feb 06 2012 James Ni <jni@redhat.com> - 0.0.1-1
- initial package
