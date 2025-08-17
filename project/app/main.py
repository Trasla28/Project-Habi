#Se realzian las importaciones necesarias
from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from app.queries import fetch_properties
from app.settings import PAGE_SIZE_DEFAULT, ALLOWED_STATUS

#Instancia de la apliacion FastApu con metadatos
app = FastAPI(title="Habi Inmuebles API", version="1.0.0")

#Mensaje de confirmacion para verificar que este arriba el servicio
@app.get("/health")
def health():
    return {"ok": True}

@app.get("/inmuebles")
#Se define lista-inmuebles para los filtros y parametros de la consulta
def listar_inmuebles(
    ciudad: Optional[str] = Query(None, description="Ciudad exacta, e.g., 'Bogotá'"),
    estado: Optional[str] = Query(None, description=f"Uno de {', '.join(ALLOWED_STATUS)}"), #Se colocan los valores permitidos en settings para el estado
    anio: Optional[int] = Query(None, ge=1900, le=2100, description="Año "),
    page: int = Query(1, ge=1),
    page_size: int = Query(PAGE_SIZE_DEFAULT, ge=1, le=200),
    order_by: str = Query("update_date"), # Campo de ordenamiento de fecha
    order_dir: str = Query("desc"), #Tipo de ordenamiento asc o desc
):
    try:
        data, total = fetch_properties(ciudad, estado, anio, page, page_size, order_by, order_dir)#SAe traen todos los datos
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    #Se retoprna los metadatos de la paginacion
    return {
        "meta": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": (total + page_size - 1) // page_size,
            "order_by": order_by,
            "order_dir": order_dir,
        },
        "data": data,
    }
