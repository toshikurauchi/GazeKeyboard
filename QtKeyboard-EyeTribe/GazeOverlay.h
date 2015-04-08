#ifndef CIRCLEWIDGET_H
#define CIRCLEWIDGET_H

#include <QWidget>
#include <QTimer>

class GazeOverlay : public QWidget
{
    Q_OBJECT
public:
    explicit GazeOverlay(QWidget *parent = 0, int radius = 10);
    QRect imagePosition();

protected slots:
    void setShow(bool show);
    void newGaze(QPoint gaze);
    void imageRescaled(QSize labelSize, QRect m_imgPos);

protected:
    void paintEvent(QPaintEvent *event);

private:
    QRect m_imgPos;
    int m_radius;
    QPoint m_gaze;
    bool show;
    QTimer timer;
};

#endif // CIRCLEWIDGET_H
