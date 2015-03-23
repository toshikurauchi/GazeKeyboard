#include <QResizeEvent>

#include "KeyboardImageWindow.h"
#include "ui_KeyboardImageWindow.h"

KeyboardImageWindow::KeyboardImageWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::KeyboardImageWindow)
{
    ui->setupUi(this);
    QPixmap pixmap("../src/Keyboard2b.png");
    ui->imageLabel->setPixmap(pixmap);
    gazeOverlay = new GazeOverlay(ui->centralwidget, 10);
    gazeListener = new GazeListener(gazeOverlay);
}

KeyboardImageWindow::~KeyboardImageWindow()
{
    delete ui;
    delete gazeListener;
    delete gazeOverlay;
}

void KeyboardImageWindow::resizeEvent(QResizeEvent *event)
{
    gazeOverlay->resize(event->size());
    event->accept();
}
