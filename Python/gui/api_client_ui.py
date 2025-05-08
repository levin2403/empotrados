
import requests


class ApiClientUI:
    """
    Class to interact with the ESP32 API via HTTP.
    Allows querying the status of sensors and actuators, as well as setting configuration parameters.
    """
    
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
    
    def getData(self):
        """
        Consults the current data of the sensors, actuators and system parameters.
        Returns a dictionary with the data or None if an error occurs.
        """
        response = {
                "temperature": {
                    "actual_value": 25,
                    "minimum": 0,
                    "maximum": 50
                },
                "humidity": {
                    "actual_value": 60,
                    "minimum": 20,
                    "maximum": 90
                },
                "light": {
                    "actual_value": 300,
                    "minimum": 20,
                    "maximum": 1000
                },
                "relays": {
                    "relay01": 0,
                    "relay02": 1
                }
            }
        print("The data has been received from the API")
        return response
        #try:
        #    response = requests.get(f"{self.base_url}/api/estado", timeout=5)
        #    response.raise_for_status()
        #    print(f"Estado consultado: {response.json()}")
        #    return response.json()
        #except (requests.RequestException, ValueError) as e:
        #    print(f"Error al consultar API: {e}")
        #    return None

    def establishParameters(self, parameters):
        """
        Sends the configuration parameters or new states to the ESP32.
        `parametros` must be a dictionary containing the keys and values you want to update.
        """
        newParameters = {
                "temperature": {
                    "minimum": parameters.get("temperatura_minima", 0),
                    "maximum": parameters.get("temperatura_maxima", 0)
                },
                "humidity": {
                    "minimum": parameters.get("humedad_minima", 0),
                    "maximum": parameters.get("humedad_maxima", 0)
                },
                "light": {
                    "minimum": parameters.get("luz_minima", 0),
                    "maximum": parameters.get("luz_maxima", 0)
                }
            }
        
        print("The parameters have been sent to the API")
        print(newParameters)
    
        #try:
        #    response = requests.post(f"{self.base_url}/api/parametros", json=newParameters, timeout=5)
        #    response.raise_for_status()
        #    print(f"Parameters succesfully updated: {response.json()}")
        #    return response.json()
        #except (requests.RequestException, ValueError) as e:
        #    print(f"Error al establecer parámetros: {e}")
        #    return None