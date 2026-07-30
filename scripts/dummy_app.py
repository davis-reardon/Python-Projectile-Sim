import tkinter as tk
from tkinter import filedialog
import time


class DummyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dummy Legacy App")
        self.root.geometry("400x200")

        self.selected_file = None

        self.select_btn = tk.Button(root, text="Select File",
                                      command=self.select_file, width=20)
        self.select_btn.pack(pady=10)

        self.file_label = tk.Label(root, text="No file selected")
        self.file_label.pack(pady=5)

        self.run_btn = tk.Button(root, text="Run", command=self.run_process,
                                   width=20, state=tk.DISABLED)
        self.run_btn.pack(pady=10)

        self.status_label = tk.Label(root, text="Status: Idle")
        self.status_label.pack(pady=10)

    def select_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.selected_file = filepath
            self.file_label.config(text=f"Selected: {filepath}")
            self.run_btn.config(state=tk.NORMAL)

    def run_process(self):
        self.status_label.config(text="Status: Running...")
        self.root.update()
        time.sleep(2)  # simulate processing delay
        self.status_label.config(text="Status: Complete - output.csv exported")


if __name__ == "__main__":
    root = tk.Tk()
    app = DummyApp(root)
    root.mainloop()