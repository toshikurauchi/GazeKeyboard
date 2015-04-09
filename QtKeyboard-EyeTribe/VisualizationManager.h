#ifndef VISUALIZATIONMANAGER_H
#define VISUALIZATIONMANAGER_H

#include <QObject>
#include <QComboBox>
#include <QString>
#include <QMap>
#include <QSlider>
#include <QCheckBox>

#include "QImageLabel.h"
#include "KeyboardLayout.h"
#include "ScanpathPlotter.h"

class VisualizationManager : public QObject
{
    Q_OBJECT
public:
    explicit VisualizationManager(QObject *parent, QComboBox *participantsCombo,
                                  QComboBox *modesCombo, QComboBox *layoutsCombo,
                                  QComboBox *wordsCombo, QComboBox *trialsCombo,
                                  QImageLabel *imageLabel, QCheckBox *showFixCheck,
                                  QSlider *fixRadSlider, QSlider *fixThreshSlider,
                                  QSlider *lineWidthSlider, QSlider *opacitySlider, QCheckBox *smoothVizCheck,
                                  QString dataDirectory, QList<KeyboardLayout *> keyboardLayouts);
    void loadVisualizations();

private:
    QComboBox *participantsCombo;
    QComboBox *modesCombo;
    QComboBox *layoutsCombo;
    QComboBox *wordsCombo;
    QComboBox *trialsCombo;
    QImageLabel *imageLabel;
    QCheckBox *showFixCheck;
    QSlider *fixRadSlider;
    QSlider *fixThreshSlider;
    QSlider *lineWidthSlider;
    QSlider *opacitySlider;
    QCheckBox *smoothVizCheck;

    QString dataDirPath;
    QStringList modesList;
    QMap<QString, KeyboardLayout *> keyboardLayouts;
    QStringList csvFilter;
    ScanpathPlotter plotter;

    typedef QMap<QString, QString> TrialFiles;
    typedef QMap<QString, TrialFiles> WordTrials;
    typedef QMap<QString, WordTrials> LayoutWords;
    typedef QMap<QString, LayoutWords> ModeLayouts;
    typedef QMap<QString, ModeLayouts> ParticipantModes;
    ParticipantModes data;

    QStringList participants();
    QStringList modes(QString participant);
    QStringList layouts(QString participant, QString mode);
    QStringList words(QString participant, QString mode, QString layout);
    QStringList trials(QString participant, QString mode, QString layout, QString word);

private slots:
    void updateModes();
    void updateLayouts();
    void updateWords();
    void updateTrials();
    void updateVisualization();
};

#endif // VISUALIZATIONMANAGER_H
