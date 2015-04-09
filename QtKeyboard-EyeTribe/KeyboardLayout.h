#ifndef KEYBOARDLAYOUT_H
#define KEYBOARDLAYOUT_H

#include <QObject>

class KeyboardLayout : public QObject
{
    Q_OBJECT
public:
    explicit KeyboardLayout(QObject *parent = 0);
    KeyboardLayout(QString name, QString filename, QObject *parent = 0);
    ~KeyboardLayout();

    QString name();
    QString trimmedName();
    QString filename();

private:
    QString m_name;
    QString m_filename;
};

#endif // KEYBOARDLAYOUT_H
