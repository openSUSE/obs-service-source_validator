#
# spec file for package gdm
#
# Copyright (c) 2017 SUSE LINUX GmbH, Nuernberg, Germany.
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


# Allow to disable wayland components
%bcond_without wayland

%define systemdsystemunitdir %(pkg-config --variable=systemdsystemunitdir systemd)

# FIXME: need to check what should be done to enable this (at least adapt the pam files). See bnc#699999
%define enable_split_authentication 0

Name:           gdm
Version:        3.26.2.1
Release:        0
Summary:        The GNOME Display Manager
License:        GPL-2.0+
Group:          System/GUI/GNOME
Url:            https://wiki.gnome.org/Projects/GDM
Source:         https://download.gnome.org/sources/gdm/3.26/%{name}-%{version}.tar.xz
Source1:        gdm.pamd
Source2:        gdm-autologin.pamd
Source3:        gdm-launch-environment.pamd
Source6:        gdm-fingerprint.pamd
Source7:        gdm-smartcard.pamd
# gdmflexiserver wrapper, to enable other display managers to abuse the gdmflexiserver namespace (like lightdm)
Source4:        gdmflexiserver-wrapper
# /etc/xinit.d/xdm integration script
Source5:        X11-displaymanager-gdm
# GDM does not boostrap using gnome-autogen.sh, but has it's own bootstrap script
Source8:        autogen.sh
# PATCH-FEATURE-OPENSUSE gdm-workaround-boo971852.patch zaitor@opensuse.org -- Work around boo971852 - xsessions is just not going to happen for a gdm user - Those users ALL have gnome-shell installed (which is mandatory for gdm to operate) - openSUSE only
Patch0:         gdm-workaround-boo971852.patch
# PATCH-FIX-OPENSUSE gdm-suse-xsession.patch vuntz@novell.com -- Use the /etc/X11/xdm/* scripts
Patch7:         gdm-suse-xsession.patch
# WARNING: do not remove/significantly change patch8 without updating the relevant patch in accountsservice too
# PATCH-FIX-OPENSUSE gdm-sysconfig-settings.patch bnc432360 bsc#919723 hpj@novell.com -- Read autologin options from /etc/sysconfig/displaymanager; note that accountsservice has a similar patch (accountsservice-sysconfig.patch)
Patch8:         gdm-sysconfig-settings.patch
# PATCH-NEEDS-REBASE PATCH-FEATURE-OPENSUSE gdm-passwordless-login.patch vuntz@opensuse.org -- Support DISPLAYMANAGER_PASSWORD_LESS_LOGIN sysconfig option
Patch9:         gdm-passwordless-login.patch
# PATCH-FIX-OPENSUSE gdm-default-wm.patch vuntz@novell.com -- Use sysconfig to know to which desktop to use by default
Patch34:        gdm-default-wm.patch
# PATCH-FIX-OPENSUSE gdm-xauthlocalhostname.patch bnc#538064 vuntz@novell.com -- Set XAUTHLOCALHOSTNAME to current hostname when we authenticate, for local logins, to avoid issues in the session in case the hostname changes later one. See comment 24 in the bug.
Patch35:        gdm-xauthlocalhostname.patch
# PATCH-FIX-OPENSUSE gdm-ignore-duplicate-session.patch xwang@suse.com -- gdm sessions entries duplicate
Patch36:        gdm-ignore-duplicate-session.patch
# PATCH-FIX-UPSTREAM gdm-plymouth-vt1.patch bnc#881676 fcrozat@suse.com -- switch to VT1 when quitting if gdm was starting with plymouth running
Patch41:        gdm-plymouth-vt1.patch
# PATCH-FIX-UPSTREAM gdm-fails-to-restart-gnome-shell.patch bsc#981976 bgo#769969 tyang@suse.com -- Gdm should stop after a few times fails
Patch42:        gdm-fails-to-restart-gnome-shell.patch
# PATCH-FIX-SLE gdm-default-wm-sle12.patch bnc#881659 cxiong@suse.com -- set default/fallback session type to SLE Classic
Patch49:        gdm-default-wm-sle12.patch
# PATCH-FIX-SLE gdm-ignore-SLE-CLASSIC-MODE.patch bsc#1060630 xwang@suse.com -- ignore env SLE_CLASSIC_MODE variable when switching from sle-classic session to gnome-classic session
Patch51:        gdm-ignore-SLE-CLASSIC-MODE.patch
# PATCH-FIX-SLE gdm-disable-gnome-initial-setup.patch bnc#1067976 qzhao@suse.com -- Disable gnome-initial-setup runs before gdm, g-i-s will only serve for CJK people to choose the input-method after login.
Patch52:        gdm-disable-gnome-initial-setup.patch
BuildRequires:  check-devel
# needed for directory ownership
BuildRequires:  dconf
BuildRequires:  gnome-common
# needed for directory ownership
BuildRequires:  fdupes
BuildRequires:  gnome-session-core
BuildRequires:  keyutils-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconfig
BuildRequires:  pwdutils
BuildRequires:  tcpd-devel
%if !0%{?is_opensuse}
BuildRequires:  translation-update-upstream
%endif
BuildRequires:  update-desktop-files
BuildRequires:  xorg-x11-server
BuildRequires:  xorg-x11-server-extra
BuildRequires:  pkgconfig(accountsservice) >= 0.6.35
BuildRequires:  pkgconfig(check)
BuildRequires:  pkgconfig(gio-2.0) >= 2.36.0
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.36.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.36.0
BuildRequires:  pkgconfig(gobject-2.0) >= 2.36.0
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 0.9.12
BuildRequires:  pkgconfig(gthread-2.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= 2.91.1
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:  pkgconfig(libcanberra-gtk3) >= 0.4
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(ply-boot-client)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xau)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xdmcp)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xinerama)
%ifnarch s390 s390x
BuildRequires:  pkgconfig(xorg-server)
%endif
BuildRequires:  pkgconfig(xrandr)
Requires(pre):  group(video)
Requires:       %{name}-branding = %{version}
Requires:       gdmflexiserver
Requires:       gnome-session-core
Requires:       gnome-settings-daemon
Requires:       gnome-shell
Requires(post): dconf
# accessibility
Recommends:     orca
# For groupadd, useradd, usermod
PreReq:         pwdutils
Recommends:     %{name}-lang
Recommends:     iso-codes
Provides:       gdm2 = %{version}
Obsoletes:      gdm2 < %{version}
Provides:       gnome-applets-gdm = %{version}
Obsoletes:      gnome-applets-gdm < %{version}
# gdmflexiserver is dropped since 3.5.90
Obsoletes:      gdmflexiserver < %{version}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
DocDir:         %{_defaultdocdir}

