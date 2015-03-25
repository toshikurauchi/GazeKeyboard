#include <QResizeEvent>
#include <QDebug>
#include <QFileDialog>

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
    gazeListener = new GazeListener(this, gazeOverlay);
    ui->recordingLabel->setStyleSheet("QLabel { color : red; }");

    connect(ui->recordButton, SIGNAL(clicked()), this, SLOT(toggleRecording()));
    connect(ui->imageLabel, SIGNAL(rescaled(QRect)), gazeOverlay, SLOT(imageRescaled(QRect)));
    connect(gazeListener, SIGNAL(newGaze(QPoint)), gazeOverlay, SLOT(newGaze(QPoint)));
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
        gazeListener->stopRecording();
    }
    else
    {
        QString filename = QFileDialog::getSaveFileName(this, "Choose file name", "../data/recordings/", "*.csv");
        if (!filename.isEmpty())
        {
            ui->recordingLabel->setText("Recording");
            ui->recordButton->setText("Stop");
            gazeListener->startRecording(filename);
        }
    }
    ui->recordingLabel->repaint();
}
