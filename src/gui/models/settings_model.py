"""
Modelo para gestión de configuraciones de la aplicación.
"""
import os
import json
import logging
from typing import Dict, Any, Optional


class SettingsModel:
    """Modelo para gestionar configuraciones de la aplicación"""
    
    def __init__(self, settings_file="settings.json"):
        """
        Inicializar el modelo de configuraciones.
        
        Args:
            settings_file: Ruta al archivo de configuraciones
        """
        self.settings_file = settings_file
        self.logger = logging.getLogger("ComputerGenerator.SettingsModel")
        
        # Valores predeterminados
        self.default_settings = {
            "theme": "System",            # Tema de la aplicación (Light, Dark, System)
            "window_size": "1200x800",    # Tamaño de ventana
            "save_window_size": True,     # Recordar tamaño de ventana
            "auto_update_data": False,    # Actualizar datos automáticamente
            "update_interval_days": 7,    # Intervalo de actualización en días
            "default_population_size": 50,  # Tamaño de población predeterminado
            "default_generations": 100,   # Generaciones predeterminadas
            "default_mutation_rate": 0.1,  # Tasa de mutación predeterminada
            "default_crossover_rate": 0.8,  # Tasa de cruce predeterminada
            "reset_to_defaults": False,   # Reiniciar a valores predeterminados al iniciar
            "language": "en",             # Idioma
            "developer_mode": False,      # Modo desarrollador
            "last_directory": "",         # Último directorio usado
        }
        
        # Configuraciones actuales
        self.settings = self.default_settings.copy()
        
        # Cargar configuraciones
        self.load_settings()
        
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
    
    def notify_settings_changed(self, setting_key=None):
        """
        Notificar a los observadores que las configuraciones han cambiado.
        
        Args:
            setting_key: Clave de configuración que cambió (None para todas)
        """
        for observer in self.observers:
            if hasattr(observer, 'on_settings_changed'):
                observer.on_settings_changed(setting_key)
    
    def load_settings(self):
        """Cargar configuraciones desde archivo"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    
                # Actualizar configuraciones, manteniendo los valores predeterminados
                # para claves que no estén en el archivo
                for key, value in loaded_settings.items():
                    if key in self.default_settings:
                        self.settings[key] = value
                        
                self.logger.info(f"Configuraciones cargadas desde {self.settings_file}")
            else:
                self.logger.info(f"Archivo de configuraciones {self.settings_file} no encontrado, usando valores predeterminados")
                
        except Exception as e:
            self.logger.error(f"Error al cargar configuraciones: {str(e)}")
            # Usar valores predeterminados en caso de error
            self.settings = self.default_settings.copy()
    
    def save_settings(self, settings=None):
        """
        Guardar configuraciones a archivo.
        
        Args:
            settings: Diccionario de configuraciones a guardar (opcional)
        """
        try:
            # Si se proporcionan configuraciones, actualizarlas
            if settings:
                for key, value in settings.items():
                    if key in self.settings:
                        self.settings[key] = value
            
            # Crear directorios si no existen
            directory = os.path.dirname(self.settings_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Guardar configuraciones a archivo JSON
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
                
            self.logger.info(f"Configuraciones guardadas en {self.settings_file}")
            
            # Notificar a los observadores
            self.notify_settings_changed()
            
        except Exception as e:
            self.logger.error(f"Error al guardar configuraciones: {str(e)}")
    
    def get_settings(self):
        """
        Obtener todas las configuraciones.
        
        Returns:
            Dict: Diccionario con todas las configuraciones
        """
        return self.settings.copy()
    
    def get_setting(self, key, default=None):
        """
        Obtener una configuración específica.
        
        Args:
            key: Clave de configuración
            default: Valor predeterminado si la clave no existe
            
        Returns:
            Any: Valor de la configuración
        """
        return self.settings.get(key, default)
    
    def update_setting(self, key, value):
        """
        Actualizar una configuración específica.
        
        Args:
            key: Clave de configuración
            value: Nuevo valor
            
        Returns:
            bool: True si se actualizó, False si la clave no existe
        """
        if key in self.settings:
            self.settings[key] = value
            
            # Guardar cambios inmediatamente
            self.save_settings()
            
            # Notificar a los observadores
            self.notify_settings_changed(key)
            
            self.logger.debug(f"Configuración actualizada: {key}={value}")
            return True
        else:
            self.logger.warning(f"Intento de actualizar configuración desconocida: {key}")
            return False
    
    def reset_to_defaults(self):
        """
        Reiniciar todas las configuraciones a valores predeterminados.
        
        Returns:
            bool: True si se reinició, False en caso de error
        """
        try:
            self.settings = self.default_settings.copy()
            self.save_settings()
            
            # Notificar a los observadores
            self.notify_settings_changed()
            
            self.logger.info("Configuraciones reiniciadas a valores predeterminados")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al reiniciar configuraciones: {str(e)}")
            return False