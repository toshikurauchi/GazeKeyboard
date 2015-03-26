#ifndef KEYBOARDIMAGEWINDOW_H
#define KEYBOARDIMAGEWINDOW_H

#include <QMainWindow>
#include <QQuickItem>

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
    QQuickItem *recLight;

    void readSettings();
    void writeSettings();

private slots:
    void toggleRecording();
};

#endif // KEYBOARDIMAGEWINDOW_H
