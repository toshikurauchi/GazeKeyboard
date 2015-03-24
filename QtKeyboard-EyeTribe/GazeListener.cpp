#include "GazeListener.h"

const QString GazeListener::header = "raw_x,raw_y,smoothed_x,smoothed_y,fix";

GazeListener::GazeListener(GazeOverlay *gazeOverlay) :
    m_gazeoverlay(gazeOverlay), file(0), out_stream(0)
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
    if (file)
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

void GazeListener::on_gaze_data(gtl::GazeData const & gaze_data)
{
    if(gaze_data.state & gtl::GazeData::GD_STATE_TRACKING_GAZE)
    {
        QPoint raw(gaze_data.raw.x, gaze_data.raw.y);
        QPoint avg(gaze_data.avg.x, gaze_data.avg.y);
        // Get gaze position in keyboard image coordinates
        raw = m_gazeoverlay->mapFromGlobal(raw);
        avg = m_gazeoverlay->mapFromGlobal(avg);
        m_gazeoverlay->setGaze(avg);

        // Normalize coordinates
        raw.setX(raw.x()/m_gazeoverlay->width());
        raw.setY(raw.y()/m_gazeoverlay->height());
        avg.setX(avg.x()/m_gazeoverlay->width());
        avg.setY(avg.y()/m_gazeoverlay->height());
        if (file)
        {
            *out_stream << raw.x() << "," << raw.y() << "," <<  avg.x() << "," << avg.y() << "," << gaze_data.fix;
        }
    }
}
