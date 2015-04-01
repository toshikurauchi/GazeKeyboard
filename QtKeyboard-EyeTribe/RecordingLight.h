#ifndef RECORDINGLIGHT_H
#define RECORDINGLIGHT_H

#include <QWidget>

class RecordingLight : public QWidget
{
    Q_OBJECT
public:
    explicit RecordingLight(QWidget *parent = 0);
    void setRecording(bool recording);
    bool isRecording();

protected:
    void paintEvent(QPaintEvent *);

private:
    bool recording;
    int paddingX;
    int paddingY;
    int radius;
};

#endif // RECORDINGLIGHT_H
