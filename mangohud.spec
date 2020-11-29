%global appname MangoHud

Name:           mangohud
Version:        0.6.0
Release:        2%{?dist}
Summary:        Vulkan overlay layer for monitoring FPS, temperatures, CPU/GPU load and more

License:        MIT
URL:            https://github.com/flightlessmango/MangoHud
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  dbus-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  glslang-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  meson
BuildRequires:  python3-mako
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(x11)

Requires:       vulkan-loader%{?_isa}

Suggests:       goverlay

Provides:       bundled(imgui)

%description
A modification of the Mesa Vulkan overlay. Including GUI improvements,
temperature reporting, and logging capabilities.

To install GUI front-end:

  sudo dnf install goverlay


%prep
%autosetup -n %{appname}-%{version} -p1

# https://github.com/flightlessmango/MangoHud/issues/411
sed -i 's|@VCS_TAG@|%{version}|' \
    version.h.in


%build
%meson \
    -Duse_system_vulkan=enabled \
    -Dwith_xnvctrl=disabled
%meson_build


%install
%meson_install


%files
%license LICENSE
%doc README.md bin/%{appname}.conf
%{_bindir}/%{name}*
%{_datadir}/vulkan/implicit_layer.d/%{appname}*.json
%{_docdir}/%{name}/%{appname}.conf.example
%{_libdir}/%{name}/
%{_mandir}/man1/%{name}.1*


%changelog
* Sun Nov 29 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.0-2
- fix: version in HUD | GH-411

* Sat Nov 28 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.0-1
- build(update): 0.6.0

* Sun Aug 16 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.5.1-1
- Update to 0.5.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 13 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.4.1-2
- Add patch which fix F33 build | GH-213

* Thu Jun 11 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.4.1-1
- Update to 0.4.1
- Disable LTO

* Sat May 02 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.5-1
- Update to 0.3.5
- Remove ExclusiveArch. Now compiles on all arches, see GitHub#88.

* Thu Mar 26 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.1-2
- Add GUI fron-end 'goverlay' as very weak dep

* Wed Mar 18 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.1-1
- Update to 0.3.1

* Sun Mar 15 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.0-1
- Update to 0.3.0

* Fri Feb 14 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.2.0-11
- Initial package
- Thanks for help with packaging to:
  gasinvein <gasinvein@gmail.com>
  Vitaly Zaitsev <vitaly@easycoding.org>
