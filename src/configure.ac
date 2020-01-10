dnl Process this file with autoconf to produce a configure script.
AC_PREREQ(2.62)
AC_INIT([fonts-tweak-tool], 0.3.2, [https://bitbucket.org/tagoh/fonts-tweak-tool/issues])

AM_INIT_AUTOMAKE([1.11 -Wno-portability])
AM_MAINTAINER_MODE

dnl silent build rules, requires at least automake-1.11.
dnl by either passing --enable-silent-rules to configure or
dnl V=0 to make.
m4_ifdef([AM_SILENT_RULES], [AM_SILENT_RULES([yes])])


AC_PROG_LIBTOOL
AC_PROG_INTLTOOL

AM_PATH_PYTHON

AM_MISSING_PROG([GIT], [git])

GOBJECT_INTROSPECTION_CHECK([1.30.0])
if test "x$enable_introspection"  != "xyes"; then
	AC_MSG_ERROR([gobject-introspection is required to build.])
fi
PKG_CHECK_MODULES(GIO, gio-2.0 >= 2.32)

dnl ======================================================================
dnl gettext stuff
dnl ======================================================================
GETTEXT_PACKAGE=$PACKAGE
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE", [Gettext package])

AM_GLIB_GNU_GETTEXT

dnl ======================================================================
dnl output
dnl ======================================================================
AC_CONFIG_COMMANDS([chmod-scripts],
	[chmod 0755 fonts-tweak-tool])
AC_CONFIG_FILES([
	Makefile
	data/Makefile
	fontstweak/Makefile
	po/Makefile.in
])
AC_OUTPUT
