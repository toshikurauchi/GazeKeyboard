#include <QPaintEvent>
#include <QPainter>

#include "RecordingLight.h"

RecordingLight::RecordingLight(QWidget *parent) :
    QWidget(parent), recording(false), paddingX(50), paddingY(5), radius(5)
{
    setMinimumWidth(4*paddingX);
    setMinimumHeight(4*paddingY);
}

void RecordingLight::setRecording(bool recording)
{
    this->recording = recording;
    update();
}

bool RecordingLight::isRecording()
{
    return recording;
}

void RecordingLight::paintEvent(QPaintEvent *event)
{
    QWidget::paintEvent(event);

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    QColor color(100, 100, 100);
    if (recording) color = QColor(255, 0, 0);
    painter.setBrush(QBrush(color));
    painter.drawRoundedRect(paddingX, paddingY, width()-2*paddingX, height()-2*paddingY, radius, radius);
}
