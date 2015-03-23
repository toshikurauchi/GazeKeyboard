#include <QPainter>

#include "GazeOverlay.h"

GazeOverlay::GazeOverlay(QWidget *parent, int radius) :
    QWidget(parent), m_radius(radius), show(false)
{
}

void GazeOverlay::setGaze(QPoint gaze)
{
    m_gaze = gaze;
    show = true;
}

void GazeOverlay::paintEvent(QPaintEvent *event)
{
    if (!show) return;

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    QBrush brush(QColor(255, 0, 0));
    painter.setBrush(brush);
    painter.drawEllipse(m_gaze, m_radius, m_radius);
}
