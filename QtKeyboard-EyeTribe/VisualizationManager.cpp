#include <QDir>
#include <QDebug>

#include "VisualizationManager.h"
#include "KeyboardLayout.h"

VisualizationManager::VisualizationManager(QObject *parent, QComboBox *participantsCombo,
                                           QComboBox *modesCombo, QComboBox *layoutsCombo,
                                           QComboBox *wordsCombo, QComboBox *trialsCombo,
                                           QImageLabel *imageLabel, QCheckBox *showFixCheck,
                                           QSlider *fixRadSlider, QSlider *fixThreshSlider,
                                           QSlider *lineWidthSlider, QSlider *opacitySlider,
                                           QCheckBox *smoothVizCheck, QString dataDirectory,
                                           QList<KeyboardLayout *> keyboardLayouts) :
    QObject(parent), participantsCombo(participantsCombo), modesCombo(modesCombo),
    layoutsCombo(layoutsCombo), wordsCombo(wordsCombo), trialsCombo(trialsCombo),
    imageLabel(imageLabel), showFixCheck(showFixCheck), fixRadSlider(fixRadSlider),
    fixThreshSlider(fixThreshSlider), lineWidthSlider(lineWidthSlider),
    opacitySlider(opacitySlider), smoothVizCheck(smoothVizCheck),
    dataDirPath(dataDirectory)
{
    foreach (KeyboardLayout *layout, keyboardLayouts)
    {
        this->keyboardLayouts[layout->trimmedName()] = layout;
    }

    modesList << "gaze" << "mouse";
    csvFilter << "*.csv";

    connect(participantsCombo, SIGNAL(currentTextChanged(QString)), this, SLOT(updateModes()));
    connect(modesCombo, SIGNAL(currentTextChanged(QString)), this, SLOT(updateLayouts()));
    connect(layoutsCombo, SIGNAL(currentTextChanged(QString)), this, SLOT(updateWords()));
    connect(wordsCombo, SIGNAL(currentTextChanged(QString)), this, SLOT(updateTrials()));
    connect(trialsCombo, SIGNAL(currentTextChanged(QString)), this, SLOT(updateVisualization()));
    connect(showFixCheck, SIGNAL(toggled(bool)), fixRadSlider, SLOT(setEnabled(bool)));
    connect(showFixCheck, SIGNAL(toggled(bool)), this, SLOT(updateVisualization()));
    connect(fixThreshSlider, SIGNAL(valueChanged(int)), this, SLOT(updateVisualization()));
    connect(fixRadSlider, SIGNAL(valueChanged(int)), this, SLOT(updateVisualization()));
    connect(lineWidthSlider, SIGNAL(valueChanged(int)), this, SLOT(updateVisualization()));
    connect(opacitySlider, SIGNAL(valueChanged(int)), this, SLOT(updateVisualization()));
    connect(smoothVizCheck, SIGNAL(toggled(bool)), this, SLOT(updateVisualization()));
}

void VisualizationManager::loadVisualizations()
{
    data.clear();
    QDir dataDir(dataDirPath);
    if (dataDir.exists())
    {
        QStringList participantDirs = dataDir.entryList();
        foreach (QString participant, participantDirs)
        {
            QDir participantDir(dataDir.absoluteFilePath(participant));
            QStringList modeDirs = participantDir.entryList(modesList);
            foreach (QString mode, modeDirs)
            {
                QDir modeDir(participantDir.absoluteFilePath(mode));
                QStringList layoutDirs = modeDir.entryList(keyboardLayouts.keys());
                foreach (QString layout, layoutDirs)
                {
                    QDir layoutDir(modeDir.absoluteFilePath(layout));
                    QStringList wordFiles = layoutDir.entryList(csvFilter);
                    foreach (QString wordFile, wordFiles)
                    {
                        QRegularExpressionMatch match = QRegularExpression("(?<word>.*)(?<trial>[0-9]+).csv").match(wordFile);
                        QString word = match.captured("word");
                        QString trial = match.captured("trial");
                        QString path = layoutDir.absoluteFilePath(wordFile);
                        data[participant][mode][layout][word][trial] = path;
                    }
                }
            }
        }
    }
    participantsCombo->clear();
    participantsCombo->addItems(participants());
    updateModes();
}

QStringList VisualizationManager::participants()
{
    QStringList participantList;
    foreach (QString participant, data.keys())
    {
        if (!participant.isEmpty()) participantList << participant;
    }
    return participantList;
}

QStringList VisualizationManager::modes(QString participant)
{
    QStringList modeList;
    foreach (QString mode, data[participant].keys())
    {
        if (!mode.isEmpty()) modeList << mode;
    }
    return modeList;
}

QStringList VisualizationManager::layouts(QString participant, QString mode)
{
    QStringList layoutList;
    foreach (QString layout, data[participant][mode].keys())
    {
        if (!layout.isEmpty()) layoutList << layout;
    }
    return layoutList;
}

QStringList VisualizationManager::words(QString participant, QString mode, QString layout)
{
    QStringList wordList;
    foreach (QString word, data[participant][mode][layout].keys())
    {
        if (!word.isEmpty()) wordList << word;
    }
    return wordList;
}

QStringList VisualizationManager::trials(QString participant, QString mode, QString layout, QString word)
{
    QStringList trialList;
    foreach (QString trial, data[participant][mode][layout][word].keys())
    {
        if (!trial.isEmpty()) trialList << trial;
    }
    return trialList;
}

void VisualizationManager::updateModes()
{
    modesCombo->clear();
    modesCombo->addItems(modes(participantsCombo->currentText()));
}

void VisualizationManager::updateLayouts()
{
    layoutsCombo->clear();
    layoutsCombo->addItems(layouts(participantsCombo->currentText(),
                                   modesCombo->currentText()));
}

void VisualizationManager::updateWords()
{
    wordsCombo->clear();
    wordsCombo->addItems(words(participantsCombo->currentText(),
                               modesCombo->currentText(),
                               layoutsCombo->currentText()));
}

void VisualizationManager::updateTrials()
{
    trialsCombo->clear();
    trialsCombo->addItems(trials(participantsCombo->currentText(),
                                 modesCombo->currentText(),
                                 layoutsCombo->currentText(),
                                 wordsCombo->currentText()));
}

void VisualizationManager::updateVisualization()
{
    // Load data
    QString participant = participantsCombo->currentText();
    QString mode = modesCombo->currentText();
    QString layoutName = layoutsCombo->currentText();
    QString word = wordsCombo->currentText();
    QString trial = trialsCombo->currentText();
    if (participant.isEmpty() || mode.isEmpty() || layoutName.isEmpty() ||
        word.isEmpty() || trial.isEmpty()) return;

    QString dataFile = data[participant][mode][layoutName][word][trial];
    bool loaded = plotter.loadData(dataFile, mode.compare("gaze") == 0);

    // Draw scanpath
    KeyboardLayout *layout = keyboardLayouts[layoutName];
    QPixmap pixmap(layout->filename());
    bool smooth = smoothVizCheck->isChecked();
    float fixThresh = fixThreshSlider->value()/1000.0f;
    float fixRad = 0;
    if (showFixCheck->isChecked()) fixRad = fixRadSlider->value()/1000.0f;
    float lineWidthPercent = lineWidthSlider->value()/1000.0f;
    float opacity = opacitySlider->value()/100.0f;
    if (loaded) plotter.plot(pixmap, smooth, fixThresh, fixRad, opacity, lineWidthPercent);

    // Show image
    imageLabel->setPixmap(pixmap);
    imageLabel->update();
}
