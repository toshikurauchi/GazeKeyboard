#include <QDir>
#include <QDebug>
#include <ctime>
#include <algorithm>
#include <QPixmap>
#include <QPainter>

#include "TrialManager.h"

TrialManager::TrialManager(QObject *parent, QLineEdit *participantEdit,
                           QComboBox *wordsCombo, QSpinBox *trialsSpinBox,
                           QSpinBox *currentTrialSpinBox, QComboBox *layoutsCombo,
                           QCheckBox *useMouseCheck, QImageLabel *imageLabel,
                           QLabel *trialCountLabel, QString dataDirectory,
                           std::vector<std::string> words, int sessionSize) :
    QObject(parent), participantEdit(participantEdit), wordsCombo(wordsCombo), trialsSpinBox(trialsSpinBox),
    currentTrialSpinBox(currentTrialSpinBox), layoutsCombo(layoutsCombo), useMouseCheck(useMouseCheck),
    imageLabel(imageLabel), trialCountLabel(trialCountLabel), dataDir(dataDirectory), words(words),
    m_paused(true), sessionSize(sessionSize)
{
    connect(participantEdit, SIGNAL(textChanged(QString)), this, SLOT(updateDir()));
    connect(wordsCombo, SIGNAL(currentIndexChanged(QString)), this, SLOT(updateTrialForWord(QString)));
    connect(trialsSpinBox, SIGNAL(valueChanged(int)), this, SLOT(updateTrial()));
    connect(layoutsCombo, SIGNAL(currentIndexChanged(int)), this, SLOT(updateDir()));
    connect(useMouseCheck, SIGNAL(toggled(bool)), this, SLOT(updateDir()));
    connect(this, SIGNAL(paused()), this, SLOT(displaySessionPage()));

    if (!dataDir.exists()) QDir().mkpath(dataDirectory);
    updateDir();
    updateTrial();

    displaySessionPage();
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

bool TrialManager::isPaused()
{
    return m_paused;
}

void TrialManager::resume()
{
    m_paused = false;
    displayCurrentLayout();
}

void TrialManager::updateTrial()
{
    if (currentDir.exists())
    {
        QStringList csvFilter;
        csvFilter << "*.csv";
        int totalTrials = currentDir.entryInfoList(csvFilter).size();
        trialCountLabel->setText(QString::number(totalTrials + 1));
        if (totalTrials % sessionSize == 0)
        {
            emit paused();
        }
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
        emit paused();
        displaySessionPage(true);
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
    displaySessionPage();
}

void TrialManager::displayCurrentLayout()
{
    KeyboardLayout *layout = qvariant_cast<KeyboardLayout *>(layoutsCombo->currentData());
    QPixmap pixmap(layout->filename());
    imageLabel->setPixmap(pixmap);
    imageLabel->update();
}

void TrialManager::displaySessionPage(bool blockFinished)
{
    m_paused = true;

    QPixmap pixmap(imageLabel->size());
    QPainter painter(&pixmap);

    painter.setPen(QColor(0, 0, 0));
    painter.setRenderHint(QPainter::TextAntialiasing);
    QFont font;
    font.setPixelSize(20);
    painter.setFont(font);

    QString text;
    if (blockFinished)
    {
        text = "Block finished\nPlease wait for further instructions";
    }
    else
    {
        int curSession = (trialCountLabel->text().toInt() - 1) / sessionSize + 1;
        text.sprintf("Session %d\nPress <SPACE> to start", curSession);
    }
    painter.drawText(imageLabel->rect(), Qt::AlignCenter, text);

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
        nameFilter << "*[0123456789]" + word + "[0123456789]*.csv";
        int lastTrial = currentDir.entryInfoList(nameFilter).size();
        return lastTrial + 1;
    }
    return 1;
}

KeyboardLayout *TrialManager::currentLayout()
{
    return qvariant_cast<KeyboardLayout *>(layoutsCombo->currentData());
}
