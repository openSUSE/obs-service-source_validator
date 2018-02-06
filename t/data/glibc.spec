#
# spec file for package glibc
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


# Run with osc --with=fast_build to have a shorter turnaround
# It will avoid building some parts of glibc
%bcond_with    fast_build

%define crypt_bf_version 1.3
%define build_snapshot 0
%bcond_with ringdisabled

%define flavor @BUILD_FLAVOR@%{nil}

%bcond_with all
%define build_main 1
%define build_utils %{with all}
%define build_testsuite %{with all}
%if "%flavor" == "utils"
%if %{with ringdisabled}
ExclusiveArch:  do_not_build
%endif
%define build_main 0
%define build_utils 1
%define build_testsuite 0
%endif
%if "%flavor" == "testsuite"
%if %{with ringdisabled}
ExclusiveArch:  do_not_build
%endif
%define build_main 0
%define build_utils 0
%define build_testsuite 1
%endif

%if %{build_main}
Name:           glibc
%else
Name:           glibc-INTERNAL
%endif
Summary:        Standard Shared Libraries (from the GNU C Library)
License:        LGPL-2.1+ AND SUSE-LGPL-2.1+-with-GCC-exception AND GPL-2.0+
Group:          System/Libraries
BuildRequires:  audit-devel
BuildRequires:  fdupes
BuildRequires:  libcap-devel
BuildRequires:  libselinux-devel
BuildRequires:  makeinfo
BuildRequires:  pwdutils
BuildRequires:  systemd-rpm-macros
BuildRequires:  xz
%if %{build_testsuite}
BuildRequires:  gcc-c++
BuildRequires:  gdb
BuildRequires:  glibc-devel-static
BuildRequires:  libstdc++-devel
BuildRequires:  python-pexpect
%endif
%if %{build_utils}
BuildRequires:  gd-devel
%endif
%if "%flavor" == "i686"
ExclusiveArch:  i586 i686
BuildArch:      i686
%global optflags %(echo "%optflags"|sed -e s/i586/i686/) -march=i686 -mtune=generic
%endif

%define __filter_GLIBC_PRIVATE 1
%ifarch i686
# For i686 let's only build what's different from i586, so
# no need to build documentation
%define build_profile 1
%define build_locales 1
%define build_html 0
%else
%if %{with fast_build} || %{build_utils} && %{without all}
%define build_profile 0
%define build_locales 0
%define build_html 0
%else
# Default:
%define build_profile 1
%define build_locales 1
%define build_html 1
%endif
%endif

%define build_variants %{build_main}

%define disable_assert 0
%define enable_stackguard_randomization 1
%ifarch ppc ppc64
 %define optimize_power 1
 %ifarch ppc
 %define powerpc_optimize_base %{nil}
 %define powerpc_optimize_tune power3
 %define powerpc_optimize_cpu_power4 1
 %else
 %define powerpc_optimize_base %{nil}
 %define powerpc_optimize_tune power5
 %define powerpc_optimize_cpu_power4 0
 %endif
 # We are not building Power CPU specific optimizations for openSUSE.
 %define powerpc_optimize_cpu_power6 0
 %define powerpc_optimize_cpu_power7 0
 %define powerpc_optimize_cpu_cell 0
%else
 %define optimize_power 0
 %define powerpc_optimize_base %{nil}
 %define powerpc_optimize_cpu_power4 0
 %define powerpc_optimize_cpu_power6 0
 %define powerpc_optimize_cpu_power7 0
 %define powerpc_optimize_cpu_cell 0
%endif # ppc, ppc64
# glibc requires at least kernel 3.2
%define enablekernel 3.2
# some architectures need a newer kernel
%ifarch ppc64le
%define enablekernel 3.10
%endif
%ifarch aarch64
%define enablekernel 3.7
%endif
%ifarch ia64
%define enablekernel 3.2.18
%endif

Version:        2.26
Release:        0
%if !%{build_snapshot}
%define git_id 1c9a5c270d8b
%define libversion %version
%else
%define git_id %(echo %version | sed 's/.*\.g//')
%define libversion %(echo %version | sed 's/\.[^.]*\.g.*//')
%endif
Url:            http://www.gnu.org/software/libc/libc.html
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%if !%{build_snapshot}
Source:         http://ftp.gnu.org/pub/gnu/glibc/glibc-%{version}.tar.xz
Source1:        http://ftp.gnu.org/pub/gnu/glibc/glibc-%{version}.tar.xz.sig
%else
Source:         glibc-%{version}.tar.xz
%endif
Source2:        http://savannah.gnu.org/project/memberlist-gpgkeys.php?group=libc&download=1#/glibc.keyring
Source4:        manpages.tar.bz2
Source5:        nsswitch.conf
Source7:        bindresvport.blacklist
Source8:        glibc_post_upgrade.c
Source9:        glibc.rpmlintrc
Source10:       baselibs.conf
# For systemd 
Source20:       nscd.conf
Source21:       nscd.service
# crypt_blowfish
Source50:       http://www.openwall.com/crypt/crypt_blowfish-%{crypt_bf_version}.tar.gz
# The sign key uses MD5 which is no longer accepted by gpg
#Source51:       http://www.openwall.com/crypt/crypt_blowfish-%{crypt_bf_version}.tar.gz.sign

%if %{build_main}
# ngpt was used in 8.1 and SLES8
Obsoletes:      ngpt < 2.2.2
Obsoletes:      ngpt-devel < 2.2.2
Provides:       ngpt = 2.2.2
Provides:       ngpt-devel = 2.2.2
Conflicts:      kernel < %{enablekernel}
# bug437293 - handle update from SLES10 on PowerPC
%ifarch ppc64
Obsoletes:      glibc-64bit
%endif
%ifarch ppc
Obsoletes:      glibc-32bit
%endif
%ifarch armv6hl armv7hl
# The old runtime linker link gets not provided by rpm find.provides, but it exists
Provides:       ld-linux.so.3
Provides:       ld-linux.so.3(GLIBC_2.4)
%endif
Requires(pre):  filesystem
Recommends:     glibc-extra
Provides:       rtld(GNU_HASH)
%endif
%if %{build_utils}
Requires:       glibc = %{version}
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%ifarch i686
# We need to avoid to have only the src rpm from i686 on the media,
# since it does not work on other architectures.
NoSource:       0
%endif
#

###
# Patches are ordered in the following groups:
# Patches that we will never upstream or which have not been looked at: 0-999
# Patches taken from upstream: 1000-2000
# Patches that are going upstream, waiting approval: 2000-3000
###

###
# Patches that upstream will not accept
###

