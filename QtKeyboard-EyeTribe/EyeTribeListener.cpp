#include "EyeTribeListener.h"

EyeTribeListener::EyeTribeListener(QObject *parent, GazeOverlay *gazeOverlay) :
    GazeListener(parent, gazeOverlay, "tstamp,raw_x,raw_y,smoothed_x,smoothed_y,fix\n")
{
    // Connect to the server in push mode on the default TCP port (6555)
    if(m_api.connect(true))
    {
        // Enable GazeData notifications
        m_api.add_listener(*this);
    }
}

EyeTribeListener::~EyeTribeListener()
{
    m_api.remove_listener(*this);
    m_api.disconnect();
}

void EyeTribeListener::on_gaze_data(gtl::GazeData const & gaze_data)
{
    if(gaze_data.state & gtl::GazeData::GD_STATE_TRACKING_GAZE)
    {
        QPoint raw(gaze_data.raw.x, gaze_data.raw.y);
        QPoint avg(gaze_data.avg.x, gaze_data.avg.y);
        emit newGaze(avg);
        // Get gaze position in keyboard normalized image coordinates
        QPointF rawN = normalize(raw);
        QPointF avgN = normalize(avg);

        if (isRecording())
        {
            QString csvLine;
            csvLine.sprintf("%d,%f,%f,%f,%f,%d\n", gaze_data.time, rawN.x(), rawN.y(), avgN.x(), avgN.y(), gaze_data.fix);
            printToFile(csvLine);
        }
    }
}

