DEPENDPATH += $$PWD/src

INCLUDEPATH += $$PWD/include \
               $$(BOOST_DIR)

DEFINES += BOOST_SYSTEM_NO_DEPRECATED

LIBS += -L$$(BOOST_LIB)

HEADERS += $$PWD/include/*.h \
    $$PWD/src/*.hpp
SOURCES += $$PWD/src/*.cpp
