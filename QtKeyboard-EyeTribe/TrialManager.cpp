#include <QDir>
#include <QDebug>

#include "TrialManager.h"

const int TrialManager::MAX_TRIALS = 100;

TrialManager::TrialManager(QObject *parent, QLineEdit *participantEdit,
                           QComboBox *wordsCombo, QSpinBox *trialsSpinBox,
                           QSpinBox *currentTrialSpinBox, QString dataDirectory) :
    QObject(parent), participantEdit(participantEdit), wordsCombo(wordsCombo),
    trialsSpinBox(trialsSpinBox), currentTrialSpinBox(currentTrialSpinBox), dataDir(dataDirectory)
{
    connect(participantEdit, SIGNAL(textChanged(QString)), this, SLOT(updateTrial()));
    connect(wordsCombo, SIGNAL(currentIndexChanged(QString)), this, SLOT(updateTrialForWord(QString)));
    connect(trialsSpinBox, SIGNAL(valueChanged(int)), this, SLOT(updateTrial()));

    if (!dataDir.exists()) QDir().mkpath(dataDirectory);
    updateTrial();
}

QString TrialManager::currentFile()
{
    QString participant = participantEdit->text();
    if (participant.isEmpty())
    {
        return "";
    }
    QDir participantDir(dataDir.absoluteFilePath(participant));
    if (!participantDir.exists()) QDir().mkpath(participantDir.absolutePath());
    QString filename = wordsCombo->currentText() +
            QString::number(currentTrialSpinBox->value()) + ".csv";
    return participantDir.absoluteFilePath(filename);
}

void TrialManager::updateTrial()
{
    QString participant = participantEdit->text();
    if (participant.isEmpty())
    {
        currentTrialSpinBox->setValue(1);
        return;
    }

    QDir participantDir(dataDir.absoluteFilePath(participant));
    if (participantDir.exists())
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

int TrialManager::trialForWord(QString word)
{
    QString participant = participantEdit->text();
    if (participant.isEmpty())
    {
        return 1;
    }

    QDir participantDir(dataDir.absoluteFilePath(participant));
    if (participantDir.exists())
    {
        QStringList nameFilter;
        nameFilter << "*.csv";
        QStringList recordings = participantDir.entryList(nameFilter);
        for (int trial = 1; trial <= MAX_TRIALS; trial++)
        {
            if (!recordings.contains(word + QString::number(trial) + ".csv"))
            {
                return trial;
            }
        }
        return MAX_TRIALS;
    }
    else
    {
        return 1;
    }
}
