#ifndef IDATARECORDER_H
#define IDATARECORDER_H

#include <QString>

class IDataRecorder
{
public:
    virtual void startRecording(QString filename) = 0;
    virtual void stopRecording() = 0;
    virtual bool isRecording() = 0;
};

#endif // IDATARECORDER_H
