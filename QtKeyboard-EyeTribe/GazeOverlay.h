#ifndef CIRCLEWIDGET_H
#define CIRCLEWIDGET_H

#include <QWidget>
#include <QTimer>

class GazeOverlay : public QWidget
{
    Q_OBJECT
public:
    explicit GazeOverlay(QWidget *parent = 0, int radius = 10);

protected slots:
    void newGaze(QPoint gaze);
    void imageRescaled(QRect imgPos);

protected:
    void paintEvent(QPaintEvent *event);

private:
    QPoint origin;
    int m_radius;
    QPoint m_gaze;
    bool show;
    QTimer timer;
};

#endif // CIRCLEWIDGET_H
