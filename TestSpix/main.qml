import QtQuick 2.15
import QtQuick.Window 2.15

Window {
    id: mainWindow
    width: 640
    height: 480
    visible: true

    Item {
        id: rootItem
        anchors.fill: parent

        Loader {
            id: pageLoader
            anchors.fill: parent
        }

        states: [
            State {
                name: "page1"
                when: stateMachine.state1
                PropertyChanges {
                    target: pageLoader
                    source: "Page1.qml"
                }
            },
            State {
                name: "page2"
                when: stateMachine.state2
                PropertyChanges {
                    target: pageLoader
                    source: "Page2.qml"
                }
            },
            State {
                name: "page3"
                when: stateMachine.state3
                PropertyChanges {
                    target: pageLoader
                    source: "Page3.qml"
                }
            }
        ]
    }
}
