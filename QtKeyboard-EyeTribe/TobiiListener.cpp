/*
 * This code is based on MinimalGazeDataStream.c provided in the Tobii SDK.
 * I couldn't find the documentation for the C++ API (and I only found C++11 code), so I used the C API.
 */

#include <QDebug>
#include <cassert>

#include "TobiiListener.h"

// Function declarations
void initialize();
void release();
bool InitializeGlobalInteractorSnapshot(TX_CONTEXTHANDLE hContext);
void TX_CALLCONVENTION OnSnapshotCommitted(TX_CONSTHANDLE hAsyncData, TX_USERPARAM param);
void TX_CALLCONVENTION OnEngineConnectionStateChanged(TX_CONNECTIONSTATE connectionState, TX_USERPARAM userParam);
void OnGazeDataEvent(TX_HANDLE hGazeDataBehavior);
void TX_CALLCONVENTION HandleEvent(TX_CONSTHANDLE hAsyncData, TX_USERPARAM userParam);

// ID of the global interactor that provides our data stream; must be unique within the application.
static const TX_STRING InteractorId = "KeyEyeInteractor";

// global variables
static TX_HANDLE g_hGlobalInteractorSnapshot = TX_EMPTY_HANDLE;
static TX_CONTEXTHANDLE hContext = TX_EMPTY_HANDLE;
static QList<TobiiListener *> instances;

TobiiListener::TobiiListener(QObject *parent, GazeOverlay *gazeOverlay) :
    GazeListener(parent, gazeOverlay, "tstamp,gaze_x,gaze_y\n")
{
    if (instances.size() == 0) initialize();
    instances.append(this);
}

TobiiListener::~TobiiListener()
{
    instances.removeAll(this);
    if (instances.size() == 0) release();
}

void TobiiListener::onGaze(double tstamp, QPointF gaze)
{
    emit newGaze(gaze.toPoint());
    // Get gaze position in keyboard normalized image coordinates
    gaze = normalize(gaze.toPoint());

    if (isRecording())
    {
        QString csvLine;
        csvLine.sprintf("%f,%f,%f\n", tstamp, gaze.x(), gaze.y());
        printToFile(csvLine);
    }
}

void initialize()
{
    hContext = TX_EMPTY_HANDLE;
    TX_TICKET hConnectionStateChangedTicket = TX_INVALID_TICKET;
    TX_TICKET hEventHandlerTicket = TX_INVALID_TICKET;
    bool success;

    // initialize and enable the context that is our link to the EyeX Engine.
    success = txInitializeEyeX(TX_EYEXCOMPONENTOVERRIDEFLAG_NONE, NULL, NULL, NULL, NULL) == TX_RESULT_OK;
    success &= txCreateContext(&hContext, TX_FALSE) == TX_RESULT_OK;
    success &= InitializeGlobalInteractorSnapshot(hContext);
    success &= txRegisterConnectionStateChangedHandler(hContext, &hConnectionStateChangedTicket, &OnEngineConnectionStateChanged, NULL) == TX_RESULT_OK;
    success &= txRegisterEventHandler(hContext, &hEventHandlerTicket, HandleEvent, NULL) == TX_RESULT_OK;
    success &= txEnableConnection(hContext) == TX_RESULT_OK;

    // let the events flow until a key is pressed.
    if (success) {
        qDebug() << "(EyeX) Initialization was successful.";
    } else {
        qDebug() << "(EyeX) Initialization failed.";
    }
}

void release()
{
    // disable and delete the context.
    bool success;
    txDisableConnection(hContext);
    txReleaseObject(&g_hGlobalInteractorSnapshot);
    success = txShutdownContext(hContext, TX_CLEANUPTIMEOUT_DEFAULT, TX_FALSE) == TX_RESULT_OK;
    success &= txReleaseContext(&hContext) == TX_RESULT_OK;
    success &= txUninitializeEyeX() == TX_RESULT_OK;
    if (!success) {
        qDebug() << "EyeX could not be shut down cleanly. Did you remember to release all handles?";
    }
}

/*
 * Initializes g_hGlobalInteractorSnapshot with an interactor that has the Gaze Point behavior.
 */
bool InitializeGlobalInteractorSnapshot(TX_CONTEXTHANDLE hContext)
{
    TX_HANDLE hInteractor = TX_EMPTY_HANDLE;
    TX_GAZEPOINTDATAPARAMS params = { TX_GAZEPOINTDATAMODE_LIGHTLYFILTERED };
    bool success;

    success = txCreateGlobalInteractorSnapshot(
        hContext,
        InteractorId,
        &g_hGlobalInteractorSnapshot,
        &hInteractor) == TX_RESULT_OK;
    success &= txCreateGazePointDataBehavior(hInteractor, &params) == TX_RESULT_OK;

    txReleaseObject(&hInteractor);

    return success;
}

