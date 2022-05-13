%global appname MangoHud

%global imgui_ver       1.81
%global imgui_wrap_ver  1

Name:           mangohud
Version:        0.6.7.1
Release:        %autorelease
Summary:        Vulkan overlay layer for monitoring FPS, temperatures, CPU/GPU load and more

License:        MIT
URL:            https://github.com/flightlessmango/MangoHud
Source0:        %{url}/archive/v0.6.7-1/%{name}-%{version}.tar.gz
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

Provides:       bundled(imgui) = %{imgui_ver}

%description
A modification of the Mesa Vulkan overlay. Including GUI improvements,
temperature reporting, and logging capabilities.

To install GUI front-end:

  sudo dnf install goverlay


%prep
%autosetup -n %{appname}-0.6.7-1 -p1
%autosetup -n %{appname}-0.6.7-1 -DTa1
%autosetup -n %{appname}-0.6.7-1 -DTa2

mkdir subprojects/imgui
mv imgui-%{imgui_ver}/* subprojects/imgui/


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
%{_datadir}/vulkan/implicit_layer.d/*Mango*.json
%{_docdir}/%{name}/%{appname}.conf.example
%{_libdir}/%{name}/
%{_mandir}/man1/%{name}.1*


%changelog
%autochangelog
