#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "viewcontroller.h"
#include <Spix/AnyRpcServer.h>
#include <Spix/QtQmlBot.h>

int main(int argc, char *argv[])
{
#if QT_VERSION < QT_VERSION_CHECK(6, 0, 0)
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
#endif
    QGuiApplication app(argc, argv);

    // start app
    statechart m_stateMachine;
    m_stateMachine.start();
    ViewController viewController(&m_stateMachine);

    // start qml engine
    QQmlApplicationEngine engine;
    // ViewController als QML-Objekt registrieren
    engine.rootContext()->setContextProperty("viewController", &viewController);
    // Statemachine direkt für QML-State-Bindings bereitstellen
    engine.rootContext()->setContextProperty("stateMachine", &m_stateMachine);

    const QUrl url(QStringLiteral("qrc:/main.qml"));
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreated,
        &app,
        [url](QObject *obj, const QUrl &objUrl) {
            if (!obj && url == objUrl)
                QCoreApplication::exit(-1);
        },
        Qt::QueuedConnection);
    engine.load(url);

    // Spix RPC Server starten
    spix::AnyRpcServer server;
    
    // Custom Command Handler für Navigation registrieren
    server.setGenericCommandHandler([&viewController](std::string command, std::string payload) {
        if (command == "gotoPage1") {
            viewController.gotoPage1();
        } else if (command == "gotoPage2") {
            viewController.gotoPage2();
        } else if (command == "gotoPage3") {
            viewController.gotoPage3();
        }
    });
    
    auto bot = new spix::QtQmlBot();
    bot->runTestServer(server);

    return app.exec();
}
