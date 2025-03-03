#include <QApplication>
#include "SnapshotApp.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    SnapshotApp snapshotApp;
    snapshotApp.show();
    return app.exec();
}
