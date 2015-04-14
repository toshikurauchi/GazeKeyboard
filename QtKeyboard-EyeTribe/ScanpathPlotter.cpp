#include <QFile>
#include <QDebug>
#include <QPainter>

#include "ScanpathPlotter.h"

ScanpathPlotter::ScanpathPlotter() :
    sacColor(0, 0, 255), fixColor(0, 0, 150)
{
}

bool ScanpathPlotter::loadData(QString csvfile, bool isGaze)
{
    QFile file(csvfile);
    if (!file.open(QIODevice::ReadOnly)) {
        qDebug() << file.errorString();
        return false;
    }

    foreach (Entry *entry, entries)
    {
        delete entry;
    }
    entries.clear();
    if (!file.atEnd()) file.readLine(); // Ignore header
    while (!file.atEnd()) {
        QString line = file.readLine();
        QStringList entry = line.split(',');
        int minSize = 3;
        if (isGaze) minSize = 5;
        if (entry.size() < minSize)
        {
            qWarning() << "Data file does not follow the required format";
            entries.clear();
            return false;
        }
        if (isGaze)
        {
            qint64 tstamp = entry[0].toInt();
            QPointF raw(entry[1].toFloat(), entry[2].toFloat());
            QPointF smooth(entry[3].toFloat(), entry[4].toFloat());
            entries.append(new GazeEntry(tstamp, raw, smooth));
        }
        else
        {
            qint64 tstamp = entry[0].toInt();
            QPointF position(entry[1].toFloat(), entry[2].toFloat());
            entries.append(new MouseEntry(tstamp, position));
        }
    }
    return true;
}

void ScanpathPlotter::plot(QPixmap &pixmap, bool smoothed, float threshPercent, float maxFixRadPercent, float opacity, float lineWidthPercent)
{
    QPainter painter(&pixmap);
    QList<Fixation> fixations = detectFixations(pixmap.size(), smoothed, threshPercent);
    int maxFixRad = (int) pixmap.size().width() * maxFixRadPercent;
    int lineWidth = (int) pixmap.size().width() * lineWidthPercent;

    painter.save();
    painter.setPen(QPen(QBrush(sacColor), lineWidth));
    for (int i = 0; i < fixations.size() - 1; i++)
    {
        painter.drawLine(fixations[i].position, fixations[i+1].position);
    }

    qint64 maxDuration = 0;
    foreach (Fixation fix, fixations) {
        if (fix.duration > maxDuration) maxDuration = fix.duration;
    }
    if (maxDuration > 0 && maxFixRad > 0)
    {
        painter.restore();
        painter.setOpacity(opacity);
        painter.setBrush(QBrush(fixColor));
        foreach (Fixation fix, fixations) {
            int rad = (int) maxFixRad * fix.duration / maxDuration;
            painter.drawEllipse(fix.position, rad, rad);
        }
    }
}

QList<ScanpathPlotter::Fixation> ScanpathPlotter::detectFixations(QSize imageSize, bool smoothed, float threshPercent)
{
    float thresh = imageSize.width() * threshPercent;
    qint64 avgFrameTime = computeAverageFrameTime();
    QList<Fixation> fixations;
    QList<DenormalizedEntry> denormalizedEntries;
    QList<DenormalizedEntry> cluster;

    // Denormalize entries
    foreach (Entry *entry, entries)
    {
        QPointF normPos = entry->pos(smoothed);
        QPoint denormPos = QPoint((int) (normPos.x() * imageSize.width()), (int) (normPos.y() * imageSize.height()));
        denormalizedEntries.append(DenormalizedEntry(entry->timestamp(), denormPos));
    }

    foreach (DenormalizedEntry entry, denormalizedEntries)
    {
        if (!cluster.isEmpty() && dist2cluster(cluster, entry) >= thresh)
        {
            fixations.append(computeFixation(cluster, avgFrameTime));
            cluster.clear();
        }
        cluster.append(entry);
    }
    fixations.append(computeFixation(cluster, avgFrameTime));
    return fixations;
}

qint64 ScanpathPlotter::computeAverageFrameTime()
{
    qint64 total = 0;
    qint64 prevTstamp = -1;

    if (entries.size() < 2) return 0;

    foreach (Entry *entry, entries)
    {
        qint64 tstamp = entry->timestamp();
        if (prevTstamp >= 0)
        {
            total += tstamp - prevTstamp;
        }
        prevTstamp = tstamp;
    }
    return total/(entries.size()-1);
}

ScanpathPlotter::Fixation ScanpathPlotter::computeFixation(QList<DenormalizedEntry> cluster, qint64 frameTime)
{
    QPoint center = clusterCenter(cluster);
    qint64 duration = 0;
    if (!cluster.isEmpty()) duration = cluster.last().timestamp - cluster.first().timestamp + frameTime;
    return Fixation(duration, center);
}

QPoint ScanpathPlotter::clusterCenter(QList<DenormalizedEntry> cluster)
{
    if (cluster.isEmpty())
    {
        qWarning() << "Cannot compute center from empty cluster";
        return QPoint(-1, -1);
    }

    int totalX = 0;
    int totalY = 0;
    foreach (DenormalizedEntry entry, cluster)
    {
        totalX += entry.position.x();
        totalY += entry.position.y();
    }
    return QPoint(totalX/cluster.size(), totalY/cluster.size());
}

float ScanpathPlotter::dist2cluster(QList<DenormalizedEntry> cluster, DenormalizedEntry entry)
{
    QPoint displacement = entry.position - clusterCenter(cluster);
    return sqrt((float) QPoint::dotProduct(displacement, displacement));
}

// *********** GazeEntry ************** //

ScanpathPlotter::GazeEntry::GazeEntry(qint64 tstamp, QPointF raw, QPointF smooth) :
    tstamp(tstamp), raw(raw), smooth(smooth)
{
}

qint64 ScanpathPlotter::GazeEntry::timestamp()
{
    return tstamp;
}

QPointF ScanpathPlotter::GazeEntry::pos(bool smoothed)
{
    if (smoothed) return smooth;
    return raw;
}

// *********** MouseEntry ************** //

ScanpathPlotter::MouseEntry::MouseEntry(qint64 tstamp, QPointF position) :
    tstamp(tstamp), m_pos(position)
{
}

qint64 ScanpathPlotter::MouseEntry::timestamp()
{
    return tstamp;
}

QPointF ScanpathPlotter::MouseEntry::pos(bool smoothed)
{
    Q_UNUSED(smoothed)
    return m_pos;
}

// *********** DenormalizedEntry ************** //

ScanpathPlotter::DenormalizedEntry::DenormalizedEntry(qint64 timestamp, QPoint position) :
    timestamp(timestamp), position(position)
{
}

// *********** Fixation ************** //

ScanpathPlotter::Fixation::Fixation(qint64 duration, QPoint position) :
    duration(duration), position(position)
{
}
