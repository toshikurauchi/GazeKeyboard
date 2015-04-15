#-------------------------------------------------
#
# Project created by QtCreator 2015-03-23T15:07:49
#
#-------------------------------------------------

QT       += core gui quick

include(tet-cpp-client/tet-cpp-client.pri)

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = QtKeyboard-EyeTribe
TEMPLATE = app

INCLUDEPATH += $$PWD/include

SOURCES += main.cpp\
    KeyboardImageWindow.cpp \
    QImageLabel.cpp \
    GazeOverlay.cpp \
    TrialManager.cpp \
    KeyboardLayout.cpp \
    RecordingLight.cpp \
    MouseListener.cpp \
    GazeListener.cpp \
    VisualizationManager.cpp \
    ScanpathPlotter.cpp \
    EyeTribeListener.cpp \
    TobiiListener.cpp

HEADERS  += KeyboardImageWindow.h \
    QImageLabel.h \
    GazeOverlay.h \
    GazeListener.h \
    TrialManager.h \
    KeyboardLayout.h \
    RecordingLight.h \
    MouseListener.h \
    IDataRecorder.h \
    VisualizationManager.h \
    ScanpathPlotter.h \
    EyeTribeListener.h \
    TobiiListener.h

FORMS    += KeyboardImageWindow.ui

OTHER_FILES += \
    README.md \
    words.txt

qmls.path   = $${OUT_PWD}
qmls.files += $${OTHER_FILES}
dlls.path   = $${OUT_PWD}
win32 {
    !contains(QMAKE_TARGET.arch, x86_64) {
        ## Windows x86 (32bit)
        message("x86 build")
        dlls.files += $$PWD/lib/x86/Tobii.EyeX.Client.dll
        LIBS += -L$$PWD/lib/x86/ -lTobii.EyeX.Client
    } else {
        ## Windows x64 (64bit)
        message("x86_64 build")
        dlls.files += $$PWD/lib/x64/Tobii.EyeX.Client.dll
        LIBS += -L$$PWD/lib/x64/ -lTobii.EyeX.Client
    }
}
INSTALLS   += qmls dlls
