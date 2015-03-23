#include "KeyboardImageWindow.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    KeyboardImageWindow w;
    w.show();

    return a.exec();
}
