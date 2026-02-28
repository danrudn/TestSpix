#ifndef VIEWCONTROLLER_H
#define VIEWCONTROLLER_H

#include <QObject>
#include "statechart.h"

class ViewController : public QObject
{
    Q_OBJECT
public:
    explicit ViewController(statechart *stateMachine, QObject *parent = nullptr);

public slots:
    void gotoPage1();
    void gotoPage2();
    void gotoPage3();

signals:
    void page1();
    void page2();
    void page3();

private:
    statechart *m_stateMachine;
};

#endif // VIEWCONTROLLER_H
