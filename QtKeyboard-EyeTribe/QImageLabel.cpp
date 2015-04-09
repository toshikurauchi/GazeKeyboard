#include <QPainter>
#include <QPaintEvent>
#include <QDebug>

#include "QImageLabel.h"

QImageLabel::QImageLabel(QWidget *parent) :
    QWidget(parent)
{
    setMouseTracking(true);
}

void QImageLabel::paintEvent(QPaintEvent *event)
{
    QWidget::paintEvent(event);

    if (pix.isNull())
        return;

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);

    painter.drawPixmap(origin, scaledPix);
}

void QImageLabel::resizeEvent(QResizeEvent *event)
{
    initScaledPixmap(event->size());
}

void QImageLabel::mouseMoveEvent(QMouseEvent *event)
{
    emit mouseMoved(mapToGlobal(event->pos()));
}

const QPixmap* QImageLabel::pixmap() const
{
    return &pix;
}

QRect QImageLabel::imagePos()
{
    return imgPos;
}

void QImageLabel::setPixmap (const QPixmap &pixmap)
{
    pix = pixmap;
    initScaledPixmap(size());
}

void QImageLabel::initScaledPixmap(QSize frameSize)
{
    QSize pixSize = pix.size();
    pixSize.scale(frameSize, Qt::KeepAspectRatio);
    scaledPix = pix.scaled(pixSize,
                           Qt::KeepAspectRatio,
                           Qt::SmoothTransformation
                           );
    origin.setX((width() - scaledPix.width())/2);
    origin.setY((height() - scaledPix.height())/2);
    imgPos = QRect(origin, scaledPix.size());
    emit rescaled(frameSize, imgPos);
}
