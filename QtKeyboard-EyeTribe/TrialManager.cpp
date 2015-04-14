#include <QDir>
#include <QDebug>
#include <ctime>
#include <algorithm>

#include "TrialManager.h"

const int TrialManager::MAX_TRIALS = 100;

TrialManager::TrialManager(QObject *parent, QLineEdit *participantEdit,
                           QComboBox *wordsCombo, QSpinBox *trialsSpinBox,
                           QSpinBox *currentTrialSpinBox, QComboBox *layoutsCombo,
                           QCheckBox *useMouseCheck, QImageLabel *imageLabel,
                           QLabel *trialCountLabel, QString dataDirectory,
                           std::vector<std::string> words) :
    QObject(parent), participantEdit(participantEdit), wordsCombo(wordsCombo), trialsSpinBox(trialsSpinBox),
    currentTrialSpinBox(currentTrialSpinBox), layoutsCombo(layoutsCombo), useMouseCheck(useMouseCheck),
    imageLabel(imageLabel), trialCountLabel(trialCountLabel), dataDir(dataDirectory), words(words)
{
    connect(participantEdit, SIGNAL(textChanged(QString)), this, SLOT(updateDir()));
    connect(wordsCombo, SIGNAL(currentIndexChanged(QString)), this, SLOT(updateTrialForWord(QString)));
    connect(trialsSpinBox, SIGNAL(valueChanged(int)), this, SLOT(updateTrial()));
    connect(layoutsCombo, SIGNAL(currentIndexChanged(int)), this, SLOT(updateDir()));
    connect(useMouseCheck, SIGNAL(toggled(bool)), this, SLOT(updateDir()));

    connect(layoutsCombo, SIGNAL(currentIndexChanged(int)), this, SLOT(changeLayout(int)));
    changeLayout(layoutsCombo->currentIndex());

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
    int trialId = trialCountLabel->text().toInt();
    QString trialText;
    trialText.sprintf("%03d", trialId);
    QString filename = trialText + wordsCombo->currentText() +
            QString::number(currentTrialSpinBox->value()) + ".csv";
    return currentDir.absoluteFilePath(filename);
}

void TrialManager::updateTrial()
{
    if (currentDir.exists())
    {
        QStringList csvFilter;
        csvFilter << "*.csv";
        int totalTrials = currentDir.entryInfoList(csvFilter).size();
        trialCountLabel->setText(QString::number(totalTrials + 1));
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
        trialCountLabel->setText(QString::number(1));
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
    std::srand(unsigned(std::time(0)));
    std::random_shuffle(words.begin(), words.end());
    QStringList wordList;
    for (std::vector<std::string>::iterator it = words.begin(); it != words.end(); it++)
    {
        wordList.append(QString(it->c_str()));
    }
    wordsCombo->clear();
    wordsCombo->addItems(wordList);
    QString participant = participantEdit->text();
    if (participant.isEmpty())
    {
        currentDir = QDir();
    }
    else
    {
        currentDir = QDir(dataDir.absoluteFilePath(participant));
        if (useMouseCheck->isChecked()) currentDir = QDir(currentDir.absoluteFilePath("mouse"));
        else currentDir = QDir(currentDir.absoluteFilePath("gaze"));
        currentDir = QDir(currentDir.absoluteFilePath(currentLayout()->trimmedName()));
    }
    updateTrial();
}

void TrialManager::changeLayout(int layoutIdx)
{
    KeyboardLayout *layout = qvariant_cast<KeyboardLayout *>(layoutsCombo->itemData(layoutIdx));
    QPixmap pixmap(layout->filename());
    imageLabel->setPixmap(pixmap);
    imageLabel->update();
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
        QStringList nameFilter;
        nameFilter << "[0123456789]*" + word + "[0123456789]*.csv";
        int lastTrial = currentDir.entryInfoList(nameFilter).size();
        return lastTrial + 1;
    }
    return 1;
}

KeyboardLayout *TrialManager::currentLayout()
{
    return qvariant_cast<KeyboardLayout *>(layoutsCombo->currentData());
}
