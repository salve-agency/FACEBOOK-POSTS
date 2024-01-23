import os

def delete_items(path):
    if os.path.isdir(path):
        # Obtener la lista de archivos y subdirectorios
        contenido_carpeta = os.listdir(path)
         
        # Iterar sobre el contenido y eliminar archivos o directorios
        for item in contenido_carpeta:
            ruta_item = os.path.join(path, item)
            
            if os.path.isfile(ruta_item):
                # Si es un archivo, eliminarlo
                os.remove(ruta_item)

            elif os.path.isdir(ruta_item):
                # Si es una carpeta, eliminarla recursivamente
                delete_items(ruta_item)
        
        # Una vez que el contenido se ha eliminado, eliminar el directorio vacío
        os.rmdir(path)
        print(f"Carpeta {path} eliminada exitosamente.")
    else:
        print(f"{path} no es una carpeta válida.")