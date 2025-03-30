import sys
import os

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import load_social_network_from_txt
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from classes.social_network import SocialNetwork
from algorithms.wrappers import modciFB, modciPD, modciV

class SocialNetworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Análisis de Red Social")

        # Botón para cargar archivo
        self.btn_cargar = tk.Button(root, text="Cargar Archivo TXT", command=self.cargar_archivo)
        self.btn_cargar.pack()

        # Dropdown para seleccionar el algoritmo
        self.algoritmo_var = tk.StringVar(value="Seleccionar Algoritmo")
        self.dropdown_algoritmo = tk.OptionMenu(root, self.algoritmo_var, "Voraz", "Fuerza Bruta", "Programación Dinámica")
        self.dropdown_algoritmo.pack()

        # Botón para ejecutar el algoritmo
        self.btn_ejecutar = tk.Button(root, text="Ejecutar Algoritmo", command=self.ejecutar_algoritmo)
        self.btn_ejecutar.pack()

        # Área para gráficos
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

        # Etiquetas para esfuerzo y conflicto
        self.lbl_esfuerzo = tk.Label(root, text="Esfuerzo: ")
        self.lbl_esfuerzo.pack()
        self.lbl_conflicto = tk.Label(root, text="Conflicto: ")
        self.lbl_conflicto.pack()

        self.social_network = None
        self.file_path = None

    def cargar_archivo(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Archivos TXT", "*.txt")])
        if self.file_path:
            try:
                self.social_network = load_social_network_from_txt(self.file_path)
                if not isinstance(self.social_network, SocialNetwork):
                    raise ValueError("El archivo no generó una red social válida.")
                messagebox.showinfo("Éxito", "Archivo cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")

    def ejecutar_algoritmo(self):
        if not self.social_network:
            messagebox.showwarning("Advertencia", "Primero carga un archivo TXT.")
            return

        algoritmo = self.algoritmo_var.get()
        if algoritmo == "Seleccionar Algoritmo":
            messagebox.showwarning("Advertencia", "Selecciona un algoritmo válido.")
            return

        try:
            print(f"Ejecutando algoritmo: {algoritmo}")

            if algoritmo == "Voraz":
                resultado = modciV(self.social_network)
            elif algoritmo == "Fuerza Bruta":
                resultado = modciFB(self.social_network)
            elif algoritmo == "Programación Dinámica":
                resultado = modciPD(self.social_network)

            if not isinstance(resultado, tuple) or len(resultado) != 3:
                raise ValueError(f"El resultado del algoritmo no es válido: {resultado}")

            estrategia, esfuerzo, conflicto = resultado

            if not isinstance(esfuerzo, (int, float)) or not isinstance(conflicto, (int, float)):
                raise ValueError("Los valores de esfuerzo y conflicto no son numéricos.")

            self.mostrar_resultado(estrategia, esfuerzo, conflicto)
        except Exception as e:
            print(f"Error al ejecutar el algoritmo: {e}")
            messagebox.showerror("Error", f"Ocurrió un error al ejecutar el algoritmo: {e}")

    def mostrar_resultado(self, estrategia, esfuerzo, conflicto):
        self.ax.clear()
        etiquetas = [f"Grupo {i+1}" for i in range(len(estrategia))]
        valores = list(estrategia)

        self.ax.bar(etiquetas, valores)
        self.ax.set_title("Resultados del Algoritmo")
        self.canvas.draw()

        self.lbl_esfuerzo.config(text=f"Esfuerzo: {esfuerzo}")
        self.lbl_conflicto.config(text=f"Conflicto: {conflicto}")

        # Guardar resultados en un archivo
        try:
            with open("resultado.txt", "w") as f:
                f.write("Estrategia:\n")
                f.write(" ".join(map(str, estrategia)) + "\n")
                f.write(f"Esfuerzo: {esfuerzo}\n")
                f.write(f"Conflicto: {conflicto}\n")
            messagebox.showinfo("Éxito", "Resultados guardados en 'resultado.txt'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SocialNetworkApp(root)
    root.mainloop()