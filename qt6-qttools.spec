#define beta rc2
# QtDeclarative has a BR on linguist tools, but
# QtTools has a BR on QtDeclarative...
# Allow a bootstrap build without Declarative bits
# and pieces.
%bcond_with bootstrap

Name:		qt6-qttools
Version:	6.7.1
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qttools-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qttools-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Patch0:		qttools-6.0.0-clang-linkage.patch
Patch1:		qttools-6.7.0-zstd-detection.patch
Group:		System/Libraries
Summary:	Qt %{qtmajor} Tools
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	llvm-bolt
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6OpenGL)
BuildRequires:	cmake(Qt6OpenGLWidgets)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	%mklibname zstd -s -d
%if ! %{with bootstrap}
BuildRequires:	cmake(Qt6Qml)
BuildRequires:	cmake(Qt6QmlModels)
BuildRequires:	cmake(Qt6QmlTools)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:	qt6-qtdeclarative
%endif
BuildRequires:	qt6-cmake
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(xkbcommon)
BuildRequires:	pkgconfig(vulkan)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	spirv-llvm-translator
BuildRequires:	cmake(LLVM)
BuildRequires:	cmake(Clang)
BuildRequires:	llvm-static-devel
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{qtmajor} tools

%package assistant
Summary:	Qt Assistant - a help file viewer
Group:		Development/Tools

%description assistant
Qt Assistant - a help file viewer

%package dbus
Summary:	Command line tool for talking to DBus
Group:		Development/Tools

%description dbus
Command line tool for talking to DBus

%package dbusviewer
Summary:	Graphical tool for talking to DBus
Group:		Development/Tools

%description dbusviewer
Graphical tool for talking to DBus

%package designer
Summary:	Qt Designer - a graphical UI builder
Group:		Development/Tools

%description designer
Qt Designer - a graphical UI builder

%package distancefieldgenerator
Summary:	Qt Distance Field Generator - font cache builder
Group:		Development/Tools
Url:		https://doc.qt.io/qt-6/qtdistancefieldgenerator-index.html

%description distancefieldgenerator
If the user interface of an application has a lot of text, it may cause a
small, but noticeable, performance impact the first time it is displayed to
the user. This is especially true if the text is rendered in multiple
different fonts or use a large amount of distinct characters (common for
instance in writing systems such as Hanzi, written Chinese).

The reason is that in order to render the text efficiently later, Qt will
spend some time creating graphical assets for each of the glyphs that will
later be reused. This happens the first time a glyph is displayed in the
scene.

For advanced users who want to optimize startup performance, it is possible
to pregenerate this font cache, as long as Text.QtRendering is the rendering
type in use. The Qt Distance Field Generator tool can be used to pregenerate
the cache, either for all glyphs in the fonts, or just a selection that are
known to be displayed during a critical phase.

%package linguist
Summary:	Qt Linguist - a frontend for translating software
Group:		Development/Tools
Requires:	%{name}-linguist-tools = %{EVRD}

%description linguist
Qt Linguist - a frontend for translating software

%package linguist-tools
Summary:	Tools for working with translation files generated by Qt Linguist
Group:		Development/Tools

%description linguist-tools
Tools for working with translation files generated by Qt Linguist

%package examples
Summary:	Examples demonstrating the use of Qt Tools
Group:		Development/Tools

%description examples
Examples demonstrating the use of Qt Tools

%package devel
Summary:	Development files for working with Qt Tools
Group:		Development/KDE and Qt
Requires:	%{name}-doc = %{EVRD}
Requires:	%{name}-linguist-tools = %{EVRD}
# qhelpgenerator's qch files are, in fact, sqlite
# databases - written to by QSql
Requires:	qt6-qtbase-sql-sqlite

%description devel
Development files for working with Qt Tools

%package doc
Summary:	Documentation generator for Qt
Group:		Development/Tools
Provides:	qdoc = %{EVRD}

%description doc
Documentation generator for Qt

%qt6libs Designer DesignerComponents Help UiTools

%prep
%autosetup -p1 -n qttools%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON \
	--log-level=STATUS

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall

%files assistant
%{_qtdir}/bin/assistant

%files designer
%{_qtdir}/bin/designer
%{_qtdir}/plugins/designer

%files linguist
%{_qtdir}/bin/linguist

