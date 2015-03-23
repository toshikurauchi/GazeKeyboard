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

    QSize pixSize = pix.size();
    pixSize.scale(event->rect().size(), Qt::KeepAspectRatio);

    QPixmap scaledPix = pix.scaled(pixSize,
                                   Qt::KeepAspectRatio,
                                   Qt::SmoothTransformation
                                   );

    painter.drawPixmap(QPoint(), scaledPix);
    imgPos.setWidth(scaledPix.width());
    imgPos.setHeight(scaledPix.height());
}

void QImageLabel::resizeEvent(QResizeEvent *event)
{
    QSize imgSize = pix.size();
    imgSize.scale(event->size(), Qt::KeepAspectRatio);
    emit resized(imgSize);
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
