from db_handler_ui import DBHandlerUI 

class Prueba:
    
    def __init__(self):
        self.db = DBHandlerUI(
            host="localhost",
            user="root",
            password="Saymyname15",
            database="empotrados"
    )
        
    def test(self):
        registro = self.db.getRegistersByDate("2025-04-01 00:00:00", "2025-4-30 23:59:59")
        print(registro)

if __name__ == "__main__":
    prueba = Prueba()
    prueba.test()

