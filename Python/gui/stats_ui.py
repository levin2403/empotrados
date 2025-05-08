# stats_ui.py
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from db_handler_ui import DBHandlerUI
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tkcalendar import DateEntry
from tkinter import messagebox

class StatsUI(tk.Toplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sistema de Monitoreo - Estación Meteorológica (Mock)")
        self.geometry("900x600")
        self.crear_widgets()

    def crear_widgets(self):
        self.mostrar_graficas()

    db = DBHandlerUI(
        host="localhost",
        user="root",
        password="Saymyname15",
        database="empotrados"
    )

    def mostrar_graficas(self):

        # frame para los parametros de busqueda
        entry_frame = tk.LabelFrame(self, text="Parametros de busqueda", padx=10, pady=10)
        entry_frame.pack(fill="x", anchor="n", pady=10)

        # campo de entrada para la fecha de inicio
        fecha_inicio_frame = tk.Frame(entry_frame)
        fecha_inicio_frame.pack(fill="x", pady=5)
        tk.Label(fecha_inicio_frame, text="Fecha Inicio:").pack(side="left", padx=5)
        self.fecha_inicio = DateEntry(fecha_inicio_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.fecha_inicio.pack(side="left", padx=5)

        # campo de entrada para la fecha de fin
        fecha_fin_frame = tk.Frame(entry_frame)
        fecha_fin_frame.pack(fill="x", pady=5)
        tk.Label(fecha_fin_frame, text="Fecha Fin:").pack(side="left", padx=5)
        self.fecha_fin = DateEntry(fecha_fin_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.fecha_fin.pack(side="left", padx=5)

        # Botón de envío
        search_button = tk.Button(entry_frame, text="Buscar", command=self.updateGraphs)
        search_button.pack(pady=5)

        graficas_frame = tk.Frame(self)
        graficas_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fig, (self.ax_temp, self.ax_hum, self.ax_luz) = plt.subplots(3, 1, figsize=(9, 6))
        fig.tight_layout(pad=2.0)

        # Títulos
        self.ax_temp.set_title("Temperatura")
        self.ax_hum.set_title("Humedad")
        self.ax_luz.set_title("Luz")

        # Datos de prueba
        x_data = list(range(10))
        y_data = [0]*10
        self.ax_temp.plot(x_data, y_data, label="Temp (°C)")
        self.ax_hum.plot(x_data, y_data, label="Humedad (%)")   
        self.ax_luz.plot(x_data, y_data, label="Luz (lx)")

        self.canvas = FigureCanvasTkAgg(fig, master=graficas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)


    def updateGraphs(self):
        # Get the date range from the DateEntry widgets
        begin_date = self.fecha_inicio.get() + " 00:00:00"
        end_date = self.fecha_fin.get() + " 23:59:59"

        # Fetch data from the database
        data = self.db.getRegistersByDate(begin_date, end_date)

        if data:
            # Extract data for each parameter
            x_data = [data[i]['date_time'] for i in range(len(data))]
            temp_data = [data[i]['temperature'] for i in range(len(data))]
            hum_data = [data[i]['humidity'] for i in range(len(data))]
            luz_data = [data[i]['light'] for i in range(len(data))]

            # Clear the existing plots
            self.ax_temp.clear()
            self.ax_hum.clear()
            self.ax_luz.clear()

            # Update the plots with new data
            self.ax_temp.plot(x_data, temp_data, label="Temp (°C)", color="red")
            self.ax_hum.plot(x_data, hum_data, label="Humedad (%)", color="blue")
            self.ax_luz.plot(x_data, luz_data, label="Luz (lx)", color="green")

            # Set titles and labels
            self.ax_temp.set_title("Temperatura")
            self.ax_hum.set_title("Humedad")
            self.ax_luz.set_title("Luz")
            self.ax_temp.set_ylabel("°C")
            self.ax_hum.set_ylabel("%")
            self.ax_luz.set_ylabel("lx")

            # Remove x-axis labels
            self.ax_temp.set_xticklabels([])
            self.ax_hum.set_xticklabels([])
            self.ax_luz.set_xticklabels([])

            # Redraw the canvas
            self.canvas.draw()
        else:
            messagebox.showinfo("Sin datos", "No se encontraron datos para el rango de fechas seleccionado.")

        

        
