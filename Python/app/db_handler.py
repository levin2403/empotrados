# db_handler.py

import mysql.connector
from datetime import datetime

class DBHandler:

    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self._create_table_if_not_exist()

    def _create_table_if_not_exist(self):
        """
        Crea la tabla sensores si no existe.
        """
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date_time DATETIME NOT NULL,
                temperature FLOAT,
                humidity FLOAT,
                light FLOAT,
                relay01 TINYINT(1),
                relay02 TINYINT(1)
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()

    def insert_lecture(self, datos):
        """
        Inserta una nueva lectura en la base de datos.
        `datos` debe ser un diccionario con claves: temperatura, humedad, luz, relevador01, relevador02
        """
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO sensors (date_time, temperature, humidity, light, relay01, relay02)
            VALUES (%s, %s, %s, %s, %s, %s)''', (
            datetime.now(),
            datos.get('temperature'),
            datos.get('humidity'),
            datos.get('light'),
            int(datos.get('relay01', 0)),
            int(datos.get('relay02', 0)) 
        ))
        conn.commit()
        cursor.close()
        conn.close()
        print("Data inserted successfully")
