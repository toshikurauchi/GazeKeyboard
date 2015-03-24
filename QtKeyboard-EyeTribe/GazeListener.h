#ifndef GAZELISTENER_H
#define GAZELISTENER_H

#include <QFile>
#include <QTextStream>

#include "tet-cpp-client/include/gazeapi.h"
#include "GazeOverlay.h"

class GazeListener : public QObject, public gtl::IGazeListener
{
    Q_OBJECT

public:
    explicit GazeListener(QObject *parent, GazeOverlay *gazeOverlay);
    ~GazeListener();
    void startRecording(QString filename);
    void stopRecording();

signals:
    void newGaze(QPoint gaze);

private:
   void on_gaze_data(gtl::GazeData const & gaze_data);

   gtl::GazeApi m_api;
   GazeOverlay *m_gazeoverlay;

   static const QString header;
   QFile *file;
   QTextStream *out_stream;
};

#endif // GAZELISTENER_H
