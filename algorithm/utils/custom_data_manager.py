"""
Gestor de datos personalizado que obtiene datos de data.py o de la base de datos.
"""
import logging
import sys
import os
from typing import List, Optional

from models import CPU, GPU, RAM, Storage, Motherboard, PSU, Cooling, Case

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
        
        # Intentar cargar datos directamente
        self.logger.info("Intentando importar data.py directamente")
        try:
            # Asegurar que el directorio actual esté en el path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
                self.logger.info(f"Añadido {project_root} al path")
            
            # Importar directamente
            import data
            self.cpus_original = data.cpus
            self.gpus_original = data.gpus
            self.rams_original = data.rams
            self.storages_original = data.storages
            self.motherboards_original = data.motherboards
            self.psus_original = data.psus
            self.logger.info("✅ data.py importado exitosamente")
        except ImportError as e:
            self.logger.warning(f"No se pudo importar data.py directamente: {e}")
            # Intentar usar el puente de datos como respaldo
            try:
                self.logger.info("Intentando cargar desde data_bridge")
                from algorithm.utils.data_bridge import data_components
                cpus_data, gpus_data, rams_data, storages_data, motherboards_data, psus_data = data_components
                
                # Guardar los datos originales
                self.cpus_original = cpus_data
                self.gpus_original = gpus_data
                self.rams_original = rams_data
                self.storages_original = storages_data
                self.motherboards_original = motherboards_data
                self.psus_original = psus_data
                
                # Verificar si se cargaron datos
                if len(self.cpus_original) > 0:
                    self.logger.info("✅ Datos cargados desde data_bridge")
                else:
                    self.logger.warning("data_bridge no devolvió datos, creando datos de respaldo")
                    self._create_minimal_data()
            except Exception as e:
                self.logger.error(f"Error cargando desde data_bridge: {e}")
                self._create_minimal_data()
        
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
    
    def _create_minimal_data(self):
        """Crea datos mínimos de respaldo cuando todo lo demás falla"""
        self.logger.info("Creando datos mínimos de respaldo")
        
        # Crear datos mínimos para CPUs
        self.cpus_original = [
            CPU(
                maker="Intel Core i7",
                model="14700K",
                performance=78,
                price=419.99,
                power_consumption=125,
                has_integrated_graphics=True,
                integrated_graphics_power=15
            ),
            CPU(
                maker="AMD Ryzen 7",
                model="7800X3D",
                performance=80,
                price=449.99,
                power_consumption=105,
                has_integrated_graphics=False,
                integrated_graphics_power=0
            )
        ]
        
        # Crear datos mínimos para GPUs
        self.gpus_original = [
            None,  # Opción para gráficos integrados
            GPU(
                maker="NVIDIA RTX 4070",
                price=599.99,
                power_consumption=200,
                power=70
            ),
            GPU(
                maker="AMD Radeon RX 7800 XT",
                price=499.99,
                power_consumption=250,
                power=65
            )
        ]
        
        # Crear datos mínimos para RAM
        self.rams_original = [
            RAM(
                maker="Corsair",
                model="Vengeance LPX",
                capacity=16,
                frequency=3200,
                type="DDR4",
                price=89.99
            ),
            RAM(
                maker="G.Skill",
                model="Trident Z5",
                capacity=32,
                frequency=6000,
                type="DDR5",
                price=179.99
            )
        ]
        
        # Crear datos mínimos para almacenamiento
        self.storages_original = [
            Storage(
                maker="Samsung",
                model="970 EVO",
                type="SSD",
                capacity=1000,
                price=99.99
            ),
            Storage(
                maker="Western Digital",
                model="Black",
                type="HDD",
                capacity=2000,
                price=79.99
            )
        ]
        
        # Crear datos mínimos para placas base
        self.motherboards_original = [
            Motherboard(
                maker="ASUS",
                model="ROG Strix Z790-E",
                price=399.99,
                power_consumption=30,
                max_ram_capacity=128,
                max_ram_frequency=7000,
                ram_socket_type="DDR5",
                compatible_cpus=["14", "13", "12"]
            ),
            Motherboard(
                maker="MSI",
                model="MAG B650 TOMAHAWK",
                price=299.99,
                power_consumption=25,
                max_ram_capacity=128,
                max_ram_frequency=6000,
                ram_socket_type="DDR5",
                compatible_cpus=["7", "8"]
            )
        ]
        
        # Crear datos mínimos para fuentes de alimentación
        self.psus_original = [
            PSU(
                maker="Corsair",
                model="RM850x",
                capacity=850,
                price=129.99
            ),
            PSU(
                maker="EVGA",
                model="SuperNOVA 750 G5",
                capacity=750,
                price=109.99
            )
        ]
    
    # Los métodos originales permanecen sin cambios
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