#include <QDebug>
#include "GazeListener.h"

GazeListener::GazeListener(QObject *parent, GazeOverlay *gazeOverlay, QString header) :
    QObject(parent), m_gazeoverlay(gazeOverlay), header(header), file(0), out_stream(0)
{
}

GazeListener::~GazeListener()
{
    if (isRecording())
    {
        stopRecording();
    }
}

void GazeListener::startRecording(QString filename)
{
    file = new QFile(filename);
    file->open(QIODevice::WriteOnly | QIODevice::Text);
    out_stream = new QTextStream(file);
    *out_stream << header;
}

void GazeListener::stopRecording()
{
    file->close();
    delete out_stream;
    delete file;
    out_stream = 0;
    file = 0;
}

bool GazeListener::isRecording()
{
    return out_stream != 0;
}

QPointF GazeListener::normalize(QPoint point)
{
    QRect imgPos = m_gazeoverlay->imagePosition();

    point = m_gazeoverlay->mapFromGlobal(point);
    float x = (float) (point.x() - imgPos.x())/imgPos.width();
    float y = (float) (point.y() - imgPos.y())/imgPos.height();
    return QPointF(x, y);
}

void GazeListener::printToFile(QString csvLine)
{
    *out_stream << csvLine;
}
