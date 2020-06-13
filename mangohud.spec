# Git submodules
# * ImGui
%global commit 1f02d240b38f445abb0381ade0867752d5d2bc7b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global appname MangoHud

Name:           mangohud
Version:        0.4.1
Release:        2%{?dist}
Summary:        Vulkan overlay layer for monitoring FPS, temperatures, CPU/GPU load and more

License:        MIT
URL:            https://github.com/flightlessmango/MangoHud
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/flightlessmango/ImGui/archive/%{commit}/ImGui-%{shortcommit}.tar.gz
Patch0:         https://github.com/flightlessmango/MangoHud/pull/208.patch#/fix-wformat-security-warning-with-gcc-10.1.patch

# https://github.com/flightlessmango/MangoHud/issues/213
Patch1:         https://github.com/flightlessmango/MangoHud/commit/db070816174b4b84d0859ac5e29ef71520376d01.patch#/use-xml.etree.elementtree.patch

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

Provides:       bundled(ImGui) = 0~git%{shortcommit}

%description
A modification of the Mesa Vulkan overlay. Including GUI improvements,
temperature reporting, and logging capabilities.

To install GUI front-end:

  sudo dnf install goverlay


%prep
%setup -n %{appname}-%{version} -q
%setup -n %{appname}-%{version} -q -D -T -a1
%patch0 -p1
%patch1 -p1
mv imgui-%{commit}/* modules/ImGui/src/


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


%changelog
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
