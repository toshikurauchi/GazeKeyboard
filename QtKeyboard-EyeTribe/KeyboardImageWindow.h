#ifndef KEYBOARDIMAGEWINDOW_H
#define KEYBOARDIMAGEWINDOW_H

#include <QMainWindow>
#include <QQuickItem>
#include <QMessageBox>
#include <vector>

#include "GazeOverlay.h"
#include "GazeListener.h"
#include "MouseListener.h"
#include "TrialManager.h"
#include "VisualizationManager.h"
#include "KeyboardLayout.h"

namespace Ui {
class KeyboardImageWindow;
}

class KeyboardImageWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit KeyboardImageWindow(QWidget *parent = 0);
    ~KeyboardImageWindow();

protected:
    void closeEvent(QCloseEvent *event);
    void keyPressEvent(QKeyEvent *event);

private:
    Ui::KeyboardImageWindow *ui;
    GazeOverlay *gazeOverlay;
    GazeListener *gazeListener;
    MouseListener *mouseListener;
    std::vector<std::string> words;
    TrialManager *trialManager;
    VisualizationManager *vizManager;
    bool recording;
    QMessageBox noParticipantMessageBox;
    QList<KeyboardLayout *> layouts;

    void readSettings();
    void writeSettings();
    void loadWordList();
    void createLayoutsList();

    static const QString REC_DIR;

private slots:
    void toggleRecording();
    void useMouseToggled(bool useMouse);
    void loadVisualizations();
    void updateGazeListener();
};

#endif // KEYBOARDIMAGEWINDOW_H
