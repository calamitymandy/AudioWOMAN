import tkinter as tk

root = tk.Tk()
root.geometry("400x400")

canvas = tk.Canvas(root, bg="lightgray")
canvas.pack(fill="both", expand=True)

def on_mouse_wheel(event):
    print(f"Delta: {event.delta}")  # Print scroll values for debugging

canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # Windows/macOS

root.mainloop()