%files linguist-tools
%{_qtdir}/bin/lconvert
%{_qtdir}/bin/lrelease
%{_qtdir}/bin/lupdate
%{_qtdir}/libexec/lprodump
%{_qtdir}/libexec/lrelease-pro
%{_qtdir}/libexec/lupdate-pro
# This may be mixing -devel files and non-devel
# files in a single package, but given lconvert,
# lrelease and lupdate are virtually never used
# outside of a -devel context, it is the right
# thing to do
%{_qtdir}/modules/Linguist.json
%{_qtdir}/lib/cmake/Qt6LinguistTools
%{_libdir}/pkgconfig/Qt6Linguist.pc
%{_qtdir}/mkspecs/modules/qt_lib_linguist.pri
%{_qtdir}/lib/cmake/Qt6Linguist

%files dbus
%{_qtdir}/bin/qdbus

%files dbusviewer
%{_qtdir}/bin/qdbusviewer

%files doc
%{_qtdir}/bin/qdoc

%files
%{_qtdir}/bin/pixeltool
%{_qtdir}/bin/qtdiag
%{_qtdir}/bin/qtdiag6
%{_qtdir}/bin/qtplugininfo
%dir %{_qtdir}/phrasebooks
%lang(da) %{_qtdir}/phrasebooks/danish.qph
%lang(nl) %{_qtdir}/phrasebooks/dutch.qph
%lang(fi) %{_qtdir}/phrasebooks/finnish.qph
%lang(fr) %{_qtdir}/phrasebooks/french.qph
%lang(de) %{_qtdir}/phrasebooks/german.qph
%lang(hu) %{_qtdir}/phrasebooks/hungarian.qph
%lang(it) %{_qtdir}/phrasebooks/italian.qph
%lang(ja) %{_qtdir}/phrasebooks/japanese.qph
%lang(no) %{_qtdir}/phrasebooks/norwegian.qph
%lang(pl) %{_qtdir}/phrasebooks/polish.qph
%lang(ru) %{_qtdir}/phrasebooks/russian.qph
%lang(es) %{_qtdir}/phrasebooks/spanish.qph
%lang(sv) %{_qtdir}/phrasebooks/swedish.qph

%if ! %{with bootstrap}
%files distancefieldgenerator
%{_qtdir}/bin/qdistancefieldgenerator
%endif

%files examples
%{_qtdir}/examples/assistant
%{_qtdir}/examples/designer
%{_qtdir}/examples/help
%{_qtdir}/examples/linguist
%{_qtdir}/examples/uitools

%files devel
%{_qtdir}/include/QtQDocCatchConversions
%{_qtdir}/include/QtQDocCatchGenerators
%{_qtdir}/include/QtTools
%{_qtdir}/include/QtUiPlugin
%{_qtdir}/lib/cmake/Qt6/FindWrapLibClang.cmake
%{_qtdir}/lib/cmake/Qt6BuildInternals/StandaloneTests/QtToolsTestsConfig.cmake
%{_qtdir}/lib/cmake/Qt6QDocCatchConversionsPrivate
%{_qtdir}/lib/cmake/Qt6QDocCatchGeneratorsPrivate
%{_qtdir}/lib/cmake/Qt6Tools
%{_qtdir}/lib/cmake/Qt6ToolsTools
%{_qtdir}/lib/cmake/Qt6UiPlugin
%{_qtdir}/mkspecs/modules/qt_lib_qdoccatchconversions_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_qdoccatchgenerators_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_tools_private.pri
%{_qtdir}/mkspecs/modules/qt_lib_uiplugin.pri
%{_qtdir}/libexec/qhelpgenerator
%{_qtdir}/libexec/qtattributionsscanner
%{_qtdir}/modules/QDocCatchConversionsPrivate.json
%{_qtdir}/modules/QDocCatchGeneratorsPrivate.json
%{_qtdir}/modules/Tools.json
%{_qtdir}/modules/UiPlugin.json
%{_libdir}/pkgconfig/Qt6UiPlugin.pc
%{_qtdir}/include/QtQDocCatch
%{_qtdir}/lib/cmake/Qt6QDocCatchPrivate
%{_qtdir}/mkspecs/modules/qt_lib_qdoccatch_private.pri
%{_qtdir}/modules/QDocCatchPrivate.json
