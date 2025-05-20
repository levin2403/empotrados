
import requests


class ApiClientUI:
    """
    Class to interact with the ESP32 API via HTTP.
    Allows querying the status of sensors and actuators, as well as setting configuration parameters.
    """
    
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')


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
    
        try:
            response = requests.post(f"{self.base_url}/api/parametros", json=newParameters, timeout=5)
            response.raise_for_status()
            print(f"Parameters succesfully updated: {response.json()}")
            return response.json()
        except (requests.RequestException, ValueError) as e:
            print(f"Error al establecer parámetros: {e}")
            return None