###
# openSUSE specific patches - won't go upstream
###
### openSUSE extensions, configuration
# PATCH-FEATURE-OPENSUSE -- add crypt_blowfish support - bnc#700876
Patch1:         glibc-2.14-crypt.diff
# PATCH-FEATURE-OPENSUSE constify crypt_blowfish
Patch2:         crypt_blowfish-const.patch
# PATCH-FEATURE-OPENSUSE -- add sha support to crypt_blowfish lnussel@suse.de
Patch3:         crypt_blowfish-1.2-sha.diff
# PATCH-FEATURE-OPENSUSE Move crypt_gensalt_rn to separate library
Patch4:         crypt_blowfish-gensalt.patch
# PATCH-FEATURE-OPENSUSE Avoid build failure on noexecstack marker on ARM dmueller@suse.de
Patch5:         crypt_blowfish-1.2-hack_around_arm.diff
# PATCH-FIX-OPENSUSE Fix path for nscd databases
Patch6:         glibc-2.3.3-nscd-db-path.diff
# PATCH-FIX-OPENSUSE Fix path for nss_db (bnc#753657) - aj@suse.de
Patch7:         nss-db-path.patch
# PATCH-FIX-OPENSUSE adjust nscd.conf
Patch8:         glibc-nscd.conf.patch
# PATCH-FIX-OPENSUSE do not use compile time in binaries
Patch9:         glibc-nodate.patch
# PATCH-FIX-OPENSUSE -- add some extra information to version output - kukuk@suse.de
Patch10:        glibc-version.diff
# PATCH-FIX-OPENSUSE -- Make --no-archive default for localedef - kukuk@suse.de
Patch13:        glibc-2.3.2.no_archive.diff
# PATCH-FIX-OPENSUSE -- add blacklist for bindresvport
Patch14:        glibc-bindresvport-blacklist.diff
# PATCH-FIX-OPENSUSE prefer -lang rpm packages
Patch15:        glibc-2.3.90-langpackdir.diff
# PATCH-FEATURE-SLE Use nscd user for nscd
Patch19:        nscd-server-user.patch
# PATCH-FEATURE-SLE powerpc: enable TLE only if GLIBC_ELISION_ENABLE=yes is defined
Patch21:        powerpc-elision-enable-envvar.patch
# PATCH-FEATURE-SLE s390: enable TLE only if GLIBC_ELISION_ENABLE=yes is defined
Patch22:        s390-elision-enable-envvar.patch

### Locale related patches
# PATCH-FIX-OPENSUSE Add additional locales
Patch100:       add-locales.patch
# PATCH-FIX-OPENSUSE -- Add no_NO back (XXX: Still needed?)
Patch102:       glibc-2.4.90-no_NO.diff
# PATCH-FIX-OPENSUSE -- Renames for China
Patch103:       glibc-2.4-china.diff
# PATCH-FIX-OPENSUSE -- Add C.UTF-8 locale
Patch104:       glibc-c-utf8-locale.patch
# PATCH-FIX-OPENSUSE -- Disable gettext for C.UTF-8 locale
Patch105:       glibc-disable-gettext-for-c-utf8.patch

### Broken patches in glibc that we revert for now:

### Network related patches
# PATCH-FIX-OPENSUSE Warn about usage of mdns in resolv.conv
Patch304:       glibc-resolv-mdnshint.diff
# PATCH-FIX-OPENSUSE disable rewriting ::1 to 127.0.0.1 for /etc/hosts bnc#684534, bnc#706719
Patch306:       glibc-fix-double-loopback.diff

###
# Patches from upstream
###
# PATCH-FIX-UPSTREAM Fix leaks of resolver contexts (BZ #21885, BZ #21932)
Patch1000:      resolv-context-leak.patch
# PATCH-FIX-UPSTREAM Use _dl_runtime_resolve_opt only with AVX512F (BZ #21871)
Patch1001:      dl-runtime-resolve-opt-avx512f.patch
# PATCH-FIX-UPSTREAM Don't use IFUNC resolver for longjmp or system in libpthread (BZ #21041)
Patch1002:      libpthread-compat-wrappers.patch
# PATCH-FIX-UPSTREAM Do not use __builtin_types_compatible_p in C++ mode (BZ #21930, BZ #22146, BZ #22235, BZ #22296)
Patch1003:      math-c++-compat.patch
# PATCH-FIX-UPSTREAM Remove nis and compat from default NSS configs
Patch1004:      remove-nss-nis-compat.patch
# PATCH-FIX-UPSTREAM Properly terminate .eh_frame (BZ #22051)
Patch1005:      eh-frame-zero-terminator.patch
# PATCH-FIX-UPSTREAM x86: Add x86_64 to x86-64 HWCAP (BZ #22093)
Patch1006:      ld-so-hwcap-x86-64.patch
# PATCH-FIX-UPSTREAM assert: Suppress pedantic warning caused by statement expression (BZ #21242, BZ #21972)
Patch1007:      assert-pedantic.patch
# PATCH-FIX-UPSTREAM Fix errno and h_errno handling in getaddrinfo (BZ #21915, BZ #21922)
Patch1008:      getaddrinfo-errno.patch
# PATCH-FIX-UPSTREAM Fix memory handling in OOM situation during resolv.conf parsing (BZ #22095, BZ #22096)
Patch1009:      resolv-conf-oom.patch
# PATCH-FIX-UPSTREAM Fix initial size of dynarray allocation and set errno on overflow error
Patch1010:      dynarray-allocation.patch
# PATCH-FIX-UPSTREAM Avoid spurious inexact in nearbyint (BZ #22225)
Patch1011:      nearbyint-inexact.patch
# PATCH-FIX-UPSTREAM Move nss_compat from nis to nss subdir and install it unconditionally
Patch1012:      nss-compat.patch
# PATCH-FIX-UPSTREAM Remove reference to libnsl from nscd
Patch1013:      nscd-libnsl.patch
# PATCH-FIX-UPSTREAM malloc: Fix tcache leak after thread destruction (BZ #22111)
Patch1014:      malloc-tcache-leak.patch
# PATCH-FIX-UPSTREAM aarch64: Optimized implementation of memcpy/memmove for Qualcomm Falkor
Patch1015:      falkor-memcpy-memmove.patch
# PATCH-FIX-UPSTREAM aarch64: Fix glibc.tune.cpu tunable handling
Patch1016:      aarch64-cpu-features.patch
# PATCH-FIX-UPSTREAM nss_files: Avoid large buffers with many host addresses (BZ #22078)
Patch1017:      nss-files-large-buffers.patch
# PATCH-FIX-UPSTREAM sysconf: Fix missing definition of UIO_MAXIOV on Linux (BZ #22321)
Patch1018:      sysconf-uio-maxiov.patch
# PATCH-FIX-UPSTREAM glob: Fix buffer overflows (CVE-2017-15670, CVE-2017-15671, CVE-2017-15804, BZ #22320, BZ #22325, BZ #22332)
Patch1019:      glob-tilde-overflow.patch
# PATCH-FIX-UPSTREAM x86-64: Use fxsave/xsave/xsavec in _dl_runtime_resolve (BZ #21265)
Patch1020:      dl-runtime-resolve-xsave.patch
# PATCH-FIX-UPSTREAM posix: Fix improper assert in Linux posix_spawn (BZ #22273)
Patch1021:      spawni-assert.patch
# PATCH-FIX-UPSTREAM x86-64: Don't set GLRO(dl_platform) to NULL (BZ #22299)
Patch1022:      x86-64-dl-platform.patch
# PATCH-FIX-UPSTREAM no compat glob64 on s390
Patch1023:      glob64-s390.patch
# PATCH-FIX-UPSTREAM tst-tlsopt-powerpc as a shared lib
Patch1024:      tst-tlsopt-powerpc.patch
# PATCH-FIX-UPSTREAM Update HWCAP for powerpc
Patch1025:      powerpc-hwcap-bits.patch
# PATCH-FIX-UPSTREAM Fix integer overflow in malloc when tcache is enabled (CVE-2017-17426, BZ #22375)
Patch1026:      malloc-tcache-check-overflow.patch
# PATCH-FIX-UPSTREAM Count components of the expanded path in _dl_init_path (CVE-2017-1000408, CVE-2017-1000409, bsc#1071319, BZ #22607, BZ #22627)
Patch1027:      dl-init-paths-overflow.patch
# PATCH-FIX-UPSTREAM Check for empty tokens before dynamic string token expansion (CVE-2017-16997, bsc#1073231, BZ #22625)
Patch1028:      fillin-rpath-empty-tokens.patch
# PATCH-FIX-UPSTREAM make getcwd(3) fail if it cannot obtain an absolute path (CVE-2018-1000001, BZ #22679)
Patch1029:      getcwd-absolute.patch

