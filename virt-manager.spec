# TODO
# - pldize spec (use pld macros in post scriptes, fix deps)
# - fix BR python 2.14
Summary:	Virtual Machine Manager
Name:		virt-manager
Version:	0.8.7
Release:	0.1
License:	GPL v2+
Group:		Applications/Emulators
Source0:	http://virt-manager.et.redhat.com/download/sources/virt-manager/%{name}-%{version}.tar.gz
# Source0-md5:	9b1f3ead125d53bf506216c4bc7c4a84
URL:		http://virt-manager.et.redhat.com/
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	intltool
BuildRequires:	perl-tools-pod
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python-pygobject-devel >= 2.14
BuildRequires:	python-pygtk-devel >= 2.14
BuildRequires:	scrollkeeper
Requires(post):	GConf2
Requires(pre):	GConf2
Requires(preun):	GConf2
# These two are just the oldest version tested
Requires:	python-gnome-gconf >= 1.99.11-7
Requires:	python-pygtk-gtk >= 1.99.12-6
# Absolutely require this version or newer
Requires:	python-libvirt >= 0.4.5
# Definitely does not work with earlier due to python API changes
Requires:	python-dbus >= 0.61
Requires:	python-gnome-vfs >= 2.15.4
# Minimum we've tested with
# Required for loading the glade UI
# Required for our graphics which are currently SVG format
# Required to install Xen & QEMU guests
Requires:	python-gnome-desktop-librsvg >= 2.14
Requires:	python-libxml2 >= 2.6.23
Requires:	python-pygtk-glade >= 2.12
Requires:	python-virtinst >= 0.500.1
# Earlier vte had broken python binding module
Requires:	vte >= 0.12.2
# For online help
Requires:	scrollkeeper
# For console widget
Requires:	python-gtk-vnc >= 0.3.4
# For local authentication against PolicyKit
Requires:	PolicyKit-gnome
Requires:	python-urlgrabber
Requires:	python-vte
Suggests:	gnome-keyring >= 0.4.9
Suggests:	python-gnome-desktop-keyring >= 2.15.4
ExclusiveArch:	%{ix86} x86_64 ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Virtual Machine Manager provides a graphical tool for administering
virtual machines for KVM, Xen, and QEmu. Start, stop, add or remove
virtual devices, connect to a graphical or serial console, and see
resource usage statistics for existing VMs on local or remote
machines. Uses libvirt as the backend management API.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/pixmaps/*.svg

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
%attr(755,root,root) %{_bindir}/%{name}-tui
%{_libexecdir}/%{name}-launch

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*.glade
%dir %{_datadir}/%{name}/pixmaps
%{_datadir}/%{name}/pixmaps/*.png
%{_datadir}/%{name}/pixmaps/hicolor/*/actions/*.png

# TODO: py_comp/py_ocomp in install (see template-specs/python.spec)
%{_datadir}/%{name}/*.py
#%{_datadir}/%{name}/*.pyc
#%{_datadir}/%{name}/*.pyo

%dir %{_datadir}/%{name}/virtManager
%{_datadir}/%{name}/virtManager/*.py
#%{_datadir}/%{name}/virtManager/*.pyc
#%{_datadir}/%{name}/virtManager/*.pyo
%dir %{_datadir}/%{name}/virtManagerTui
%{_datadir}/%{name}/virtManagerTui/*.py

#%dir %{_datadir}/omf/%{name}
#%{_datadir}/omf/%{name}/*.omf
#%dir %{_datadir}/gnome/help
#%{_datadir}/gnome/help/%{name}
%{_desktopdir}/%{name}.desktop
%{_datadir}/dbus-1/services/%{name}.service
%{_mandir}/man1/%{name}.1*
