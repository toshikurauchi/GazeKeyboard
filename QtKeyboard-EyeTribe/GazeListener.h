#ifndef GAZELISTENER_H
#define GAZELISTENER_H

#include "gazeapi.h"
#include "GazeOverlay.h"

class GazeListener : public gtl::IGazeListener
{
public:
    GazeListener(GazeOverlay *gazeOverlay);
    ~GazeListener();

private:
       void on_gaze_data(gtl::GazeData const & gaze_data);
       gtl::GazeApi m_api;
       GazeOverlay *m_gazeoverlay;
};

#endif // GAZELISTENER_H
