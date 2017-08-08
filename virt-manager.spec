Summary:	Virtual Machine Manager
Summary(pl.UTF-8):	Zarządca maszyn wirtualnych
Name:		virt-manager
Version:	1.4.1
Release:	1
Epoch:		1
License:	GPL v2+
Group:		Applications/Emulators
Source0:	https://releases.pagure.org/virt-manager/%{name}-%{version}.tar.gz
# Source0-md5:	9be90a61e688187e29cb737b1558077b
URL:		http://virt-manager.org/
BuildRequires:	gettext-tools >= 0.14.1
BuildRequires:	glib2-devel
BuildRequires:	intltool >= 0.35.0
BuildRequires:	perl-tools-pod
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	rpmbuild(macros) >= 1.592
Requires(post,postun):	glib2
Requires(post,postun):	gtk-update-icon-cache
Requires:	gtk+3 >= 3.14
Requires:	gtk3-vnc >= 0.4.3
Requires:	hicolor-icon-theme
Requires:	libosinfo >= 0.2.10
Requires:	libvirt-glib >= 0.0.9
Requires:	python-dbus >= 0.84.0
Requires:	python-gnome-desktop-librsvg >= 2.32.0
Requires:	python-gnome-gconf >= 2.28.1
Requires:	python-ipaddr
Requires:	python-libvirt >= 0.9.6
Requires:	python-pygobject3 >= 3.14
Requires:	python-virtinst = %{epoch}:%{version}-%{release}
Requires:	spice-gtk
Requires:	vte >= 0.34
Suggests:	gnome-keyring >= 0.4.9
Suggests:	python-gnome-desktop-keyring >= 2.15.4
Suggests:	python-libguestfs >= 1.12.0
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

%package -n python-virtinst
Summary:	Python modules and utilities for installing virtual machines
Summary(pl.UTF-8):	Moduły Pythona i narzędzia do instalowania maszyn wirtualnych
Group:		Libraries/Python
Requires:	python-libvirt >= 0.9.6
Requires:	python-libxml2 >= 1:2.7.8
Requires:	python-modules
Requires:	python-urlgrabber
Suggests:	python-selinux
Suggests:	virt-viewer >= 0.0.1

%description -n python-virtinst
virtinst is a module that helps build and install libvirt based
virtual machines. Currently supports KVM, QEmu and Xen virtual
machines. Package includes several command line utilities, including
virt-install (build and install new VMs) and virt-clone (clone an
existing virtual machine).

%description -n python-virtinst -l pl.UTF-8
virtinst to moduł pomagający przy tworzeniu i instalowaniu maszyn
wirtualnych opartych na libvirt. Obecnie obsługiwane są maszyny KVM,
QEmu i Xen. Pakiet zawiera kilka działających z linii poleceń
skryptów, w tym virt-install (tworzący i instalujący nowe VM-y) oraz
virt-clone (klonujący istniejącą maszynę wirtualną).

%prep
%setup -q

%build
%{__python} setup.py configure \
	--prefix=%{_prefix} \
	--libvirt-package-names=libvirt \
	--kvm-package-names=qemu-lvm

%py_build

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}
# requires patching(?)
#%%py_postclean %{_datadir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%glib_compile_schemas
%update_icon_cache hicolor

%postun
if [ "$1" = "0" ]; then
	%glib_compile_schemas
fi
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%doc NEWS.md README.md
%attr(755,root,root) %{_bindir}/virt-manager
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/ui
%dir %{_datadir}/%{name}/virtManager
%{_datadir}/%{name}/virtManager/*.py*
%attr(755,root,root) %{_datadir}/%{name}/virt-manager
%{_datadir}/GConf/gsettings/org.virt-manager.virt-manager.convert
%{_datadir}/appdata/virt-manager.appdata.xml
%{_datadir}/glib-2.0/schemas/org.virt-manager.virt-manager.gschema.xml
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/virt-manager.png
%{_mandir}/man1/virt-manager.1*

%files -n python-virtinst -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/virt-clone
%attr(755,root,root) %{_bindir}/virt-convert
%attr(755,root,root) %{_bindir}/virt-install
%attr(755,root,root) %{_bindir}/virt-xml
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/virtcli
%{_datadir}/%{name}/virtcli/*.py*
%{_datadir}/%{name}/virtcli/cli.cfg
%dir %{_datadir}/%{name}/virtconv
%{_datadir}/%{name}/virtconv/*.py*
%dir %{_datadir}/%{name}/virtinst
%{_datadir}/%{name}/virtinst/*.py*
%attr(755,root,root) %{_datadir}/%{name}/virt-clone
%attr(755,root,root) %{_datadir}/%{name}/virt-convert
%attr(755,root,root) %{_datadir}/%{name}/virt-install
%attr(755,root,root) %{_datadir}/%{name}/virt-xml
%{_mandir}/man1/virt-clone.1*
%{_mandir}/man1/virt-convert.1*
%{_mandir}/man1/virt-install.1*
%{_mandir}/man1/virt-xml.1*
