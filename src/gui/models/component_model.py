"""
Modelo para componentes de computadora.
"""
import logging
from typing import List, Dict, Any, Optional


class ComponentModel:
    """Modelo para gestionar componentes de computadora"""
    
    def __init__(self, data_manager):
        """
        Inicializar el modelo de componentes.
        
        Args:
            data_manager: Gestor de datos de componentes
        """
        self.data_manager = data_manager
        self.logger = logging.getLogger("ComputerGenerator.ComponentModel")
        
        # Inicializar caché de componentes
        self._cpu_cache = None
        self._gpu_cache = None
        self._ram_cache = None
        self._storage_cache = None
        self._motherboard_cache = None
        self._psu_cache = None
        self._cooling_cache = None
        self._case_cache = None
        
        # Observadores (patrón Observer)
        self.observers = []
    
    def add_observer(self, observer):
        """
        Agregar un observador para notificaciones.
        
        Args:
            observer: Objeto observador que implementa los métodos de notificación
        """
        if observer not in self.observers:
            self.observers.append(observer)
    
    def remove_observer(self, observer):
        """
        Eliminar un observador.
        
        Args:
            observer: Observador a eliminar
        """
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify_components_updated(self, component_type):
        """
        Notificar a los observadores que los componentes han sido actualizados.
        
        Args:
            component_type: Tipo de componente actualizado
        """
        for observer in self.observers:
            if hasattr(observer, 'on_components_updated'):
                observer.on_components_updated(component_type)
    
    def get_cpu_list(self, refresh=False):
        """
        Obtener lista de CPUs.
        
        Args:
            refresh: Si se debe actualizar la caché
            
        Returns:
            List: Lista de CPUs
        """
        if self._cpu_cache is None or refresh:
            try:
                self._cpu_cache = self.data_manager.get_cpus()
                self.logger.debug(f"Obtenidos {len(self._cpu_cache)} CPUs del gestor de datos")
            except Exception as e:
                self.logger.error(f"Error al obtener CPUs: {str(e)}", exc_info=True)
                self._cpu_cache = []
        
        return self._cpu_cache
    
    def get_gpu_list(self, refresh=False):
        """
        Obtener lista de GPUs.
        
        Args:
            refresh: Si se debe actualizar la caché
            
        Returns:
            List: Lista de GPUs
        """
        if self._gpu_cache is None or refresh:
            try:
                self._gpu_cache = self.data_manager.get_gpus()
                self.logger.debug(f"Obtenidos {len(self._gpu_cache)} GPUs del gestor de datos")
            except Exception as e:
                self.logger.error(f"Error al obtener GPUs: {str(e)}", exc_info=True)
                self._gpu_cache = []
        
        return self._gpu_cache
    
    def get_ram_list(self, refresh=False):
        """
        Obtener lista de RAMs.
        
        Args:
            refresh: Si se debe actualizar la caché
            
        Returns:
            List: Lista de RAMs
        """
        if self._ram_cache is None or refresh:
            try:
                self._ram_cache = self.data_manager.get_rams()
                self.logger.debug(f"Obtenidos {len(self._ram_cache)} RAMs del gestor de datos")
            except Exception as e:
                self.logger.error(f"Error al obtener RAMs: {str(e)}", exc_info=True)
                self._ram_cache = []
        
        return self._ram_cache
    
    def get_storage_list(self, refresh=False):
        """
        Obtener lista de almacenamientos.
        
        Args:
            refresh: Si se debe actualizar la caché
            
        Returns:
            List: Lista de almacenamientos
        """
        if self._storage_cache is None or refresh:
            try:
                self._storage_cache = self.data_manager.get_storages()
                self.logger.debug(f"Obtenidos {len(self._storage_cache)} almacenamientos del gestor de datos")
            except Exception as e:
                self.logger.error(f"Error al obtener almacenamientos: {str(e)}", exc_info=True)
                self._storage_cache = []
        
        return self._storage_cache
    
    def get_motherboard_list(self, refresh=False):
        """
        Obtener lista de placas base.
        
        Args:
            refresh: Si se debe actualizar la caché
            
        Returns:
            List: Lista de placas base
        """
        if self._motherboard_cache is None or refresh:
            try:
                self._motherboard_cache = self.data_manager.get_motherboards()
                self.logger.debug(f"Obtenidas {len(self._motherboard_cache)} placas base del gestor de datos")
            except Exception as e:
                self.logger.error(f"Error al obtener placas base: {str(e)}", exc_info=True)
                self._motherboard_cache = []
        
        return self._motherboard_cache
    
    def get_psu_list(self, refresh=False):
        """
        Obtener lista de fuentes de alimentación.
        
        Args:
            refresh: Si se debe actualizar la caché
            
        Returns:
            List: Lista de fuentes de alimentación
        """
        if self._psu_cache is None or refresh:
            try:
                self._psu_cache = self.data_manager.get_psus()
                self.logger.debug(f"Obtenidas {len(self._psu_cache)} fuentes de alimentación del gestor de datos")
            except Exception as e:
                self.logger.error(f"Error al obtener fuentes de alimentación: {str(e)}", exc_info=True)
                self._psu_cache = []
        
        return self._psu_cache
    
    def get_cooling_list(self, refresh=False):
        """
        Obtener lista de soluciones de refrigeración.
        
        Args:
            refresh: Si se debe actualizar la caché
            
        Returns:
            List: Lista de soluciones de refrigeración
        """
        if self._cooling_cache is None or refresh:
            try:
                self._cooling_cache = self.data_manager.get_coolings()
                self.logger.debug(f"Obtenidas {len(self._cooling_cache)} soluciones de refrigeración del gestor de datos")
            except Exception as e:
                self.logger.error(f"Error al obtener soluciones de refrigeración: {str(e)}", exc_info=True)
                self._cooling_cache = []
        
        return self._cooling_cache
    
    def get_case_list(self, refresh=False):
        """
        Obtener lista de cajas.
        
        Args:
            refresh: Si se debe actualizar la caché
            
        Returns:
            List: Lista de cajas
        """
        if self._case_cache is None or refresh:
            try:
                self._case_cache = self.data_manager.get_cases()
                self.logger.debug(f"Obtenidas {len(self._case_cache)} cajas del gestor de datos")
            except Exception as e:
                self.logger.error(f"Error al obtener cajas: {str(e)}", exc_info=True)
                self._case_cache = []
        
        return self._case_cache
    
    def refresh_all_components(self):
        """Actualizar caché de todos los componentes"""
        self.get_cpu_list(refresh=True)
        self.get_gpu_list(refresh=True)
        self.get_ram_list(refresh=True)
        self.get_storage_list(refresh=True)
        self.get_motherboard_list(refresh=True)
        self.get_psu_list(refresh=True)
        self.get_cooling_list(refresh=True)
        self.get_case_list(refresh=True)
        
        # Notificar a los observadores
        self.notify_components_updated("all")
        
        self.logger.info("Todos los componentes actualizados")
    
    def find_component_by_name(self, component_type, name):
        """
        Buscar un componente por su nombre.
        
        Args:
            component_type: Tipo de componente
            name: Nombre del componente
            
        Returns:
            Optional: Componente encontrado o None
        """
        components = self._get_components_by_type(component_type)
        
        for component in components:
            # Diferentes componentes tienen diferentes atributos para su nombre
            if hasattr(component, 'maker') and component.maker == name:
                return component
            elif hasattr(component, 'model') and component.model == name:
                return component
        
        return None
    
    def filter_components(self, component_type, filters):
        """
        Filtrar componentes según criterios.
        
        Args:
            component_type: Tipo de componente
            filters: Diccionario con filtros a aplicar
            
        Returns:
            List: Lista de componentes filtrados
        """
        components = self._get_components_by_type(component_type)
        filtered_components = []
        
        for component in components:
            # Verificar si el componente cumple todos los filtros
            meets_criteria = True
            
            for key, value in filters.items():
                if not hasattr(component, key):
                    meets_criteria = False
                    break
                
                component_value = getattr(component, key)
                
                # Manejar diferentes tipos de comparaciones
                if isinstance(value, tuple) and len(value) == 2:
                    # Rango (min, max)
                    op, compare_value = value
                    
                    if op == '>=' and not (component_value >= compare_value):
                        meets_criteria = False
                        break
                    elif op == '<=' and not (component_value <= compare_value):
                        meets_criteria = False
                        break
                    elif op == '>' and not (component_value > compare_value):
                        meets_criteria = False
                        break
                    elif op == '<' and not (component_value < compare_value):
                        meets_criteria = False
                        break
                        
                elif isinstance(value, list):
                    # Lista de valores posibles
                    if component_value not in value:
                        meets_criteria = False
                        break
                        
                else:
                    # Valor exacto
                    if component_value != value:
                        meets_criteria = False
                        break
            
            if meets_criteria:
                filtered_components.append(component)
        
        return filtered_components
    
    def search_components(self, component_type, search_term):
        """
        Buscar componentes que coincidan con un término de búsqueda.
        
        Args:
            component_type: Tipo de componente
            search_term: Término de búsqueda
            
        Returns:
            List: Lista de componentes que coinciden
        """
        components = self._get_components_by_type(component_type)
        search_term = search_term.lower()
        results = []
        
        for component in components:
            # Buscar en atributos comunes
            if (hasattr(component, 'maker') and search_term in component.maker.lower()) or \
               (hasattr(component, 'model') and search_term in component.model.lower()):
                results.append(component)
                continue
            
            # Buscar en otros atributos específicos según el tipo
            if component_type == "cpu" and hasattr(component, 'socket_type') and search_term in component.socket_type.lower():
                results.append(component)
            elif component_type == "gpu" and hasattr(component, 'vram_type') and search_term in component.vram_type.lower():
                results.append(component)
            # ...otros casos específicos
        
        return results
    
    def _get_components_by_type(self, component_type):
        """
        Obtener componentes por tipo.
        
        Args:
            component_type: Tipo de componente
            
        Returns:
            List: Lista de componentes
        """
        if component_type == "cpu":
            return self.get_cpu_list()
        elif component_type == "gpu":
            return self.get_gpu_list()
        elif component_type == "ram":
            return self.get_ram_list()
        elif component_type == "storage":
            return self.get_storage_list()
        elif component_type == "motherboard":
            return self.get_motherboard_list()
        elif component_type == "psu":
            return self.get_psu_list()
        elif component_type == "cooling":
            return self.get_cooling_list()
        elif component_type == "case":
            return self.get_case_list()
        else:
            self.logger.warning(f"Tipo de componente desconocido: {component_type}")
            return []