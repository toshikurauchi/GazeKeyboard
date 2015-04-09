#ifndef TRIALMANAGER_H
#define TRIALMANAGER_H

#include <QObject>
#include <QLineEdit>
#include <QComboBox>
#include <QCheckBox>
#include <QSpinBox>
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
                          QString dataDirectory, std::vector<std::string> words);
    QString currentFile();

public slots:
    void updateTrial();

protected slots:
    void updateTrialForWord(QString word);
    void updateDir();

private slots:
    void changeLayout(int layoutIdx);

private:
    QLineEdit *participantEdit;
    QComboBox *wordsCombo;
    QSpinBox *trialsSpinBox;
    QSpinBox *currentTrialSpinBox;
    QComboBox *layoutsCombo;
    QCheckBox *useMouseCheck;
    QImageLabel *imageLabel;
    QDir dataDir;
    QDir currentDir;
    std::vector<std::string> words;

    int trialForWord(QString word);
    KeyboardLayout *currentLayout();

    static const int MAX_TRIALS;
};

#endif // TRIALMANAGER_H
