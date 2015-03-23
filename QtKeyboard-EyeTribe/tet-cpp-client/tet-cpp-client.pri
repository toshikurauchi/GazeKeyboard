DEPENDPATH += $$PWD/src

INCLUDEPATH += $$PWD/include \
               $$(BOOST_DIR)

LIBS += -L$$(BOOST_LIB)

HEADERS += $$PWD/include/*.h
SOURCES += $$PWD/src/*.cpp
