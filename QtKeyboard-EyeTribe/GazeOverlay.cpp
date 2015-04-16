#include <QPainter>
#include <QDebug>
#include <QDateTime>

#include "GazeOverlay.h"

GazeOverlay::GazeOverlay(QWidget *parent, int mouseRadius, int gazeRadius) :
    QWidget(parent), m_mouseRadius(mouseRadius), m_gazeRadius(gazeRadius), show(false), timer(this)
{
    connect(&timer, SIGNAL(timeout()), this, SLOT(repaint()));
    timer.start(17);
    // We need this in case the layers below want to track the mouse position
    setMouseTracking(true);
}

QRect GazeOverlay::imagePosition()
{
    return m_imgPos;
}

void GazeOverlay::setGazeMode(bool inGazeMode)
{
    this->inGazeMode = inGazeMode;
}

void GazeOverlay::setShow(bool show)
{
    this->show = show;
}

void GazeOverlay::newGaze(QPoint gaze)
{
    m_gaze = mapFromGlobal(gaze);
    if (inGazeMode)
    {
        prevPoints.append(TstampPoint(m_gaze, QDateTime::currentMSecsSinceEpoch()));
    }
}

void GazeOverlay::imageRescaled(QSize labelSize, QRect imgPos)
{
    m_imgPos = imgPos;
    resize(labelSize);
}

void GazeOverlay::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);
    if (!show) return;

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    if (inGazeMode)
    {
        filterOldPoints();
        for (int i = 0; i < prevPoints.size(); i++) {
            TstampPoint point = prevPoints.at(i);
            QColor pointColor(255, 0, 0, 255*(i+1)/(prevPoints.size()+1)); // We don't want the oldest to be completely transparent
            QBrush brush(pointColor);
            painter.setBrush(brush);
            painter.setPen(pointColor);
            painter.drawEllipse(point, m_gazeRadius, m_gazeRadius);
        }
    }
    else
    {
        QBrush brush(QColor(255, 0, 0));
        painter.setBrush(brush);
        painter.drawEllipse(m_gaze, m_mouseRadius, m_mouseRadius);
    }
}

void GazeOverlay::filterOldPoints()
{
    qint64 now = QDateTime::currentMSecsSinceEpoch();
    QMutableListIterator<TstampPoint> it(prevPoints);
    while (it.hasNext()) {
        if (now - it.next().tstamp() > 500)
        {
            it.remove();
        }
    }
}

//******************** TstampPoint *********************//

GazeOverlay::TstampPoint::TstampPoint(QPoint p, qint64 tstamp) :
    QPoint(p.x(), p.y()), m_tstamp(tstamp)
{
}

qint64 GazeOverlay::TstampPoint::tstamp()
{
    return m_tstamp;
}
