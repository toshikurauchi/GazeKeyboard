#-------------------------------------------------
#
# Project created by QtCreator 2015-03-23T15:07:49
#
#-------------------------------------------------

QT       += core gui

include(tet-cpp-client/tet-cpp-client.pri)

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = QtKeyboard-EyeTribe
TEMPLATE = app


SOURCES += main.cpp\
    KeyboardWindow.cpp \
    KeyboardImageWindow.cpp \
    QImageLabel.cpp \
    GazeOverlay.cpp \
    GazeListener.cpp

HEADERS  += KeyboardImageWindow.h \
    KeyboardWindow.h \
    QImageLabel.h \
    GazeOverlay.h \
    GazeListener.h

FORMS    += KeyboardImageWindow.ui \
    KeyboardWindow.ui
