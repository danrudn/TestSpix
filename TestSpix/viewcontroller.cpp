#include "viewcontroller.h"

ViewController::ViewController(statechart *stateMachine, QObject *parent)
    : QObject(parent)
    , m_stateMachine(stateMachine)
{
    setObjectName("viewController");
}

void ViewController::gotoPage1()
{
    m_stateMachine->submitEvent("gotoPage1");
}

void ViewController::gotoPage2()
{
    m_stateMachine->submitEvent("gotoPage2");
}

void ViewController::gotoPage3()
{
    m_stateMachine->submitEvent("gotoPage3");
}
