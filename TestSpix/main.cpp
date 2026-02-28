#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQuickWindow>
#include <QQuickItem>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QFile>
#include "viewcontroller.h"
#include <Spix/AnyRpcServer.h>
#include <Spix/QtQmlBot.h>

// Helper function to recursively dump QML tree
QJsonObject dumpQmlObject(QObject* obj, int maxDepth = 10, int currentDepth = 0) {
    QJsonObject result;
    
    if (!obj || currentDepth >= maxDepth) {
        return result;
    }
    
    // Basic object info
    result["objectName"] = obj->objectName();
    result["className"] = QString(obj->metaObject()->className());
    
    // Get all properties
    QJsonObject properties;
    const QMetaObject* metaObj = obj->metaObject();
    for (int i = 0; i < metaObj->propertyCount(); ++i) {
        QMetaProperty prop = metaObj->property(i);
        QString propName = prop.name();
        QVariant propValue = obj->property(prop.name());
        
        // Only include simple types that can be serialized
        if (propValue.canConvert<QString>()) {
            properties[propName] = propValue.toString();
        } else if (propValue.canConvert<int>()) {
            properties[propName] = propValue.toInt();
        } else if (propValue.canConvert<bool>()) {
            properties[propName] = propValue.toBool();
        } else if (propValue.canConvert<double>()) {
            properties[propName] = propValue.toDouble();
        }
    }
    result["properties"] = properties;
    
    // Get children
    QJsonArray children;
    if (auto quickItem = qobject_cast<QQuickItem*>(obj)) {
        // For QQuickItem, use childItems()
        for (auto child : quickItem->childItems()) {
            children.append(dumpQmlObject(child, maxDepth, currentDepth + 1));
        }
    } else {
        // For regular QObject, use children()
        for (auto child : obj->children()) {
            children.append(dumpQmlObject(child, maxDepth, currentDepth + 1));
        }
    }
    
    if (!children.isEmpty()) {
        result["children"] = children;
    }
    
    return result;
}

int main(int argc, char *argv[])
{
    // // Force software rendering for deterministic screenshots
    // qputenv("QT_QUICK_BACKEND", "software");
    // qputenv("QSG_RHI_BACKEND", "software");
    
    // // Disable anti-aliasing for pixel-perfect rendering
    // QQuickWindow::setTextRenderType(QQuickWindow::NativeTextRendering);
    
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
    
    // Get mainWindow and add dynamic property for tree dump
    QObject* mainWindow = engine.rootObjects().first();
    mainWindow->setProperty("_qmlTreeJson", QString());  // Initialize property

    // Spix RPC Server starten
    spix::AnyRpcServer server;
    
    // Custom Command Handler
    server.setGenericCommandHandler([&viewController, mainWindow](std::string command, std::string payload) {
        if (command == "gotoPage1") {
            viewController.gotoPage1();
        } else if (command == "gotoPage2") {
            viewController.gotoPage2();
        } else if (command == "gotoPage3") {
            viewController.gotoPage3();
        } else if (command == "dumpQmlTree") {
            // Dump QML tree and store in mainWindow property
            QJsonObject tree = dumpQmlObject(mainWindow, 50);
            QJsonDocument doc(tree);
            QString jsonString = doc.toJson(QJsonDocument::Compact);  // Compact for transfer
            
            // Store in dynamic property (readable via getStringProperty)
            mainWindow->setProperty("_qmlTreeJson", jsonString);
            
            // Optional: Also write to file as fallback
            if (!payload.empty()) {
                QFile file(QString::fromStdString(payload));
                if (file.open(QIODevice::WriteOnly)) {
                    file.write(doc.toJson(QJsonDocument::Indented));
                    file.close();
                }
            }
        }
        
        return std::string();
    });
    
    auto bot = new spix::QtQmlBot();
    bot->runTestServer(server);

    return app.exec();
}
