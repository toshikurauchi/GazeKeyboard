#ifndef TRIALMANAGER_H
#define TRIALMANAGER_H

#include <QObject>
#include <QLineEdit>
#include <QComboBox>
#include <QSpinBox>
#include <QDir>

class TrialManager : public QObject
{
    Q_OBJECT
public:
    explicit TrialManager(QObject *parent, QLineEdit *participantEdit,
                          QComboBox *wordsCombo, QSpinBox *trialsSpinBox,
                          QSpinBox *currentTrialSpinBox, QString dataDirectory);
    QString currentFile();

public slots:
    void updateTrial();

protected slots:
    void updateTrialForWord(QString word);

private:
    QLineEdit *participantEdit;
    QComboBox *wordsCombo;
    QSpinBox *trialsSpinBox;
    QSpinBox *currentTrialSpinBox;
    QDir dataDir;

    int trialForWord(QString word);
    static const int MAX_TRIALS;
};

#endif // TRIALMANAGER_H