%description
The GNOME Display Manager is a system service that is responsible for
providing graphical log-ins and managing local and remote displays.

%package -n libgdm1
Summary:        Client Library for Communicating with GDM Greeter Server
Group:          System/Libraries
Recommends:     gdm

%description -n libgdm1
The GNOME Display Manager is a system service that is responsible for
providing graphical log-ins and managing local and remote displays.

%package -n typelib-1_0-Gdm-1_0
Summary:        Client Library for Communicating with GDM Greeter Server -- Introspection bindings
Group:          System/Libraries

%description -n typelib-1_0-Gdm-1_0
The GNOME Display Manager is a system service that is responsible for
providing graphical log-ins and managing local and remote displays.

This package provides the GObject Introspection bindings for
communicating with the GDM greeter server.

%package devel
Summary:        Libraries for GDM -- Development Files
Group:          Development/Libraries/GNOME
Requires:       libgdm1 = %{version}
Requires:       typelib-1_0-Gdm-1_0 = %{version}

%description devel
The GNOME Display Manager is a system service that is responsible for
providing graphical log-ins and managing local and remote displays.

%package branding-upstream
Summary:        The GNOME Display Manager -- Upstream default configuration
Group:          System/GUI/GNOME
Requires:       %{name} = %{version}
Provides:       %{name}-branding = %{version}
Conflicts:      otherproviders(%{name}-branding)
Supplements:    packageand(%{name}:branding-upstream)
BuildArch:      noarch
#BRAND: Provide one file:
#BRAND: /etc/gdm/custom.conf
#BRAND:   Default configuration of gdm

%description branding-upstream
The GNOME Display Manager is a system service that is responsible for
providing graphical log-ins and managing local and remote displays.

This package provides the upstream default configuration for gdm.

%package -n gdmflexiserver
Summary:        Gdmflexiserver Compatibility Wrapper for Display Managers
Group:          System/GUI/GNOME
Suggests:       gdm
BuildArch:      noarch

%description -n gdmflexiserver
The gdmflexiserver tool interacts with the display manager to
enable fast user switching. This package contains a wrapper that
selects the correct gdmflexiserver implementatoin, based on the
running display manager.

%lang_package
%prep
%setup -q
cp %{S:8} .
%if !0%{?is_opensuse}
translation-update-upstream
%endif
%if 0%{?is_opensuse}
# Disabled for now, see boo#981372 and boo#971852
#patch0 -p1
%endif
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch41 -p1
%patch42 -p1
%if !0%{?is_opensuse}
%patch49 -p1
%patch51 -p1
%patch52 -p1
%endif