/*
 * Callback function invoked when a snapshot has been committed.
 */
void TX_CALLCONVENTION OnSnapshotCommitted(TX_CONSTHANDLE hAsyncData, TX_USERPARAM param)
{
    Q_UNUSED(param)
    // check the result code using an assertion.
    // this will catch validation errors and runtime errors in debug builds. in release builds it won't do anything.

    TX_RESULT result = TX_RESULT_UNKNOWN;
    txGetAsyncDataResultCode(hAsyncData, &result);
    assert(result == TX_RESULT_OK || result == TX_RESULT_CANCELLED);
}

/*
 * Callback function invoked when the status of the connection to the EyeX Engine has changed.
 */
void TX_CALLCONVENTION OnEngineConnectionStateChanged(TX_CONNECTIONSTATE connectionState,
                                                                     TX_USERPARAM userParam)
{
    Q_UNUSED(userParam)
    switch (connectionState) {
    case TX_CONNECTIONSTATE_CONNECTED: {
            bool success;
            qDebug() << "(EyeX) The connection state is now CONNECTED (We are connected to the EyeX Engine)";
            // commit the snapshot with the global interactor as soon as the connection to the engine is established.
            // (it cannot be done earlier because committing means "send to the engine".)
            success = txCommitSnapshotAsync(g_hGlobalInteractorSnapshot, OnSnapshotCommitted, NULL) == TX_RESULT_OK;
            if (!success) {
                qDebug() << "(EyeX) Failed to initialize the data stream.";
            }
            else {
                qDebug() << "(EyeX) Waiting for gaze data to start streaming...";
            }
        }
        break;

    case TX_CONNECTIONSTATE_DISCONNECTED:
        qDebug() << "(EyeX) The connection state is now DISCONNECTED (We are disconnected from the EyeX Engine)";
        break;

    case TX_CONNECTIONSTATE_TRYINGTOCONNECT:
        qDebug() << "(EyeX) The connection state is now TRYINGTOCONNECT (We are trying to connect to the EyeX Engine)";
        break;

    case TX_CONNECTIONSTATE_SERVERVERSIONTOOLOW:
        qDebug() << "(EyeX) The connection state is now SERVER_VERSION_TOO_LOW: this application requires a more recent version of the EyeX Engine to run.";
        break;

    case TX_CONNECTIONSTATE_SERVERVERSIONTOOHIGH:
        qDebug() << "(EyeX) The connection state is now SERVER_VERSION_TOO_HIGH: this application requires an older version of the EyeX Engine to run.";
        break;
    }
}

/*
 * Handles an event from the Gaze Point data stream.
 */
void OnGazeDataEvent(TX_HANDLE hGazeDataBehavior)
{
    TX_GAZEPOINTDATAEVENTPARAMS eventParams;
    if (txGetGazePointDataEventParams(hGazeDataBehavior, &eventParams) == TX_RESULT_OK) {
        foreach (TobiiListener *listener, instances) {
            listener->onGaze(eventParams.Timestamp, QPointF(eventParams.X, eventParams.Y));
        }
    } else {
        qDebug() << "(EyeX) Failed to interpret gaze data event packet.";
    }
}

/*
 * Callback function invoked when an event has been received from the EyeX Engine.
 */
void TX_CALLCONVENTION HandleEvent(TX_CONSTHANDLE hAsyncData, TX_USERPARAM userParam)
{
    Q_UNUSED(userParam)
    TX_HANDLE hEvent = TX_EMPTY_HANDLE;
    TX_HANDLE hBehavior = TX_EMPTY_HANDLE;

    txGetAsyncDataContent(hAsyncData, &hEvent);

    // NOTE. Uncomment the following line of code to view the event object. The same function can be used with any interaction object.
    //OutputDebugStringA(txDebugObject(hEvent));

    if (txGetEventBehavior(hEvent, &hBehavior, TX_BEHAVIORTYPE_GAZEPOINTDATA) == TX_RESULT_OK) {
        OnGazeDataEvent(hBehavior);
        txReleaseObject(&hBehavior);
    }

    // NOTE since this is a very simple application with a single interactor and a single data stream,
    // our event handling code can be very simple too. A more complex application would typically have to
    // check for multiple behaviors and route events based on interactor IDs.

    txReleaseObject(&hEvent);
}
