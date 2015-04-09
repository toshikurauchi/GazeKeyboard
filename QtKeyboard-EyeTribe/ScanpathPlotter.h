#ifndef SCANPATHPLOTTER_H
#define SCANPATHPLOTTER_H

#include <QColor>
#include <QPoint>
#include <QPixmap>

class ScanpathPlotter
{
public:
    ScanpathPlotter();
    bool loadData(QString csvfile, bool isGaze);
    void plot(QPixmap &pixmap, bool smoothed, float threshPercent, float maxFixRadPercent, float opacity, float lineWidthPercent);

private:
    class Entry
    {
    public:
        virtual qint64 timestamp() = 0;
        virtual QPointF pos(bool smoothed) = 0;
    };

    class MouseEntry : public Entry
    {
    public:
        MouseEntry(qint64 tstamp, QPointF position);
        qint64 timestamp();
        QPointF pos(bool smoothed);
    private:
        QPointF m_pos;
        qint64 tstamp;
    };

    class GazeEntry : public Entry
    {
    public:
        GazeEntry(qint64 tstamp, QPointF raw, QPointF smooth);
        qint64 timestamp();
        QPointF pos(bool smoothed);
    private:
        QPointF raw;
        QPointF smooth;
        qint64 tstamp;
    };

    struct DenormalizedEntry
    {
        DenormalizedEntry(qint64 timestamp, QPoint position);
        qint64 timestamp;
        QPoint position;
    };

    struct Fixation
    {
        Fixation(qint64 duration, QPoint position);
        qint64 duration;
        QPoint position;
    };

private:
    QColor sacColor;
    QColor fixColor;
    QList<Entry *> entries;

    QList<Fixation> detectFixations(QSize imageSize, bool smoothed, float threshPercent);
    qint64 computeAverageFrameTime();
    Fixation computeFixation(QList<DenormalizedEntry> cluster, qint64 frameTime);
    QPoint clusterCenter(QList<DenormalizedEntry> cluster);
    float dist2cluster(QList<DenormalizedEntry> cluster, DenormalizedEntry entry);
};

#endif // SCANPATHPLOTTER_H
