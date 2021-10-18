%global appname MangoHud

%global imgui_ver       1.81
%global imgui_wrap_ver  1

Name:           mangohud
Version:        0.6.6
Release:        1%{?dist}
Summary:        Vulkan overlay layer for monitoring FPS, temperatures, CPU/GPU load and more

License:        MIT
URL:            https://github.com/flightlessmango/MangoHud
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/ocornut/imgui/archive/v%{imgui_ver}/imgui-%{imgui_ver}.tar.gz
Source2:        https://wrapdb.mesonbuild.com/v1/projects/imgui/%{imgui_ver}/%{imgui_wrap_ver}/get_zip#/imgui-%{imgui_ver}-%{imgui_wrap_ver}-wrap.zip

BuildRequires:  dbus-devel
BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  git-core
BuildRequires:  glew-devel
BuildRequires:  glfw-devel
BuildRequires:  glslang-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  meson
BuildRequires:  python3-mako
BuildRequires:  spdlog-devel

BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(x11)

Requires:       vulkan-loader%{?_isa}

Recommends:     (mangohud(x86-32) if glibc(x86-32))

Suggests:       goverlay

Provides:       bundled(imgui)

%description
A modification of the Mesa Vulkan overlay. Including GUI improvements,
temperature reporting, and logging capabilities.

To install GUI front-end:

  sudo dnf install goverlay


%prep
%autosetup -n %{appname}-%{version} -p1
%autosetup -n %{appname}-%{version} -DTa1
%autosetup -n %{appname}-%{version} -DTa2

mkdir subprojects/imgui
mv imgui-%{imgui_ver}/* subprojects/imgui/

# https://github.com/flightlessmango/MangoHud/issues/411
sed -i 's|@VCS_TAG@|v%{version}|' \
    version.h.in


%build
%meson \
    -Duse_system_spdlog=enabled \
    -Duse_system_vulkan=enabled \
    -Dwith_xnvctrl=disabled \
    %{nil}
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
* Mon Oct 18 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.6-1
- chore(update): 0.6.6

* Thu Oct 07 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.5-3
- build: Fix multilib dep | rh#1830718

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.5-1
- build(update): 0.6.5

* Thu Jun 24 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.4-1
- build(update): 0.6.4

* Sat Jun 12 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.3-1
- build(update): 0.6.3

* Fri Jun 11 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.2-1
- build(update): 0.6.2

* Wed Jan 27 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.1-3
- build: Install 32-bit version automagically if multilib packages already
  installed on end user machine

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Nov 29 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.1-1
- build(update): 0.6.1

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
