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

private:
    Ui::KeyboardImageWindow *ui;
    GazeOverlay *gazeOverlay;
    GazeListener *gazeListener;

private slots:
    void toggleRecording();
};

#endif // KEYBOARDIMAGEWINDOW_H
