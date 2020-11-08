%define beta beta3
#define snapshot 20200627
%define major 6

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qttools
Version:	6.0.0
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
BuildRequires:	%{_lib}Qt%{major}Network-devel
BuildRequires:	%{_lib}Qt%{major}Qml-devel
BuildRequires:	qt%{major}-cmake
License:	LGPLv3/GPLv3/GPLv2
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)

%description
Qt %{major} tools

%prep
%autosetup -p1 -n qttools%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
# FIXME why are OpenGL lib paths autodetected incorrectly, preferring
# /usr/lib over /usr/lib64 even on 64-bit boxes?
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DBUILD_EXAMPLES:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=ON \
	-DFEATURE_cxx2a:BOOL=ON \
	-DFEATURE_dynamicgl:BOOL=ON \
	-DFEATURE_ftp:BOOL=ON \
	-DFEATURE_opengl_dynamic:BOOL=ON \
	-DFEATURE_use_lld_linker:BOOL=ON \
	-DFEATURE_xcb_native_painting:BOOL=ON \
	-DFEATURE_openssl:BOOL=ON \
	-DFEATURE_openssl_linked:BOOL=ON \
	-DFEATURE_system_sqlite:BOOL=ON \
	-DINPUT_sqlite=system \
	-DQT_WILL_INSTALL:BOOL=ON \
	-D_OPENGL_LIB_PATH=%{_libdir} \
	-DOPENGL_egl_LIBRARY=%{_libdir}/libEGL.so \
	-DOPENGL_glu_LIBRARY=%{_libdir}/libGLU.so \
	-DOPENGL_glx_LIBRARY=%{_libdir}/libGLX.so \
	-DOPENGL_opengl_LIBRARY=%{_libdir}/libOpenGL.so

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
for i in %{buildroot}%{_qtdir}/lib/cmake/*; do
	ln -s ../qt%{major}/lib/cmake/$(basename ${i}) %{buildroot}%{_libdir}/cmake/
done

%files
%{_libdir}/cmake/Qt%{major}BuildInternals
%{_libdir}/cmake/Qt%{major}Designer
%{_libdir}/cmake/Qt%{major}DesignerComponents
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
%{_qtdir}/bin/assistant
%{_qtdir}/bin/designer
%{_qtdir}/bin/lconvert
%{_qtdir}/bin/linguist
%{_qtdir}/bin/lprodump
%{_qtdir}/bin/lrelease
%{_qtdir}/bin/lrelease-pro
%{_qtdir}/bin/lupdate
%{_qtdir}/bin/lupdate-pro
%{_qtdir}/bin/pixeltool
%{_qtdir}/bin/qcollectiongenerator
%{_qtdir}/bin/qdbus
%{_qtdir}/bin/qdbusviewer
%{_qtdir}/bin/qdistancefieldgenerator
%{_qtdir}/bin/qdoc
%{_qtdir}/bin/qhelpgenerator
%{_qtdir}/bin/qtattributionsscanner
%{_qtdir}/bin/qtdiag
%{_qtdir}/bin/qtpaths
%{_qtdir}/bin/qtplugininfo
%{_qtdir}/examples/assistant
%{_qtdir}/examples/designer
%{_qtdir}/examples/help
%{_qtdir}/examples/linguist
%{_qtdir}/examples/plugins/designer
%{_qtdir}/examples/uitools
%{_qtdir}/include/QtDesigner
%{_qtdir}/include/QtDesignerComponents
%{_qtdir}/include/QtHelp
%{_qtdir}/include/QtTools
%{_qtdir}/include/QtUiPlugin
%{_qtdir}/include/QtUiTools
%{_qtdir}/lib/cmake/Qt%{major}BuildInternals/StandaloneTests/QtToolsTestsConfig.cmake
%{_qtdir}/lib/cmake/Qt%{major}Designer
%{_qtdir}/lib/cmake/Qt%{major}DesignerComponents
%{_qtdir}/lib/cmake/Qt%{major}Help
%{_qtdir}/lib/cmake/Qt%{major}Linguist
%{_qtdir}/lib/cmake/Qt%{major}LinguistTools
%{_qtdir}/lib/cmake/Qt%{major}Tools
%{_qtdir}/lib/cmake/Qt%{major}ToolsTools
%{_qtdir}/lib/cmake/Qt%{major}UiPlugin
%{_qtdir}/lib/cmake/Qt%{major}UiTools
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
%{_qtdir}/mkspecs/modules/qt_plugin_qquickwidget.pri
%{_qtdir}/modules/Designer.json
%{_qtdir}/modules/DesignerComponents.json
%{_qtdir}/modules/Help.json
%{_qtdir}/modules/Linguist.json
%{_qtdir}/modules/Tools.json
%{_qtdir}/modules/UiPlugin.json
%{_qtdir}/modules/UiTools.json
%{_qtdir}/plugins/designer/libqquickwidget.so
