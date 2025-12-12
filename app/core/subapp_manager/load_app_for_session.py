# session_manager_with_fallback.py
import sys
import os
import importlib.util
import subprocess
import time
from pathlib import Path
from typing import Optional


# ---------- Utility: dynamic loader for Qt widgets ----------
def load_app_widget(path: Path):
    """
    Try to import a Python file and return an instance of a Qt widget/class.
    Looks for names: AppMain, MainWidget, MainWindow, Window.
    Raises ValueError if not found or not a QWidget/QMainWindow subclass.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")

    # Create unique module name based on absolute path (to avoid collisions)
    mod_name = f"dynamic_app_{abs(hash(str(path)))}"

    spec = importlib.util.spec_from_file_location(mod_name, str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create spec for {path}")

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        # Importing ran code and failed (or main guarded code used __name__ check)
        # Re-raise so caller knows embedding failed.
        raise ImportError(f"Import failed for {path!s}: {e}") from e

    # Candidate attribute names (common conventions)
    candidates = ["AppMain", "MainWidget", "MainWindow", "Window"]

    for name in candidates:
        cls_or_obj = getattr(module, name, None)
        if cls_or_obj is None:
            continue

        # If it's a class, instantiate it
        try:
            if isinstance(cls_or_obj, type):
                instance = cls_or_obj()
            else:
                # could be a pre-created widget instance
                instance = cls_or_obj
        except Exception as e:
            raise RuntimeError(f"Failed to instantiate {name}: {e}") from e

        # Validate it's a QWidget/QMainWindow
        try:
            from PySide6.QtWidgets import QWidget, QMainWindow
            if isinstance(instance, (QWidget, QMainWindow)):
                return instance
            else:
                raise TypeError(f"{name} is not a QWidget/QMainWindow instance")
        except ImportError:
            raise RuntimeError("PySide6 not available in environment")

    # Nothing found
    raise ValueError("No suitable Qt widget/class found in module (AppMain/MainWidget/MainWindow/Window)")
