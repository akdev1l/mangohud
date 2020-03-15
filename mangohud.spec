# LTO
%global optflags        %{optflags} -flto
%global build_ldflags   %{build_ldflags} -flto

# Git submodules
# * ImGui
%global commit1         e628122da006c0e9f7e695592765696d8253cf6f
%global shortcommit1    %(c=%{commit1}; echo ${c:0:7})

%global appname MangoHud

Name:           mangohud
Version:        0.3.0
Release:        1%{?dist}
Summary:        Vulkan overlay layer for monitoring FPS, temperatures, CPU/GPU load and more

License:        MIT
URL:            https://github.com/flightlessmango/MangoHud
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        https://github.com/flightlessmango/ImGui/archive/%{commit1}/ImGui-%{shortcommit1}.tar.gz

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

Provides:       bundled(ImGui) = 0~git%{shortcommit1}

%description
A modification of the Mesa Vulkan overlay. Including GUI improvements,
temperature reporting, and logging capabilities.


%prep
%setup -n %{appname}-%{version} -q
%setup -n %{appname}-%{version} -q -D -T -a1
mv imgui-%{commit1}/* modules/ImGui/src/


%build
%meson -Duse_system_vulkan=enabled
%meson_build


%install
%meson_install


%files
%license LICENSE
%doc README.md bin/%{appname}.conf
%{_bindir}/%{name}
%{_datadir}/vulkan/implicit_layer.d/%{appname}*.json
%{_docdir}/%{name}/%{appname}.conf.example
%{_libdir}/%{name}/


%changelog
* Sun Mar 15 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.0-1
- Update to 0.3.0

* Fri Feb 14 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.2.0-11
- Initial package
- Thanks for help with packaging to:
  gasinvein <gasinvein@gmail.com>
  Vitaly Zaitsev <vitaly@easycoding.org>
