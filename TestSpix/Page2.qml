import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    Rectangle {
        anchors.fill: parent
        color: "#1a1a2e"

        Column {
            anchors.centerIn: parent
            spacing: 40

            Text {
                text: "⚙️ Dashboard"
                font.pixelSize: 44
                font.bold: true
                color: "#00d4ff"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Row {
                spacing: 20
                anchors.horizontalCenter: parent.horizontalCenter

                Rectangle {
                    width: 120
                    height: 120
                    color: "#16213e"
                    radius: 10
                    border.color: "#00d4ff"
                    border.width: 2

                    Column {
                        anchors.centerIn: parent
                        spacing: 10

                        Text {
                            text: "📊"
                            font.pixelSize: 40
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                        Text {
                            text: "Statistiken"
                            font.pixelSize: 14
                            color: "white"
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                Rectangle {
                    width: 120
                    height: 120
                    color: "#16213e"
                    radius: 10
                    border.color: "#00d4ff"
                    border.width: 2

                    Column {
                        anchors.centerIn: parent
                        spacing: 10

                        Text {
                            text: "📈"
                            font.pixelSize: 40
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                        Text {
                            text: "Berichte"
                            font.pixelSize: 14
                            color: "white"
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }
                }

                Rectangle {
                    width: 120
                    height: 120
                    color: "#16213e"
                    radius: 10
                    border.color: "#00d4ff"
                    border.width: 2

                    Column {
                        anchors.centerIn: parent
                        spacing: 10

                        Text {
                            text: "⚡"
                            font.pixelSize: 40
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                        Text {
                            text: "Schnell"
                            font.pixelSize: 14
                            color: "white"
                            anchors.horizontalCenter: parent.horizontalCenter
                        }
                    }
                }
            }

            Row {
                spacing: 20
                anchors.horizontalCenter: parent.horizontalCenter

                Button {
                    text: "← Zurück"
                    font.pixelSize: 14
                    onClicked: viewController.gotoPage1()

                    background: Rectangle {
                        color: parent.pressed ? "#0f3460" : "#16213e"
                        border.color: "#00d4ff"
                        border.width: 2
                        radius: 8
                        implicitWidth: 120
                        implicitHeight: 45
                    }
                    contentItem: Text {
                        text: parent.text
                        font: parent.font
                        color: "#00d4ff"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
            }
        }
    }
}
