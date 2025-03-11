Summary:	LAL wrapping of the XML library
Summary(pl.UTF-8):	Obudowanie LAL do biblioteki XML
Name:		lal-xml
Version:	1.2.4
Release:	9
License:	GPL v2+
Group:		Libraries
Source0:	http://software.igwn.org/lscsoft/source/lalsuite/lalxml-%{version}.tar.xz
# Source0-md5:	8890f9630f59a5cc9e9c32df29f5da5c
Patch0:		%{name}-env.patch
Patch1:		%{name}-octave.patch
Patch2:		%{name}-libxml2.patch
URL:		https://wiki.ligo.org/Computing/LALSuite
BuildRequires:	autoconf >= 2.63
BuildRequires:	automake >= 1:1.11
BuildRequires:	gsl-devel >= 1.13
BuildRequires:	lal-devel >= 6.18.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-devel >= 1:2.6
BuildRequires:	octave-devel >= 1:3.2.0
BuildRequires:	pkgconfig
BuildRequires:	python3-devel
BuildRequires:	python3-numpy-devel
BuildRequires:	swig >= 4.1.0
BuildRequires:	swig-python >= 2.0.12
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	gsl >= 1.13
Requires:	lal >= 6.18.0
Requires:	libxml2 >= 1:2.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LAL wrapping of the XML library.

%description -l pl.UTF-8
Obudowanie LAL do biblioteki XML.

%package devel
Summary:	Header files for lal-xml library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki lal-xml
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gsl-devel >= 1.13
Requires:	lal-devel >= 6.18.0
Requires:	libxml2-devel >= 1:2.6

%description devel
Header files for lal-xml library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki lal-xml.

%package static
Summary:	Static lal-xml library
Summary(pl.UTF-8):	Statyczna biblioteka lal-xml
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static lal-xml library.

%description static -l pl.UTF-8
Statyczna biblioteka lal-xml.

%package -n octave-lalxml
Summary:	Octave interface for LAL XML
Summary(pl.UTF-8):	Interfejs Octave do biblioteki LAL XML
Group:		Applications/Math
Requires:	%{name} = %{version}-%{release}
Requires:	octave-lal >= 6.18.0

%description -n octave-lalxml
Octave interface for LAL XML.

%description -n octave-lalxml -l pl.UTF-8
Interfejs Octave do biblioteki LAL XML.

%package -n python3-lalxml
Summary:	Python bindings for LAL XML
Summary(pl.UTF-8):	Wiązania Pythona do biblioteki LAL XML
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}
Requires:	python3-lal >= 6.18.0
Requires:	python3-modules >= 1:2.6
Obsoletes:	python-lalxml < 1.2.4-4

%description -n python3-lalxml
Python bindings for LAL XML.

%description -n python3-lalxml -l pl.UTF-8
Wiązania Pythona do biblioteki LAL XML.

%prep
%setup -q -n lalxml-%{version}
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1

%build
%{__libtoolize}
%{__aclocal} -I gnuscripts
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	PYTHON=%{__python3} \
	--disable-dependency-tracking \
	--disable-silent-rules \
	--enable-swig
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/liblalxml.la

install -d $RPM_BUILD_ROOT/etc/shrc.d
%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/*sh $RPM_BUILD_ROOT/etc/shrc.d

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/lalxml_version
%attr(755,root,root) %{_libdir}/liblalxml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblalxml.so.2
%{_datadir}/lalxml
/etc/shrc.d/lalxml-user-env.csh
/etc/shrc.d/lalxml-user-env.fish
/etc/shrc.d/lalxml-user-env.sh

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblalxml.so
%{_includedir}/lal/LALXML*.h
%{_includedir}/lal/SWIGLALXML*.h
%{_includedir}/lal/SWIGLALXML*.i
%{_includedir}/lal/swiglalxml.i
%{_pkgconfigdir}/lalxml.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/liblalxml.a

%files -n octave-lalxml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/octave/*/site/oct/*/lalxml.oct

%files -n python3-lalxml
%defattr(644,root,root,755)
%dir %{py3_sitedir}/lalxml
%attr(755,root,root) %{py3_sitedir}/lalxml/_lalxml.so
%{py3_sitedir}/lalxml/*.py
%{py3_sitedir}/lalxml/__pycache__
