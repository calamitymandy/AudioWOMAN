import tkinter as tk
from tkinter import messagebox

def generate_paths():
    """Genera las rutas concatenadas a partir del texto pegado y la extensión."""
    try:
        column1_text = column1_textbox.get("1.0", tk.END).strip().splitlines()
        column2_text = column2_textbox.get("1.0", tk.END).strip().splitlines()
        extension = extension_entry.get().strip()

        if not column1_text or not column2_text:
            messagebox.showwarning("Warning", "Both colums have to have data.")
            return
        if len(column1_text) != len(column2_text):
            messagebox.showwarning("Warning", "Both colums have to have same number of rows.")
            return
        if not extension:
            messagebox.showwarning("Warning", "Introduce an extension.")
            return

        # Generar las rutas concatenadas
        concatenated_paths = [
            f"{col1}{col2}{extension}"
            for col1, col2 in zip(column1_text, column2_text)
        ]

        # Mostrar el resultado en el cuadro de texto
        result_textbox.delete("1.0", tk.END)
        result_textbox.insert(tk.END, "\n".join(concatenated_paths))
    except Exception as e:
        messagebox.showerror("Warning", f"Not possible to create path: {e}")

# Configuración de la ventana principal
root = tk.Tk()
root.title("BATMAN like")
root.geometry("800x600")

# Entrada para la primera columna
column1_label = tk.Label(root, text="Where it is:")
column1_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
column1_textbox = tk.Text(root, height=10, width=40)
column1_textbox.grid(row=1, column=0, padx=10, pady=5)

# Entrada para la segunda columna
column2_label = tk.Label(root, text="Who is it:")
column2_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
column2_textbox = tk.Text(root, height=10, width=40)
column2_textbox.grid(row=1, column=1, padx=10, pady=5)

# Entrada para la extensión
extension_label = tk.Label(root, text="Extension (e.g., .wav):")
extension_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
extension_entry = tk.Entry(root)
extension_entry.grid(row=2, column=1, padx=10, pady=5)

# Botón para generar rutas
generate_button = tk.Button(root, text="Concatenate", command=generate_paths)
generate_button.grid(row=3, column=0, columnspan=2, pady=10)

# Área de resultados
result_label = tk.Label(root, text="Result:")
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w")
result_textbox = tk.Text(root, height=10, width=80)
result_textbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
