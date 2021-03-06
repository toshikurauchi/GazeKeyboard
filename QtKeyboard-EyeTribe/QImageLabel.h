#ifndef QIMAGELABEL_H
#define QIMAGELABEL_H

#include <QWidget>

class QImageLabel : public QWidget
{
    Q_OBJECT

public:
    explicit QImageLabel(QWidget *parent = 0);
    const QPixmap* pixmap() const;
    QRect imagePos();

signals:
    void rescaled(QSize labelSize, QRect imgPos);
    void mouseMoved(QPoint position);

public slots:
    void setPixmap(const QPixmap&);

protected:
    void paintEvent(QPaintEvent *);
    void resizeEvent(QResizeEvent *event);
    void mouseMoveEvent(QMouseEvent *event);

private:
    QPixmap pix;
    QPixmap scaledPix;
    QPoint origin;
    QRect imgPos;

    void initScaledPixmap(QSize frameSize);
};

#endif // QIMAGELABEL_H
