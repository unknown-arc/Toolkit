import sys
import subprocess
from pathlib import Path
import random

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import QTimer, Qt

from core.signal_manager import Lab_eb, Session_eb
from core.lab_and_session_manager.registor_external_app import register


class ExternalProcessWidget(QWidget):

    def __init__(self, app_path: Path, app_name: str, lab_id: str, session_id: str, parent=None):
        super().__init__(parent)

        self.lab_id = lab_id
        self.session_id = session_id
        self.app_path = Path(app_path)
        self.app_name = app_name
        self._closing = False

        register(self)

        # Start the external Python script
        self.proc = subprocess.Popen(
            [sys.executable, str(self.app_path)],
            cwd=str(self.app_path.parent),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.DEVNULL
        )

        self.setWindowTitle(f"{self.app_name} (External App)")
        self.setMinimumSize(400, 140)

        # -------------------------------
        # Modern UI Layout
        # -------------------------------
        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        layout.setContentsMargins(40, 25, 40, 25)

        # ------------------------------------------------------
        # 1) LOADING MESSAGE (shown first)
        # ------------------------------------------------------
        self.loading_label = QLabel("Your app is loading...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: 500;
                color: #555;
            }
        """)
        layout.addStretch(2)
        layout.addWidget(self.loading_label, alignment=Qt.AlignCenter)

        # ------------------------------------------------------
        # 2) REAL UI (hidden for first 3 seconds)
        # ------------------------------------------------------
        self.real_ui = QWidget()
        real_layout = QVBoxLayout(self.real_ui)
        real_layout.setSpacing(18)
        real_layout.setContentsMargins(0, 0, 0, 0)

        # App Name
        title = QLabel(f"{self.app_name} is running in new Window")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: 600;
                color: #1a1a1a;
            }
        """)

        # Show App Button
        btn_show = QPushButton("Show App")
        btn_show.setFixedHeight(38)
        btn_show.setFixedWidth(300)
        btn_show.setStyleSheet("""
            QPushButton {
                background-color: #C5DBFF;
                color: white;
                font-size: 15px;
                border-radius: 8px;
                padding: 6px 14px;
            }
            QPushButton:hover {
                background-color: #1a66e5;
            }
        """)

        # Close App Button
        btn_close = QPushButton("Close App")
        btn_close.setFixedHeight(38)
        btn_close.setFixedWidth(300)
        btn_close.setStyleSheet("""
            QPushButton {
                background-color: #FFC5C5;
                color: white;
                font-size: 15px;
                border-radius: 8px;
                padding: 6px 14px;
            }
            QPushButton:hover {
                background-color: #e84848;
            }
        """)

        btn_show.clicked.connect(self._bring_to_front)
        btn_close.clicked.connect(self._terminate_process)

        real_layout.addWidget(title)
        real_layout.addWidget(btn_show, alignment=Qt.AlignCenter)
        real_layout.addWidget(btn_close, alignment=Qt.AlignCenter)

        self.real_ui.hide()        # <== Hide real UI
        layout.addWidget(self.real_ui)  # Add AFTER loading label
        layout.addStretch(3)


        # ------------------------------------------------------
        # 3) SHOW REAL UI AFTER 3 SECONDS
        # ------------------------------------------------------
        QTimer.singleShot(random.randint(2000, 4000), self._show_real_ui)


        # Monitor process
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._check_process)
        self.timer.start(1000)

        Session_eb.session_closed.connect(self._session_closed)
        Session_eb.all_sessions_closed.connect(self.force_close)

    # -------------------------------
    # Helper functions
    # -------------------------------
    def _show_real_ui(self):
        self.loading_label.hide()
        self.real_ui.show()

    def _bring_to_front(self):
        """Bring the external process window to the front (Windows only)."""
        try:
            import ctypes
            import time

            time.sleep(0.1)  # tiny delay so window is ready

            user32 = ctypes.windll.user32
            kernel32 = ctypes.windll.kernel32

            pid = self.proc.pid

            # Callback to find matching window by PID
            hwnd_target = None

            def enum_windows_callback(hwnd, lParam):
                nonlocal hwnd_target
                window_pid = ctypes.c_ulong()
                user32.GetWindowThreadProcessId(hwnd, ctypes.byref(window_pid))
                if window_pid.value == pid:
                    hwnd_target = hwnd
                    return False  # stop searching
                return True

            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool,
                                                ctypes.c_int,
                                                ctypes.c_int)

            user32.EnumWindows(EnumWindowsProc(enum_windows_callback), 0)

            if hwnd_target:
                user32.ShowWindow(hwnd_target, 5)       # SW_SHOW
                user32.SetForegroundWindow(hwnd_target) # Bring to front
            else:
                print("Window not found for PID:", pid)

        except Exception as e:
            print("Bring-to-front failed:", e)


    def _check_process(self):
        if self.proc.poll() is not None:
            self.timer.stop()
            Lab_eb.close_lab.emit(self.lab_id)
            self.force_close()

    def _terminate_process(self):
        if self.proc and self.proc.poll() is None:
            try:
                self.proc.terminate()
            except:
                try:
                    self.proc.kill()
                except:
                    pass

    def _session_closed(self, sid: str):
        if sid == self.session_id:
            self.force_close()

    def closeEvent(self, event):
        if self._closing:
            event.accept()
            return
        self._closing = True

        try: self._terminate_process()
        except: pass
        try: self.timer.stop()
        except: pass

        event.accept()

    def force_close(self):
        if self._closing:
            return

        self._closing = True

        try: self._terminate_process()
        except: pass
        try: super().close()
        except: pass

    def __del__(self):
        try: self._terminate_process()
        except: pass
