#include <QDir>
#include <QDebug>

#include "TrialManager.h"

const int TrialManager::MAX_TRIALS = 100;

TrialManager::TrialManager(QObject *parent, QLineEdit *participantEdit,
                           QComboBox *wordsCombo, QSpinBox *trialsSpinBox,
                           QSpinBox *currentTrialSpinBox, QComboBox *layoutsCombo, QString dataDirectory) :
    QObject(parent), participantEdit(participantEdit), wordsCombo(wordsCombo), trialsSpinBox(trialsSpinBox),
    currentTrialSpinBox(currentTrialSpinBox), layoutsCombo(layoutsCombo), dataDir(dataDirectory)
{
    connect(participantEdit, SIGNAL(textChanged(QString)), this, SLOT(updateDir()));
    connect(wordsCombo, SIGNAL(currentIndexChanged(QString)), this, SLOT(updateTrialForWord(QString)));
    connect(trialsSpinBox, SIGNAL(valueChanged(int)), this, SLOT(updateTrial()));
    connect(layoutsCombo, SIGNAL(currentIndexChanged(int)), this, SLOT(updateDir()));

    if (!dataDir.exists()) QDir().mkpath(dataDirectory);
    updateDir();
    updateTrial();
}

QString TrialManager::currentFile()
{
    QString participant = participantEdit->text();
    if (participant.isEmpty())
    {
        return "";
    }
    if (!currentDir.exists()) QDir().mkpath(currentDir.absolutePath());
    QString filename = wordsCombo->currentText() +
            QString::number(currentTrialSpinBox->value()) + ".csv";
    return currentDir.absoluteFilePath(filename);
}

void TrialManager::updateTrial()
{
    if (currentDir.exists())
    {
        int trials = trialsSpinBox->value();
        for (int i = 0; i < wordsCombo->count(); i++)
        {
            QString word = wordsCombo->itemText(i);
            int trial = trialForWord(word);
            if (trial <= trials)
            {
                currentTrialSpinBox->setValue(trial);
                wordsCombo->setCurrentIndex(i);
                return;
            }
        }
        updateTrialForWord(wordsCombo->currentText());
    }
    else
    {
        currentTrialSpinBox->setValue(1);
        wordsCombo->setCurrentIndex(0);
    }
}

void TrialManager::updateTrialForWord(QString word)
{
    currentTrialSpinBox->setValue(trialForWord(word));
}

void TrialManager::updateDir()
{
    QString participant = participantEdit->text();
    if (participant.isEmpty())
    {
        currentDir = QDir();
    }
    else
    {
        currentDir = QDir(dataDir.absoluteFilePath(participant));
        currentDir = QDir(currentDir.absoluteFilePath(currentLayout()->name().simplified().replace(" ", "")));
    }
    updateTrial();
}

int TrialManager::trialForWord(QString word)
{
    QString participant = participantEdit->text();
    if (participant.isEmpty())
    {
        return 1;
    }

    if (currentDir.exists())
    {
        for (int trial = 1; trial <= MAX_TRIALS; trial++)
        {
            QString filename = word + QString::number(trial) + ".csv";
            QFile trialFile(currentDir.absoluteFilePath(filename));
            if (!trialFile.exists())
            {
                return trial;
            }
        }
        return MAX_TRIALS;
    }
    return 1;
}

KeyboardLayout *TrialManager::currentLayout()
{
    return qvariant_cast<KeyboardLayout *>(layoutsCombo->currentData());
}
