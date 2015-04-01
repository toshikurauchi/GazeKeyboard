#include <QResizeEvent>
#include <QDebug>
#include <QFileDialog>
#include <QSettings>
#include <QQuickView>
#include <QQmlProperty>

#include "KeyboardImageWindow.h"
#include "ui_KeyboardImageWindow.h"

const QString KeyboardImageWindow::REC_DIR = "../data/recordings/";

KeyboardImageWindow::KeyboardImageWindow(QWidget *parent) :
    QMainWindow(parent), ui(new Ui::KeyboardImageWindow), recording(false), noParticipantMessageBox(this)
{
    // Setup application
    QCoreApplication::setOrganizationName("Boston University");
    QCoreApplication::setApplicationName("CameraMouseSuite");
    ui->setupUi(this);
    setFocusPolicy(Qt::StrongFocus);

    // Create recording light
    QQuickView *view = new QQuickView();
    view->setOpacity(0);
    view->setColor(palette().color(QPalette::Background));
    QWidget *container = QWidget::createWindowContainer(view, this);
    container->setStyleSheet("background-color:black;");
    view->setSource(QUrl::fromLocalFile("RecordingLight.qml"));
    recLight = view->rootObject();
    ui->infoBar->insertWidget(0, container);
    container->setMinimumSize(recLight->property("width").toInt(), recLight->property("height").toInt());
    recLight->setProperty("recording", recording);

    // Setup message box (to show up when no participant id was set)
    noParticipantMessageBox.setText("You must type a participant ID to start recording");

    // Load settings
    readSettings();
    // Create gaze overlay and listener
    gazeOverlay = new GazeOverlay(ui->imageLabel, 10);
    gazeListener = new GazeListener(this, gazeOverlay);

    // Load words in combobox
    loadWordList();
    ui->wordsCombo->addItems(words);

    // Load layouts in combobox
    createLayoutsList();
    foreach (KeyboardLayout *layout, layouts)
    {
        ui->layoutsCombo->addItem(layout->name(), qVariantFromValue(layout));
    }
    changeLayout(ui->layoutsCombo->currentIndex());

    // Create trial manager
    trialManager = new TrialManager(this, ui->participantEdit, ui->wordsCombo, ui->trialsSpinBox, ui->currentTrialSpinBox, REC_DIR);

    // Connect signals
    connect(ui->imageLabel, SIGNAL(rescaled(QSize, QRect)), gazeOverlay, SLOT(imageRescaled(QSize, QRect)));
    connect(gazeListener, SIGNAL(newGaze(QPoint)), gazeOverlay, SLOT(newGaze(QPoint)));
    connect(ui->layoutsCombo, SIGNAL(currentIndexChanged(int)), this, SLOT(changeLayout(int)));
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
            if (!word.isEmpty()) words.append(word);
        }
        wordsFile.close();
    }
}

void KeyboardImageWindow::createLayoutsList()
{
    layouts.clear();
    layouts.append(new KeyboardLayout("QWERTY", "../src/Keyboard2a.png"));
    layouts.append(new KeyboardLayout("Phone", "../src/Keyboard-phone.jpg"));
    layouts.append(new KeyboardLayout("Circ-AB", "../src/Keyboard-circ.jpg"));
}

void KeyboardImageWindow::toggleRecording()
{
    if (recording)
    {
        gazeListener->stopRecording();
        recLight->setProperty("recording", false);
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
            gazeListener->startRecording(filename);
            recLight->setProperty("recording", true);
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
