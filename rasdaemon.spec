Summary:	Utility to receive RAS error tracings
Name:		rasdaemon
Version:	0.5.8
Release:	0.1
License:	GPL v2
Group:		Applications/System
URL:		http://git.infradead.org/users/mchehab/rasdaemon.git
Source0:	http://www.infradead.org/~mchehab/rasdaemon/%{name}-%{version}.tar.bz2
BuildRequires:	gettext-devel
BuildRequires:	sqlite-devel
BuildRequires:	systemd-devel
Requires:	hwdata
Requires:	perl-DBD-SQLite
ExcludeArch:	s390 s390x
%ifarch %{ix86} x86_64
Requires:	dmidecode
%endif
Requires(post):	systemd
Requires(preun):	systemd
Requires(postun):	systemd

%description
%{name} is a RAS (Reliability, Availability and Serviceability)
logging tool. It currently records memory errors, using the EDAC
tracing events. EDAC is drivers in the Linux kernel that handle
detection of ECC errors from memory controllers for most chipsets on
i386 and x86_64 architectures. EDAC drivers for other architectures
like arm also exists. This userspace component consists of an init
script which makes sure EDAC drivers and DIMM labels are loaded at
system startup, as well as an utility for reporting current error
counts from the EDAC sysfs files.

%prep
%setup -q

%build
%configure \
	--enable-mce \
	--enable-aer \
	--enable-sqlite3 \
	--enable-extlog \
	--enable-abrt-report \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D -p misc/rasdaemon.service $RPM_BUILD_ROOT/%{systemdunitdir}/rasdaemon.service
install -D -p misc/ras-mc-ctl.service $RPM_BUILD_ROOT%{systemdunitdir}/ras-mc-ctl.service

rm INSTALL $RPM_BUILD_ROOT%{_includedir}/*.h

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING README TODO
%attr(755,root,root) %{_sbindir}/rasdaemon
%attr(755,root,root) %{_sbindir}/ras-mc-ctl
%{_mandir}/*/*
%{systemdunitdir}/*.service
%{_sharedstatedir}/rasdaemon
%{_sysconfdir}/ras/dimm_labels.d
