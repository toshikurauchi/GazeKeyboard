#ifndef CIRCLEWIDGET_H
#define CIRCLEWIDGET_H

#include <QWidget>

class GazeOverlay : public QWidget
{
    Q_OBJECT
public:
    explicit GazeOverlay(QWidget *parent = 0, int radius = 10);
    void setGaze(QPoint gaze);

protected:
    void paintEvent(QPaintEvent *event);

private:
    int m_radius;
    QPoint m_gaze;
    bool show;

};

#endif // CIRCLEWIDGET_H
