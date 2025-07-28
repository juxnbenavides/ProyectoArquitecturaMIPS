import tkinter as tk
from tkinter import filedialog, messagebox

class MIPSSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador MIPS 32 bits")

        self.instrucciones = []
        self.labels_circulos = []

        # Canvas para la arquitectura
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

        # Panel derecho para botones e instrucciones
        frame_derecho = tk.Frame(self.root)
        frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

        btn_cargar = tk.Button(frame_derecho, text="Seleccionar archivo", command=self.cargar_archivo)
        btn_cargar.pack(pady=5)

        self.frame_instrucciones = tk.Frame(frame_derecho)
        self.frame_instrucciones.pack(fill=tk.BOTH, expand=True)

        btn_ejecutar = tk.Button(frame_derecho, text="Ejecutar", command=self.ejecutar)
        btn_ejecutar.pack(pady=5)

        self.dibujar_arquitectura()

    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if not archivo:
            return

        with open(archivo, "r") as f:
            lineas = [linea.strip() for linea in f.readlines() if linea.strip()]

        if len(lineas) > 10:
            messagebox.showerror("Error", "Máximo 10 líneas permitidas.")
            return

        self.instrucciones = lineas
        self.mostrar_instrucciones()

    def mostrar_instrucciones(self):
        for widget in self.frame_instrucciones.winfo_children():
            widget.destroy()

        self.labels_circulos = []

        for instr in self.instrucciones:
            frame_linea = tk.Frame(self.frame_instrucciones)
            frame_linea.pack(anchor="w")
            lbl_circulo = tk.Label(frame_linea, text="●", fg="gray")
            lbl_circulo.pack(side=tk.LEFT)
            lbl_texto = tk.Label(frame_linea, text=instr)
            lbl_texto.pack(side=tk.LEFT)
            self.labels_circulos.append(lbl_circulo)

    def ejecutar(self):
        if not self.instrucciones:
            messagebox.showwarning("Atención", "Primero carga un archivo de instrucciones.")
            return

        def paso_a_paso(i):
            if i > 0:
                self.labels_circulos[i-1].config(fg="gray")
            if i < len(self.instrucciones):
                self.labels_circulos[i].config(fg="green")
                self.resaltar_bloque(i)
                self.root.after(1000, paso_a_paso, i+1)

        paso_a_paso(0)

    def dibujar_arquitectura(self):
        self.bloques = [
            ("Memoria Principal", 50, 50),
            ("Registros", 50, 150),
            ("ALU", 300, 100),
            ("Unidad de Control", 200, 250)
        ]
        self.rects = []
        for nombre, x, y in self.bloques:
            rect = self.canvas.create_rectangle(x, y, x+150, y+60, fill="lightgray")
            self.canvas.create_text(x+75, y+30, text=nombre)
            self.rects.append(rect)
    def resaltar_bloque(self, indice):
        # Alterna bloques según índice
        for i, rect in enumerate(self.rects):
            self.canvas.itemconfig(rect, fill="lightgray")
        bloque_index = indice % len(self.rects)
        self.canvas.itemconfig(self.rects[bloque_index], fill="lightgreen")
if __name__ == "__main__":
    root = tk.Tk()
    app = MIPSSimulator(root)
    root.mainloop()
