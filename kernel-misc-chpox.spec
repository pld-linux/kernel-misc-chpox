# bcond
# _without_dist_kernel          without distribution kernel

%define		_orig_name	chpox
%define		_rel		0.1

Summary:	Kernel modules for transparent dumping of specified processes
Summary(pl):	Modu³y j±dra pozwalaj±ce na zrzucanie procesów do pliku
Name:		kernel-misc-%{_orig_name}
Version:	0.3
Release:	%{_rel}@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://www.cluster.kiev.ua/support/files/%{_orig_name}-%{version}-1a.tar.gz
%{!?_without_dist_kernel:BuildRequires:         kernel-headers}
BuildRequires:	%{kgcc_package}
Prereq:		/sbin/depmod
%{!?_without_dist_kernel:%requires_releq_kernel_up}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
%{_orig_name} is a set of the Linux kernel modules for transparent
dumping of specified processes into disk file and restarting ones.

%description -l pl
%{_orig_name} to zestaw modu³ów j±dra pozwalaj±cy na transparentne
"zrzucanie" okre¶lonych procesów do pliku, oraz ich restart.

%package -n kernel-smp-misc-%{_orig_name}
Summary:	Kernel modules for transparent dumping of specified processes
Summary(pl):	Modu³y j±dra pozwalaj±ce na zrzucanie procesów do pliku
Release:	%{_rel}@%{_kernel_ver_str}
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
Group:		Base/Kernel
Prereq:		/sbin/depmod

%description -n kernel-smp-misc-%{_orig_name}
%{_orig_name} is a set of the Linux kernel modules for transparent
dumping of specified processes into disk file and restarting ones.

%description -n kernel-smp-misc-%{_orig_name} -l pl
%{_orig_name} to zestaw modu³ów j±dra pozwalaj±cy na transparentne
"zrzucanie" okre¶lonych procesów do pliku, oraz ich restart.

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
/sbin/depmod -a

%postun
/sbin/depmod -a

%post -n kernel-smp-misc-%{_orig_name}
/sbin/depmod -a

%postun -n kernel-smp-misc-%{_orig_name}
/sbin/depmod -a

%files
%defattr(644,root,root,755)
%doc README Changes vmad.sgml
/lib/modules/%{_kernel_ver}/misc/*

%files -n kernel-smp-misc-%{_orig_name}
%doc README Changes vmad.sgml
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/*
