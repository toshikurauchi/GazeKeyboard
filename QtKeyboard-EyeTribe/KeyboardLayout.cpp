#include "KeyboardLayout.h"

KeyboardLayout::KeyboardLayout(QObject *parent) : QObject(parent)
{
}

KeyboardLayout::KeyboardLayout(QString name, QString filename, QObject *parent) :
    QObject(parent), m_name(name), m_filename(filename)
{
}

KeyboardLayout::~KeyboardLayout()
{
}

QString KeyboardLayout::name()
{
    return m_name;
}

QString KeyboardLayout::filename()
{
    return m_filename;
}
