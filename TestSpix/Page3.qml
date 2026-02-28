import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#f093fb" }
            GradientStop { position: 0.5; color: "#f5576c" }
            GradientStop { position: 1.0; color: "#4facfe" }
        }

        Column {
            anchors.centerIn: parent
            spacing: 30

            Text {
                text: "🎉 Fertig!"
                font.pixelSize: 52
                font.bold: true
                color: "white"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Rectangle {
                width: 350
                height: 200
                color: "white"
                opacity: 0.3
                radius: 20
                anchors.horizontalCenter: parent.horizontalCenter

                Column {
                    anchors.centerIn: parent
                    spacing: 15

                    Text {
                        text: "✨ Erfolg!"
                        font.pixelSize: 24
                        font.bold: true
                        color: "white"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Text {
                        text: "Du hast alle Seiten durchlaufen"
                        font.pixelSize: 16
                        color: "white"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Rectangle {
                        width: 250
                        height: 4
                        color: "white"
                        opacity: 0.5
                        anchors.horizontalCenter: parent.horizontalCenter
                    }

                    Text {
                        text: "⭐⭐⭐⭐⭐"
                        font.pixelSize: 28
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }
            }
        }

        // Animierte Kreise im Hintergrund
        Repeater {
            model: 5
            Rectangle {
                width: 60 + index * 20
                height: width
                radius: width / 2
                color: "transparent"
                border.color: "white"
                border.width: 2
                opacity: 0.2
                x: Math.random() * parent.width
                y: Math.random() * parent.height

                SequentialAnimation on scale {
                    loops: Animation.Infinite
                    NumberAnimation { from: 0.8; to: 1.2; duration: 2000 + index * 500 }
                    NumberAnimation { from: 1.2; to: 0.8; duration: 2000 + index * 500 }
                }
            }
        }
    }
}
