#ifndef KEYBOARDIMAGEWINDOW_H
#define KEYBOARDIMAGEWINDOW_H

#include <QMainWindow>

#include "GazeOverlay.h"
#include "GazeListener.h"

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

private:
    Ui::KeyboardImageWindow *ui;
    GazeOverlay *gazeOverlay;
    GazeListener *gazeListener;
    QString recordingsDir;

    void readSettings();
    void writeSettings();

private slots:
    void toggleRecording();
};

#endif // KEYBOARDIMAGEWINDOW_H
