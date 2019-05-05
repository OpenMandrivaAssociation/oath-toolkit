%define major		0
%define libname		%mklibname oath %{major}
%define develname	%mklibname oath -d

Name:		oath-toolkit
Version:	2.6.2
Release:	%mkrel 4
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
BuildRequires:	pkgconfig(libxml-2.0)

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
Requires:	%{libname} = %{version}
Provides:	liboath-devel = %{version}-%{release}

%description -n	%{develname}
Development files and documentation for liboath.

%prep
%autosetup -p1

%build
export CC=gcc
export CXX=g++
#autoreconf -fi
# For now, disable PSKC, since it requires XMLSEC which we don't ship yet.
%configure \
	    --with-pam-dir=/%{_lib}/security \
	    --disable-static \
	    --disable-pskc \
	    --with-pic

%make_build -j1

%install
%make_install

# we don't want these
find %{buildroot} -name "*.la" -delete

%check
make check

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
%{_mandir}/man3/oath_*.*.*


%changelog
* Mon Sep 24 2018 wally <wally> 2.6.2-4.mga7
  (not released yet)
+ Revision: 1303575
- add patches from upstream to fix build with glibc >= 2.28
- sync patches with Fedora
- provide liboath-devel with devel pkg
+ umeabot <umeabot>
- Mageia 7 Mass Rebuild

* Sun Oct 08 2017 cjw <cjw> 2.6.2-2.mga7
+ Revision: 1170277
- add buildrequires: pkgconfig(libxml-2.0)
- patch1: fix build with gcc 7

* Mon Aug 14 2017 daviddavid <daviddavid> 2.6.2-1.mga7
+ Revision: 1140356
- new version: 2.6.2

* Thu Jan 07 2016 danf <danf> 2.6.1-1.mga6
+ Revision: 920230
- New version 2.6.1
- Removed strdup-null-check.patch (merged upstream)

* Tue Nov 18 2014 luigiwalser <luigiwalser> 2.4.1-4.mga5
+ Revision: 797753
- add patch from fedora to check for strdup failure (rhbz#1161360)

* Wed Oct 15 2014 umeabot <umeabot> 2.4.1-3.mga5
+ Revision: 739132
- Second Mageia 5 Mass Rebuild

* Tue Sep 16 2014 umeabot <umeabot> 2.4.1-2.mga5
+ Revision: 682959
- Mageia 5 Mass Rebuild

* Mon Feb 24 2014 luigiwalser <luigiwalser> 2.4.1-1.mga5
+ Revision: 596647
- 2.4.1 (fixes CVE-2013-7322)

* Tue Oct 22 2013 umeabot <umeabot> 2.4.0-2.mga4
+ Revision: 541358
- Mageia 4 Mass Rebuild

* Sat Oct 12 2013 mitya <mitya> 2.4.0-1.mga4
+ Revision: 495654
- New version 2.4.0

* Sat Jan 12 2013 umeabot <umeabot> 1.12.6-2.mga3
+ Revision: 361091
- Mass Rebuild - https://wiki.mageia.org/en/Feature:Mageia3MassRebuild

* Sun Sep 16 2012 mitya <mitya> 1.12.6-1.mga3
+ Revision: 294619
- New version 1.12.6

* Thu May 05 2011 mitya <mitya> 1.8.2-1.mga1
+ Revision: 94979
- imported package oath-toolkit

