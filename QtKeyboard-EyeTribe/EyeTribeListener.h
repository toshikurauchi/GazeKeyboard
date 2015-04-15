#ifndef EYETRIBELISTENER_H
#define EYETRIBELISTENER_H

#include "GazeListener.h"
#include "tet-cpp-client/include/gazeapi.h"

class EyeTribeListener : public GazeListener, public gtl::IGazeListener
{
    Q_OBJECT

public:
    EyeTribeListener(QObject *parent, GazeOverlay *gazeOverlay);
    ~EyeTribeListener();

private:
    gtl::GazeApi m_api;

    void on_gaze_data(gtl::GazeData const & gaze_data);
};

#endif // EYETRIBELISTENER_H
