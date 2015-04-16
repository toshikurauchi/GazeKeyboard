#ifndef CIRCLEWIDGET_H
#define CIRCLEWIDGET_H

#include <QWidget>
#include <QTimer>

class GazeOverlay : public QWidget
{
    Q_OBJECT
public:
    explicit GazeOverlay(QWidget *parent = 0, int mouseRadius = 10, int gazeRadius = 2);
    QRect imagePosition();
    void setGazeMode(bool inGazeMode);

public slots:
    void setShow(bool show);

protected slots:
    void newGaze(QPoint gaze);
    void imageRescaled(QSize labelSize, QRect m_imgPos);

protected:
    void paintEvent(QPaintEvent *event);

private:
    class TstampPoint : public QPoint
    {
    public:
        TstampPoint(QPoint p, qint64 tstamp);
        qint64 tstamp();
    private:
        qint64 m_tstamp;
    };

    QRect m_imgPos;
    int m_mouseRadius;
    int m_gazeRadius;
    QPoint m_gaze;
    bool show;
    QTimer timer;
    QList<TstampPoint> prevPoints;
    bool inGazeMode;

    void filterOldPoints();
};

#endif // CIRCLEWIDGET_H
