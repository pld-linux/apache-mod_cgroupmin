%define		apxs		/usr/sbin/apxs
%define		mod_name	cgroupmin
Summary:	Resource management per vhost
Name:		apache-mod_%{mod_name}
Version:	0.0.1
Release:	1
License:	GPL
Group:		Networking/Daemons/HTTP
Source0:	https://github.com/arekm/mod_cgroupmin/archive/v0.0.1.tar.gz
# Source0-md5:	3e56d21b6efbbda3cb6510edd153de97
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0
BuildRequires:	apr-devel >= 1:1.0
BuildRequires:	apr-util-devel >= 1:1.0
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_cgroupmin provides a system administrator with the capability to
provide predictable service levels for each virtual host declared in
httpd.

mod_cgroup can be used for:
- Offering grades of service per virtual host or a group of virtual
  hosts.
- Protecting other virtual hosts from problematic resource abuse in
  another vhost.
- Penalizing a virtual host which fails to respect resouce
  limitations.
- Ensuring a predictable capacity level is provided to all web
  services.

%prep
%setup -q -n mod_%{mod_name}-%{version}

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.la

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
install mod_%{mod_name}.conf  $RPM_BUILD_ROOT%{_sysconfdir}/00_mod_cgroupmin.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README.md
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/mod_%{mod_name}.so
