#Se realzian las importaciones necesarias
from typing import Iterable, List
#Se define la funcion con un arrewglo de enteros
def ordenar_bloques(my_array: Iterable[int]) -> str:
    #Lista para grupos ya procesados
    bloques: List[str] = []

    #Lista donde se van acumulando los numeros del grupo actual
    actual: List[int] = []

    #Funcion que cierra el grupo cuando aparece un 0
    def cerrar_bloque():
        nonlocal actual, bloques
        if not actual: #Si el grupo esta vacio se coloca una X
            bloques.append("X")
        else:
            actual.sort() #Si el grupo no esta vacio se organiza
            bloques.append("".join(str(x) for x in actual))
        actual = []

    #Recorrer cada numero del arreglo
    for x in my_array:
        if x == 0:
            cerrar_bloque()
        else:
            actual.append(int(x))

    #Ciera el ultimop grupo terminado
    cerrar_bloque()

    if len(list(my_array)) == 0:  # arreglo vacío
        return ""

    #Se une los bloques con un espacio
    return " ".join(bloques)


if __name__ == "__main__":
    # Se escribe los numeros
    myArray = (8,5,2,0,0,4,5,0,6,3,9)

    # Llamada a la función
    resultado = ordenar_bloques(myArray)

    # Imprime directamente la respuesta
    print(resultado)