### 
# Patches awaiting upstream approval
###
# PATCH-FIX-UPSTREAM Always to locking when accessing streams (BZ #15142)
Patch2000:      fix-locking-in-_IO_cleanup.patch
# PATCH-FIX-UPSTREAM Never try to execute the file in ldd (BZ #16750)
Patch2001:      ldd-system-interp.patch
# PATCH-FIX-UPSTREAM Don't close or flush stdio streams on abort (BZ #15436)
Patch2002:      abort-no-flush.patch
# PATCH-FIX-UPSTREAM Fix fnmatch handling of collating elements (BZ #17396, BZ #16976)
Patch2004:      fnmatch-collating-elements.patch
# PATCH-FIX-UPSTREAM Properly reread entry after failure in nss_files getent function (BZ #18991)
Patch2005:      nss-files-long-lines-2.patch
# PATCH-FIX-UPSTREAM Fix iconv buffer handling with IGNORE error handler (BZ #18830)
Patch2006:      iconv-reset-input-buffer.patch

# Non-glibc patches
# PATCH-FIX-OPENSUSE Remove debianisms from manpages
Patch3000:      manpages.patch

%description
The GNU C Library provides the most important standard libraries used
by nearly all programs: the standard C library, the standard math
library, and the POSIX thread library. A system is not functional
without these libraries.

%package -n glibc-utils
Summary:        Development utilities from the GNU C Library
License:        LGPL-2.1+
Group:          Development/Languages/C and C++
Requires:       glibc = %{version}

%description -n glibc-utils
The glibc-utils package contains mtrace, a memory leak tracer and
xtrace, a function call tracer which can be helpful during program
debugging.

If you are unsure if you need this, do not install this package.

%package -n glibc-testsuite
Summary:        Testsuite results from the GNU C Library
License:        LGPL-2.1+
Group:          Development/Languages/C and C++

%description -n glibc-testsuite
This package contains the testsuite results from the GNU C Library.

%if %{build_main}
%package info
Summary:        Info Files for the GNU C Library
License:        GFDL-1.1
Group:          Documentation/Other
Requires(post): %{install_info_prereq}
Requires(preun): %{install_info_prereq}
BuildArch:      noarch

%description info
This package contains the documentation for the GNU C library stored as
info files. Due to a lack of resources, this documentation is not
complete and is partially out of date.

%package html
Summary:        HTML Documentation for the GNU C Library
License:        GFDL-1.1
Group:          Documentation/HTML
BuildArch:      noarch

%description html
This package contains the HTML documentation for the GNU C library. Due
to a lack of resources, this documentation is not complete and is
partially out of date.

%package i18ndata
Summary:        Database Sources for 'locale'
License:        GPL-2.0+ AND MIT
Group:          System/Libraries
BuildArch:      noarch

%description i18ndata
This package contains the data needed to build the locale data files to
use the internationalization features of the GNU libc. It is normally
not necessary to install this packages, the data files are already
created.

%package locale
Summary:        Locale Data for Localized Programs
License:        GPL-2.0+ AND MIT AND LGPL-2.1+
Group:          System/Libraries
Requires(post): /bin/cat
Requires:       glibc = %{version}
# bug437293
%ifarch ppc64
Obsoletes:      glibc-locale-64bit
%endif
%ifarch ppc
Obsoletes:      glibc-locale-32bit
%endif

%description locale
Locale data for the internationalisation features of the GNU C library.

%package -n nscd
Summary:        Name Service Caching Daemon
License:        GPL-2.0+
Group:          System/Daemons
Provides:       glibc:/usr/sbin/nscd
Requires:       glibc = %{version}
Obsoletes:      unscd <= 0.48
Requires(pre):  pwdutils
%{?systemd_requires}

%description -n nscd
Nscd caches name service lookups and can dramatically improve
performance with NIS, NIS+, and LDAP.

%package profile
Summary:        Libc Profiling and Debugging Versions
License:        LGPL-2.1+ AND SUSE-LGPL-2.1+-with-GCC-exception AND GPL-2.0+
Group:          Development/Libraries/C and C++
Requires:       glibc = %{version}
# bug437293
%ifarch ppc64
Obsoletes:      glibc-profile-64bit
%endif
%ifarch ppc
Obsoletes:      glibc-profile-32bit
%endif

%description profile
This package contains special versions of the GNU C library which are
necessary for profiling and debugging.

%package devel
Summary:        Include Files and Libraries Mandatory for Development
License:        BSD-3-Clause AND LGPL-2.1+ AND SUSE-LGPL-2.1+-with-GCC-exception AND GPL-2.0+
Group:          Development/Libraries/C and C++
Obsoletes:      epoll = 1.0
Provides:       epoll < 1.0
# bug437293
%ifarch ppc64
Obsoletes:      glibc-devel-64bit
%endif
%ifarch ppc
Obsoletes:      glibc-devel-32bit
%endif
Requires:       glibc = %{version}
Requires:       linux-kernel-headers

%description devel
These libraries are needed to develop programs which use the standard C
library.

