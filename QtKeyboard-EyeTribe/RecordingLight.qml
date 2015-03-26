import QtQuick 2.0

Rectangle {
    property bool recording: true
    anchors.centerIn: parent
    border.color: "black"
    radius: 10
    width: 2*radius
    height: 2*radius
    color: recording?"red":"gray"
}
