#ifndef GAZELISTENER_H
#define GAZELISTENER_H

#include <QFile>
#include <QTextStream>

#include "GazeOverlay.h"
#include "IDataRecorder.h"

class GazeListener : public QObject, public IDataRecorder
{
    Q_OBJECT

public:
    GazeListener(QObject *parent, GazeOverlay *gazeOverlay, QString header);
    ~GazeListener();
    void startRecording(QString filename);
    void stopRecording();
    bool isRecording();

signals:
    void newGaze(QPoint gaze);

protected:
    QPointF normalize(QPoint point);
    void printToFile(QString csvLine);

private:
   GazeOverlay *m_gazeoverlay;

   QString header;
   QFile *file;
   QTextStream *out_stream;
};

#endif // GAZELISTENER_H
