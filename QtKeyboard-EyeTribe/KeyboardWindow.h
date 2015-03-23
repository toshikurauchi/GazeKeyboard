#ifndef KEYBOARDWINDOW_H
#define KEYBOARDWINDOW_H

#include <QMainWindow>

namespace Ui {
class KeyboardWindow;
}

class KeyboardWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit KeyboardWindow(QWidget *parent = 0);
    ~KeyboardWindow();

private:
    Ui::KeyboardWindow *ui;
};

#endif // KEYBOARDWINDOW_H
