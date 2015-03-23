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
    void resized(QSize size);

public slots:
    void setPixmap(const QPixmap&);

protected:
    void paintEvent(QPaintEvent *);
    void resizeEvent(QResizeEvent *event);

private:
    QPixmap pix;
    QRect imgPos;
};

#endif // QIMAGELABEL_H
