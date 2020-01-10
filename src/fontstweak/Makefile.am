-include $(INTROSPECTION_MAKEFILE)

NULL =
EXTRA_DIST =			\
	$(pyscripts_sources)	\
	$(NULL)
DISTCLEANFILES =		\
	*.pyc			\
	*.pyo			\
	$(NULL)
BUILT_SOURCES =			\
	fonts-tweak-resources.c	\
	fonts-tweak-resources.h	\
	$(NULL)
CLEANFILES = $(BUILT_SOURCES)
INTROSPECTION_GIRS =
INTROSPECTION_SCANNER_ARGS =		\
	--add-include-path=$(srcdir)	\
	--warn-all			\
	$(NULL)
INTROSPECTION_COMPILER_ARGS =		\
	--includedir=$(srcdir)		\
	$(NULL)

##
pyscripts_sources =	\
	__init__.py	\
	aliasui.py	\
	chooserui.py	\
	fontstweak.py	\
	langui.py	\
	propui.py	\
	substui.py	\
	util.py		\
	$(NULL)

pyscripts_PYTHON = $(pyscripts_sources)
pyscriptsdir = $(pythondir)/fontstweak

lib_LTLIBRARIES =			\
	libfontstweak-resources.la	\
	$(NULL)

libfontstweak_resources_la_SOURCES =	\
	$(BUILT_SOURCES)		\
	$(NULL)
libfontstweak_resources_la_CFLAGS =	\
	$(GIO_CFLAGS)			\
	$(NULL)
libfontstweak_resources_la_LIBS =	\
	$(GIO_LIBS)			\
	$(NULL)

resource_files = $(shell glib-compile-resources --sourcedir=$(top_srcdir)/data --generate-dependencies $(srcdir)/gresource.xml)
fonts-tweak-resources.c: gresource.xml $(resource_files)
	$(AM_V_GEN) glib-compile-resources --target=$@ --sourcedir=$(top_srcdir)/data --generate-source --c-name fonts_tweak $<
fonts-tweak-resources.h: gresource.xml $(resource_files)
	$(AM_V_GEN) glib-compile-resources --target=$@ --sourcedir=$(top_srcdir)/data --generate-source --c-name fonts_tweak $<

introspection_sources =				\
	$(libfontstweak_resources_la_SOURCES)	\
	$(NULL)

EXTRA_DIST += $(resource_files) gresource.xml

FontsTweak-0.gir: $(INTROSPECTION_SCANNER) libfontstweak-resources.la Makefile
FontsTweak_0_gir_INCLUDES =		\
	GObject-2.0			\
	Gio-2.0				\
	$(NULL)
FontsTweak_0_gir_SCANNERFLAGS =		\
	--symbol-prefix=fonts_tweak	\
	$(NULL)
FontsTweak_0_gir_CFLAGS =		\
	$(AM_CPPFLAGS)			\
	$(NULL)
FontsTweak_0_gir_LIBS =			\
	libfontstweak-resources.la	\
	$(NULL)
FontsTweak_0_gir_FILES = $(introspection_sources)
INTROSPECTION_GIRS += FontsTweak-0.gir

girdir = $(datadir)/gir-1.0
gir_DATA = $(INTROSPECTION_GIRS)

typelibdir = $(libdir)/girepository-1.0
typelib_DATA = $(INTROSPECTION_GIRS:.gir=.typelib)

CLEANFILES += $(gir_DATA) $(typelib_DATA)

-include $(top_srcdir)/git.mk
