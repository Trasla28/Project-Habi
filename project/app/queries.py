#Se realizan las importaciones necesarias
from typing import Any, Dict, List, Tuple, Optional
from app.db import get_conn
from app.settings import STATUS_MAP, ALLOWED_STATUS

def fetch_properties(
    ciudad: Optional[str],
    estado: Optional[str],
    anio: Optional[int],
    page: int,
    page_size: int,
    order_by: str = "update_date",
    order_dir: str = "desc",
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Devuelve lista paginada de inmuebles con su último estado,
    filtrando por ciudad, estado (un solo estado) y año (ver nota).
    Nota sobre 'anio':
      - Si existe columna property.year (no la vemos en tu captura), filtra por ella.
      - Si NO existe, como fallback filtra por YEAR(sh.update_date) del último estado.
        (Cámbialo a tu lógica real cuando tengas la columna de construcción).
    """
    #Se valida el estado
    if estado and estado not in ALLOWED_STATUS:
        raise ValueError(f"Estado no permitido. Usa uno de: {', '.join(ALLOWED_STATUS)}")

    # Se valida el ordenamiento de los parametros
    order_by_allowed = {"price", "update_date", "city", "id"}
    if order_by not in order_by_allowed:
        order_by = "update_date"
    order_dir = "desc" if order_dir.lower() == "desc" else "asc"

    #Lista para ir guardando los parametros de la query SQL
    params: List[Any] = []

    #Subconsulta, se obtiene el último estado de cada propiedad
    latest_status_cte = """
        SELECT sh.property_id, sh.status_id, sh.update_date
        FROM status_history sh
        INNER JOIN (
            SELECT property_id, MAX(update_date) AS max_ud
            FROM status_history
            GROUP BY property_id
        ) t ON t.property_id = sh.property_id AND t.max_ud = sh.update_date
    """

    # Query principal que une las propiedades
    base = f"""
        SELECT p.id, p.address, p.city, p.price,
               ls.status_id, ls.update_date
        FROM property p
        INNER JOIN ({latest_status_cte}) ls ON ls.property_id = p.id
        WHERE 1=1
    """

    # Filtros dinamicos segun los parametros
    if ciudad:
        base += " AND p.city = %s"
        params.append(ciudad)

    if estado:
        base += " AND ls.status_id = %s"
        params.append(STATUS_MAP[estado])

    if anio is not None:
        base += " AND YEAR(ls.update_date) = %s"
        params.append(anio)

    #Solo aceptra los estaods esperedaos
    base += " AND ls.status_id IN (%s,%s,%s)"  # pre_venta, en_venta, vendido
    params.extend([STATUS_MAP["pre_venta"], STATUS_MAP["en_venta"], STATUS_MAP["vendido"]])

    # Query para contar el total de registros
    count_sql = f"SELECT COUNT(*) FROM ({base}) AS q"
    # se añade el ordanimiento
    base += f" ORDER BY {order_by} {order_dir} LIMIT %s OFFSET %s"

    # Calcula offset
    page = max(1, page)
    page_size = max(1, page_size)
    offset = (page - 1) * page_size
    params_with_paging = params + [page_size, offset]

    #Conexion a la base de datos y ejecuecion de queries
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(count_sql, params)
        total = cur.fetchone()["COUNT(*)"]
        cur.execute(base, params_with_paging)
        rows = cur.fetchall()

    # Convierte los IDs de estado en nombres más legibles (ejemplo: 1 -> "vendido")
    status_rev = {v: k for k, v in STATUS_MAP.items()}
    for r in rows:
        r["estado"] = status_rev.get(r["status_id"], f"status_{r['status_id']}")
    return rows, total
