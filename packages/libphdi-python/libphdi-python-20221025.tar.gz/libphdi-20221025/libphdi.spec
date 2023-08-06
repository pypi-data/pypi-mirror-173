Name: libphdi
Version: 20221025
Release: 1
Summary: Library to access the Parallels Hard Disk image (PHDI) format
Group: System Environment/Libraries
License: LGPLv3+
Source: %{name}-%{version}.tar.gz
URL: https://github.com/libyal/libphdi
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
               
BuildRequires: gcc               

%description -n libphdi
Library to access the Parallels Hard Disk image (PHDI) format

%package -n libphdi-static
Summary: Library to access the Parallels Hard Disk image (PHDI) format
Group: Development/Libraries
Requires: libphdi = %{version}-%{release}

%description -n libphdi-static
Static library version of libphdi.

%package -n libphdi-devel
Summary: Header files and libraries for developing applications for libphdi
Group: Development/Libraries
Requires: libphdi = %{version}-%{release}

%description -n libphdi-devel
Header files and libraries for developing applications for libphdi.

%package -n libphdi-python3
Summary: Python 3 bindings for libphdi
Group: System Environment/Libraries
Requires: libphdi = %{version}-%{release} python3
BuildRequires: python3-devel

%description -n libphdi-python3
Python 3 bindings for libphdi

%package -n libphdi-tools
Summary: Several tools for reading Parallels Hard Disk image (PHDI) files
Group: Applications/System
Requires: libphdi = %{version}-%{release} fuse-libs
BuildRequires: fuse-devel

%description -n libphdi-tools
Several tools for reading Parallels Hard Disk image (PHDI) files

%prep
%setup -q

%build
%configure --prefix=/usr --libdir=%{_libdir} --mandir=%{_mandir} --enable-python3
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -n libphdi
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.so.*

%files -n libphdi-static
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_libdir}/*.a

%files -n libphdi-devel
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/*.so
%{_libdir}/pkgconfig/libphdi.pc
%{_includedir}/*
%{_mandir}/man3/*

%files -n libphdi-python3
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%{_libdir}/python3*/site-packages/*.a
%{_libdir}/python3*/site-packages/*.so

%files -n libphdi-tools
%defattr(644,root,root,755)
%license COPYING COPYING.LESSER
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*

%changelog
* Tue Oct 25 2022 Joachim Metz <joachim.metz@gmail.com> 20221025-1
- Auto-generated