%build
NOCONFIGURE=1 sh autogen.sh
%configure\
        --disable-static \
        --libexecdir=%{_prefix}/lib/gdm \
        --localstatedir=%{_localstatedir} \
        --with-at-spi-registryd-directory=%{_libexecdir}/at-spi \
        --with-check-accelerated-directory=%{_libexecdir} \
        --with-gnome-settings-daemon-directory=%{_libexecdir}/gnome-settings-daemon-3.0 \
        --with-pam-mod-dir=/%{_lib}/security \
        --enable-ipv6 \
        --enable-gdm-xsession \
        --with-plymouth \
%if %{with wayland}
        --enable-wayland-support \
%else
        --disable-wayland-support \
%endif
%if 0%{?is_opensuse}
        --enable-systemd-journal \
%else
        --disable-systemd-journal \
%endif
%if %{enable_split_authentication}
        --enable-split-authentication \
%else
        --disable-split-authentication \
%endif
        --with-initial-vt=7 \
        --with-run-dir=/run/gdm
%__make %{?jobs:-j%jobs} V=1

%install
%make_install
find %{buildroot} -name '*.la' -type f -delete -print
# Do not ship the systemd.service file: openSUSE uses xdm, which enables the DM based on sysconfig.
rm %{buildroot}%{systemdsystemunitdir}/gdm.service
## Install PAM files.
mkdir -p %{buildroot}/etc/pam.d
# Generic pam config
cp %{SOURCE1} %{buildroot}/etc/pam.d/gdm
# Pam config for autologin
cp %{SOURCE2} %{buildroot}/etc/pam.d/gdm-autologin
# Pam config for the greeter session
cp %{SOURCE3} %{buildroot}/etc/pam.d/gdm-launch-environment
%if %{enable_split_authentication}
# Pam config for fingerprint authentication
cp %{SOURCE6} %{buildroot}/etc/pam.d/gdm-fingerprint
# Pam config for smartcard authentication
cp %{SOURCE7} %{buildroot}/etc/pam.d/gdm-smartcard
%endif
# The default gdm pam configuration is the one to be used as pam-password too
%if %{enable_split_authentication}
rm %{buildroot}/etc/pam.d/gdm-password
echo "We are not ready for this, we need to know what to put in gdm-fingerprint and gdm-smartcard pam config files."
false
%endif
ln -s gdm %{buildroot}/etc/pam.d/gdm-password
## Install other files
# Install PostLogin script.
mv %{buildroot}%{_sysconfdir}/gdm/PostLogin/Default.sample %{buildroot}%{_sysconfdir}/gdm/PostLogin/Default
# Move gdmflexiserver to libexecdir and replace it with the compatibility wrapper
mv %{buildroot}%{_bindir}/gdmflexiserver %{buildroot}%{_libexecdir}/gdm/gdmflexiserver
install -m 755 %{SOURCE4} %{buildroot}%{_bindir}/gdmflexiserver
#Install /etc/xinit.d/xdm integration script
install -D -m 644 %{SOURCE5} %{buildroot}%{_libexecdir}/X11/displaymanagers/gdm
mkdir -p %{buildroot}%{_sysconfdir}/alternatives
touch %{buildroot}%{_sysconfdir}/alternatives/default-displaymanager
ln -s %{_sysconfdir}/alternatives/default-displaymanager %{buildroot}%{_libexecdir}/X11/displaymanagers/default-displaymanager

# Install other files
mkdir -p %{buildroot}%{_localstatedir}/log/gdm
mkdir -p %{buildroot}/run/gdm
mkdir -p %{buildroot}%{_bindir}
ln -s ../sbin/gdm %{buildroot}%{_bindir}/gdm
%find_lang %{name} %{?no_lang_C}
%fdupes -s %{buildroot}%{_datadir}/help

%clean
rm -rf %{buildroot}

