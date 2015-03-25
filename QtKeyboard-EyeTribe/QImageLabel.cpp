#include <QPainter>
#include <QPaintEvent>

#include "QImageLabel.h"

QImageLabel::QImageLabel(QWidget *parent) :
    QWidget(parent)
{
}

void QImageLabel::paintEvent(QPaintEvent *event) {
    QWidget::paintEvent(event);

    if (pix.isNull())
        return;

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    painter.drawPixmap(origin, scaledPix);
}

void QImageLabel::resizeEvent(QResizeEvent *event)
{
    QSize pixSize = pix.size();
    pixSize.scale(event->size(), Qt::KeepAspectRatio);
    scaledPix = pix.scaled(pixSize,
                           Qt::KeepAspectRatio,
                           Qt::SmoothTransformation
                           );
    origin.setX((width() - scaledPix.width())/2);
    origin.setY((height() - scaledPix.height())/2);
    imgPos.setWidth(scaledPix.width());
    imgPos.setHeight(scaledPix.height());
    imgPos.setTopLeft(origin);
    emit rescaled(imgPos);
}

const QPixmap* QImageLabel::pixmap() const {
    return &pix;
}

QRect QImageLabel::imagePos() {
    return imgPos;
}

void QImageLabel::setPixmap (const QPixmap &pixmap){
    pix = pixmap;
}
