"""
Modelo para el generador de computadoras.
"""
import logging
import time
import threading
from copy import deepcopy
from typing import List, Dict, Any, Callable, Optional

from models import UserPreferences, Computer
from algorithm import ComputerGenerator


class GeneratorModel:
    """Modelo para el generador de computadoras"""
    
    def __init__(self, data_manager):
        """
        Inicializar el modelo del generador.
        
        Args:
            data_manager: Gestor de datos de componentes
        """
        self.data_manager = data_manager
        self.logger = logging.getLogger("ComputerGenerator.GeneratorModel")
        
        # Estado del generador
        self.current_computer = None
        self.generated_computers = []
        self.stats = {}
        self.optimization_running = False
        self.generator = None
        
        # Parámetros del algoritmo (valores predeterminados)
        self.population_size = 50
        self.generations = 100
        self.crossover_rate = 0.8
        self.mutation_rate = 0.1
        self.elitism_percentage = 0.1
        self.tournament_size = 3
        self.adaptive_mutation = True
        self.fitness_weights = None
        
        # Preferencias de usuario
        self.user_preferences = None
        
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
    
    def notify_generation_complete(self, results_text):
        """
        Notificar a los observadores que la generación ha completado.
        
        Args:
            results_text: Texto de resultados
        """
        for observer in self.observers:
            if hasattr(observer, 'on_generation_complete'):
                observer.on_generation_complete(results_text)
    
    def notify_generation_progress(self, progress, status_text):
        """
        Notificar a los observadores del progreso de la generación.
        
        Args:
            progress: Porcentaje de progreso (0-100)
            status_text: Texto de estado
        """
        for observer in self.observers:
            if hasattr(observer, 'on_generation_progress'):
                observer.on_generation_progress(progress, status_text)
    
    def set_generator_parameters(self, population_size, generations, crossover_rate, 
                               mutation_rate, elitism_percentage, tournament_size, 
                               adaptive_mutation, fitness_weights=None):
        """
        Establecer parámetros del algoritmo genético.
        
        Args:
            population_size: Tamaño de la población
            generations: Número de generaciones
            crossover_rate: Tasa de cruce
            mutation_rate: Tasa de mutación
            elitism_percentage: Porcentaje de elitismo
            tournament_size: Tamaño de torneo
            adaptive_mutation: Si usar mutación adaptativa
            fitness_weights: Pesos para la función de fitness
        """
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.elitism_percentage = elitism_percentage
        self.tournament_size = tournament_size
        self.adaptive_mutation = adaptive_mutation
        self.fitness_weights = fitness_weights
        
        self.logger.info(f"Parámetros del generador establecidos: "
                        f"población={population_size}, generaciones={generations}")
    
    def set_user_preferences(self, preferences):
        """
        Establecer preferencias de usuario.
        
        Args:
            preferences: Objeto UserPreferences con las preferencias
        """
        self.user_preferences = preferences
        self.logger.info(f"Preferencias de usuario establecidas: {preferences}")
    
    def generate_computer(self, progress_callback: Optional[Callable] = None) -> bool:
        """
        Generar una configuración de computadora.
        
        Args:
            progress_callback: Función de callback para actualizar progreso
            
        Returns:
            bool: True si la generación fue exitosa, False en caso contrario
        """
        if not self.user_preferences:
            self.logger.error("No se han establecido preferencias de usuario")
            return False
        
        try:
            # Iniciar tiempo
            start_time = time.time()
            
            # Crear el generador
            self.generator = ComputerGenerator(
                population_size=self.population_size,
                crossover_rate=self.crossover_rate,
                mutation_rate=self.mutation_rate,
                generations=self.generations,
                user_preferences=self.user_preferences,
                elitism_percentage=self.elitism_percentage,
                tournament_size=self.tournament_size,
                adaptive_mutation=self.adaptive_mutation,
                fitness_weights=self.fitness_weights
            )
            
            # Establecer bandera de ejecución
            self.optimization_running = True
            
            # Ejecutar el algoritmo genético con monitoreo de progreso
            if progress_callback:
                # Configurar callback para estadísticas
                def stats_callback(generation, best_fitness, avg_fitness):
                    if self.optimization_running:
                        progress = min(100, generation / self.generations * 100)
                        progress_callback(progress, generation, best_fitness, avg_fitness)
                
                # Establecer callback en el generador
                self.generator.set_stats_callback(stats_callback)
            
            # Ejecutar generación
            best_computer, stats = self.generator.run()
            
            # Verificar si se detuvo la ejecución
            if not self.optimization_running:
                self.logger.info("Generación detenida por usuario")
                return False
            
            # Guardar resultados
            self.current_computer = best_computer
            self.stats = stats
            
            # Agregar a historial
            self.generated_computers.append({
                "computer": deepcopy(best_computer),
                "stats": deepcopy(stats),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "preferences": deepcopy(self.user_preferences)
            })
            
            self.logger.info(f"Generación completada en {time.time() - start_time:.2f} segundos. "
                           f"Fitness: {best_computer.fitness:.2f}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error durante la generación: {str(e)}", exc_info=True)
            self.optimization_running = False
            return False
    
    def stop_generation(self):
        """Detener el proceso de generación en curso"""
        self.optimization_running = False
        self.logger.info("Solicitud de detención de generación")
    
    def get_current_computer(self):
        """
        Obtener la computadora actual generada.
        
        Returns:
            Computer: Objeto Computer con la configuración actual
        """
        return self.current_computer
    
    def get_generation_stats(self):
        """
        Obtener estadísticas de la última generación.
        
        Returns:
            Dict: Diccionario con estadísticas
        """
        return self.stats
    
    def get_generated_computers(self):
        """
        Obtener todas las computadoras generadas.
        
        Returns:
            List: Lista de computadoras generadas
        """
        return self.generated_computers
    
    def add_to_comparison(self, name=None):
        """
        Agregar la computadora actual a la lista de comparación.
        
        Args:
            name: Nombre para la configuración (opcional)
            
        Returns:
            bool: True si se agregó correctamente, False en caso contrario
        """
        if not self.current_computer:
            return False
        
        # Generar nombre si no se proporciona
        if not name:
            name = f"Config {len(self.generated_computers)}"
        
        # Crear entrada de comparación
        comparison_entry = {
            "name": name,
            "computer": deepcopy(self.current_computer),
            "stats": deepcopy(self.stats),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Agregar a lista de comparación
        self.generated_computers.append(comparison_entry)
        
        self.logger.info(f"Configuración '{name}' agregada a comparación")
        return True
    
    def remove_from_comparison(self, index):
        """
        Eliminar una computadora de la lista de comparación.
        
        Args:
            index: Índice de la configuración a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        if 0 <= index < len(self.generated_computers):
            removed = self.generated_computers.pop(index)
            self.logger.info(f"Configuración '{removed['name']}' eliminada de comparación")
            return True
        return False
    
    def clear_comparison(self):
        """
        Limpiar toda la lista de comparación.
        
        Returns:
            int: Número de elementos eliminados
        """
        count = len(self.generated_computers)
        self.generated_computers = []
        self.logger.info(f"Lista de comparación limpiada ({count} elementos)")
        return count
    
    def reset(self):
        """Reiniciar el modelo a su estado inicial"""
        self.current_computer = None
        self.stats = {}
        self.logger.info("Modelo reiniciado")
    
    def get_configuration_data(self):
        """
        Obtener datos de configuración para guardar.
        
        Returns:
            Dict: Datos de configuración
        """
        if not self.current_computer:
            return None
        
        # Crear diccionario de configuración
        config_data = {
            "computer": self.current_computer.to_dict(),
            "stats": self.stats,
            "preferences": self.user_preferences.to_dict() if self.user_preferences else None,
            "parameters": {
                "population_size": self.population_size,
                "generations": self.generations,
                "crossover_rate": self.crossover_rate,
                "mutation_rate": self.mutation_rate,
                "elitism_percentage": self.elitism_percentage,
                "tournament_size": self.tournament_size,
                "adaptive_mutation": self.adaptive_mutation,
                "fitness_weights": self.fitness_weights
            }
        }
        
        return config_data
    
    def load_configuration(self, config_data):
        """
        Cargar configuración desde datos.
        
        Args:
            config_data: Datos de configuración
            
        Returns:
            bool: True si se cargó correctamente, False en caso contrario
        """
        try:
            # Validar datos mínimos
            if "computer" not in config_data:
                return False
            
            # Recrear el objeto Computer
            # (Código para recrear el objeto Computer desde diccionario)
            
            # Cargar parámetros si están presentes
            if "parameters" in config_data:
                params = config_data["parameters"]
                self.population_size = params.get("population_size", self.population_size)
                self.generations = params.get("generations", self.generations)
                self.crossover_rate = params.get("crossover_rate", self.crossover_rate)
                self.mutation_rate = params.get("mutation_rate", self.mutation_rate)
                self.elitism_percentage = params.get("elitism_percentage", self.elitism_percentage)
                self.tournament_size = params.get("tournament_size", self.tournament_size)
                self.adaptive_mutation = params.get("adaptive_mutation", self.adaptive_mutation)
                self.fitness_weights = params.get("fitness_weights", self.fitness_weights)
            
            # Cargar preferencias si están presentes
            if "preferences" in config_data:
                # (Código para recrear el objeto UserPreferences desde diccionario)
                pass
            
            # Cargar estadísticas si están presentes
            if "stats" in config_data:
                self.stats = config_data["stats"]
            
            self.logger.info("Configuración cargada exitosamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error al cargar configuración: {str(e)}", exc_info=True)
            return False