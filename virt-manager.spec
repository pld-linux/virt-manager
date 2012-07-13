# TODO
# - fix BR python 2.14
Summary:	Virtual Machine Manager
Summary(pl.UTF-8):	Zarządca maszyn wirtualnych
Name:		virt-manager
Version:	0.9.3
Release:	1
License:	GPL v2+
Group:		Applications/Emulators
Source0:	http://virt-manager.org/download/sources/virt-manager/%{name}-%{version}.tar.gz
# Source0-md5:	4c03f1628c76a891f45c0375bf5590da
URL:		http://virt-manager.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-devel >= 0.14.1
BuildRequires:	glib2-devel
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	perl-tools-pod
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	sed >= 4.0
Requires(pre,preun,post):	GConf2
Requires(post,postun):	gtk-update-icon-cache
Requires:	python-gnome-gconf >= 2.28.1
Requires:	python-pygobject >= 2.28.6
Requires:	python-pygtk-gtk >= 2.24.0
Requires:	python-libvirt >= 0.9.6
Requires:	python-dbus >= 0.84.0
Requires:	python-gnome-desktop-librsvg >= 2.32.0
Requires:	python-libxml2 >= 1:2.7.8
Requires:	python-virtinst >= 0.600.1
Requires:	hicolor-icon-theme
Requires:	python-gtk-vnc >= 0.4.3
Requires:	python-urlgrabber
Requires:	python-pycairo
Requires:	python-vte0 >= 0.28.2
Suggests:	gnome-keyring >= 0.4.9
Suggests:	python-gnome-desktop-keyring >= 2.15.4
Suggests:	python-libguestfs >= 1.12.0
Suggests:	python-spice-gtk
ExclusiveArch:	%{ix86} %{x8664} ia64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Virtual Machine Manager provides a graphical tool for administering
virtual machines for KVM, Xen, and QEmu. Start, stop, add or remove
virtual devices, connect to a graphical or serial console, and see
resource usage statistics for existing VMs on local or remote
machines. Uses libvirt as the backend management API.

%description -l pl.UTF-8
Virtual Machine Manager udostępnia graficzne narzędzie do
administrowania maszynami wirtualnymi dla środowisk KVM, Xen i QEmu.
Pozwala uruchamiać, zatrzymywać, dodawać i usuwać urządzenia
wirtualne, łączyć się z konsolą graficzną lub szeregową oraz oglądać
statystyki wykorzystania zasobów istniejących maszyn wirtualnych na
maszynach lokalnych i zdalnych. Wykorzystuje libvirt jako API do
zarządzania.

%prep
%setup -q

%{__sed} -i -e 's|PWD|shell pwd|g' icons/hicolor/*/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-libvirt-package-names=libvirt \
	--with-kvm-packages=qemu-kvm
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}
# requires patching
#%%py_postclean %{_datadir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install %{name}.schemas
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall %{name}.schemas

%postun
%update_icon_cache hicolor


%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%attr(755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/%{name}-tui
%{_libexecdir}/%{name}-launch

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/icons
%{_iconsdir}/hicolor/*/apps/virt-manager.png

%{_datadir}/%{name}/*.py
%{_datadir}/%{name}/*.py[co]
%dir %{_datadir}/%{name}/virtManager
%{_datadir}/%{name}/virtManager/*.py
%{_datadir}/%{name}/virtManager/*.py[co]
%dir %{_datadir}/%{name}/virtManagerTui
%{_datadir}/%{name}/virtManagerTui/*.py
%{_datadir}/%{name}/virtManagerTui/*.py[co]
%dir %{_datadir}/%{name}/virtManagerTui/importblacklist
%{_datadir}/%{name}/virtManagerTui/importblacklist/*.py
%{_datadir}/%{name}/virtManagerTui/importblacklist/*.py[co]
%{_datadir}/%{name}/vmm-*.ui

%{_desktopdir}/%{name}.desktop
%{_datadir}/dbus-1/services/%{name}.service
%{_mandir}/man1/%{name}.1*