%package devel-static
Summary:        C library static libraries for -static linking
License:        BSD-3-Clause AND LGPL-2.1+ AND SUSE-LGPL-2.1+-with-GCC-exception AND GPL-2.0+
Group:          Development/Libraries/C and C++
Requires:       %{name}-devel = %{version}
# Provide Fedora name for package to make packaging easier
Provides:       %{name}-static = %{version}

%description devel-static
The glibc-devel-static package contains the C library static libraries
for -static linking.  You don't need these, unless you link statically,
which is highly discouraged.

# makedb requires libselinux. We add this program in a separate
# package so that glibc does not require libselinux.
%package extra
Summary:        Extra binaries from GNU C Library
License:        LGPL-2.1+
Group:          Development/Libraries/C and C++
Requires:       glibc = %{version}

%description extra
The glibc-extra package contains some extra binaries for glibc that
are not essential but recommend to use.

makedb: A program to create a database for nss
%endif # main

%prep
%setup -n glibc-%{version} -q -a 4
# Owl crypt_blowfish
tar -xzf %SOURCE50
pushd crypt_blowfish-%{crypt_bf_version}
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5
popd
mv crypt/{crypt.h,gnu-crypt.h}
mv crypt_blowfish-%crypt_bf_version/*.[chS] crypt/
#
%patch1 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
# avoid changing nscd_stat.c mtime to avoid code generation
# differences on each rebuild
touch -r nscd/nscd_stat.c nscd/s-stamp
%patch9 -p1
touch -r nscd/s-stamp nscd/nscd_stat.c
rm nscd/s-stamp
%patch10 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch19 -p1
%patch21 -p1
%patch22 -p1

%patch100 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1

%patch304 -p1
%patch306 -p1

%patch1000 -p1
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1
%patch1007 -p1
%patch1008 -p1
%patch1009 -p1
%patch1010 -p1
%patch1011 -p1
%patch1012 -p1
%patch1013 -p1
%patch1014 -p1
%patch1015 -p1
%patch1016 -p1
%patch1017 -p1
%patch1018 -p1
%patch1019 -p1
%patch1020 -p1
%patch1021 -p1
%patch1022 -p1
%patch1023 -p1
%patch1024 -p1
%patch1025 -p1
%patch1026 -p1
%patch1027 -p1
%patch1028 -p1
%patch1029 -p1

%patch2000 -p1
%patch2001 -p1
%patch2002 -p1
%patch2004 -p1
%patch2005 -p1
%patch2006 -p1

%patch3000

#
# Inconsistency detected by ld.so: dl-close.c: 719: _dl_close: Assertion `map->l_init_called' failed!
#
# Glibc 2.8 introduced the HP_TIMING element to the rtld_global_ro struct # definition.
# If the base is built without power4 the loader won't have this element in
# the struct whereas the power4/5/6/... libc will, so there will be a disconnect
# between the size of the rtld_global_ro struct between the two and dl_close
# ends up getting called incorrectly when it's actually attempting to call a
# resolver function.  This is because the GLRO() macro simply attempts to
# compute an offset and gets the wrong one.
# Building the base glibc with --with-cpu=power4 solves this problem.
# But: ppc32 can not default to -mcpu=power4 because it would emit instructions
# which are not available on G3, G4 etc.
#
# We simply remove the power4 files, and build the base glibc for a generic powerpc cpu
# Additional cputuned libs can now be used on powerpc32
#
rm -fv sysdeps/powerpc/powerpc32/power4/hp-timing.c sysdeps/powerpc/powerpc32/power4/hp-timing.h
find . -name configure | xargs touch

%build
if [ -x /bin/uname.bin ]; then
	/bin/uname.bin -a
else
	uname -a
fi
uptime || :
ulimit -a
nice
# We do not want configure to figure out the system its building one
# to support a common ground and thus set build and host to the
# target_cpu.
%ifarch %arm
%define target %{_target_cpu}-suse-linux-gnueabi
%else
%define target %{_target_cpu}-suse-linux
%endif
# Don't use as-needed, it breaks glibc assumptions
# Before enabling it, run the testsuite and verify that it
# passes completely
export SUSE_ASNEEDED=0
# Adjust glibc version.h
echo "#define CONFHOST \"%{target}\"" >> version.h
echo "#define GITID \"%{git_id}\"" >> version.h
#
# Default CFLAGS and Compiler
#
BuildFlags="%{optflags} -U_FORTIFY_SOURCE"
enable_stack_protector=
for opt in $BuildFlags; do
  case $opt in
    -fstack-protector-strong) enable_stack_protector=strong ;;
    -fstack-protector-all) enable_stack_protector=all ;;
    -fstack-protector) enable_stack_protector=yes ;;
  esac
done
BuildFlags=$(echo $BuildFlags | sed -e 's#-fstack-protector[^ ]*##' -e 's#-ffortify=[0-9]*##')
BuildCC="%__cc"
BuildCCplus="%__cxx"
add_ons=libidn
#
#now overwrite for some architectures
#
%ifarch sparc64
	BuildFlags="-O2 -mcpu=ultrasparc -mvis -fcall-used-g6"
	BuildCC="gcc -m64"
	BuildCCplus="$BuildCCplus -m64"
%endif
%ifarch sparc
	BuildFlags="$BuildFlags -fcall-used-g6"
	BuildCC="gcc -m32"
	BuildCCplus="$BuildCCplus -m32"
%endif
%ifarch sparcv9
	BuildFlags="$BuildFlags -mcpu=ultrasparc -fcall-used-g6"
	BuildCC="gcc -m32"
	BuildCCplus="$BuildCCplus -m32"
%endif
%ifarch alphaev6
	BuildFlags="-mcpu=ev6"
%endif
%ifarch ppc ppc64
	BuildFlags="$(echo $BuildFlags | sed 's#-mminimal-toc##')"
%endif
%ifarch ppc64
	BuildCC="$BuildCC -m64"
	BuildCCplus="$BuildCCplus -m64"
%endif
%ifarch hppa
	BuildFlags="$BuildFlags -mpa-risc-1-1 -fstrict-aliasing"
%endif
# Add flags for all plattforms except AXP
%ifnarch alpha
	BuildFlags="$BuildFlags -g"
%endif
%if %{disable_assert}
	BuildFlags="$BuildFlags -DNDEBUG=1"
%endif
%ifarch mipsel
	# fails to build otherwise - need to recheck and fix
	%define enable_stackguard_randomization 0
%endif

configure_and_build_glibc() {
	local dirname="$1"; shift
	local cflags="$1"; shift
	mkdir "cc-$dirname"
	cd "cc-$dirname"
%ifarch %arm aarch64
	# remove asynchronous-unwind-tables during configure as it causes
	# some checks to fail spuriously on arm
	conf_cflags="${cflags/-fasynchronous-unwind-tables/}"
	conf_cflags="${conf_cflags/-funwind-tables/}"
%else
	conf_cflags="$cflags"
%endif

	profile="--disable-profile"
%if %{build_profile}
        if [ "$dirname" = "base" ] ; then
	    profile="--enable-profile"
	fi
%endif
	elision=--enable-lock-elision
	if [ "$dirname" = "noelision" ]; then
	    elision=--disable-lock-elision
	fi
	../configure \
		CFLAGS="$conf_cflags" BUILD_CFLAGS="$conf_cflags" \
		CC="$BuildCC" CXX="$BuildCCplus" \
		--prefix=%{_prefix} \
		--libexecdir=%{_libexecdir} --infodir=%{_infodir} \
		--enable-add-ons=$add_ons \
	        $profile $elision \
		"$@" \
		--build=%{target} --host=%{target} \
%ifarch armv7hl ppc ppc64 ppc64le i686 x86_64 sparc sparc64 s390 s390x
		--enable-multi-arch \
%endif
%ifarch mipsel
		--without-fp \
%endif
%ifarch ppc64p7
		--with-cpu=power7 \
%endif
%if %{enable_stackguard_randomization}
		--enable-stackguard-randomization \
%endif
		${enable_stack_protector:+--enable-stack-protector=$enable_stack_protector} \
		--enable-tunables \
		--enable-kernel=%{enablekernel} \
		--with-bugurl=http://bugs.opensuse.org \
		--enable-bind-now \
		--enable-obsolete-rpc \
		--disable-timezone-tools
# Should we enable --enable-systemtap?
# Should we enable --enable-nss-crypt to build use freebl3 hash functions?
	# explicitly set CFLAGS to use the full CFLAGS (not the reduced one for configure)
	make %{?_smp_mflags} CFLAGS="$cflags" BUILD_CFLAGS="$cflags"
	cd ..
}

%if !%{optimize_power}
	#
	# Build base glibc
	#
	configure_and_build_glibc base "$BuildFlags"
%else
	#
	# Build POWER-optimized glibc
	#
	# First, base build:
	pBuildFlags="$BuildFlags -mtune=%{powerpc_optimize_tune}"
	%if "%{powerpc_optimize_base}" != ""
	pBuildFlags+=" -mcpu=%{powerpc_optimize_base}"
	%endif
	%if "%{powerpc_optimize_base}" != ""
	configure_and_build_glibc base "$pBuildFlags" --with-cpu=%{powerpc_optimize_base}
	%else
	# Use no default CPU
	configure_and_build_glibc base "$pBuildFlags"
	%endif
	%if %{build_variants}
	# Then other power variants:
	for pcpu in \
	%if %{powerpc_optimize_cpu_power4}
		power4 \
	%endif
	%if %{powerpc_optimize_cpu_power6}
		power6 \
	%endif
	%if %{powerpc_optimize_cpu_power7}
		power7 \
	%endif
	; do
		configure_and_build_glibc $pcpu "$BuildFlags -mcpu=$pcpu" \
			--with-cpu=$pcpu
	done
	# Eventually, special Cell variant:
	%if %{powerpc_optimize_cpu_cell}
		configure_and_build_glibc ppc-cell-be "$BuildFlags -mcpu=cell"
	%endif
	%endif # %{build_variants}
%endif # optimize_power

%if %{build_variants}
%ifarch i686 x86_64
configure_and_build_glibc noelision "$BuildFlags"
%endif
%endif

#
# Build html documentation
#
%if %{build_html}
make -C cc-base html
%endif

#
# Build glibc_post_upgrade binary
#
$BuildCC -static %{optflags} -Os $RPM_SOURCE_DIR/glibc_post_upgrade.c -o glibc_post_upgrade \
     -Lcc-base -Bcc-base/csu \
    '-DREMOVE_TLS_DIRS' '-DREMOVE_PPC_OPTIMIZE_POWER5' \
%ifarch ppc ppc64
 %if !%{powerpc_optimize_cpu_power4}
    '-DREMOVE_PPC_OPTIMIZE_POWER4' \
 %endif
 %if !%{powerpc_optimize_cpu_power6}
    '-DREMOVE_PPC_OPTIMIZE_POWER6' \
 %endif
 %if !%{powerpc_optimize_cpu_power7}
    '-DREMOVE_PPC_OPTIMIZE_POWER7' \
 %endif
 %if !%{powerpc_optimize_cpu_cell}
    '-DREMOVE_PPC_OPTIMIZE_CELL' \
 %endif
%endif
    '-DLIBDIR="/%{_lib}"' '-DGCONV_MODULES_DIR="%{_libdir}/gconv"'

# crypt_blowfish man pages
pushd crypt_blowfish-%{crypt_bf_version}
make man
popd

%check
%if %{build_testsuite}
# The testsuite will fail if asneeded is used
export SUSE_ASNEEDED=0
# Increase timeout
export TIMEOUTFACTOR=16
# The testsuite does its own malloc checking
unset MALLOC_CHECK_
make -C cc-base -k check || {
  cd cc-base
  o=$-
  set +x
  for sum in subdir-tests.sum */subdir-tests.sum; do
    while read s t; do
      case $s in
	XPASS:|PASS:)
	  echo ++++++ $s $t ++++++
	  ;;
	*) # X?FAIL:
	  echo ------ $s $t ------
	  test ! -f $t.out || cat $t.out
	  ;;
	esac
    done < $sum
  done
  set -$o
  # Fail build if there where compilation errors during testsuite run
  test -f tests.sum
}
%else
# This has to pass on all platforms!
# Exceptions:
# None!
make %{?_smp_mflags} -C cc-base check-abi
%endif

