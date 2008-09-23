
Summary:	Virtual Machine Manager
Name:		virt-manager
Version:	0.6.0
Release:	0.1
License:	GPL v2+
Group:		Applications/Emulators
URL:		http://virt-manager.et.redhat.com/
Source0:	http://virt-manager.et.redhat.com/download/sources/virt-manager/%{name}-%{version}.tar.gz
# Source0-md5:	fd0acd111f180a0766b08d5f42cf5468
Patch0:		%{name}-python.patch
BuildRequires:	atk-devel
BuildRequires:	cairo-devel
BuildRequires:	gettext
BuildRequires:	glib2-devel
#BuildRequires: gtk2-devel
BuildRequires:	intltool
BuildRequires:	pango-devel
BuildRequires:	python-devel >= 2.14
BuildRequires:	python-pygobject-devel >= 2.14
BuildRequires:	python-pygtk-devel >= 2.14
BuildRequires:	scrollkeeper

# These two are just the oldest version tested
Requires:	gnome-python2-gconf >= 1.99.11-7
Requires:	pygtk2 >= 1.99.12-6
# Absolutely require this version or newer
Requires:	libvirt-python >= 0.4.5
# Definitely does not work with earlier due to python API changes
Requires:	dbus-python >= 0.61
# Might work with earlier, but this is what we've tested
Requires:	gnome-keyring >= 0.4.9
# Minimum we've tested with
# Although if you don't have this, comment it out and the app
# will work just fine - keyring functionality will simply be
# disabled
Requires:	gnome-python2-gnomekeyring >= 2.15.4
Requires:	gnome-python2-gnomevfs >= 2.15.4
# Minimum we've tested with
# Required for loading the glade UI
# Required for our graphics which are currently SVG format
# Required to install Xen & QEMU guests
Requires:	librsvg2
Requires:	libxml2-python >= 2.6.23
Requires:	pygtk2-libglade
Requires:	python-virtinst >= 0.400.0
# Earlier vte had broken python binding module
Requires:	vte >= 0.12.2
# For online help
Requires:	scrollkeeper
# For console widget
Requires:	gtk-vnc-python >= 0.3.4
# For local authentication against PolicyKit
Requires:	PolicyKit-gnome

ExclusiveArch:	%{ix86} x86_64 ia64

Requires(post):	GConf2
Requires(pre):	GConf2
Requires(preun):	GConf2

%description
Virtual Machine Manager provides a graphical tool for administering
virtual machines for KVM, Xen, and QEmu. Start, stop, add or remove
virtual devices, connect to a graphical or serial console, and see
resource usage statistics for existing VMs on local or remote
machines. Uses libvirt as the backend management API.

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make}


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install  DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/sparkline.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/sparkline.la
%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ "$1" -gt 1 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
fi

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule \
  %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :

update-desktop-database %{_desktopdir}

if which scrollkeeper-update>/dev/null 2>&1; then scrollkeeper-update -q -o %{_datadir}/omf/%{name}; fi

%postun
update-desktop-database %{_desktopdir}

if which scrollkeeper-update>/dev/null 2>&1; then scrollkeeper-update -q; fi

%preun
if [ "$1" -eq 0 ]; then
    export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
    gconftool-2 --makefile-uninstall-rule \
      %{_sysconfdir}/gconf/schemas/%{name}.schemas > /dev/null || :
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README COPYING COPYING-DOCS AUTHORS ChangeLog NEWS
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%attr(755,root,root) %{_bindir}/%{name}
%{_libexecdir}/%{name}-launch
%{_libdir}/%{name}/*

%{_datadir}/%{name}/*.glade
%{_datadir}/%{name}/pixmaps/*.png
%{_datadir}/%{name}/pixmaps/*.svg

%{_datadir}/%{name}/*.py
#%{_datadir}/%{name}/*.pyc
#%{_datadir}/%{name}/*.pyo

%{_datadir}/%{name}/virtManager/*.py
#%{_datadir}/%{name}/virtManager/*.pyc
#%{_datadir}/%{name}/virtManager/*.pyo

%{_datadir}/omf/%{name}
%{_datadir}/gnome/help

%{_desktopdir}/%{name}.desktop
%{_datadir}/dbus-1/services/%{name}.service

%{_mandir}/man1/%{name}.1*
