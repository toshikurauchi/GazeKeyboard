#ifndef GAZELISTENER_H
#define GAZELISTENER_H

#include <QFile>
#include <QTextStream>

#include "gazeapi.h"
#include "GazeOverlay.h"

class GazeListener : public gtl::IGazeListener
{
public:
    GazeListener(GazeOverlay *gazeOverlay);
    ~GazeListener();
    void startRecording(QString filename);
    void stopRecording();

private:
   void on_gaze_data(gtl::GazeData const & gaze_data);

   gtl::GazeApi m_api;
   GazeOverlay *m_gazeoverlay;

   static const QString header;
   QFile *file;
   QTextStream *out_stream;
};

#endif // GAZELISTENER_H
