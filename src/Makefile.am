NULL =
AUTOMAKE_OPTIONS =	\
	dist-bzip2	\
	$(NULL)
SUBDIRS =		\
	data		\
	fontstweak	\
	po		\
	$(NULL)
EXTRA_DIST =			\
	$(desktop_in_files)	\
	$(bin_SCRIPTS)		\
	$(NULL)
MAINTAINERCLEANFILES =		\
	$(srcdir)/INSTALL	\
	$(srcdir)/aclocal.m4	\
	$(srcdir)/autoscan.log	\
	$(srcdir)/compile	\
	$(srcdir)/config.guess	\
	$(srcdir)/config.sub	\
	$(srcdir)/depcomp	\
	$(srcdir)/install-sh	\
	$(srcdir)/ltmain.sh	\
	$(srcdir)/missing	\
	$(srcdir)/mkinstalldirs	\
	$(srcdir)/py-compile	\
	$(srcdir)/ChangeLog	\
	`find "$(srcdir)" -type f -name Makefile.in -print`	\
	$(NULL)
DISTCLEANFILES =		\
	$(desktop_DATA)		\
	$(NULL)
CLEANFILES =				\
	$(desktop_DATA)			\
	$(NULL)

##
desktopdir = $(datadir)/applications
desktop_in_files =			\
	fonts-tweak-tool.desktop.in	\
	$(NULL)
desktop_DATA = $(desktop_in_files:.desktop.in=.desktop)
@INTLTOOL_DESKTOP_RULE@

##
bin_SCRIPTS =			\
	fonts-tweak-tool	\
	$(NULL)

##
ChangeLog: $(srcdir)/ChangeLog
$(srcdir)/ChangeLog:
	$(AM_V_GEN) if test -d "$(srcdir)/.git"; then		\
	 (GIT_DIR=$(top_srcdir)/.git $(GIT) log --stat) |	\
	 fmt --split-only > $@.tmp				\
	 && mv -f $@.tmp $@					\
	 || ($(RM) $@.tmp;					\
	     echo Failed to generate ChangeLog.  your ChangeLog may be outdated >&2;	\
	     (test -f $@ || echo git-log is required to genereate this file >> $@));	\
	 else							\
	   test -f $@ || 					\
	   (echo A git checkout and git-log is required to genereate ChangeLog >&2 &&	\
	    echo A git checkout and git-log is required to genereate this file >> $@);	\
	fi

.PHONY: $(srcdir)/ChangeLog

-include $(top_srcdir)/git.mk
