%global __remake_config 1

Name:           libfabric
Version:        1.17.0
Release:        3%{?dist}.1
Summary:        Open Fabric Interfaces

License:        BSD or GPLv2
URL:            https://github.com/ofiwg/libfabric
Source0:        https://github.com/ofiwg/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.bz2

%if %{__remake_config}
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
%endif
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libnl3-devel
# RDMA not available on 32-bit ARM: #1484155
%ifnarch %{arm}
BuildRequires:  libibverbs-devel
BuildRequires:  librdmacm-devel
%endif
%ifarch x86_64
%if 0%{?fedora} || 0%{?rhel} == 7
BuildRequires:  infinipath-psm-devel
%endif
%if 0%{?fedora} || 0%{?rhel} >= 7
BuildRequires:  libpsm2-devel
%endif
BuildRequires:  numactl-devel
%endif

%description
OpenFabrics Interfaces (OFI) is a framework focused on exporting fabric
communication services to applications.  OFI is best described as a collection
of libraries and applications used to export fabric services.  The key
components of OFI are: application interfaces, provider libraries, kernel
services, daemons, and test applications.

Libfabric is a core component of OFI.  It is the library that defines and
exports the user-space API of OFI, and is typically the only software that
applications deal with directly.  It works in conjunction with provider
libraries, which are often integrated directly into libfabric.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n %{name}-%{version}

%build
%if %{__remake_config}
./autogen.sh
%endif
%configure --disable-static --disable-silent-rules
%make_build


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'


%ldconfig_scriptlets


%files
%license COPYING
%{_bindir}/fi_info
%{_bindir}/fi_pingpong
%{_bindir}/fi_strerror
%{_libdir}/*.so.1*
%{_mandir}/man1/*.1*

%files devel
%license COPYING
%doc AUTHORS README
# We knowingly share this with kernel-headers and librdmacm-devel
# https://github.com/ofiwg/libfabric/issues/1277
%{_includedir}/rdma/
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/*.3*
%{_mandir}/man7/*.7*


%changelog
* Wed Feb 08 2023 Michal Schmidt <mschmidt@redhat.com> - 1.17.0-3.1
- Re-enable autotools remake to fix unwanted rpath in binaries.
- Resolves: rhbz#2168098

* Wed Feb 08 2023 Michal Schmidt <mschmidt@redhat.com> - 1.17.0-3
- Update to upstream release 1.17.0
- Resolves: rhbz#2168098

* Wed Aug 17 2022 Michal Schmidt <mschmidt@redhat.com> - 1.15.1-1
- Update to upstream release 1.15.1
- Disable LTO on x86_64 due to memory issues (copied from Fedora)
- Resolves: rhbz#2040450

* Thu Nov 25 2021 Honggang Li <honli@redhat.com> - 1.14.0-1
- Rebase to upstream release v1.14.0
- Resolves: bz1970601

* Thu May 13 2021 Honggang Li <honli@redhat.com> - 1.12.1-1
- Rebase to upstream release v1.12.1
- Enable psm3 support
- Resolves: bz1921238

* Tue Dec 22 2020 Honggang Li <honli@redhat.com> - 1.11.2-1
- Rebase to upstream release v1.11.2
- Fix "shm" segfault issue
- Resolves: bz1904291

* Tue Nov 17 2020 Honggang Li <honli@redhat.com> - 1.11.1-1
- Rebase to upstream release v1.11.1
- EFA Support requires libfabric
- Resolves: bz1831145, bz1852636

* Sat Apr 25 2020 Honggang Li <honli@redhat.com> - 1.10.0-1
- Rebase to upstream release v1.10.0
- Resolves: bz1739283

* Tue Nov 05 2019 Honggang Li <honli@redhat.com> - 1.9.0rc1-1
- Rebase to upstream release v1.9.0rc1
- Resolves: bz1719678

* Wed Aug 14 2019 Honggang Li <honli@redhat.com> - 1.8.0-2
- Fix segment fault issue for linux container
- Resolves: bz1731749

* Fri Jul 12 2019 Honggang Li <honli@redhat.com> - 1.8.0-1
- Rebase to upstream release v1.8.0
- Resolves: bz1660621

* Mon Dec 10 2018 Honggang Li <honli@redhat.com> - 1.6.2-1
- Rebase to upstream release v1.6.2
- Resolves: bz1654870

* Mon Oct  8 2018 Honggang Li <honli@redhat.com> - 1.6.1-3
- Revert a psm2 commit to avoid sporadic assertion failures
- Resolves: bz1627981

* Sun Jul  1 2018 Honggang Li <honli@redhat.com> - 1.6.1-2
- No longer support infinipath-psm

* Fri Jun 22 2018 Honggang Li <honli@redhat.com> - 1.6.1-1
- Rebase to latest upstream release 1.6.1
- Resolves: bz1550404

* Thu Mar 15 2018 Orion Poplawski <orion@nwra.com> - 1.6.0-1
- Update to 1.6.0

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 23 2017 Adam Williamson <awilliam@redhat.com> - 1.4.2-5
- Disable RDMA support on 32-bit ARM (#1484155)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 1.4.2-3
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 11 2017 Orion Poplawski <orion@cora.nwra.com> - 1.4.2-1
- Update to 1.4.2

* Mon Apr 10 2017 Orion Poplawski <orion@cora.nwra.com> - 1.4.1-1
- Update to 1.4.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 3 2016 Orion Poplawski <orion@cora.nwra.com> - 1.4.0-1
- Update to 1.4.0

* Thu Jul 21 2016 Orion Poplawski <orion@cora.nwra.com> - 1.3.0-3
- Rebuild for aarch64 glibc update

* Tue May 31 2016 Orion Poplawski <orion@cora.nwra.com> - 1.3.0-2
- Use psm/psm2 if possible on Fedora (bug #1340988)

* Tue Apr 12 2016 Orion Poplawski <orion@cora.nwra.com> - 1.3.0-1
- Update to 1.3.0

* Wed Mar 9 2016 Orion Poplawski <orion@cora.nwra.com> - 1.2.0-1
- Update to 1.2.0
- Use psm/psm2 if possible on EL
- Add upstream patch to fix non-x86 builds

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 26 2015 Orion Poplawski <orion@cora.nwra.com> - 1.1.0-1
- Update to 1.1.0

* Mon Jul 20 2015 Orion Poplawski <orion@cora.nwra.com> - 1.0.0-1
- Initial package
