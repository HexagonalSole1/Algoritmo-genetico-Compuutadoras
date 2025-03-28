"""
Diálogo de preferencias de la aplicación.
"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import logging


class PreferencesDialog:
    """Diálogo para configurar preferencias de la aplicación"""
    
    def __init__(self, parent, settings_model, theme_manager):
        """
        Inicializar diálogo de preferencias.
        
        Args:
            parent: Widget padre
            settings_model: Modelo de configuraciones
            theme_manager: Gestor de temas
        """
        self.parent = parent
        self.settings_model = settings_model
        self.theme_manager = theme_manager
        self.logger = logging.getLogger("ComputerGenerator.PreferencesDialog")
        
        # Variables para almacenar cambios
        self.changed_settings = {}
        
        # Crear diálogo
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Preferences")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Crear notebook para categorías de preferencias
        self.create_notebook()
        
        # Cargar configuraciones actuales
        self.load_current_settings()
        
        # Configurar cierre del diálogo
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
        
        self.logger.debug("Diálogo de preferencias inicializado")
    
    def create_notebook(self):
        """Crear notebook para categorías de preferencias"""
        self.preferences_notebook = ttk.Notebook(self.dialog)
        self.preferences_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear pestañas
        self.create_general_tab()
        self.create_algorithm_tab()
        self.create_data_tab()
        
        # Crear frame de botones
        self.create_buttons_frame()
    
    def create_general_tab(self):
        """Crear pestaña de preferencias generales"""
        general_frame = ttk.Frame(self.preferences_notebook)
        self.preferences_notebook.add(general_frame, text="General")
        
        # Variables
        self.theme_var = tk.StringVar()
        self.save_window_size_var = tk.BooleanVar()
        self.reset_defaults_var = tk.BooleanVar()
        self.language_var = tk.StringVar()
        
        # Opción de tema
        ttk.Label(general_frame, text="Theme:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        theme_combo = ttk.Combobox(general_frame, textvariable=self.theme_var, 
                                values=["Light", "Dark", "System"], 
                                width=15, state="readonly")
        theme_combo.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        # Opción de guardar tamaño de ventana
        ttk.Label(general_frame, text="Remember window size:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        save_size_check = ttk.Checkbutton(general_frame, variable=self.save_window_size_var)
        save_size_check.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        
        # Opción de reiniciar a valores predeterminados
        ttk.Label(general_frame, text="Reset to defaults on startup:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        reset_defaults_check = ttk.Checkbutton(general_frame, variable=self.reset_defaults_var)
        reset_defaults_check.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        
        # Opción de idioma
        ttk.Label(general_frame, text="Language:").grid(row=3, column=0, sticky="w", padx=10, pady=10)
        language_combo = ttk.Combobox(general_frame, textvariable=self.language_var, 
                                   values=["English", "Spanish", "French", "German"], 
                                   width=15, state="readonly")
        language_combo.grid(row=3, column=1, sticky="w", padx=10, pady=10)
    
    def create_algorithm_tab(self):
        """Crear pestaña de preferencias de algoritmo"""
        algorithm_frame = ttk.Frame(self.preferences_notebook)
        self.preferences_notebook.add(algorithm_frame, text="Algorithm")
        
        # Variables
        self.default_pop_var = tk.StringVar()
        self.default_gen_var = tk.StringVar()
        self.default_mutation_var = tk.StringVar()
        self.default_crossover_var = tk.StringVar()
        self.adaptive_mutation_var = tk.BooleanVar()
        self.autosave_var = tk.BooleanVar()
        
        # Tamaño de población predeterminado
        ttk.Label(algorithm_frame, text="Default Population Size:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        default_pop_entry = ttk.Entry(algorithm_frame, textvariable=self.default_pop_var, width=10)
        default_pop_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        # Generaciones predeterminadas
        ttk.Label(algorithm_frame, text="Default Generations:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        default_gen_entry = ttk.Entry(algorithm_frame, textvariable=self.default_gen_var, width=10)
        default_gen_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        
        # Tasa de mutación predeterminada
        ttk.Label(algorithm_frame, text="Default Mutation Rate:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        default_mutation_entry = ttk.Entry(algorithm_frame, textvariable=self.default_mutation_var, width=10)
        default_mutation_entry.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        
        # Tasa de cruce predeterminada
        ttk.Label(algorithm_frame, text="Default Crossover Rate:").grid(row=3, column=0, sticky="w", padx=10, pady=10)
        default_crossover_entry = ttk.Entry(algorithm_frame, textvariable=self.default_crossover_var, width=10)
        default_crossover_entry.grid(row=3, column=1, sticky="w", padx=10, pady=10)
        
        # Usar mutación adaptativa
        ttk.Label(algorithm_frame, text="Use Adaptive Mutation:").grid(row=4, column=0, sticky="w", padx=10, pady=10)
        adaptive_mutation_check = ttk.Checkbutton(algorithm_frame, variable=self.adaptive_mutation_var)
        adaptive_mutation_check.grid(row=4, column=1, sticky="w", padx=10, pady=10)
        
        # Autoguardar resultados
        ttk.Label(algorithm_frame, text="Auto-save results:").grid(row=5, column=0, sticky="w", padx=10, pady=10)
        autosave_check = ttk.Checkbutton(algorithm_frame, variable=self.autosave_var)
        autosave_check.grid(row=5, column=1, sticky="w", padx=10, pady=10)
    
    def create_data_tab(self):
        """Crear pestaña de preferencias de datos"""
        data_frame = ttk.Frame(self.preferences_notebook)
        self.preferences_notebook.add(data_frame, text="Data")
        
        # Variables
        self.auto_update_var = tk.BooleanVar()
        self.update_freq_var = tk.StringVar()
        self.data_source_var = tk.StringVar()
        
        # Actualizar datos automáticamente
        ttk.Label(data_frame, text="Auto-update component data:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        auto_update_check = ttk.Checkbutton(data_frame, variable=self.auto_update_var)
        auto_update_check.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        # Frecuencia de actualización
        ttk.Label(data_frame, text="Update frequency:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        update_freq_combo = ttk.Combobox(data_frame, textvariable=self.update_freq_var, 
                                      values=["1", "7", "14", "30"], 
                                      width=10, state="readonly")
        update_freq_combo.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        ttk.Label(data_frame, text="days").grid(row=1, column=2, sticky="w")
        
        # Fuente de datos personalizada
        ttk.Label(data_frame, text="Custom data source:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        data_source_entry = ttk.Entry(data_frame, textvariable=self.data_source_var, width=30)
        data_source_entry.grid(row=2, column=1, columnspan=2, sticky="w", padx=10, pady=10)
        
        # Botón de examinar
        browse_button = ctk.CTkButton(data_frame, text="Browse", 
                                   command=self.browse_data_source,
                                   width=20)
        browse_button.grid(row=2, column=3, padx=5, pady=10)
        
        # Botón de comprobar actualizaciones
        check_updates_button = ctk.CTkButton(data_frame, text="Check for Updates Now", 
                                         command=self.check_for_updates)
        check_updates_button.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=10)
    
    def create_buttons_frame(self):
        """Crear frame de botones"""
        buttons_frame = ttk.Frame(self.dialog)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Botón de guardar
        save_button = ctk.CTkButton(buttons_frame, text="Save", 
                                 command=self.save_preferences)
        save_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Botón de cancelar
        cancel_button = ctk.CTkButton(buttons_frame, text="Cancel", 
                                   command=self.dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Botón de reiniciar
        reset_button = ctk.CTkButton(buttons_frame, text="Reset to Default", 
                                  command=self.reset_to_default)
        reset_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def load_current_settings(self):
        """Cargar configuraciones actuales en la interfaz"""
        # Obtener configuraciones
        settings = self.settings_model.get_settings()
        
        # Cargar en variables de la interfaz
        self.theme_var.set(settings.get("theme", "System"))
        self.save_window_size_var.set(settings.get("save_window_size", True))
        self.reset_defaults_var.set(settings.get("reset_to_defaults", False))
        self.language_var.set(self._get_language_display(settings.get("language", "en")))
        
        self.default_pop_var.set(str(settings.get("default_population_size", 50)))
        self.default_gen_var.set(str(settings.get("default_generations", 100)))
        self.default_mutation_var.set(str(settings.get("default_mutation_rate", 0.1)))
        self.default_crossover_var.set(str(settings.get("default_crossover_rate", 0.8)))
        self.adaptive_mutation_var.set(settings.get("adaptive_mutation", True))
        self.autosave_var.set(settings.get("autosave_results", False))
        
        self.auto_update_var.set(settings.get("auto_update_data", False))
        self.update_freq_var.set(str(settings.get("update_interval_days", 7)))
        self.data_source_var.set(settings.get("custom_data_source", ""))
        
        self.logger.debug("Configuraciones actuales cargadas en el diálogo")
    
    def _get_language_display(self, language_code):
        """
        Convertir código de idioma a nombre para mostrar.
        
        Args:
            language_code: Código de idioma (en, es, fr, de)
            
        Returns:
            str: Nombre del idioma para mostrar
        """
        language_map = {
            "en": "English",
            "es": "Spanish",
            "fr": "French",
            "de": "German"
        }
        return language_map.get(language_code, "English")
    
    def _get_language_code(self, language_display):
        """
        Convertir nombre de idioma a código.
        
        Args:
            language_display: Nombre del idioma para mostrar
            
        Returns:
            str: Código de idioma (en, es, fr, de)
        """
        language_map = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de"
        }
        return language_map.get(language_display, "en")
    
    def browse_data_source(self):
        """Abrir diálogo para seleccionar fuente de datos"""
        directory = tk.filedialog.askdirectory()
        if directory:
            self.data_source_var.set(directory)
    
    def check_for_updates(self):
        """Comprobar actualizaciones de datos de componentes"""
        # Esta función simularía comprobar actualizaciones de datos
        tk.messagebox.showinfo("Update Check", 
                           "Checking for component updates...\n\n"
                           "This would check for updates from the data source.")
    
    def reset_to_default(self):
        """Reiniciar configuraciones a valores predeterminados"""
        # Confirmar reinicio
        confirm = tk.messagebox.askyesno("Confirm Reset", 
                                     "Are you sure you want to reset all preferences to default values?")
        if not confirm:
            return
        
        # Reiniciar configuraciones en el modelo
        if self.settings_model.reset_to_defaults():
            # Actualizar interfaz
            self.load_current_settings()
            tk.messagebox.showinfo("Reset Complete", "Preferences have been reset to default values.")
        else:
            tk.messagebox.showerror("Reset Failed", "Failed to reset preferences.")
    
    def save_preferences(self):
        """Guardar preferencias"""
        try:
            # Recopilar cambios
            settings = {
                "theme": self.theme_var.get(),
                "save_window_size": self.save_window_size_var.get(),
                "reset_to_defaults": self.reset_defaults_var.get(),
                "language": self._get_language_code(self.language_var.get()),
                
                "default_population_size": int(self.default_pop_var.get()),
                "default_generations": int(self.default_gen_var.get()),
                "default_mutation_rate": float(self.default_mutation_var.get()),
                "default_crossover_rate": float(self.default_crossover_var.get()),
                "adaptive_mutation": self.adaptive_mutation_var.get(),
                "autosave_results": self.autosave_var.get(),
                
                "auto_update_data": self.auto_update_var.get(),
                "update_interval_days": int(self.update_freq_var.get()),
                "custom_data_source": self.data_source_var.get()
            }
            
            # Guardar configuraciones
            self.settings_model.save_settings(settings)
            
            # Aplicar cambios que requieren acción inmediata
            if settings["theme"] != self.theme_manager.current_theme:
                self.theme_manager.apply_theme(settings["theme"])
            
            # Cerrar diálogo
            self.dialog.destroy()
            
            # Mostrar mensaje de éxito
            tk.messagebox.showinfo("Preferences Saved", "Preferences have been saved successfully.")
            
            self.logger.info("Preferencias guardadas correctamente")
            
        except ValueError as e:
            # Manejar errores de conversión
            tk.messagebox.showerror("Input Error", f"Invalid input value: {str(e)}")
            self.logger.error(f"Error al guardar preferencias: {str(e)}")
            
        except Exception as e:
            # Manejar otros errores
            tk.messagebox.showerror("Error", f"Error saving preferences: {str(e)}")
            self.logger.error(f"Error al guardar preferencias: {str(e)}", exc_info=True)
    
    def on_close(self):
        """Manejar cierre del diálogo"""
        # Simplemente destruir el diálogo
        self.dialog.destroy()