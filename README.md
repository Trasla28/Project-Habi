# Project-Habi
Pruebas tecnicas
1) Objetivo del repositorio

-Implementar dos ejercicios:

-API de Inmuebles (FastAPI, sin ORM) con filtros, paginación y la funcionalidad de “Me gusta”.

-Algoritmo de bloques: dado un arreglo de enteros donde 0 separa bloques, ordenar cada bloque y representar bloques vacíos con X.

2) Tecnologías a utilizar

-Python 3.11

-FastAPI — framework web asíncrono y rápido.

-Uvicorn — ASGI server para ejecutar la API.

-mysql-connector-python — cliente oficial de MySQL (sin ORM).

-python-dotenv — manejo de variables de entorno desde .env.

-Pytest / pytest-mock / httpx — pruebas unitarias y de endpoints (sin tocar la BD real).


3) Enfoque de desarrollo
  3.1 Arquitectura (capa fina, sin ORM)
  
    app/main.py: define la API (rutas, validaciones de entrada, respuestas).
    
    app/queries.py: capa de acceso a datos; construye SQL y mapea resultados.
    
    app/db.py: connection pooling con MySQLConnectionPool.
    
    app/settings.py: carga robusta de .env (rutas absolutas), constantes y mapeos.
    
    app/ejericicio2.py: lógica del ejercicio 2 (ordenar bloques separados por 0).

  3.2 Decisiones clave
  
  Estados: se aceptan solo pre_venta, en_venta, vendido (mapa STATUS_MAP → status_id).
  
  Último estado por inmueble: subconsulta con MAX(update_date) en status_history.
  
  Paginación y orden: query params page, page_size, order_by, order_dir con lista blanca de campos.
  
  .env: credenciales y config fuera del código; ejemplo en .env.example.
  
  “Me gusta”: tabla likes con UNIQUE(user_id, property_id) (idempotente) y FK a property.

4) Estructura del proyecto
  project/
    app/
      main.py         # Rutas FastAPI
      db.py           # Pool de conexiones MySQL
      queries.py      # SQL crudo (inmuebles + likes)
      settings.py     # Carga .env y constantes
    Ejericio2/
      ejercicio2.py          # Unit tests Ejercicio 2
    requirements.txt
    .env
    README.md
5) Configuración del entorno
  Instralar todas las dependecias, clases y librerias
  
  crar .env
    MYSQL_HOST=13.58.82.14
    MYSQL_PORT=3309
    MYSQL_USER=pruebas
    MYSQL_PASSWORD=CAMBIA_ESTA_CLAVE
    MYSQL_DB=habi_db
    PAGE_SIZE_DEFAULT=20

6) Ejecutar la API localmente
  uvicorn app.main:app --reload --port 8000
  Swagger: http://127.0.0.1:8000/docs

