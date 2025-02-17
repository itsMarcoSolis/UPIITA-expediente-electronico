import os
import re
import ctypes
import win32gui
import win32com.client
import time
from threading import Thread
    
class WindowMgr:
    """Encapsulates calls to the winapi for window management
    """

    def __init__(self):
        self._handle = None

    @property
    def handle(self):
        return self._handle

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)
        return self
    
def set_icon(icon_path: str, hWnd=None):
    # from https://github.com/zauberzeug/nicegui/issues/620#issuecomment-1483818006
    assert os.path.exists(icon_path), f"Invalid icon file path supplied: {icon_path}"

    # Load the necessary Windows API functions using ctypes
    user32 = ctypes.windll.user32

    # Get the handle of the current process and the current window
    # Ideally replace this to directly reference the created webview window
    if hWnd is None:
        hWnd = user32.GetForegroundWindow()

    # Constants for Win32 API calls
    ICON_SMALL = 0
    ICON_BIG = 1
    WM_SETICON = 0x0080

    # Load the icon file
    hIcon = user32.LoadImageW(None, icon_path, 1, 0, 0, 0x00000010)

    # Set the window icon using WM_SETICON message
    ctypes.windll.user32.SendMessageW(hWnd, WM_SETICON, ICON_SMALL, hIcon)
    ctypes.windll.user32.SendMessageW(hWnd, WM_SETICON, ICON_BIG, hIcon)



def set_window_icon(icon_path: str, window_name: str, tries: int = 10):
    def _set_window_icon(icon_path: str, window_name: str, tries: int):
        for _ in range(tries):
            handle = WindowMgr().find_window_wildcard(window_name).handle
            if handle is not None:
                set_icon(icon_path=icon_path, hWnd=handle)
                break
            time.sleep(1)

    Thread(
        target=_set_window_icon, args=[icon_path, window_name, tries], daemon=True
    ).start()