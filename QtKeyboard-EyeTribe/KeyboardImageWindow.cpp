#include <QResizeEvent>
#include <QDebug>
#include <QFileDialog>
#include <QSettings>
#include <QQuickView>
#include <QQmlProperty>
#include <QMouseEvent>

#include "KeyboardImageWindow.h"
#include "ui_KeyboardImageWindow.h"
#include "IDataRecorder.h"

const QString KeyboardImageWindow::REC_DIR = "../data/recordings/";

KeyboardImageWindow::KeyboardImageWindow(QWidget *parent) :
    QMainWindow(parent), ui(new Ui::KeyboardImageWindow), recording(false), noParticipantMessageBox(this)
{
    // Setup application
    QCoreApplication::setOrganizationName("Boston University");
    QCoreApplication::setApplicationName("CameraMouseSuite");
    ui->setupUi(this);
    setFocusPolicy(Qt::StrongFocus);

    // Setup message box (to show up when no participant id was set)
    noParticipantMessageBox.setText("You must type a participant ID to start recording");

    // Load settings
    readSettings();
    // Create gaze overlay and listener
    gazeOverlay = new GazeOverlay(ui->imageLabel, 10);
    gazeListener = new GazeListener(this, gazeOverlay);
    mouseListener = new MouseListener(this, gazeOverlay);

    // Set mouse movement tracking to true
    centralWidget()->setMouseTracking(true);
    gazeOverlay->setMouseTracking(true);
    ui->imageLabel->setMouseTracking(true);
    setMouseTracking(true);

    // Load words in combobox
    loadWordList();

    // Load layouts in combobox
    createLayoutsList();
    foreach (KeyboardLayout *layout, layouts)
    {
        ui->layoutsCombo->addItem(layout->name(), qVariantFromValue(layout));
    }
    changeLayout(ui->layoutsCombo->currentIndex());

    // Create trial manager
    trialManager = new TrialManager(this, ui->participantEdit, ui->wordsCombo,
                                    ui->trialsSpinBox, ui->currentTrialSpinBox,
                                    ui->layoutsCombo, ui->useMouseCheck, REC_DIR, words);
    ui->recordingLight->setWord(ui->wordsCombo->currentText());

    // Connect signals
    connect(ui->imageLabel, SIGNAL(rescaled(QSize, QRect)), gazeOverlay, SLOT(imageRescaled(QSize, QRect)));
    connect(ui->layoutsCombo, SIGNAL(currentIndexChanged(int)), this, SLOT(changeLayout(int)));
    connect(ui->wordsCombo, SIGNAL(currentTextChanged(QString)), ui->recordingLight, SLOT(setWord(QString)));
    connect(ui->useMouseCheck, SIGNAL(toggled(bool)), this, SLOT(useMouseToggled(bool)));
    connect(ui->showPointerCheck, SIGNAL(toggled(bool)), gazeOverlay, SLOT(setShow(bool)));
    useMouseToggled(ui->useMouseCheck->isChecked());
}

KeyboardImageWindow::~KeyboardImageWindow()
{
    delete ui;
    delete gazeListener;
    delete gazeOverlay;
    delete trialManager;
    foreach (KeyboardLayout *layout, layouts)
    {
        delete layout;
    }
}

void KeyboardImageWindow::closeEvent(QCloseEvent *event)
{
    Q_UNUSED(event);
    writeSettings();
}

void KeyboardImageWindow::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Space)
    {
        toggleRecording();
    }
}

void KeyboardImageWindow::mouseMoveEvent(QMouseEvent *mouseEvent)
{
    mouseListener->mouseMoved(mapToGlobal(mouseEvent->pos()));
}


void KeyboardImageWindow::readSettings()
{
    QSettings settings;
    ui->participantEdit->setText(settings.value("participant", "").toString());
    ui->trialsSpinBox->setValue(settings.value("trials", 1).toInt());
}

void KeyboardImageWindow::writeSettings()
{
    QSettings settings;
    settings.setValue("participant", ui->participantEdit->text());
    settings.setValue("trials", ui->trialsSpinBox->value());
}

void KeyboardImageWindow::loadWordList()
{
    QFile wordsFile("words.txt");
    if (wordsFile.open(QIODevice::ReadOnly))
    {
        QTextStream in(&wordsFile);
        while (!in.atEnd())
        {
            QString word = in.readLine();
            if (!word.isEmpty()) words.push_back(word.toStdString());
        }
        wordsFile.close();
    }
}

void KeyboardImageWindow::createLayoutsList()
{
    layouts.clear();
    layouts.append(new KeyboardLayout("Double Ring", "../layout/DoubleRing.bmp"));
    layouts.append(new KeyboardLayout("QWERTY", "../layout/QWERTY.bmp"));
    layouts.append(new KeyboardLayout("Single Ring", "../layout/SingleRing.bmp"));
    layouts.append(new KeyboardLayout("Squared Phone", "../layout/SquaredPhone.bmp"));
}

void KeyboardImageWindow::toggleRecording()
{
    IDataRecorder *currentRecorder;
    if (ui->useMouseCheck->isChecked()) currentRecorder = mouseListener;
    else currentRecorder = gazeListener;
    if (recording)
    {
        currentRecorder->stopRecording();
        ui->recordingLight->setRecording(false);
        trialManager->updateTrial();
        recording = false;
    }
    else
    {
        QString filename = trialManager->currentFile();
        if (filename.isEmpty())
        {
            noParticipantMessageBox.show();
        }
        else
        {
            currentRecorder->startRecording(filename);
            ui->recordingLight->setRecording(true);
            recording = true;
        }
    }
}

void KeyboardImageWindow::changeLayout(int layoutIdx)
{
    KeyboardLayout *layout = qvariant_cast<KeyboardLayout *>(ui->layoutsCombo->itemData(layoutIdx));
    QPixmap pixmap(layout->filename());
    ui->imageLabel->setPixmap(pixmap);
    ui->imageLabel->update();
}

void KeyboardImageWindow::useMouseToggled(bool useMouse)
{
    IDataRecorder *prevRecorder;
    if (useMouse)
    {
        prevRecorder = gazeListener;
        disconnect(gazeListener, SIGNAL(newGaze(QPoint)), gazeOverlay, SLOT(newGaze(QPoint)));
        connect(mouseListener, SIGNAL(newMousePos(QPoint)), gazeOverlay, SLOT(newGaze(QPoint)));
    }
    else
    {
        prevRecorder = mouseListener;
        disconnect(mouseListener, SIGNAL(newMousePos(QPoint)), gazeOverlay, SLOT(newGaze(QPoint)));
        connect(gazeListener, SIGNAL(newGaze(QPoint)), gazeOverlay, SLOT(newGaze(QPoint)));
    }
    if (prevRecorder->isRecording()) prevRecorder->stopRecording();
}
