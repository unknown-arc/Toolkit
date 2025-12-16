# capture.py
import pyautogui
import tkinter as tk
from tkinter import messagebox


def full_screenshot():
    return pyautogui.screenshot()


def rectangular_screenshot(x, y, width, height):
    return pyautogui.screenshot(region=(x, y, width, height))


class CustomCapture:
    def __init__(self):
        self.start_x = 0
        self.start_y = 0
        self.end_x = 0
        self.end_y = 0
        self.rect = None 

    def capture(self):
        messagebox.showinfo("Instruction", "Drag mouse to select area")

        overlay = tk.Toplevel()
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-alpha", 0.3)

        canvas = tk.Canvas(overlay, cursor="cross")
        canvas.pack(fill=tk.BOTH, expand=True)

        def on_press(event):
            self.start_x = event.x
            self.start_y = event.y

        def on_drag(event):
            if self.rect:
                canvas.delete(self.rect)
            self.rect = canvas.create_rectangle(
                self.start_x,
                self.start_y,
                event.x,
                event.y,
                outline="red",
                width=2
            )

        def on_release(event):
            self.end_x = event.x
            self.end_y = event.y
            overlay.destroy()

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

        overlay.mainloop()

        x = min(self.start_x, self.end_x)
        y = min(self.start_y, self.end_y)
        w = abs(self.end_x - self.start_x)
        h = abs(self.end_y - self.start_y)

        return pyautogui.screenshot(region=(x, y, w, h))
