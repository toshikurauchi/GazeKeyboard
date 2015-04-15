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
#include "EyeTribeListener.h"
#include "TobiiListener.h"

const QString KeyboardImageWindow::REC_DIR = "../data/recordings/";
const QString KeyboardImageWindow::EYE_TRIBE = "EyeTribe";
const QString KeyboardImageWindow::TOBII = "Tobii EyeX";

KeyboardImageWindow::KeyboardImageWindow(QWidget *parent) :
    QMainWindow(parent), ui(new Ui::KeyboardImageWindow), gazeListener(0), recording(false), noParticipantMessageBox(this)
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
    mouseListener = new MouseListener(this, gazeOverlay);
    // Create eye tracker options in menu
    actionEyeTrackerGroup = new QActionGroup(ui->menuEye_tracker);
    actionEyeTrackerGroup->setExclusive(true);
    QAction *actionEyeTribe = actionEyeTrackerGroup->addAction(EYE_TRIBE);
    actionEyeTribe->setCheckable(true);
    QAction *actionTobii = actionEyeTrackerGroup->addAction(TOBII);
    actionTobii->setCheckable(true);
    actionTobii->setChecked(true);
    connect(actionEyeTrackerGroup, SIGNAL(triggered(QAction*)), this, SLOT(updateGazeListener()));
    ui->menuEye_tracker->addActions(actionEyeTrackerGroup->actions());
    updateGazeListener();

    // Load words in combobox
    loadWordList();

    // Load layouts in combobox
    createLayoutsList();
    foreach (KeyboardLayout *layout, layouts)
    {
        ui->layoutsCombo->addItem(layout->name(), qVariantFromValue(layout));
    }

    // Create trial manager
    trialManager = new TrialManager(this, ui->participantEdit, ui->wordsCombo,
                                    ui->trialsSpinBox, ui->currentTrialSpinBox,
                                    ui->layoutsCombo, ui->useMouseCheck,
                                    ui->imageLabel, ui->trialCountLabel, REC_DIR,
                                    words, 20);

    // Create visualization manager
    vizManager = new VisualizationManager(this, ui->participantsComboViz, ui->modeComboViz,
                                          ui->layoutsComboViz, ui->wordsComboViz, ui->trialComboViz,
                                          ui->imageLabelViz, ui->showFixCheck, ui->fixRadSlider,
                                          ui->fixThreshSlider, ui->lineWidthSlider, ui->opacitySlider,
                                          ui->smoothVizCheck, REC_DIR, layouts);

    // Connect signals
    connect(ui->tabWidget, SIGNAL(currentChanged(int)), this, SLOT(loadVisualizations()));
    connect(ui->imageLabel, SIGNAL(rescaled(QSize, QRect)), gazeOverlay, SLOT(imageRescaled(QSize, QRect)));
    connect(ui->wordsCombo, SIGNAL(currentTextChanged(QString)), ui->recordingLight, SLOT(setWord(QString)));
    connect(ui->useMouseCheck, SIGNAL(toggled(bool)), this, SLOT(useMouseToggled(bool)));
    connect(ui->imageLabel, SIGNAL(mouseMoved(QPoint)), mouseListener, SLOT(mouseMoved(QPoint)));
    connect(ui->showPointerCheck, SIGNAL(toggled(bool)), gazeOverlay, SLOT(setShow(bool)));
    connect(trialManager, SIGNAL(paused()), ui->recordingLight, SLOT(hideWord()));
    useMouseToggled(ui->useMouseCheck->isChecked());
    gazeOverlay->setShow(ui->showPointerCheck->isChecked());
}

KeyboardImageWindow::~KeyboardImageWindow()
{
    delete ui;
    delete gazeListener;
    delete mouseListener;
    delete gazeOverlay;
    delete trialManager;
    delete vizManager;
    delete actionEyeTrackerGroup;
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
        if (trialManager->isPaused())
        {
            trialManager->resume();
            ui->recordingLight->setWord(ui->wordsCombo->currentText());
            ui->recordingLight->showWord();
        }
        else
        {
            toggleRecording();
        }
    }
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
    layouts.append(new KeyboardLayout("Phone", "../layout/SquaredPhone.bmp"));
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

void KeyboardImageWindow::loadVisualizations()
{
    if (ui->tabWidget->currentWidget() == ui->tabViz)
    {
        vizManager->loadVisualizations();
    }
}

void KeyboardImageWindow::updateGazeListener()
{
    if (gazeListener != 0) delete gazeListener;
    if (actionEyeTrackerGroup->checkedAction()->text() == EYE_TRIBE)
    {
        gazeListener = new EyeTribeListener(this, gazeOverlay);
    }
    else
    {
        gazeListener = new TobiiListener(this, gazeOverlay);
    }
}
