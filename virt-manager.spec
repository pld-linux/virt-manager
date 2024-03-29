Summary:	Virtual Machine Manager
Summary(pl.UTF-8):	Zarządca maszyn wirtualnych
Name:		virt-manager
Version:	4.1.0
Release:	1
Epoch:		1
License:	GPL v2+
Group:		Applications/Emulators
Source0:	https://releases.pagure.org/virt-manager/%{name}-%{version}.tar.gz
# Source0-md5:	8bf86bcc7e43a956ff94ebdaf4d7d399
URL:		https://virt-manager.org/
# rst2man
BuildRequires:	docutils
BuildRequires:	gettext-tools >= 0.14.1
BuildRequires:	python3-devel >= 1:3
BuildRequires:	rpmbuild(macros) >= 1.592
Requires(post,postun):	glib2
Requires(post,postun):	gtk-update-icon-cache
Requires:	gtk+3 >= 3.22.0
Requires:	gtk3-vnc >= 0.4.3
Requires:	gtksourceview4
Requires:	hicolor-icon-theme
Requires:	libosinfo >= 0.2.10
Requires:	libvirt-glib >= 0.0.9
Requires:	python3-libvirt >= 0.9.6
Requires:	python3-pygobject3 >= 3.32
Requires:	python3-virtinst = %{epoch}:%{version}-%{release}
Requires:	spice-gtk
Requires:	vte >= 0.34
Requires:	xorriso
Suggests:	gnome-keyring >= 0.4.9
Suggests:	python3-libguestfs >= 1.12.0
BuildArch:	noarch
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

%package -n bash-completion-virt-manager
Summary:	bash-completion for virt-clone, virt-install and virt-xml commands
Summary(pl.UTF-8):	bashowe uzupełnianie parametrów poleceń virt-clone, virt-install i virt-xml
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-virt-manager
Bash-completion for virt-clone, virt-install and virt-xml commands.

%description -n bash-completion-virt-manager -l pl.UTF-8
Bashowe uzupełnianie parametrów polecenń virt-clone, virt-install i
virt-xml.

%package -n python3-virtinst
Summary:	Python modules and utilities for installing virtual machines
Summary(pl.UTF-8):	Moduły Pythona i narzędzia do instalowania maszyn wirtualnych
Group:		Libraries/Python
Requires:	python3-libvirt >= 0.9.6
Requires:	python3-libxml2 >= 1:2.7.8
Requires:	python3-modules
Requires:	python3-requests
Suggests:	python3-selinux
Suggests:	virt-viewer >= 0.0.1
Obsoletes:	python-virtinst < 2.0.0

%description -n python3-virtinst
virtinst is a module that helps build and install libvirt based
virtual machines. Currently supports KVM, QEmu and Xen virtual
machines. Package includes several command line utilities, including
virt-install (build and install new VMs) and virt-clone (clone an
existing virtual machine).

%description -n python3-virtinst -l pl.UTF-8
virtinst to moduł pomagający przy tworzeniu i instalowaniu maszyn
wirtualnych opartych na libvirt. Obecnie obsługiwane są maszyny KVM,
QEmu i Xen. Pakiet zawiera kilka działających z linii poleceń
skryptów, w tym virt-install (tworzący i instalujący nowe VM-y) oraz
virt-clone (klonujący istniejącą maszynę wirtualną).

%prep
%setup -q

%build
%{__python3} setup.py configure \
	--prefix=%{_prefix} \
	--default-graphics="spice"

%install
rm -rf $RPM_BUILD_ROOT

%{__python3} setup.py \
	--no-update-icon-cache \
	--no-compile-schemas \
	install \
	--prefix=%{_prefix} \
	-O1 --root=$RPM_BUILD_ROOT

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
%dir %{_datadir}/%{name}/virtManager/details
%{_datadir}/%{name}/virtManager/details/*.py*
%dir %{_datadir}/%{name}/virtManager/device
%{_datadir}/%{name}/virtManager/device/*.py*
%dir %{_datadir}/%{name}/virtManager/lib
%{_datadir}/%{name}/virtManager/lib/*.py*
%dir %{_datadir}/%{name}/virtManager/object
%{_datadir}/%{name}/virtManager/object/*.py*
%{_datadir}/metainfo/virt-manager.appdata.xml
%{_datadir}/glib-2.0/schemas/org.virt-manager.virt-manager.gschema.xml
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/virt-manager.png
%{_mandir}/man1/virt-manager.1*

%files -n bash-completion-virt-manager
%defattr(644,root,root,755)
%{bash_compdir}/virt-clone
%{bash_compdir}/virt-install
%{bash_compdir}/virt-xml

%files -n python3-virtinst -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/virt-clone
%attr(755,root,root) %{_bindir}/virt-install
%attr(755,root,root) %{_bindir}/virt-xml
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/virtinst
%{_datadir}/%{name}/virtinst/build.cfg
%{_datadir}/%{name}/virtinst/*.py*
%dir %{_datadir}/%{name}/virtinst/devices
%{_datadir}/%{name}/virtinst/devices/*.py*
%dir %{_datadir}/%{name}/virtinst/domain
%{_datadir}/%{name}/virtinst/domain/*.py*
%dir %{_datadir}/%{name}/virtinst/install
%{_datadir}/%{name}/virtinst/install/*.py*
%{_mandir}/man1/virt-clone.1*
%{_mandir}/man1/virt-install.1*
%{_mandir}/man1/virt-xml.1*
