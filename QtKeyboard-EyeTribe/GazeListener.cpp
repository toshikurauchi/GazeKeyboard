#include "GazeListener.h"

GazeListener::GazeListener(GazeOverlay *gazeOverlay) :
    m_gazeoverlay(gazeOverlay)
{
    // Connect to the server in push mode on the default TCP port (6555)
    if(m_api.connect(true))
    {
        // Enable GazeData notifications
        m_api.add_listener(*this);
    }
}

GazeListener::~GazeListener()
{
    m_api.remove_listener(*this);
    m_api.disconnect();
}

void GazeListener::on_gaze_data(gtl::GazeData const & gaze_data)
{
    if(gaze_data.state & gtl::GazeData::GD_STATE_TRACKING_GAZE)
    {
        gtl::Point2D const & smoothedCoordinates = gaze_data.avg;
        QPoint gaze(smoothedCoordinates.x, smoothedCoordinates.y);
        gaze = m_gazeoverlay->mapFromGlobal(gaze);
        m_gazeoverlay->setGaze(gaze);
    }
}
