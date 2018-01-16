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
