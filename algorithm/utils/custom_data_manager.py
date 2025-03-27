"""
Gestor de datos personalizado que obtiene datos de data.py o de la base de datos.
"""
import logging
from typing import List, Optional

from models import CPU, GPU, RAM, Storage, Motherboard, PSU, Cooling, Case
from algorithm.utils.data_bridge import data_components

# Obtener los componentes desde el puente de datos
cpus_data, gpus_data, rams_data, storages_data, motherboards_data, psus_data = data_components

class CustomDataManager:
    """
    Versión personalizada del DataManager que usa datos directamente de data.py
    """
    
    def __init__(self):
        """
        Inicializar el gestor de datos personalizado
        """
        self.logger = logging.getLogger("CustomDataManager")
        self.logger.info("Inicializando gestor de datos personalizado")
        
        # Guardar los datos originales
        self.cpus_original = cpus_data
        self.gpus_original = gpus_data
        self.rams_original = rams_data
        self.storages_original = storages_data
        self.motherboards_original = motherboards_data
        self.psus_original = psus_data
        
        # Crear datos de muestra para coolings y cases que no existen en data.py
        self.coolings_data = [
            Cooling(
                maker="Noctua",
                model="NH-D15",
                type="Air",
                cooling_capacity=180,
                price=99.99,
                noise_level=30,
                fan_count=2,
                fan_size=140,
                rgb=False,
                height_mm=165
            ),
            Cooling(
                maker="ARCTIC",
                model="Liquid Freezer II 240",
                type="Liquid",
                cooling_capacity=250,
                price=119.99,
                noise_level=25,
                fan_count=2,
                fan_size=120,
                rgb=False,
                height_mm=240
            )
        ]
        
        self.cases_data = [
            Case(
                maker="Lian Li",
                model="O11 Dynamic",
                form_factors=["ATX", "Micro-ATX", "Mini-ITX"],
                max_gpu_length=420,
                cooling_support={"max_air_cooler_height": 155, "radiator_support": [240, 360]},
                price=149.99
            ),
            Case(
                maker="Fractal Design",
                model="Meshify 2",
                form_factors=["ATX", "Micro-ATX", "Mini-ITX"],
                max_gpu_length=460,
                cooling_support={"max_air_cooler_height": 185, "radiator_support": [240, 280, 360]},
                price=139.99
            )
        ]
    
    def get_cpus(self) -> List[CPU]:
        """
        Obtener todos los CPUs
        
        Returns:
            List[CPU]: Lista de objetos CPU
        """
        return self.cpus_original
    
    def get_gpus(self) -> List[Optional[GPU]]:
        """
        Obtener todos los GPUs
        
        Returns:
            List[Optional[GPU]]: Lista de objetos GPU (incluyendo None para opción de gráficos integrados)
        """
        return self.gpus_original
    
    def get_rams(self) -> List[RAM]:
        """
        Obtener todos los RAMs
        
        Returns:
            List[RAM]: Lista de objetos RAM
        """
        return self.rams_original
    
    def get_storages(self) -> List[Storage]:
        """
        Obtener todos los Storages
        
        Returns:
            List[Storage]: Lista de objetos Storage
        """
        return self.storages_original
    
    def get_motherboards(self) -> List[Motherboard]:
        """
        Obtener todos los Motherboards
        
        Returns:
            List[Motherboard]: Lista de objetos Motherboard
        """
        return self.motherboards_original
    
    def get_psus(self) -> List[PSU]:
        """
        Obtener todos los PSUs
        
        Returns:
            List[PSU]: Lista de objetos PSU
        """
        return self.psus_original
    
    def get_coolings(self) -> List[Cooling]:
        """
        Obtener todas las soluciones de refrigeración
        
        Returns:
            List[Cooling]: Lista de objetos Cooling
        """
        return self.coolings_data
    
    def get_cases(self) -> List[Case]:
        """
        Obtener todos los Cases
        
        Returns:
            List[Case]: Lista de objetos Case
        """
        return self.cases_data