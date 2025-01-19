import sqlite3
from pathlib import Path
import threading


_lock = threading.Lock()

def inicializar_base_datos(db_path: str="./data/sqlite/contador.db"):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contador(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                valor INTEGER NOT NULL
            )
        """)
        
        cursor.execute("SELECT COUNT(*) FROM contador WHERE id = 1")
        existe_registro = cursor.fetchone()[0]
        
        if not existe_registro:
            cursor.execute("INSERT OR IGNORE INTO contador (id, valor) VALUES (1, 0)")
        
        conn.commit()
    
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")
        raise e
    
    finally:
        conn.close()
    

def obtener_siguiente_id(db_path: str="./data/sqlite/contador.db") -> str:
    with _lock:
        inicializar_base_datos(db_path)
    
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            
            cursor.execute("""
                UPDATE contador
                SET valor = valor + 1
                WHERE id = 1
            """)
            conn.commit()
            
            cursor.execute("""
                SELECT valor FROM contador WHERE id = 1
            """)
            nuevo_id = cursor.fetchone()[0]
        
        except Exception as e:
            print(f"Error al obtener el siguiente ID: {e}")
            raise e
        
        finally:
            conn.close()
            
            
        return str(nuevo_id)