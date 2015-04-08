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

void RecordingLight::setWord(QString word)
{
    this->word = word;
    update();
}

void RecordingLight::paintEvent(QPaintEvent *event)
{
    QWidget::paintEvent(event);

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    QColor color(100, 100, 100);
    if (recording) color = QColor(240, 240, 240);
    painter.setBrush(QBrush(color));
    painter.setPen(color);
    painter.drawRoundedRect(paddingX, paddingY, width()-2*paddingX, height()-2*paddingY, radius, radius);
    if (!recording)
    {
        painter.setPen(QColor(255, 255, 255));
        QFont font;
        font.setPixelSize(height()-2*(paddingY+radius));
        painter.setFont(font);
        QRectF rect(paddingX+radius, paddingY+radius,
                      width()-2*(paddingX+radius), height()-2*(paddingY+radius));
        painter.drawText(rect, Qt::AlignCenter, word.toUpper());
    }
}
