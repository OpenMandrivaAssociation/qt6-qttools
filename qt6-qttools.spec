#define beta rc
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qttools
Version:	6.2.3
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qttools-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qttools-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Patch0:		qttools-6.0.0-clang-linkage.patch
Group:		System/Libraries
Summary:	Qt %{major} Tools
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	%{_lib}Qt%{major}Core-devel
BuildRequires:	%{_lib}Qt%{major}Gui-devel
BuildRequires:	%{_lib}Qt%{major}Network-devel
BuildRequires:	%{_lib}Qt%{major}Xml-devel
BuildRequires:	%{_lib}Qt%{major}Widgets-devel
BuildRequires:	%{_lib}Qt%{major}Sql-devel
BuildRequires:	%{_lib}Qt%{major}PrintSupport-devel
BuildRequires:	%{_lib}Qt%{major}OpenGL-devel
BuildRequires:	%{_lib}Qt%{major}OpenGLWidgets-devel
BuildRequires:	%{_lib}Qt%{major}DBus-devel
BuildRequires:	qt%{major}-cmake
BuildRequires:	qt%{major}-qtdeclarative
BuildRequires:	qt%{major}-qtdeclarative-devel
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	spirv-llvm-translator
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
# Not really required, but referenced by LLVMExports.cmake
# (and then required because of the integrity check)
BuildRequires:	%{_lib}gpuruntime
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} tools

%prep
%autosetup -p1 -n qttools%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
# FIXME why are OpenGL lib paths autodetected incorrectly, preferring
# /usr/lib over /usr/lib64 even on 64-bit boxes?
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
# Static helper lib without headers -- useless
rm -f %{buildroot}%{_libdir}/qt6/%{_lib}/libpnp_basictools.a
# Put stuff where tools will find it
# We can't do the same for %{_includedir} right now because that would
# clash with qt5 (both would want to have /usr/include/QtCore and friends)
mkdir -p %{buildroot}%{_bindir} %{buildroot}%{_libdir}/cmake
for i in %{buildroot}%{_qtdir}/lib/*.so*; do
	ln -s qt%{major}/lib/$(basename ${i}) %{buildroot}%{_libdir}/
done
mv %{buildroot}%{_qtdir}/lib/cmake %{buildroot}%{_libdir}/

%files
%{_libdir}/cmake/Qt%{major}BuildInternals
%{_libdir}/cmake/Qt%{major}Designer
%{_libdir}/cmake/Qt%{major}Help
%{_libdir}/cmake/Qt%{major}Linguist
%{_libdir}/cmake/Qt%{major}LinguistTools
%{_libdir}/cmake/Qt%{major}Tools
%{_libdir}/cmake/Qt%{major}ToolsTools
%{_libdir}/cmake/Qt%{major}UiPlugin
%{_libdir}/cmake/Qt%{major}UiTools
%{_libdir}/libQt%{major}Designer.so
%{_libdir}/libQt%{major}Designer.so.%{major}*
%{_libdir}/libQt%{major}DesignerComponents.so
%{_libdir}/libQt%{major}DesignerComponents.so.%{major}*
%{_libdir}/libQt%{major}Help.so
%{_libdir}/libQt%{major}Help.so.%{major}*
%{_libdir}/libQt%{major}UiTools.so
%{_libdir}/libQt%{major}UiTools.so.%{major}*
%{_qtdir}/bin/designer
%{_qtdir}/bin/lconvert
%{_qtdir}/bin/linguist
%{_qtdir}/bin/lrelease
%{_qtdir}/bin/lupdate
%{_qtdir}/bin/pixeltool
%{_qtdir}/bin/qdbus
%{_qtdir}/bin/qdbusviewer
%{_qtdir}/bin/qdistancefieldgenerator
%{_qtdir}/bin/qdoc
%{_qtdir}/bin/qhelpgenerator
%{_qtdir}/bin/qtdiag
%{_qtdir}/bin/qtdiag6
%{_qtdir}/bin/qtplugininfo
%{_qtdir}/bin/assistant
%{_qtdir}/libexec/lprodump
%{_qtdir}/libexec/lrelease-pro
%{_qtdir}/libexec/lupdate-pro
%{_qtdir}/examples/assistant
%{_qtdir}/examples/designer
%{_qtdir}/examples/help
%{_qtdir}/examples/linguist
%{_qtdir}/examples/plugins/designer
%{_qtdir}/examples/uitools
%{_qtdir}/phrasebooks
%{_qtdir}/include/QtDesigner
%{_qtdir}/include/QtDesignerComponents
%{_qtdir}/include/QtHelp
%{_qtdir}/include/QtTools
%{_qtdir}/include/QtUiPlugin
%{_qtdir}/include/QtUiTools
%{_qtdir}/lib/libQt%{major}Designer.prl
%{_qtdir}/lib/libQt%{major}Designer.so
%{_qtdir}/lib/libQt%{major}Designer.so.%{major}*
%{_qtdir}/lib/libQt%{major}DesignerComponents.prl
%{_qtdir}/lib/libQt%{major}DesignerComponents.so
%{_qtdir}/lib/libQt%{major}DesignerComponents.so.%{major}*
%{_qtdir}/lib/libQt%{major}Help.prl
%{_qtdir}/lib/libQt%{major}Help.so
%{_qtdir}/lib/libQt%{major}Help.so.%{major}*
%{_qtdir}/lib/libQt%{major}UiTools.prl
%{_qtdir}/lib/libQt%{major}UiTools.so
%{_qtdir}/lib/libQt%{major}UiTools.so.%{major}*
%{_qtdir}/mkspecs/modules/qt_lib_designer.pri
%{_qtdir}/mkspecs/modules/qt_lib_designer_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_designercomponents_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_help.pri
%{_qtdir}/mkspecs/modules/qt_lib_help_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_linguist.pri
%{_qtdir}/mkspecs/modules/qt_lib_linguist_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_tools_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_uiplugin.pri
%{_qtdir}/mkspecs/modules/qt_lib_uitools.pri
%{_qtdir}/mkspecs/modules/qt_lib_uitools_private.pri
%{_qtdir}/modules/Designer.json
%{_qtdir}/modules/Help.json
%{_qtdir}/modules/Linguist.json
%{_qtdir}/modules/Tools.json
%{_qtdir}/modules/UiPlugin.json
%{_qtdir}/modules/UiTools.json
%{_qtdir}/plugins/designer/libqquickwidget.so
%{_libdir}/cmake/Qt6/FindWrapLibClang.cmake
%{_libdir}/cmake/Qt6DesignerComponentsPrivate
%{_qtdir}/lib/metatypes/qt6designer_relwithdebinfo_metatypes.json
%{_qtdir}/lib/metatypes/qt6designercomponentsprivate_relwithdebinfo_metatypes.json
%{_qtdir}/lib/metatypes/qt6help_relwithdebinfo_metatypes.json
%{_qtdir}/lib/metatypes/qt6uitools_relwithdebinfo_metatypes.json
%{_qtdir}/libexec/qtattributionsscanner
%{_qtdir}/modules/DesignerComponentsPrivate.json

