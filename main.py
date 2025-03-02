import sys
import json
import psutil
import pygetwindow as gw
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox

SNAPSHOT_FILE = "snapshot.json"

class SnapshotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Snapshot & Restore")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        self.listWidget = QListWidget()
        layout.addWidget(self.listWidget)
        
        self.snapshotBtn = QPushButton("Take Snapshot")
        self.snapshotBtn.clicked.connect(self.take_snapshot)
        layout.addWidget(self.snapshotBtn)
        
        self.restoreBtn = QPushButton("Restore Windows")
        self.restoreBtn.clicked.connect(self.restore_snapshot)
        layout.addWidget(self.restoreBtn)
        
        self.setLayout(layout)
    
    def take_snapshot(self):
        windows = gw.getAllWindows()
        snapshot = []
        for window in windows:
            if window.title:
                for proc in psutil.process_iter(attrs=['pid', 'name']):
                    if proc.info['name'] and proc.info['pid'] == window._hwnd:
                        snapshot.append({
                            "title": window.title,
                            "process": proc.info['name']
                        })
                        break
        
        with open(SNAPSHOT_FILE, "w") as f:
            json.dump(snapshot, f, indent=4)
        
        self.listWidget.clear()
        for item in snapshot:
            self.listWidget.addItem(f"{item['process']} - {item['title']}")
        
        QMessageBox.information(self, "Snapshot Taken", "Open windows have been saved!")
    
    def restore_snapshot(self):
        try:
            with open(SNAPSHOT_FILE, "r") as f:
                snapshot = json.load(f)
            
            for item in snapshot:
                subprocess.Popen(item['process'], shell=True)
            
            QMessageBox.information(self, "Restoration Complete", "Windows have been restored!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to restore: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SnapshotApp()
    ex.show()
    sys.exit(app.exec_())

