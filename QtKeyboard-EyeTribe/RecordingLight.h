#ifndef RECORDINGLIGHT_H
#define RECORDINGLIGHT_H

#include <QWidget>

class RecordingLight : public QWidget
{
    Q_OBJECT
public:
    explicit RecordingLight(QWidget *parent = 0);
    void setRecording(bool recording);

public slots:
    void setWord(QString word = "");
    void showWord();
    void hideWord();

protected:
    void paintEvent(QPaintEvent *);

private:
    bool recording;
    int paddingX;
    int paddingY;
    int radius;
    bool shouldShowWord;
    QString word;
};

#endif // RECORDINGLIGHT_H
