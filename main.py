import subprocess
import sys
import json
import psutil
import win32gui
import win32process
import os
import pyautogui
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap

SNAPSHOT_FILE = os.path.join(os.getcwd(), "snapshot.json")
EDGE_RESTORE_IMAGE = r"C:/Program Files(x86)/winfreezeFrame/msedge-restore.png"
OUTLOOK_RESTORE_IMAGE = r"C:/Program Files(x86)/winfreezeFrame/restore_button_image.png"

class SnapshotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("WinFreezeFrame")
        self.setGeometry(100, 100, 800, 600)

        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(QPixmap(r'C:/Users/hotty/Win-Session-Restore/icons/icon.jpg')))
        self.setPalette(palette)

        layout = QVBoxLayout()

        self.listWidget = QListWidget()
        layout.addWidget(self.listWidget)

        self.snapshotBtn = QPushButton("Freeze Frame")
        self.snapshotBtn.setFont(QFont('Comic Sans MS', 14))
        self.snapshotBtn.setStyleSheet("background-color: #031b89; color: #fd3a0e;")
        self.snapshotBtn.clicked.connect(self.take_snapshot)
        layout.addWidget(self.snapshotBtn)

        self.restoreBtn = QPushButton("Restore Session")
        self.restoreBtn.setFont(QFont('Comic Sans MS', 14))
        self.restoreBtn.setStyleSheet("background-color: #09e700; color: #fd3a0e;")
        self.restoreBtn.clicked.connect(self.restore_snapshot)
        layout.addWidget(self.restoreBtn)

        self.setLayout(layout)

    def take_snapshot(self):
        try:
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
                    if pid == os.getpid():  # Skip capturing the current application
                        return
                    title = win32gui.GetWindowText(hwnd)
                    if title:
                        rect = win32gui.GetWindowRect(hwnd)
                        windows.append({
                            "pid": pid,
                            "hwnd": hwnd,
                            "title": title,
                            "window_position": rect
                        })

            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)

            if not windows:
                QMessageBox.critical(self, "No Windows Found", "No open windows were detected!")
                return

            snapshot = []
            for window in windows:
                try:
                    proc = psutil.Process(window["pid"])
                    snapshot.append({
                        "title": window["title"],
                        "process": proc.name(),
                        "exe_path": proc.exe(),
                        "cmdline": proc.cmdline(),
                        "window_position": window["window_position"],
                        "hwnd": window["hwnd"]
                    })
                except (psutil.NoSuchProcess, win32gui.error):
                    continue

            with open(SNAPSHOT_FILE, "w") as f:
                json.dump(snapshot, f, indent=4)

            self.listWidget.clear()
            for item in snapshot:
                self.listWidget.addItem(f"{item['process']} - {item['title']}")

            QMessageBox.information(self, "Snapshot Taken", "Open windows have been saved!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to take snapshot: {str(e)}")

    def restore_snapshot(self):
        try:
            if not os.path.exists(SNAPSHOT_FILE):
                QMessageBox.warning(self, "File Not Found", "Snapshot file does not exist!")
                return

            with open(SNAPSHOT_FILE, "r") as f:
                snapshot = json.load(f)

            if not snapshot or not isinstance(snapshot, list):
                QMessageBox.warning(self, "Invalid Data", "Snapshot data is corrupted or empty!")
                return

            outlook_restored = False  # Flag to handle Outlook restoration separately
            edge_restored = False  # Flag to handle Edge restoration separately

            for item in snapshot:
                try:
                    process_name = item['process'].lower()
                    if process_name == "outlook.exe":
                        if not outlook_restored:
                            self.restore_outlook()
                            outlook_restored = True
                        continue

                    if process_name == "msedge.exe":
                        if not edge_restored:
                            self.restore_edge()
                            edge_restored = True
                        continue

                    if item.get("hwnd") and win32gui.IsWindow(item["hwnd"]):
                        rect = item["window_position"]
                        win32gui.MoveWindow(item["hwnd"], rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1], True)
                        win32gui.SetForegroundWindow(item["hwnd"])
                    else:
                        subprocess.Popen(item['exe_path'], shell=True)
                except Exception as e:
                    continue

            QMessageBox.information(self, "Restoration Complete", "Windows have been restored!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to restore: {e}")

    def restore_outlook(self):
        try:
            # Check if Outlook is already running
            outlook_running = any(
                proc.info['name'].lower() == "outlook.exe" for proc in psutil.process_iter(['name'])
            )
            if not outlook_running:
                print("Starting Outlook...")
                os.startfile("outlook.exe")
                time.sleep(5)  # Wait for Outlook to fully open

            # Automate clicking "Restore Data" using PyAutoGUI
            print("Looking for 'Restore Data' button...")
            time.sleep(3)  # Give time for the recovery prompt to appear

            # Locate and click the "Restore Data" button
            restore_button_position = pyautogui.locateOnScreen(OUTLOOK_RESTORE_IMAGE)
            if restore_button_position:
                print("Found 'Restore Data' button. Clicking it...")
                pyautogui.click(restore_button_position)
            else:
                print("'Restore Data' button not found. Ensure the image matches the button.")

        except Exception as e:
            QMessageBox.warning(self, "Outlook Error", f"Failed to restore Outlook: {str(e)}")

    def restore_edge(self):
        try:
            # Check if Edge is already running
            edge_running = any(
                proc.info['name'].lower() == "msedge.exe" for proc in psutil.process_iter(['name'])
            )
            if not edge_running:
                print("Starting Edge...")
                os.startfile("msedge.exe")
                time.sleep(5)  # Wait for Edge to fully open

            # Automate clicking "Restore Tabs" using PyAutoGUI
            print("Looking for 'Restore Tabs' button in Edge...")
            time.sleep(3)  # Give time for the recovery prompt to appear

            # Locate and click the "Restore Tabs" button
            restore_button_position = pyautogui.locateOnScreen(EDGE_RESTORE_IMAGE)
            if restore_button_position:
                print("Found 'Restore Tabs' button in Edge. Clicking it...")
                pyautogui.click(restore_button_position)
            else:
                print("'Restore Tabs' button not found in Edge. Ensure the image matches the button.")

        except Exception as e:
            QMessageBox.warning(self, "Edge Error", f"Failed to restore Edge tabs: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SnapshotApp()
    ex.show()
    sys.exit(app.exec_())