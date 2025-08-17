#Se realzian las importaciones necesarias
from mysql.connector.pooling import MySQLConnectionPool
from app.settings import MYSQL_CONFIG

#Se crea el pool de conexxiones
#MYSQL_CONFIG se pasa con ** para incluir host, user, password, etc)
_pool = MySQLConnectionPool(pool_name="habi_pool", pool_size=5, **MYSQL_CONFIG)

#Se define get_conn para la conexion del pool
def get_conn():
    return _pool.get_connection()
