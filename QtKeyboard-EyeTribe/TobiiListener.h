#ifndef TOBIILISTENER_H
#define TOBIILISTENER_H

#include <QList>

#include "eyex/EyeX.h"

#include "GazeListener.h"
#include "GazeOverlay.h"

class TobiiListener : public GazeListener
{
    Q_OBJECT

public:
    TobiiListener(QObject *parent, GazeOverlay *gazeOverlay);
    ~TobiiListener();
    void onGaze(double tstamp, QPointF gaze);
};

#endif // TOBIILISTENER_H
