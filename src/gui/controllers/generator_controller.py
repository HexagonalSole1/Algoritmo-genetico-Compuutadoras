"""
Controlador para la generación de computadoras.
"""
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import customtkinter as ctk
import logging
import json
from datetime import datetime

from models import UserPreferences
from gui.views.dialogs.include_exclude_dialog import IncludeExcludeDialog
from gui.views.dialogs.fitness_weights_dialog import FitnessWeightsDialog


class GeneratorController:
    """Controlador para la generación de computadoras"""
    
    def __init__(self, generator_model, component_model):
        """
        Inicializar el controlador.
        
        Args:
            generator_model: Modelo del generador
            component_model: Modelo de componentes
        """
        self.generator_model = generator_model
        self.component_model = component_model
        self.logger = logging.getLogger("ComputerGenerator.GeneratorController")
        
        # Banderas de estado
        self.optimization_running = False
        self.stop_requested = False
        
        # Inicializar variables de estado
        self.fitness_weights = None
        self.must_include = {}
        self.must_exclude = {}
    
    def generate_computer(self, min_price, max_price, usage, priority, form_factor, future_proof,
                        brand_preferences, aesthetic, population_size, generations, 
                        crossover_rate, mutation_rate, elitism, tournament_size, 
                        adaptive_mutation, update_callback):
        """
        Iniciar la generación de una configuración de computadora.
        
        Args:
            min_price: Precio mínimo
            max_price: Precio máximo
            usage: Uso principal
            priority: Prioridad (performance, value, balanced)
            form_factor: Factor de forma
            future_proof: Si priorizar future-proofing
            brand_preferences: Preferencias de marca
            aesthetic: Preferencias estéticas
            population_size: Tamaño de la población
            generations: Número de generaciones
            crossover_rate: Tasa de cruce
            mutation_rate: Tasa de mutación
            elitism: Porcentaje de elitismo
            tournament_size: Tamaño de torneo
            adaptive_mutation: Si usar mutación adaptativa
            update_callback: Función de callback para actualizar progreso
        """
        try:
            # Mapeo de uso UI a nombres internos
            usage_mapping = {
                'gaming': 'juegos',
                'office': 'ofimática',
                'graphics': 'diseño gráfico',
                'video': 'edición de video',
                'web': 'navegación web',
                'education': 'educación',
                'architecture': 'arquitectura'
            }
            
            # Convertir uso UI a nombre interno
            internal_usage = usage_mapping.get(usage, 'juegos')
            
            # Crear objeto de preferencias de usuario
            user_prefs = UserPreferences(
                min_price=min_price,
                max_price=max_price,
                usage=internal_usage,
                priority=priority,
                brand_preferences=brand_preferences,
                form_factor=form_factor,
                aesthetic=aesthetic,
                must_include=self.must_include,
                must_exclude=self.must_exclude,
                future_proof=future_proof
            )
            
            # Establecer banderas de estado
            self.optimization_running = True
            self.stop_requested = False
            
            # Establecer parámetros del algoritmo en el modelo
            self.generator_model.set_generator_parameters(
                population_size=population_size,
                generations=generations,
                crossover_rate=crossover_rate,
                mutation_rate=mutation_rate,
                elitism_percentage=elitism,
                tournament_size=tournament_size,
                adaptive_mutation=adaptive_mutation,
                fitness_weights=self.fitness_weights
            )
            
            # Establecer preferencias de usuario
            self.generator_model.set_user_preferences(user_prefs)
            
            # Iniciar generación en un hilo separado
            generation_thread = threading.Thread(
                target=self._run_generation,
                args=(update_callback,)
            )
            generation_thread.daemon = True
            generation_thread.start()
            
            self.logger.info(f"Iniciando generación con: población={population_size}, generaciones={generations}")
            
        except Exception as e:
            self.logger.error(f"Error al iniciar generación: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"Error al iniciar generación: {str(e)}")
    
    def _run_generation(self, update_callback):
        """
        Ejecutar el algoritmo genético en un hilo separado.
        
        Args:
            update_callback: Función de callback para actualizar progreso
        """
        try:
            # Configurar callback de progreso
            def progress_callback(progress, generation, best_fitness, avg_fitness):
                if not self.stop_requested:
                    status_text = f"Generation {generation}/{self.generator_model.generations} - Best fitness: {best_fitness:.2f}"
                    update_callback(progress, status_text)
            
            # Ejecutar algoritmo genético
            success = self.generator_model.generate_computer(progress_callback)
            
            # Verificar si se detuvo la generación
            if self.stop_requested:
                self.logger.info("Generación detenida por usuario")
                return
            
            # Actualizar UI en el hilo principal
            if success:
                # Obtener resultados y actualizar UI
                computer = self.generator_model.get_current_computer()
                stats = self.generator_model.get_generation_stats()
                
                # Crear texto de resultados
                results_text = str(computer)
                results_text += "\n\nGeneration Stats:\n"
                results_text += f"Execution Time: {stats['execution_time']:.2f} seconds\n"
                results_text += f"Generations Completed: {stats['generations_completed']}\n"
                results_text += f"Final Population Size: {stats['final_population_size']}\n"
                results_text += f"Final Diversity: {stats['final_diversity']:.2f}\n"
                
                # Actualizar UI en el hilo principal
                tk.CallWrapper().call(self._update_ui_after_generation, results_text)
            
        except Exception as e:
            self.logger.error(f"Error durante la generación: {str(e)}", exc_info=True)
            # Manejar error en el hilo principal
            tk.CallWrapper().call(messagebox.showerror, "Error", f"Error durante la generación: {str(e)}")
        finally:
            # Reiniciar banderas de estado
            self.optimization_running = False
            # Actualizar UI en el hilo principal
            tk.CallWrapper().call(update_callback, 100, "Generation completed")
    
    def _update_ui_after_generation(self, results_text):
        """
        Actualizar UI después de la generación.
        
        Args:
            results_text: Texto de resultados a mostrar
        """
        # Notificar a los observadores (vistas)
        self.generator_model.notify_generation_complete(results_text)
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Generation Complete", "Computer configuration generated successfully!")
    
    def stop_generation(self):
        """Detener el proceso de generación en curso"""
        if self.optimization_running:
            self.stop_requested = True
            self.generator_model.stop_generation()
            self.optimization_running = False
            self.logger.info("Stop requested for generation process")
    
    def show_fitness_weights(self, parent):
        """
        Mostrar diálogo para ajustar pesos de fitness.
        
        Args:
            parent: Widget padre para el diálogo
        """
        # Obtener pesos actuales o usar predeterminados
        current_weights = self.fitness_weights or {
            'price_range': 20,
            'compatibility': 25,
            'usage_match': 30,
            'power_balance': 5,
            'bottleneck': 10,
            'value_cpu': 5,
            'value_gpu': 5
        }
        
        # Mostrar diálogo de pesos de fitness
        dialog = FitnessWeightsDialog(parent, current_weights)
        
        # Si se aceptaron cambios, actualizar pesos
        if dialog.result:
            self.fitness_weights = dialog.result
            self.logger.info(f"Pesos de fitness actualizados: {self.fitness_weights}")
    
    def show_include_exclude(self, parent):
        """
        Mostrar diálogo para especificar componentes a incluir o excluir.
        
        Args:
            parent: Widget padre para el diálogo
        """
        # Obtener componentes disponibles
        components = {
            'cpu': self.component_model.get_cpu_list(),
            'gpu': self.component_model.get_gpu_list(),
            'ram': self.component_model.get_ram_list(),
            'storage': self.component_model.get_storage_list(),
            'motherboard': self.component_model.get_motherboard_list(),
            'psu': self.component_model.get_psu_list(),
            'cooling': self.component_model.get_cooling_list(),
            'case': self.component_model.get_case_list()
        }
        
        # Mostrar diálogo
        dialog = IncludeExcludeDialog(parent, components, self.must_include, self.must_exclude)
        
        # Si se aceptaron cambios, actualizar preferencias
        if dialog.result:
            self.must_include, self.must_exclude = dialog.result
            
            # Registrar cambios
            include_count = sum(len(comps) for comps in self.must_include.values())
            exclude_count = sum(len(comps) for comps in self.must_exclude.values())
            self.logger.info(f"Actualizado include/exclude: {include_count} inclusiones, {exclude_count} exclusiones")
    
    def open_configuration(self):
        """Abrir una configuración guardada"""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Leer archivo JSON
            with open(file_path, 'r') as f:
                config_data = json.load(f)
            
            # Cargar configuración en el modelo
            if self.generator_model.load_configuration(config_data):
                messagebox.showinfo("Configuration Loaded", f"Configuration loaded from {os.path.basename(file_path)}")
                self.logger.info(f"Configuración cargada desde {file_path}")
            else:
                raise ValueError("Invalid configuration format")
                
        except Exception as e:
            self.logger.error(f"Error al abrir configuración: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"Error opening configuration: {str(e)}")
    
    def save_configuration(self):
        """Guardar la configuración actual"""
        # Verificar si hay una configuración para guardar
        if not self.generator_model.current_computer:
            messagebox.showinfo("No Configuration", "No computer configuration to save.")
            return
        
        # Pedir nombre de archivo
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")]
        )
        
        if not file_path:
            return
        
        try:
            # Obtener datos de configuración del modelo
            config_data = self.generator_model.get_configuration_data()
            
            # Agregar metadatos
            config_data["metadata"] = {
                "date_saved": datetime.now().isoformat(),
                "app_version": "1.0.0"
            }
            
            # Guardar a archivo JSON
            with open(file_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            messagebox.showinfo("Configuration Saved", f"Configuration saved to {os.path.basename(file_path)}")
            self.logger.info(f"Configuración guardada en {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error al guardar configuración: {str(e)}", exc_info=True)
            messagebox.showerror("Error", f"Error saving configuration: {str(e)}")