%pre
/usr/sbin/groupadd -r gdm 2> /dev/null || :
/usr/sbin/useradd -r -g gdm -G video -s /bin/false \
-c "Gnome Display Manager daemon" -d /var/lib/gdm gdm 2> /dev/null || :
/usr/sbin/usermod -g gdm -G video -s /bin/false gdm 2> /dev/null
# Fix incorrect interpretation of DISPLAYMANAGER_PASSWORD_LESS_LOGIN (#307566).
# Last done in SLED10&10.1, first fixed in 10.3.
# Can be removed after SLES12:
if test -f sbin/conf.d/SuSEconfig.gdm && grep -q gdm-autologin sbin/conf.d/SuSEconfig.gdm ; then
    if grep -q '^DISPLAYMANAGER_PASSWORD_LESS_LOGIN="no"' etc/sysconfig/displaymanager ; then
	sed 's/^\(auth[[:space:]][[:space:]]*\)include[[:space:]]\([[:space:]]*\)common-auth/\1required\2pam_permit.so/' <etc/pam.d/gdm-autologin >etc/pam.d/gdm-autologin.new
	if cmp -s etc/pam.d/gdm-autologin etc/pam.d/gdm-autologin.new ; then
	    rm etc/pam.d/gdm-autologin.new
	else
	    mv etc/pam.d/gdm-autologin.new etc/pam.d/gdm-autologin
	fi
    fi
fi
# Fix how DISPLAYMANAGER_PASSWORD_LESS_LOGIN is used. Before 11.4,
# /etc/pam.d/gdm was changed to use pam_permit. We don't want this anymore.
if test -f /sbin/conf.d/SuSEconfig.gdm; then
    grep -q pam_permit.so /etc/pam.d/gdm
    if test $? -eq 0; then
        # We'll just use the file from the new package
        mv /etc/pam.d/gdm /etc/pam.d/gdm.rpmold
    fi
fi

%post
%{_sbindir}/update-alternatives --install %{_libexecdir}/X11/displaymanagers/default-displaymanager \
  default-displaymanager %{_libexecdir}/X11/displaymanagers/gdm 25

%posttrans
# Create dconf database for gdm, to lockdown the gdm session
dconf update

%postun
[ -f %{_libexecdir}/X11/displaymanagers/gdm ] || %{_sbindir}/update-alternatives \
  --remove default-displaymanager %{_libexecdir}/X11/displaymanagers/gdm

%post -n libgdm1 -p /sbin/ldconfig

%postun -n libgdm1 -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%doc %{_datadir}/help/C/%{name}/
%dir %config %{_sysconfdir}/gdm
%config %{_sysconfdir}/gdm/[IPXl]*
%{_sbindir}/gdm
%{_bindir}/gdm
%{_bindir}/gdm-screenshot
%dir %{_datadir}/dconf
%dir %{_datadir}/dconf/profile
%{_datadir}/dconf/profile/gdm
%{_datadir}/gdm/
%{_datadir}/gnome-session/sessions/gnome-login.session
%{_datadir}/glib-2.0/schemas/org.gnome.login-screen.gschema.xml
%{_datadir}/icons/*/*/*/*.*
%{_datadir}/pixmaps/*.png
/%{_lib}/security/pam_gdm.so
%dir %{_libexecdir}/gdm
%{_libexecdir}/gdm/gdm-*
%{_libexecdir}/gdm/gdmflexiserver
%attr(750,gdm,gdm) %dir %{_localstatedir}/lib/gdm
%attr(711,root,gdm) %dir %{_localstatedir}/log/gdm
%dir %{_localstatedir}/cache/gdm
%ghost %attr(711,root,gdm) %dir /run/gdm
%config /etc/pam.d/gdm
%config /etc/pam.d/gdm-autologin
%if %{enable_split_authentication}
%config /etc/pam.d/gdm-fingerprint
%config /etc/pam.d/gdm-smartcard
%endif
%config /etc/pam.d/gdm-password
%config /etc/pam.d/gdm-launch-environment
%config %{_sysconfdir}/dbus-1/system.d/gdm.conf
# /etc/xinit.d/xdm integration
%dir %{_libexecdir}/X11/displaymanagers
%{_libexecdir}/X11/displaymanagers/default-displaymanager
%{_libexecdir}/X11/displaymanagers/gdm
%ghost %{_sysconfdir}/alternatives/default-displaymanager

%files -n libgdm1
%defattr(-,root,root)
%{_libdir}/libgdm.so.*

%files -n typelib-1_0-Gdm-1_0
%defattr(-,root,root)
%{_libdir}/girepository-1.0/Gdm-1.0.typelib

%files devel
%defattr(-,root,root)
%{_includedir}/gdm/
%{_libdir}/libgdm.so
%{_libdir}/pkgconfig/gdm.pc
%{_libdir}/pkgconfig/gdm-pam-extensions.pc
%{_datadir}/gir-1.0/Gdm-1.0.gir

%files branding-upstream
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/gdm/custom.conf

%files -n gdmflexiserver
%defattr(-,root,root)
%{_bindir}/gdmflexiserver

%files lang -f %{name}.lang

%changelog
