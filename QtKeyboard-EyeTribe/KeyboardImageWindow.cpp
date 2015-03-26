#include <QResizeEvent>
#include <QDebug>
#include <QFileDialog>
#include <QSettings>
#include <QQuickView>
#include <QQmlProperty>

#include "KeyboardImageWindow.h"
#include "ui_KeyboardImageWindow.h"

KeyboardImageWindow::KeyboardImageWindow(QWidget *parent) :
    QMainWindow(parent), ui(new Ui::KeyboardImageWindow)
{
    QCoreApplication::setOrganizationName("Boston University");
    QCoreApplication::setApplicationName("CameraMouseSuite");
    ui->setupUi(this);

    QQuickView *view = new QQuickView();
    view->setOpacity(0);
    view->setColor(palette().color(QPalette::Background));
    QWidget *container = QWidget::createWindowContainer(view, this);
    container->setMinimumSize(20, 20);
    container->setStyleSheet("background-color:black;");
    view->setSource(QUrl::fromLocalFile("RecordingLight.qml"));
    recLight = view->rootObject();
    ui->infoBar->insertWidget(0, container);

    readSettings();
    QPixmap pixmap("../src/Keyboard2b.png");
    ui->imageLabel->setPixmap(pixmap);
    gazeOverlay = new GazeOverlay(ui->imageLabel, 10);
    gazeListener = new GazeListener(this, gazeOverlay);

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
    if (ui->recordButton->text().toLower().contains("stop"))
    {
        ui->recordButton->setText("Record");
        gazeListener->stopRecording();
        recLight->setProperty("recording", false);
    }
    else
    {
        QString filename = QFileDialog::getSaveFileName(this, "Choose file name", recordingsDir, "*.csv");
        if (!filename.isEmpty())
        {
            ui->recordButton->setText("Stop");
            recordingsDir = QFileInfo(filename).absoluteDir().absolutePath();
            gazeListener->startRecording(filename);
            recLight->setProperty("recording", true);
        }
    }
}
