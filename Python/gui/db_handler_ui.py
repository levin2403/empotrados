import mysql.connector

class DBHandlerUI:
    def __init__(self, host, user, password, database):
        self.config = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }

    def getRegistersByDate(self, begin_date, end_date):
        """
        Gets the records of sensors and actuators stored in the database
        between start_date and end_date.
        
        Parameters:
            begin_date (str) Initial date in 'YYYY-MM-DD HH:MM:SS' format.
            end_date (str) Final date in 'YYYY-MM-DD HH:MM:SS' format. 
        
        Returns:
            A list of dictionaries with the data or an empty list if there are no records.
        """
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            
            query = """
            SELECT * 
            FROM sensors
            WHERE date_time BETWEEN %s AND %s
            ORDER BY date_time ASC;
            """
            cursor.execute(query, (begin_date, end_date))
            resultado = cursor.fetchall()
            
            return resultado
        
        except mysql.connector.Error as err:
            print(f"Error al consultar la base de datos: {err}")
            return []
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def getLastRegister(self):
        """
        Gets the last record of sensors and actuators stored in the database.
        
        Returns:
            A dictionary with the data or None if there are no records.
        """
        try:
            conn = mysql.connector.connect(**self.config)
            cursor = conn.cursor(dictionary=True)
            
            query = """
            SELECT * 
            FROM sensors
            ORDER BY date_time ASC
            LIMIT 1;
            """
            cursor.execute(query)
            resultado = cursor.fetchone()
            
            print("the last register has been consulted")

            return resultado
        
        except mysql.connector.Error as err:
            print(f"There was a mistake consulting the las register: {err}")
            return None
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()