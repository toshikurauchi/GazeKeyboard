#include <QPainter>
#include <QDebug>

#include "GazeOverlay.h"

GazeOverlay::GazeOverlay(QWidget *parent, int radius) :
    QWidget(parent), m_radius(radius), show(false)
{
}

void GazeOverlay::newGaze(QPoint gaze)
{
    m_gaze = gaze;
    show = true;
    repaint();
}

void GazeOverlay::imageResized(QSize size)
{
    resize(size);
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
