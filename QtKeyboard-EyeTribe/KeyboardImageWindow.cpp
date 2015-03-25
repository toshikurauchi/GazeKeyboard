#include <QResizeEvent>
#include <QDebug>
#include <QFileDialog>
#include <QSettings>

#include "KeyboardImageWindow.h"
#include "ui_KeyboardImageWindow.h"

KeyboardImageWindow::KeyboardImageWindow(QWidget *parent) :
    QMainWindow(parent), ui(new Ui::KeyboardImageWindow)
{
    QCoreApplication::setOrganizationName("Boston University");
    QCoreApplication::setApplicationName("CameraMouseSuite");
    ui->setupUi(this);

    readSettings();
    QPixmap pixmap("../src/Keyboard2b.png");
    ui->imageLabel->setPixmap(pixmap);
    gazeOverlay = new GazeOverlay(ui->imageLabel, 10);
    gazeListener = new GazeListener(this, gazeOverlay);
    ui->recordingLabel->setStyleSheet("QLabel { color : red; }");

    connect(ui->recordButton, SIGNAL(clicked()), this, SLOT(toggleRecording()));
    connect(ui->imageLabel, SIGNAL(rescaled(QSize, QRect)), gazeOverlay, SLOT(imageRescaled(QSize, QRect)));
    connect(gazeListener, SIGNAL(newGaze(QPoint)), gazeOverlay, SLOT(newGaze(QPoint)));
}

KeyboardImageWindow::~KeyboardImageWindow()
{
    delete ui;
    delete gazeListener;
    delete gazeOverlay;
}

void KeyboardImageWindow::closeEvent(QCloseEvent *event)
{
    Q_UNUSED(event);
    writeSettings();
}

void KeyboardImageWindow::readSettings()
{
    QSettings settings;
    recordingsDir = settings.value("recordDir", "../data/recordings/").toString();
}

void KeyboardImageWindow::writeSettings()
{
    QSettings settings;
    settings.setValue("recordDir", recordingsDir);
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
        QString filename = QFileDialog::getSaveFileName(this, "Choose file name", recordingsDir, "*.csv");
        if (!filename.isEmpty())
        {
            ui->recordingLabel->setText("Recording");
            ui->recordButton->setText("Stop");
            recordingsDir = QFileInfo(filename).absoluteDir().absolutePath();
            gazeListener->startRecording(filename);
        }
    }
    ui->recordingLabel->repaint();
}
