%global _disable_ld_no_undefined 1

%define major		0
%define libname		%mklibname oath %{major}
%define develname	%mklibname oath -d
%define plibname	%mklibname pskc 0
%define pdevelname	%mklibname pskc -d

Name:		oath-toolkit
Version:	2.6.2
Release:	5
License:	GPLv3
Summary:	OATH Toolkit is a software toolkit for using HOTP/TOTP schemes
URL:		http://www.nongnu.org/oath-toolkit
Group:		System/Base
Source0:	http://download.savannah.nongnu.org/releases/oath-toolkit/oath-toolkit-%{version}.tar.gz
## Fedora patches:
# Escape leading single quotes in man pages which are misinterpreted as macros,
# patch sent upstream, upstream ticket #108312
Patch0:		oath-toolkit-2.0.2-man-fix.patch
# Fix invalid reads due to references to old (freed) xmlDoc,
# upstream ticket #108736
Patch1:		oath-toolkit-2.4.1-retain-original-xmldoc.patch
Patch2:		oath-2.6.2-compile.patch
# From upsteam:
Patch10:	0001-Update-gnulib-files.patch
# From upstream merge sequest:
# https://gitlab.com/oath-toolkit/oath-toolkit/merge_requests/9/
#Patch11:	0001-gnulib-fix-fseeko-with-glibc-2.28.patch
#Patch12:	oath-toolkit-2.6.2-gcc7.patch
Patch13:	oath-toolkit-2.6.2-glibc228.patch
BuildRequires:	bison
BuildRequires:	pam-devel
BuildRequires:	help2man
BuildRequires:	gengetopt
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(xmlsec1)
BuildRequires:	libxml2-utils

%description
The OATH Toolkit provides components for building one-time password
authentication systems. It contains shared libraries, command line tools and a
PAM module. Supported technologies include the event-based HOTP algorithm
(RFC4226) and the time-based TOTP algorithm (RFC6238). OATH stands for
Initiative for Open Authentication, an industry-wide collaboration to develop
open authentication algorithms.

For secret key management, the Portable Symmetric Key Container (PSKC) format
described in RFC6030 is supported.

The components included in the package are:

* liboath: A shared and static C library for OATH handling.
* oathtool: A command line tool for generating and validating OTPs.
* pam_oath: A PAM module for pluggable login authentication for OATH.
* libpskc: A shared and static C library for PSKC handling.
* pskctool: A command line tool for manipulating PSKC data.

%package -n	pam_oath
Summary:	A PAM module for HOTP/TOTP one-time password authentication
Group:		System/Libraries

%description -n	pam_oath
A PAM module for HOTP/TOTP one-time password authentication.

%package -n	%{libname}
Summary:	A library implementing HOTP/TOTP one-time password authentication schemes
Group:		System/Libraries
License:	LGPLv2

%description -n	%{libname}
A library implementing HOTP/TOTP one-time password authentication schemes.

%package -n	%{develname}
Summary:	Development files and documentation for liboath
Group:		System/Libraries
License:	LGPLv2
Requires:	%{libname} = %{EVRD}
Provides:	liboath-devel = %{EVRD}

%description -n	%{develname}
Development files and documentation for liboath.

%package -n	%{plibname}
Summary:	A library implementing HOTP/TOTP one-time password authentication schemes
Group:		System/Libraries
License:	LGPLv2

%description -n	%{plibname}
A library implementing HOTP/TOTP one-time password authentication schemes.

%package -n	%{pdevelname}
Summary:	Development files and documentation for liboath PSKC
Group:		System/Libraries
License:	LGPLv2
Requires:	%{plibname} = %{EVRD}

%description -n	%{pdevelname}
Development files and documentation for liboath PSKC.

%package -n	pskctool
Summary:	Tool for working with PSKC (Portable Symmetric Key Container) data
Group:		System/Tools
Requires:	%{plibname} = %{EVRD}

%description -n pskctool
Tool for working with PSKC (Portable Symmetric Key Container) data

%prep
%autosetup -p1

%build
%configure \
	    --with-pam-dir=/%{_lib}/security \
	    --disable-static \
	    --with-pic

# As of 2.6.2, SMP builds try to run help2man oathtool
# before building it
%make_build -j1

%install
%make_install

%check
# pskctool tst_libexamples.sh is known to fail in 2.6.2 on x86_64
%make_build check || :

%files
%doc ChangeLog README COPYING
%{_bindir}/oathtool
%{_mandir}/man1/oathtool.*.*

%files -n pam_oath
/%{_lib}/security/pam_oath.so

%files -n %{libname}
%{_libdir}/liboath.so.%{major}{,.*}

%files -n %{develname}
%{_libdir}/liboath.so
%dir %{_includedir}/liboath
%{_includedir}/liboath/oath.h
%{_libdir}/pkgconfig/liboath.pc
%dir %{_datadir}/gtk-doc/html/liboath
%doc %{_datadir}/gtk-doc/html/liboath/*
%{_mandir}/man3/oath_*.*

%files -n pskctool
%{_bindir}/pskctool
%{_datadir}/xml/pskc
%{_mandir}/man1/pskctool.1*

%files -n %{plibname}
%{_libdir}/libpskc.so.%{major}{,.*}

%files -n %{pdevelname}
%{_libdir}/libpskc.so
%{_mandir}/man3/pskc_*.*
%{_includedir}/pskc
%{_libdir}/pkgconfig/libpskc.pc
%doc %{_datadir}/gtk-doc/html/libpskc
