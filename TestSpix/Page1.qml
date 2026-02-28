import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#667eea" }
            GradientStop { position: 1.0; color: "#764ba2" }
        }

        Column {
            anchors.centerIn: parent
            spacing: 30

            Text {
                text: "🏠 Home"
                font.pixelSize: 48
                font.bold: true
                color: "white"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Text {
                text: "Willkommen zur ersten Seite"
                font.pixelSize: 20
                color: "white"
                opacity: 0.9
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Rectangle {
                width: 300
                height: 150
                color: "white"
                opacity: 0.2
                radius: 15
                anchors.horizontalCenter: parent.horizontalCenter

                Column {
                    anchors.centerIn: parent
                    spacing: 10

                    Text {
                        text: "✓ Feature 1"
                        font.pixelSize: 18
                        color: "white"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    Text {
                        text: "✓ Feature 2"
                        font.pixelSize: 18
                        color: "white"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                    Text {
                        text: "✓ Feature 3"
                        font.pixelSize: 18
                        color: "white"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }
            }
        }
    }
}
