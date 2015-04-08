#ifndef MOUSELISTENER_H
#define MOUSELISTENER_H

#include <QObject>
#include <QFile>
#include <QTextStream>

#include "IDataRecorder.h"
#include "GazeOverlay.h"

class MouseListener : public QObject, public IDataRecorder
{
    Q_OBJECT
public:
    explicit MouseListener(QObject *parent, GazeOverlay *gazeOverlay);
    ~MouseListener();

    void startRecording(QString filename);
    void stopRecording();
    bool isRecording();

public slots:
    void mouseMoved(QPoint mousePos);

signals:
    void newMousePos(QPoint mousePos);

private:
    static const QString header;
    GazeOverlay *gazeOverlay;
    QFile *file;
    QTextStream *out_stream;
};

#endif // MOUSELISTENER_H
