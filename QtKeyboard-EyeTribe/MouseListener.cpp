#include <QDateTime>

#include "MouseListener.h"

const QString MouseListener::header = "tstamp,mouse_x,mouse_y\n";

MouseListener::MouseListener(QObject *parent, GazeOverlay *gazeOverlay) :
    QObject(parent), gazeOverlay(gazeOverlay), file(0), out_stream(0)
{
}

MouseListener::~MouseListener()
{
    if (isRecording())
    {
        stopRecording();
    }
}

void MouseListener::startRecording(QString filename)
{
    file = new QFile(filename);
    file->open(QIODevice::WriteOnly | QIODevice::Text);
    out_stream = new QTextStream(file);
    *out_stream << header;
}

void MouseListener::stopRecording()
{
    file->close();
    delete out_stream;
    delete file;
    out_stream = 0;
    file = 0;
}

bool MouseListener::isRecording()
{
    return out_stream != 0;
}

void MouseListener::mouseMoved(QPoint mousePos)
{
    // Get gaze position in keyboard image coordinates
    mousePos = gazeOverlay->mapFromGlobal(mousePos);
    emit newMousePos(mousePos);

    // Normalize coordinates
    QRect imgPos = gazeOverlay->imagePosition();
    float posX = (float) (mousePos.x() - imgPos.x())/imgPos.width();
    float posY = (float) (mousePos.y() - imgPos.y())/imgPos.height();
    if (isRecording())
    {
        *out_stream << QDateTime::currentMSecsSinceEpoch() << "," << posX << "," << posY << "\n";
    }
}
