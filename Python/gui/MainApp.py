import tkinter as tk
from tkinter import messagebox
from api_client_ui import ApiClientUI  
from db_handler_ui import DBHandlerUI  
from stats_ui import StatsUI 


class MainApp(tk.Tk):
    
    # Instance of the DBHandlerUI class to interact with the database
    db = DBHandlerUI(
        host="localhost",
        user="root",
        password="root",
        database="empotrados"
    )

    # instance of the ApiClientUI class to interact with the ESP32 API
    api = ApiClientUI(
        base_url="http://192.168.1.111" 
    )

    # Constructor of the MainApp class
    def __init__(self):
        super().__init__()  
        self.title("Consulta de Datos - Estación Meteorológica")
        self.geometry("900x600")
        self.create_widgets()
        self.geometry("900x600")
        self.update_data()  # Call to the function to update data from the database
    

    def create_widgets(self):
     # Main container frame
     main_frame = tk.Frame(self)
     main_frame.pack(fill="x", anchor="n", pady=10)

     # Configuration of the grid: 2 columns, 1 row
     main_frame.columnconfigure(0, weight=1)  # Menor peso: frame de sensores
     main_frame.columnconfigure(1, weight=2)  # Mayor peso: frame de formulario

     # Frame for the sensors and actuators status
     sensors_frame = tk.LabelFrame(main_frame, text="Estado de Sensores y Actuadores", padx=10, pady=10)
     sensors_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

     self.labels_status = {
         "temperature": tk.Label(sensors_frame, text="Temperatura: ---"),
         "humidity": tk.Label(sensors_frame, text="Humedad: ---"),
         "light": tk.Label(sensors_frame, text="Luz: ---"),
         "relay01": tk.Label(sensors_frame, text="Relevador 01: ---"),
         "relay02": tk.Label(sensors_frame, text="Relevador 02: ---"),
     }
     for lbl in self.labels_status.values():
         lbl.pack(anchor="w", pady=2)

     # Frame for the configuration parameters
     parameters_frame = tk.LabelFrame(main_frame, text="Parámetros de Configuración", padx=10, pady=10)
     parameters_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

     # frame for the entry parameters
     self.parameter_entries = {}
     for param in ["temperatura_minima", "temperatura_maxima", "humedad_minima", "humedad_maxima", "luz_minima", "luz_maxima"]:
        frame = tk.Frame(parameters_frame)
        frame.pack(fill="x", pady=2)
        tk.Label(frame, text=f"{param}:").pack(side="left")
        entry = tk.Entry(frame, width=10)
        entry.pack(side="left")
        self.parameter_entries[param] = entry

     # Auxiliary frame to center the button
     button_to_sent_frame = tk.Frame(parameters_frame)
     button_to_sent_frame.pack(fill="x", pady=5)

     send_button = tk.Button(button_to_sent_frame, text="Enviar Parámetros", command=self.send_parameters)
     send_button.pack(anchor="center")

     # Frame de acciones
     frame_button = tk.LabelFrame(main_frame, text="Acciones", padx=10, pady=10)
     frame_button.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

     # Botón de estadísticas
     look_stats_button = tk.Button(frame_button, text="Ver estadísticas", command=self.look_stats)
     look_stats_button.pack(pady=5)


    # Definition of the function to update the data from the API
    def update_data(self):
        data = self.db.getLastRegister()

        if data is not None:
            self.labels_status["temperature"].config(text=f"Temperatura: {data.get('temperature', '---')} °C")
            self.labels_status["humidity"].config(text=f"Humedad: {data.get('humidity', '---')} %")
            self.labels_status["light"].config(text=f"Luz: {data.get('light', '---')}")

            # Manejo uniforme del estado de relevadores
            relay01_status = "Encendido" if data.get('relay01') == 1 else "Apagado"
            relay02_status = "Encendido" if data.get('relay02') == 1 else "Apagado"

            self.labels_status["relay01"].config(text=f"Relevador 01: {relay01_status}")
            self.labels_status["relay02"].config(text=f"Relevador 02: {relay02_status}")
        else:
            print("No se pudo obtener el último registro.")

        self.after(5000, self.update_data)

        

    # Definition of the function to send parameters to the API
    def send_parameters(self):
        parameters = {}
        for key, entry in self.parameter_entries.items():
            value = entry.get()
            if value:
                parameters[key] = value
        
        # validation to check if the parameters are numueric valid entries
        for key, value in parameters.items():
            try:
                parameters[key] = float(value)
            except ValueError:
                messagebox.showerror("Error", f"El valor de {key} no es válido.")
                return

        self.api.establishParameters(parameters)
        # Show a message box to confirm that the parameters were sent
        messagebox.showinfo("Éxito", "Parámetros enviados correctamente.")


    # Definition of the function to show the graphs in a separate window
    def look_stats(self):
        StatsUI(self)  # It opesns like a child window of the main app


# Main function to run the application
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()


