#ifndef SNAPSHOTAPP_H
#define SNAPSHOTAPP_H

#include <QWidget>
#include <QVBoxLayout>
#include <QPushButton>
#include <QListWidget>
#include <QMessageBox>
#include <windows.h>
#include <TlHelp32.h>
#include <fstream>
#include <json/json.h>

class SnapshotApp : public QWidget
{
    Q_OBJECT

public:
    SnapshotApp(QWidget *parent = nullptr);
    ~SnapshotApp();

private slots:
    void takeSnapshot();
    void restoreSnapshot();

private:
    void saveSnapshot(const Json::Value &snapshot);
    Json::Value loadSnapshot();
    QListWidget *listWidget;
};

#endif // SNAPSHOTAPP_H
