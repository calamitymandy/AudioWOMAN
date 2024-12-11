import tkinter as tk

def procesar_texto():
    entrada = entrada_texto.get()
    salida.set(entrada.upper())  # Convierte el texto a mayúsculas

ventana = tk.Tk()
ventana.title("Manejador de Texto")

tk.Label(ventana, text="Texto de entrada:").pack()
entrada_texto = tk.Entry(ventana)
entrada_texto.pack()

tk.Button(ventana, text="Procesar", command=procesar_texto).pack()

salida = tk.StringVar()
tk.Label(ventana, textvariable=salida).pack()

ventana.mainloop()
