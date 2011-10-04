#specfile originally created for Fedora, modified for Moblin Linux
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           lcms
Version:        1.18
Release:        
Summary:        Color Management System

Group:          Applications/Productivity
License:        MIT
URL:            http://www.littlecms.com/downloads.htm
Source0:        http://www.littlecms.com/lcms-%{version}.tar.gz
Patch1:		lcms-CVE-2009-0793.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libjpeg-devel
BuildRequires:  libtiff-devel
BuildRequires:  pkgconfig
BuildRequires:  python-devel
BuildRequires:  swig >= 1.3.12
BuildRequires:  zlib-devel
BuildRequires:  automake, autoconf, libtool

Provides:       littlecms = %{version}-%{release}

%description
LittleCMS intends to be a small-footprint, speed optimized color management
engine in open source form.

%package        libs
Summary:        Library for %{name}
Group:          System/Libraries
Requires:       %{name} = %{version}-%{release}
# Introduced in F-9 to solve multilib transition
Obsoletes:      lcms < 1.17-3

%description    libs
The %{name}-libs package contains library for %{name}.

%package     -n python-%{name}
Summary:        Python interface to LittleCMS
Group:          Development/Libraries
Requires:       python
Provides:       python-littlecms = %{version}-%{release}

%description -n python-%{name}
Python interface to LittleCMS.


%package        devel
Summary:        Development files for LittleCMS
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       pkgconfig
Provides:       littlecms-devel = %{version}-%{release}

%description    devel
Development files for LittleCMS.


%prep
%setup -q
%patch1 -p1 -b .CVE-2009-0793

find . -name \*.[ch] | xargs chmod -x

# Convert not UTF-8 files
pushd doc
mkdir -p __temp
for f in LCMSAPI.TXT TUTORIAL.TXT ;do
cp -p $f __temp/$f
iconv -f ISO-8859-1 -t UTF-8 __temp/$f > $f
touch -r __temp/$f $f
done
rm -rf __temp
popd


%build
libtoolize --copy --force
autoreconf
%configure --with-python --disable-static
(cd python; ./swig_lcms)
make %{?_smp_mflags}


%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
chmod 0644 AUTHORS COPYING ChangeLog NEWS README.1ST doc/TUTORIAL.TXT doc/LCMSAPI.TXT
find ${RPM_BUILD_ROOT} -type f -name "*.la" -exec rm -f {} ';'


%clean
rm -rf ${RPM_BUILD_ROOT}


%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc README.1ST doc/TUTORIAL.TXT
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc doc/LCMSAPI.TXT
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%files -n python-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/lcms.py*
%{python_sitearch}/_lcms.so


