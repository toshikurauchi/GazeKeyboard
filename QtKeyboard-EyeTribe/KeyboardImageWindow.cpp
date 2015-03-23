#include <QResizeEvent>
#include <QDebug>

#include "KeyboardImageWindow.h"
#include "ui_KeyboardImageWindow.h"

KeyboardImageWindow::KeyboardImageWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::KeyboardImageWindow)
{
    ui->setupUi(this);
    QPixmap pixmap("../src/Keyboard2b.png");
    ui->imageLabel->setPixmap(pixmap);
    gazeOverlay = new GazeOverlay(ui->imageLabel, 10);
    gazeListener = new GazeListener(gazeOverlay);
    ui->recordingLabel->setStyleSheet("QLabel { color : red; }");

    connect(ui->recordButton, SIGNAL(clicked()), this, SLOT(toggleRecording()));
    connect(ui->imageLabel, SIGNAL(resized(QSize)), gazeOverlay, SLOT(imageResized(QSize)));
}

KeyboardImageWindow::~KeyboardImageWindow()
{
    delete ui;
    delete gazeListener;
    delete gazeOverlay;
}

void KeyboardImageWindow::toggleRecording()
{
    if (ui->recordingLabel->text().toLower().contains("recording"))
    {
        ui->recordingLabel->setText("");
        ui->recordButton->setText("Record");
    }
    else
    {
        ui->recordingLabel->setText("Recording");
        ui->recordButton->setText("Stop");
    }
    ui->recordingLabel->repaint();
}
