# gui.py
import tkinter as tk
from tkinter import messagebox, filedialog
from capture import full_screenshot, rectangular_screenshot, CustomCapture
from ocr import preprocess_image, extract_text, save_image
import time


class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Capture & OCR Toolkit")
        self.root.geometry("550x450")

        tk.Label(root, text="Screen Capture & OCR Tool",
                 font=("Arial", 16)).pack(pady=10)

        tk.Button(root, text="Full Screenshot",
                  command=self.full_capture).pack(pady=5)

        tk.Button(root, text="Rectangular Screenshot",
                  command=self.rect_capture).pack(pady=5)

        tk.Button(root, text="Custom Screenshot",
                  command=self.custom_capture).pack(pady=5)

        self.text_box = tk.Text(root, height=12, width=65)
        self.text_box.pack(pady=10)

        tk.Button(root, text="Save Extracted Text",
                  command=self.save_text).pack(pady=5)

        self.extracted_text = ""

    def process_image(self, image):
        path = save_image(image)
        processed = preprocess_image(image)
        self.extracted_text = extract_text(processed)

        if self.text_box.winfo_exists():
            self.text_box.delete(1.0, tk.END)
            self.text_box.insert(tk.END, self.extracted_text)

        messagebox.showinfo("Saved", f"Screenshot saved at:\n{path}")

    def full_capture(self):
        self.root.withdraw()
        time.sleep(0.3)
        img = full_screenshot()
        self.root.deiconify()
        self.process_image(img)

    def rect_capture(self):
        self.root.withdraw()
        time.sleep(0.3)

        # ✅ FIXED region capture (center of screen)
        screen_w, screen_h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x = int(screen_w * 0.25)
        y = int(screen_h * 0.25)
        w = int(screen_w * 0.5)
        h = int(screen_h * 0.5)

        img = rectangular_screenshot(x, y, w, h)
        self.root.deiconify()
        self.process_image(img)

    def custom_capture(self):
        self.root.withdraw()
        time.sleep(0.3)

        capture_tool = CustomCapture()
        img = capture_tool.capture()

        self.root.deiconify()
        self.process_image(img)

    def save_text(self):
        if not self.extracted_text.strip():
            messagebox.showwarning("Warning", "No text to save")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )

        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.extracted_text)
            messagebox.showinfo("Success", "Text saved successfully")
