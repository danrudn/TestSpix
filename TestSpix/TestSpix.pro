QT += quick scxml

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
        main.cpp \
        viewcontroller.cpp

HEADERS += \
        viewcontroller.h

RESOURCES += qml.qrc


# Add Spix
SPIX_PREFIX = $$PWD/libs/spix/install
SPIX_INCDIR = $$SPIX_PREFIX/include
SPIX_LIBDIR = $$SPIX_PREFIX/lib

# Add AnyRPC
ANYRPC_PREFIX = $$PWD/libs/anyrpc
ANYRPC_INCDIR = $$ANYRPC_PREFIX/include
ANYRPC_LIBDIR = $$ANYRPC_PREFIX/build/bin

INCLUDEPATH += $$SPIX_INCDIR $$ANYRPC_INCDIR
LIBS += -L$$SPIX_LIBDIR \
        -lSpixCore \
        -lSpixQtQuick \
        -L$$ANYRPC_LIBDIR \
        -lanyrpc

# Linux runtime path
QMAKE_RPATHDIR += $$SPIX_LIBDIR $$ANYRPC_LIBDIR


# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH =

# Additional import path used to resolve QML modules just for Qt Quick Designer
QML_DESIGNER_IMPORT_PATH =

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

STATECHARTS += \
    statechart.scxml

DISTFILES +=

HEADERS += \
    viewcontroller.h
