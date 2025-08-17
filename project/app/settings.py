#Se realzian las importaciones necesarias
import os
from dotenv import load_dotenv


load_dotenv()
#Se agrega los datos para la conexion
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", ""),
}

PAGE_SIZE_DEFAULT = int(os.getenv("PAGE_SIZE_DEFAULT", "20"))


# Se ajustan los IDs reales difieren.
STATUS_MAP = {
    "pre_venta": 1,
    "en_venta": 2,
    "vendido": 3,
}
ALLOWED_STATUS = set(STATUS_MAP.keys())
