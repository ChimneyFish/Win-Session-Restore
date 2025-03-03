#include "SnapshotApp.h"

SnapshotApp::SnapshotApp(QWidget *parent)
    : QWidget(parent)
{
    setWindowTitle("Snapshot & Restore");
    setGeometry(100, 100, 400, 300);

    QVBoxLayout *layout = new QVBoxLayout(this);

    listWidget = new QListWidget(this);
    layout->addWidget(listWidget);

    QPushButton *snapshotBtn = new QPushButton("Take Snapshot", this);
    connect(snapshotBtn, &QPushButton::clicked, this, &SnapshotApp::takeSnapshot);
    layout->addWidget(snapshotBtn);

    QPushButton *restoreBtn = new QPushButton("Restore Windows", this);
    connect(restoreBtn, &QPushButton::clicked, this, &SnapshotApp::restoreSnapshot);
    layout->addWidget(restoreBtn);

    setLayout(layout);
}

SnapshotApp::~SnapshotApp() {}

void SnapshotApp::takeSnapshot()
{
    // Capture running processes and window titles
    Json::Value snapshot;
    HWND hwnd = GetTopWindow(NULL);
    while (hwnd != NULL)
    {
        char wnd_title[256];
        GetWindowTextA(hwnd, wnd_title, sizeof(wnd_title));
        DWORD pid;
        GetWindowThreadProcessId(hwnd, &pid);

        HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, pid);
        if (hProcess)
        {
            char exePath[MAX_PATH];
            if (GetModuleFileNameExA(hProcess, NULL, exePath, MAX_PATH))
            {
                Json::Value process;
                process["title"] = wnd_title;
                process["exe"] = exePath;
                // For simplicity, command line args not captured here
                snapshot.append(process);
            }
            CloseHandle(hProcess);
        }
        hwnd = GetNextWindow(hwnd, GW_HWNDNEXT);
    }

    saveSnapshot(snapshot);

    listWidget->clear();
    for (const auto &item : snapshot)
    {
        listWidget->addItem(QString::fromStdString(item["exe"].asString()) + " - " + QString::fromStdString(item["title"].asString()));
    }

    QMessageBox::information(this, "Snapshot Taken", "Open windows have been saved!");
}

void SnapshotApp::restoreSnapshot()
{
    Json::Value snapshot = loadSnapshot();
    for (const auto &item : snapshot)
    {
        std::string exe = item["exe"].asString();
        std::string title = item["title"].asString();
        ShellExecuteA(NULL, "open", exe.c_str(), NULL, NULL, SW_SHOW);
    }
    QMessageBox::information(this, "Restoration Complete", "Windows have been restored!");
}

void SnapshotApp::saveSnapshot(const Json::Value &snapshot)
{
    std::ofstream file("snapshot.json");
    file << snapshot;
    file.close();
}

Json::Value SnapshotApp::loadSnapshot()
{
    std::ifstream file("snapshot.json");
    Json::Value snapshot;
    file >> snapshot;
    file.close();
    return snapshot;
}
