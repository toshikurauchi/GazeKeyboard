#ifndef TRIALMANAGER_H
#define TRIALMANAGER_H

#include <QObject>
#include <QLineEdit>
#include <QComboBox>
#include <QCheckBox>
#include <QSpinBox>
#include <QLabel>
#include <QDir>
#include <vector>

#include "KeyboardLayout.h"
#include "QImageLabel.h"

class TrialManager : public QObject
{
    Q_OBJECT
public:
    explicit TrialManager(QObject *parent, QLineEdit *participantEdit,
                          QComboBox *wordsCombo, QSpinBox *trialsSpinBox,
                          QSpinBox *currentTrialSpinBox, QComboBox *layoutsCombo,
                          QCheckBox *useMouseCheck, QImageLabel *imageLabel,
                          QLabel *trialCountLabel, QString dataDirectory,
                          std::vector<std::string> words, int sessionSize);
    QString currentFile();
    bool isPaused();
    void resume();

signals:
    void paused();

public slots:
    void updateTrial();

protected slots:
    void updateTrialForWord(QString word);
    void updateDir();

private slots:
    void displayCurrentLayout();
    void displaySessionPage(bool blockFinished = false);

private:
    QLineEdit *participantEdit;
    QComboBox *wordsCombo;
    QSpinBox *trialsSpinBox;
    QSpinBox *currentTrialSpinBox;
    QComboBox *layoutsCombo;
    QCheckBox *useMouseCheck;
    QImageLabel *imageLabel;
    QLabel *trialCountLabel;
    QDir dataDir;
    QDir currentDir;
    std::vector<std::string> words;
    bool m_paused;
    int sessionSize;

    int trialForWord(QString word);
    KeyboardLayout *currentLayout();
};

#endif // TRIALMANAGER_H
