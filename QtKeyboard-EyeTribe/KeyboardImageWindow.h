#ifndef KEYBOARDIMAGEWINDOW_H
#define KEYBOARDIMAGEWINDOW_H

#include <QMainWindow>
#include <QQuickItem>
#include <QMessageBox>

#include "GazeOverlay.h"
#include "GazeListener.h"
#include "TrialManager.h"

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
    QQuickItem *recLight;
    QStringList words;
    TrialManager *trialManager;
    bool recording;
    QMessageBox noParticipantMessageBox;

    void readSettings();
    void writeSettings();
    void loadWordList();

    static const QString REC_DIR;

private slots:
    void toggleRecording();
};

#endif // KEYBOARDIMAGEWINDOW_H
