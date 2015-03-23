#include "KeyboardWindow.h"
#include "ui_KeyboardWindow.h"

KeyboardWindow::KeyboardWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::KeyboardWindow)
{
    ui->setupUi(this);
}

KeyboardWindow::~KeyboardWindow()
{
    delete ui;
}
