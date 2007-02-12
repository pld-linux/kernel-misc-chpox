#
# Conditional build:
# _without_dist_kernel		- without distribution kernel
#
%define		_orig_name	chpox
%define		_rel		0.1

Summary:	Kernel modules for transparent dumping of specified processes
Summary(pl.UTF-8):   Moduły jądra pozwalające na zrzucanie procesów do pliku
Name:		kernel-misc-%{_orig_name}
Version:	0.3
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://www.cluster.kiev.ua/support/files/%{_orig_name}-%{version}-1a.tar.gz
# Source0-md5:	06db5787b13f59aa9f1c8d45fe7cfd81
%{!?_without_dist_kernel:BuildRequires:	kernel-headers}
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):		/sbin/depmod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
%{_orig_name} is a set of the Linux kernel modules for transparent
dumping of specified processes into disk file and restarting ones.

%description -l pl.UTF-8
%{_orig_name} to zestaw modułów jądra pozwalający na transparentne
"zrzucanie" określonych procesów do pliku, oraz ich restart.

%package -n kernel-smp-misc-%{_orig_name}
Summary:	Kernel SMP modules for transparent dumping of specified processes
Summary(pl.UTF-8):   Moduły jądra SMP pozwalające na zrzucanie procesów do pliku
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):		/sbin/depmod

%description -n kernel-smp-misc-%{_orig_name}
%{_orig_name} is a set of the Linux SMP kernel modules for transparent
dumping of specified processes into disk file and restarting ones.

%description -n kernel-smp-misc-%{_orig_name} -l pl.UTF-8
%{_orig_name} to zestaw modułów jądra SMP pozwalający na transparentne
"zrzucanie" określonych procesów do pliku, oraz ich restart.

%prep
%setup -q -n %{_orig_name}-%{version}-1a

%build
./configure

%{__make} CC="%{kgcc} -D__SMP__"

mv -f %{_orig_name}.o %{_orig_name}.smp.o
mv -f vmadump.o vmadump.smp.o

%{__make} CC="%{kgcc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc
cp %{_orig_name}.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
cp vmadump.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc
cp %{_orig_name}.smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/%{_orig_name}.o
cp vmadump.smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/vmadump.o

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-misc-%{_orig_name}
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-misc-%{_orig_name}
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
%doc README Changes vmad.sgml
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-misc-%{_orig_name}
%defattr(644,root,root,755)
%doc README Changes vmad.sgml
/lib/modules/%{_kernel_ver}smp/misc/*
