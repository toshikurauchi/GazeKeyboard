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

SOURCES += main.cpp\
    KeyboardImageWindow.cpp \
    QImageLabel.cpp \
    GazeOverlay.cpp \
    GazeListener.cpp \
    TrialManager.cpp \
    KeyboardLayout.cpp

HEADERS  += KeyboardImageWindow.h \
    QImageLabel.h \
    GazeOverlay.h \
    GazeListener.h \
    TrialManager.h \
    KeyboardLayout.h

FORMS    += KeyboardImageWindow.ui

OTHER_FILES += \
    README.md \
    RecordingLight.qml \
    words.txt

qmls.path   = $${OUT_PWD}
qmls.files += $${OTHER_FILES}
INSTALLS   += qmls
