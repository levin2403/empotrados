# api_client.py

import time
from db_handler import DBHandler
from api_client import ApiClient 

def main():  
    """
    Main function to run the application.
    It initializes the database handler and API client, and enters a loop to fetch data from the API and store it in the database.
    It fetches data every 5 seconds and handles any exceptions that may occur during the process.
    """
    db = DBHandler(
        host="localhost",
        user="root",
        password="root",
        database="empotrados"
    )
    
    api = ApiClient(
        base_url="http://192.168.1.111"  # que no se te olvide cambiarlo kevin
    )

    seconds_interval = 10  # tiempo entre consultas
    
    while True:
        try:
            data = api.get_lecture()  # regresa un diccionario con los datos de los sensores
            
            sensed_temperature = data.get("temperature", {}).get("actual_value", None)
            sensed_humidity = data.get("humidity", {}).get("actual_value", None)
            sensed_light = data.get("light", {}).get("actual_value", None)
            sensed_relay01 = data.get("relays", {}).get("relay01", None)
            sensed_relay02 = data.get("relays", {}).get("relay02", None)
            
            if sensed_temperature is not None and sensed_humidity is not None and sensed_light is not None:
                db.insert_lecture({
                    "temperature": sensed_temperature,
                    "humidity": sensed_humidity,
                    "light": sensed_light,
                    "relay01": sensed_relay01, 
                    "relay02": sensed_relay02
                })
            else:
                print("Uncomplete recived data: ", data)
        except Exception as e:
            print("There was an error at the moment of obtain or save the data: ", e)

        time.sleep(seconds_interval)

if __name__ == "__main__":
    main()
