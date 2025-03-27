"""
Módulo puente para cargar datos del archivo data.py original.
"""
import sys
import os
import logging
from typing import Dict, List, Any, Optional, Union, Tuple

# Configurar logging
logger = logging.getLogger(__name__)

def load_data_components():
    """
    Carga los componentes directamente desde data.py
    
    Returns:
        Tuple con las listas de componentes (cpus, gpus, rams, storages, motherboards, psus)
    """
    try:
        logger.info("Intentando importar data.py")
        try:
            # Primer intento: importar directamente
            from data import cpus, gpus, rams, storages, motherboards, psus
            logger.info("Datos importados directamente de data.py")
        except ImportError:
            # Segundo intento: añadir el directorio raíz al path
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            sys.path.insert(0, current_dir)
            logger.info(f"Añadiendo directorio raíz al path: {current_dir}")
            
            try:
                from data import cpus, gpus, rams, storages, motherboards, psus
                logger.info("Datos importados desde data.py después de ajustar el path")
            except ImportError as e:
                # Tercer intento: buscar data.py en todas las rutas posibles
                found = False
                for path in sys.path:
                    data_file = os.path.join(path, 'data.py')
                    if os.path.exists(data_file):
                        logger.info(f"Encontrado data.py en: {data_file}")
                        # Añadir el directorio que contiene data.py al path
                        if path not in sys.path:
                            sys.path.insert(0, path)
                        from data import cpus, gpus, rams, storages, motherboards, psus
                        found = True
                        logger.info("Datos importados después de encontrar data.py")
                        break
                
                if not found:
                    logger.error(f"No se pudo encontrar data.py en ninguna ruta. Rutas buscadas: {sys.path}")
                    raise ImportError(f"No se pudo importar data.py. Error original: {e}")
        
        return cpus, gpus, rams, storages, motherboards, psus
        
    except Exception as e:
        logger.error(f"Error al cargar datos de data.py: {e}")
        # Retornar listas vacías en caso de error
        return [], [], [], [], [], []

# Cargar datos al importar el módulo
data_components = load_data_components()