%install
%if %{build_main}
# We don't want to strip the .symtab from our libraries in find-debuginfo.sh,
# certainly not from libpthread.so.* because it is used by libthread_db to find
# some non-exported symbols in order to detect if threading support
# should be enabled.  These symbols are _not_ exported, and we can't easily
# export them retroactively without changing the ABI.  So we have to
# continue to "export" them via .symtab, instead of .dynsym :-(
# But we also want to keep .symtab and .strtab of other libraries since some
# debugging tools currently require these sections directly inside the main
# files - specifically valgrind and PurifyPlus.
export STRIP_KEEP_SYMTAB=*.so*

# Make sure we will create the gconv-modules.cache
mkdir -p %{buildroot}%{_libdir}/gconv
touch %{buildroot}%{_libdir}/gconv/gconv-modules.cache

# Install base glibc
make %{?_smp_mflags} install_root=%{buildroot} install -C cc-base

install_optimized_variant() {
	local dirname="$1"; shift
	local subdir="$1"; shift
	local subdir_up="$1"; shift

cd "cc-$dirname"
destdir=$RPM_BUILD_ROOT/%{_lib}/$subdir
mkdir -p $destdir
# Don't run a complete make install, we know which libraries
# we want
for lib in libc math/libm nptl/libpthread rt/librt nptl_db/libthread_db
do
  libbase=${lib#*/}
  libbaseso=$(basename $RPM_BUILD_ROOT/%{_lib}/${libbase}-*.so)
  # Only install if different from base lib
  if cmp -s ${lib}.so ../cc-base/${lib}.so; then
    ln -sf $subdir_up/$libbaseso $destdir/$libbaseso
  else
    cp -a ${lib}.so $destdir/$libbaseso
  fi
done
cd ..
cc-base/elf/ldconfig -vn $destdir
}

# Install power-optimized glibc
%if %{optimize_power}
	%if %{powerpc_optimize_cpu_power4}
	install_optimized_variant power4 power4 ".."
	%endif
	%if %{powerpc_optimize_cpu_power6}
	install_optimized_variant power6 power6 ".."
	%endif
	%if %{powerpc_optimize_cpu_power7}
	install_optimized_variant power7 power7 ".."
	%endif
	%if %{powerpc_optimize_cpu_cell}
	install_optimized_variant ppc-cell-be ppc-cell-be ".."
	%endif
	%if %{powerpc_optimize_cpu_power6}
	# power6 is compatible with power6x
	# doing a directory symlink doesnt work, ldconfig follows them and accepts only the first real dir
	if test -d %{buildroot}/%{_lib}/power6; then
	    mkdir -p %{buildroot}/%{_lib}/power6x
	    for i in %{buildroot}/%{_lib}/power6/*.so; do
		b=$(basename $i)
		ln -vs ../power6/$b %{buildroot}/%{_lib}/power6x/$b
	    done
	    cc-base/elf/ldconfig -vn %{buildroot}/%{_lib}/power6x
	fi
	%endif
%endif # optimize_power

%ifarch i686 x86_64
cd cc-noelision
destdir=$RPM_BUILD_ROOT/%{_lib}/noelision
mkdir -p $destdir
install -m 755 nptl/libpthread.so $destdir/libpthread-%{libversion}.so
cd ..
cc-base/elf/ldconfig -vn $destdir
%endif

# Install locales
%if %{build_locales}
	# XXX Do not install locales in parallel!
	cd cc-base
	# localedef creates hardlinks to other locales if possible
	# this will not work if we generate them in parallel.
	# thus we need to run fdupes on  /usr/lib/locale/
	# Still, on my system this is a speed advantage:
	# non-parallel build for install-locales: 9:34mins
	# parallel build with fdupes: 7:08mins
	make %{?_smp_mflags} install_root=%{buildroot} localedata/install-locales
	%fdupes %{buildroot}/usr/lib/locale
	cd ..
%endif
# Create file list for glibc-locale package
%{find_lang} libc

# remove nsl compat library
rm -f %{buildroot}%{_libdir}/libnsl*
# part of libnsl-devel
rm -f %{buildroot}%{_includedir}/rpcsvc/yppasswd.*

# Miscelanna:

install -m 0700 glibc_post_upgrade %{buildroot}%{_sbindir}

install -m 644 %{SOURCE7} %{buildroot}/etc
install -m 644 %{SOURCE5} %{buildroot}/etc
install -m 644 posix/gai.conf %{buildroot}/etc

mkdir -p %{buildroot}/etc/default
install -m 644 nis/nss %{buildroot}/etc/default/

mkdir -p %{buildroot}%{_includedir}/resolv
install -m 0644 resolv/mapv4v6addr.h %{buildroot}%{_includedir}/resolv/
install -m 0644 resolv/mapv4v6hostent.h %{buildroot}%{_includedir}/resolv/

%if %{build_html}
mkdir -p %{buildroot}%{_datadir}/doc/glibc
cp -p cc-base/manual/libc/*.html %{buildroot}%{_datadir}/doc/glibc
%endif

cd manpages; make install_root=%{buildroot} install; cd ..

# crypt_blowfish man pages
pushd crypt_blowfish-%{crypt_bf_version}
install -m755 -d %{buildroot}%{_mandir}/man3
install -m644 *.3 %{buildroot}%{_mandir}/man3
popd

# nscd tools:

%ifnarch i686
cp nscd/nscd.conf %{buildroot}/etc
mkdir -p %{buildroot}/etc/init.d
ln -sf /sbin/service %{buildroot}/usr/sbin/rcnscd
mkdir -p %{buildroot}/run/nscd
mkdir -p %{buildroot}/var/lib/nscd
%endif

#
# Create ld.so.conf
#
cat > %{buildroot}/etc/ld.so.conf <<EOF
%if "%{_lib}" != "lib"
/usr/local/%{_lib}
%endif
%ifarch ppc
/usr/local/lib64
%endif
/usr/local/lib
include /etc/ld.so.conf.d/*.conf
# /lib64, /lib, /usr/lib64 and /usr/lib gets added
# automatically by ldconfig after parsing this file.
# So, they do not need to be listed.
EOF
# Add ldconfig cache directory for directory ownership
mkdir -p %{buildroot}/var/cache/ldconfig
# Empty the ld.so.cache:
rm -f %{buildroot}/etc/ld.so.cache
touch %{buildroot}/etc/ld.so.cache

# Don't look at ldd! We don't wish a /bin/sh requires
chmod 644 %{buildroot}%{_bindir}/ldd

rm -f %{buildroot}/sbin/sln

# Remove the buildflags tracking section and the build-id
for o in %{buildroot}/%{_libdir}/crt[1in].o %{buildroot}/%{_libdir}/lib*_nonshared.a; do
	objcopy -R ".comment.SUSE.OPTs" -R ".note.gnu.build-id" $o
done

%ifnarch i686
mkdir -p %{buildroot}/usr/lib/tmpfiles.d/
install -m 644 %{SOURCE20} %{buildroot}/usr/lib/tmpfiles.d/
mkdir -p %{buildroot}/usr/lib/systemd/system
install -m 644 %{SOURCE21} %{buildroot}/usr/lib/systemd/system
%endif

%ifarch armv6hl armv7hl
# Provide compatibility link
ln -s ld-%{libversion}.so %{buildroot}/lib/ld-linux.so.3
%endif

# Move getconf to %{_libexecdir}/getconf/ to avoid cross device link
mv %{buildroot}%{_bindir}/getconf %{buildroot}%{_libexecdir}/getconf/getconf
ln -s %{_libexecdir}/getconf/getconf %{buildroot}%{_bindir}/getconf

%if !%{build_utils}
# Remove unwanted files (packaged in glibc-utils)
rm -f %{buildroot}/%{_lib}/libmemusage*
rm -f %{buildroot}/%{_lib}/libpcprofile*
rm -f %{buildroot}%{_bindir}/memusage*
rm -f %{buildroot}%{_bindir}/mtrace
rm -f %{buildroot}%{_bindir}/pcprofiledump
rm -f %{buildroot}%{_bindir}/sotruss
rm -f %{buildroot}%{_bindir}/xtrace
rm -f %{buildroot}%{_bindir}/pldd
rm -rf %{buildroot}%{_libdir}/audit

%ifarch i686
# Remove files from glibc-{extra,info,i18ndata} and nscd
rm -rf %{buildroot}%{_infodir} %{buildroot}%{_prefix}/share/i18n
rm -f %{buildroot}%{_bindir}/makedb %{buildroot}/var/lib/misc/Makefile
rm -f %{buildroot}%{_sbindir}/nscd
%endif # i686
%endif # !utils

# LSB
%ifarch %ix86
ln -sf /%{_lib}/ld-linux.so.2 $RPM_BUILD_ROOT/%{_lib}/ld-lsb.so.3
%endif
%ifarch x86_64
ln -sf /%{_lib}/ld-linux-x86-64.so.2 $RPM_BUILD_ROOT/%{_lib}/ld-lsb-x86-64.so.3
%endif
%ifarch ppc
ln -sf /%{_lib}/ld.so.1 $RPM_BUILD_ROOT/%{_lib}/ld-lsb-ppc32.so.3
%endif
%ifarch ppc64
ln -sf /%{_lib}/ld64.so.1 $RPM_BUILD_ROOT/%{_lib}/ld-lsb-ppc64.so.3
%endif
%ifarch s390
ln -sf /%{_lib}/ld.so.1 $RPM_BUILD_ROOT/%{_lib}/ld-lsb-s390.so.3
%endif
%ifarch s390x
ln -sf /%{_lib}/ld64.so.1 $RPM_BUILD_ROOT/%{_lib}/ld-lsb-s390x.so.3
%endif

%else # !main

%if %{build_utils}

make %{?_smp_mflags} install_root=%{buildroot} install -C cc-base \
  subdirs='malloc debug elf'
cd manpages; make install_root=%{buildroot} install; cd ..
# Remove unwanted files
rm -f %{buildroot}/%{_lib}/ld*.so* %{buildroot}/%{_lib}/lib[!mp]*
rm -f %{buildroot}/lib/ld*.so*
rm -f %{buildroot}%{_libdir}/lib*
rm -f %{buildroot}%{_bindir}/{catchsegv,ldd*,sprof}
rm -rf %{buildroot}%{_mandir}/man*
rm -rf %{buildroot}/sbin %{buildroot}%{_includedir}

%endif # utils

%endif # !main

%if %{build_main}

%post -p %{_sbindir}/glibc_post_upgrade
%postun -p /sbin/ldconfig

%post locale
for l in /usr/share/locale/locale.alias %{_libdir}/gconv/gconv-modules; do
	[ -d "$l.d" ] || continue
	echo "###X# The following is autogenerated from extra files in the .d directory:" >>"$l"
	cat "$l.d"/* >>"$l"
done
/usr/sbin/iconvconfig

%post info
%install_info --info-dir=%{_infodir} %{_infodir}/libc.info.gz

%preun info
%install_info_delete --info-dir=%{_infodir} %{_infodir}/libc.info.gz

%pre -n nscd
getent group nscd >/dev/null || %{_sbindir}/groupadd -r nscd
getent passwd nscd >/dev/null || %{_sbindir}/useradd -r -g nscd -c "User for nscd" -s /sbin/nologin -d /run/nscd nscd
%service_add_pre nscd.service

%preun -n nscd
%service_del_preun nscd.service

%post -n nscd
%service_add_post nscd.service
%tmpfiles_create /usr/lib/tmpfiles.d/nscd.conf
# Previously we had nscd.socket, remove it
test -x /usr/bin/systemctl && /usr/bin/systemctl stop nscd.socket 2>/dev/null || :
test -x /usr/bin/systemctl && /usr/bin/systemctl disable nscd.socket 2>/dev/null  || :
# Hard removal in case the above did not work
rm -f /etc/systemd/system/sockets.target.wants/nscd.socket
exit 0

%postun -n nscd
%service_del_postun nscd.service
exit 0

%files
# glibc
%defattr(-,root,root)
%doc LICENSES
%config(noreplace) /etc/bindresvport.blacklist
%config /etc/ld.so.conf
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
%config(noreplace) /etc/rpc
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/gai.conf
%config(noreplace) /etc/default/nss
%doc %{_mandir}/man1/gencat.1.gz
%doc %{_mandir}/man1/getconf.1.gz
%doc %{_mandir}/man5/*
/%{_lib}/ld-%{libversion}.so

# Each architecture has a different name for the dynamic linker:
%ifarch %arm
%ifarch armv6hl armv7hl
/%{_lib}/ld-linux-armhf.so.3
# Keep compatibility link
/%{_lib}/ld-linux.so.3
%else
/%{_lib}/ld-linux.so.3
%endif
%endif
%ifarch ia64
/%{_lib}/ld-linux-ia64.so.2
%endif
%ifarch ppc s390 mips hppa m68k
/%{_lib}/ld.so.1
%endif
%ifarch ppc64
/%{_lib}/ld64.so.1
%endif
%ifarch ppc64le
/%{_lib}/ld64.so.2
%endif
%ifarch s390x
/lib/ld64.so.1
/%{_lib}/ld64.so.1
%endif
%ifarch x86_64
/%{_lib}/ld-linux-x86-64.so.2
%endif
%ifarch %ix86 %sparc
/%{_lib}/ld-linux.so.2
%endif
%ifarch aarch64
/lib/ld-linux-aarch64.so.1
/%{_lib}/ld-linux-aarch64.so.1
%endif
%ifarch %ix86 x86_64 ppc ppc64 s390 s390x
# LSB
/%{_lib}/*-lsb*.so.3
%endif

/%{_lib}/libBrokenLocale-%{libversion}.so
/%{_lib}/libBrokenLocale.so.1
/%{_lib}/libSegFault.so
/%{_lib}/libanl-%{libversion}.so
/%{_lib}/libanl.so.1
/%{_lib}/libc-%{libversion}.so
/%{_lib}/libc.so.6*
/%{_lib}/libcidn-%{libversion}.so
/%{_lib}/libcidn.so.1
/%{_lib}/libcrypt-%{libversion}.so
/%{_lib}/libcrypt.so.1
/%{_lib}/libowcrypt-%{libversion}.so
/%{_lib}/libowcrypt.so.1
/%{_lib}/libdl-%{libversion}.so
/%{_lib}/libdl.so.2*
/%{_lib}/libm-%{libversion}.so
/%{_lib}/libm.so.6*
%ifarch x86_64
/%{_lib}/libmvec-%{libversion}.so
/%{_lib}/libmvec.so.1
%endif
/%{_lib}/libnsl-%{libversion}.so
/%{_lib}/libnsl.so.1
/%{_lib}/libnss_compat-%{libversion}.so
/%{_lib}/libnss_compat.so.2
/%{_lib}/libnss_db-%{libversion}.so
/%{_lib}/libnss_db.so.2
/%{_lib}/libnss_dns-%{libversion}.so
/%{_lib}/libnss_dns.so.2
/%{_lib}/libnss_files-%{libversion}.so
/%{_lib}/libnss_files.so.2
/%{_lib}/libnss_hesiod-%{libversion}.so
/%{_lib}/libnss_hesiod.so.2
/%{_lib}/libpthread-%{libversion}.so
/%{_lib}/libpthread.so.0
/%{_lib}/libresolv-%{libversion}.so
/%{_lib}/libresolv.so.2
/%{_lib}/librt-%{libversion}.so
/%{_lib}/librt.so.1
/%{_lib}/libthread_db-1.0.so
/%{_lib}/libthread_db.so.1
/%{_lib}/libutil-%{libversion}.so
/%{_lib}/libutil.so.1
%define optimized_libs() \
	%dir %attr(0755,root,root) /%{_lib}/%1\
	/%{_lib}/%1/libc-%{libversion}.so\
	/%{_lib}/%1/libc.so.6*\
	/%{_lib}/%1/libm-%{libversion}.so\
	/%{_lib}/%1/libm.so.6*\
	/%{_lib}/%1/libpthread-%{libversion}.so\
	/%{_lib}/%1/libpthread.so.0\
	/%{_lib}/%1/librt-%{libversion}.so\
	/%{_lib}/%1/librt.so.1\
	/%{_lib}/%1/libthread_db-1.0.so\
	/%{_lib}/%1/libthread_db.so.1

%if %{optimize_power}
	%if %{powerpc_optimize_cpu_power4}
		%{optimized_libs power4}
	%endif
	%if %{powerpc_optimize_cpu_power6}
		%{optimized_libs power6}
		%{optimized_libs power6x}
	%endif
	%if %{powerpc_optimize_cpu_power7}
		%{optimized_libs power7}
	%endif
	%if %{powerpc_optimize_cpu_cell}
		%{optimized_libs ppc-cell-be}
	%endif
%endif # optimize_power
%ifarch i686 x86_64
/%{_lib}/noelision
%endif
%dir %attr(0700,root,root) /var/cache/ldconfig
/sbin/ldconfig
%{_bindir}/gencat
%{_bindir}/getconf
%{_bindir}/getent
%{_bindir}/iconv
%attr(755,root,root) %{_bindir}/ldd
%ifarch %ix86 sparc sparcv9 m68k
	%{_bindir}/lddlibc4
%endif
%{_bindir}/locale
%{_bindir}/localedef
%dir %attr(0755,root,root) %{_libexecdir}/getconf
%{_libexecdir}/getconf/*
%{_sbindir}/glibc_post_upgrade
%{_sbindir}/iconvconfig

%files locale -f libc.lang
%defattr(-,root,root)
%{_datadir}/locale/locale.alias
%if %{build_locales}
	/usr/lib/locale
%endif
%{_libdir}/gconv

%files devel
%defattr(-,root,root)
%doc COPYING COPYING.LIB NEWS README BUGS CONFORMANCE
%doc %{_mandir}/man1/catchsegv.1.gz
%doc %{_mandir}/man1/rpcgen.1.gz
%doc %{_mandir}/man3/*
%{_bindir}/catchsegv
%{_bindir}/rpcgen
%{_bindir}/sprof
%{_includedir}/*
%{_libdir}/*.o
%{_libdir}/*.so
# These static libraries are needed even for shared builds
%{_libdir}/libc_nonshared.a
%{_libdir}/libg.a
%{_libdir}/libieee.a
%ifarch ppc ppc64 ppc64le s390 s390x sparc sparcv8 sparcv9 sparcv9v
# This is not built on sparc64.
	%{_libdir}/libnldbl_nonshared.a
%endif
%{_libdir}/libmcheck.a
%ifarch x86_64
%{_libdir}/libmvec_nonshared.a
%endif
%{_libdir}/libpthread_nonshared.a
%{_libdir}/librpcsvc.a

%files devel-static
%defattr(-,root,root)
%{_libdir}/libBrokenLocale.a
%{_libdir}/libanl.a
%{_libdir}/libc.a
%{_libdir}/libcrypt.a
%{_libdir}/libowcrypt.a
%{_libdir}/libdl.a
%{_libdir}/libm.a
%ifarch x86_64
%{_libdir}/libm-%{libversion}.a
%{_libdir}/libmvec.a
%endif
%{_libdir}/libpthread.a
%{_libdir}/libresolv.a
%{_libdir}/librt.a
%{_libdir}/libutil.a

%ifnarch i686
%files info
%defattr(-,root,root)
%doc %{_infodir}/libc.info.gz
%doc %{_infodir}/libc.info-?.gz
%doc %{_infodir}/libc.info-??.gz

%if %{build_html}
%files html
%defattr(-,root,root)
%doc %{_prefix}/share/doc/glibc
%endif

%files i18ndata
%defattr(-,root,root)
%{_prefix}/share/i18n

%files -n nscd
%defattr(-,root,root)
%config(noreplace) /etc/nscd.conf
%{_sbindir}/nscd
%{_sbindir}/rcnscd
/usr/lib/systemd/system/nscd.service
%dir /usr/lib/tmpfiles.d
/usr/lib/tmpfiles.d/nscd.conf
%dir %attr(0755,root,root) %ghost /run/nscd
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /run/nscd/nscd.pid
%attr(0666,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /run/nscd/socket
%dir %attr(0755,root,root) /var/lib/nscd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/nscd/services
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/nscd/netgroup
%endif # !i686

%if %{build_profile}
%files profile
%defattr(-,root,root)
%{_libdir}/libc_p.a
%{_libdir}/libBrokenLocale_p.a
%{_libdir}/libanl_p.a
%{_libdir}/libm_p.a
%ifarch x86_64
%{_libdir}/libmvec_p.a
%endif
%{_libdir}/libcrypt_p.a
%{_libdir}/libowcrypt_p.a
%{_libdir}/libpthread_p.a
%{_libdir}/libresolv_p.a
%{_libdir}/librt_p.a
%{_libdir}/librpcsvc_p.a
%{_libdir}/libutil_p.a
%{_libdir}/libdl_p.a
%endif

%ifnarch i686
%files extra
%defattr(-,root,root)
%{_bindir}/makedb
/var/lib/misc/Makefile
%endif # !i686

%endif # main

%if %{build_utils}
%files -n glibc-utils
%defattr(-,root,root)
/%{_lib}/libmemusage.so
/%{_lib}/libpcprofile.so
%dir %{_libdir}/audit
%{_libdir}/audit/sotruss-lib.so
%{_bindir}/memusage
%{_bindir}/memusagestat
%{_bindir}/mtrace
%{_bindir}/pcprofiledump
%{_bindir}/sotruss
%{_bindir}/xtrace
%{_bindir}/pldd
%endif # utils

%changelog
