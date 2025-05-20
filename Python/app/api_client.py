
import requests

class ApiClient:

    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
    
    def get_lecture(self):
        """
        Consulta los datos actuales de los sensores, actuadores y parámetros del sistema.
        Retorna un diccionario con los datos o None si ocurre un error.
        """
        try:
            response = requests.get(f"{self.base_url}/api/estado", timeout=5)
            response.raise_for_status()
            print(f"Consulted state: {response.json()}")
            return response.json()
            

        except (requests.RequestException, ValueError) as e:
            print(f"Error when consulting the API: {e}")
            return None

