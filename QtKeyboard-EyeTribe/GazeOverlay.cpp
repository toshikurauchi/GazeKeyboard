#include <QPainter>
#include <QDebug>

#include "GazeOverlay.h"

GazeOverlay::GazeOverlay(QWidget *parent, int radius) :
    QWidget(parent), m_radius(radius), show(false), timer(this)
{
    connect(&timer, SIGNAL(timeout()), this, SLOT(repaint()));
    timer.start(17);
}

QRect GazeOverlay::imagePosition()
{
    return m_imgPos;
}

void GazeOverlay::newGaze(QPoint gaze)
{
    m_gaze = gaze;
    show = true;
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

    QBrush brush(QColor(255, 0, 0));
    painter.setBrush(brush);
    painter.drawEllipse(m_gaze, m_radius, m_radius);
}
