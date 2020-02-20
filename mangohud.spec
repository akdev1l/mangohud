# LTO
%global optflags        %{optflags} -flto
%global build_ldflags   %{build_ldflags} -flto

# Git submodules
# * ImGui
%global commit1         6c1a73774dabd2be64f85543b1286e44632d1905
%global shortcommit1    %(c=%{commit1}; echo ${c:0:7})

%global appname MangoHud

Name:           mangohud
Version:        0.2.0
Release:        11%{?dist}
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
# Change default libdir path
# * https://github.com/flightlessmango/MangoHud/issues/31
mkdir -p %{buildroot}%{_libdir}/%{name}
mv  %{buildroot}%{_libdir}/lib%{appname}.so \
    %{buildroot}%{_libdir}/%{name}/
sed -i 's|"library_path": "libMangoHud.so"|"library_path": "%{_libdir}/%{name}/libMangoHud.so"|' \
    %{buildroot}%{_datadir}/vulkan/implicit_layer.d/%{name}.json
sed -i 's|"name": "MangoHud 64bit"|"name": "MangoHud %{_arch}"|' \
    %{buildroot}%{_datadir}/vulkan/implicit_layer.d/%{name}.json
mv  %{buildroot}%{_datadir}/vulkan/implicit_layer.d/%{name}.json \
    %{buildroot}%{_datadir}/vulkan/implicit_layer.d/%{name}.%{_arch}.json


%files
%license LICENSE
%doc README.md bin/%{appname}.conf
%{_libdir}/%{name}/
%{_datadir}/vulkan/implicit_layer.d/%{name}*.json


%changelog
* Fri Feb 14 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.2.0-11
- Initial package
- Thanks for help with packaging to:
  gasinvein <gasinvein@gmail.com>
  Vitaly Zaitsev <vitaly@easycoding.org>
