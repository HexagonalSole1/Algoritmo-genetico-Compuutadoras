"""
Ventana principal de la aplicación que coordina todas las vistas.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import logging

from gui.views.tabs.generator_tab import GeneratorTab
from gui.views.tabs.results_tab import ResultsTab
from gui.views.tabs.comparison_tab import ComparisonTab
from gui.views.tabs.visualization_tab import VisualizationTab
from gui.views.tabs.browser_tab import BrowserTab

from gui.controllers.generator_controller import GeneratorController
from gui.controllers.results_controller import ResultsController
from gui.controllers.comparison_controller import ComparisonController
from gui.controllers.visualization_controller import VisualizationController
from gui.controllers.browser_controller import BrowserController

from gui.models.settings_model import SettingsModel
from gui.models.generator_model import GeneratorModel
from gui.models.component_model import ComponentModel

from gui.views.dialogs.preferences_dialog import PreferencesDialog
from gui.views.dialogs.about_dialog import AboutDialog


class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self, master, data_manager, theme_manager):
        """
        Inicializar la ventana principal.
        
        Args:
            master: Widget maestro (ventana principal)
            data_manager: Gestor de datos de componentes
            theme_manager: Gestor de temas
        """
        self.master = master
        self.data_manager = data_manager
        self.theme_manager = theme_manager
        self.logger = logging.getLogger("ComputerGenerator.MainWindow")
        
        # Inicializar modelos
        self.settings_model = SettingsModel()
        self.generator_model = GeneratorModel(self.data_manager)
        self.component_model = ComponentModel(self.data_manager)
        
        # Configurar grid layout
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        
        # Crear menú
        self.create_menu()
        
        # Crear notebook para pestañas
        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Inicializar controladores
        self.generator_controller = GeneratorController(self.generator_model, self.component_model)
        self.results_controller = ResultsController(self.generator_model, self.component_model)
        self.comparison_controller = ComparisonController(self.generator_model)
        self.visualization_controller = VisualizationController(self.generator_model)
        self.browser_controller = BrowserController(self.component_model)
        
        # Inicializar pestañas
        self.generator_tab = GeneratorTab(self.notebook, self.generator_controller)
        self.results_tab = ResultsTab(self.notebook, self.results_controller)
        self.comparison_tab = ComparisonTab(self.notebook, self.comparison_controller)
        self.visualization_tab = VisualizationTab(self.notebook, self.visualization_controller)
        self.browser_tab = BrowserTab(self.notebook, self.browser_controller)
        
        # Agregar pestañas al notebook
        self.notebook.add(self.generator_tab.frame, text=" Generator ")
        self.notebook.add(self.results_tab.frame, text=" Results ")
        self.notebook.add(self.comparison_tab.frame, text=" Comparison ")
        self.notebook.add(self.visualization_tab.frame, text=" Visualization ")
        self.notebook.add(self.browser_tab.frame, text=" Component Browser ")
        
        # Crear barra de estado
        self.status_bar = ttk.Label(self.master, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky="ew")
        
        # Vincular evento de cambio de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        # Cargar configuración inicial
        self.load_settings()
        
        self.logger.info("Ventana principal inicializada")
        
    def create_menu(self):
        """Crear el menú de la aplicación"""
        menubar = tk.Menu(self.master)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Configuration", command=self.new_configuration)
        file_menu.add_command(label="Open Configuration", command=self.open_configuration)
        file_menu.add_command(label="Save Configuration", command=self.save_configuration)
        file_menu.add_separator()
        file_menu.add_command(label="Export Results", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Menú Editar
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Preferences", command=self.show_preferences)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Menú Ver
        view_menu = tk.Menu(menubar, tearoff=0)
        
        # Submenú Tema
        theme_menu = tk.Menu(view_menu, tearoff=0)
        theme_menu.add_command(label="Light Mode", command=lambda: self.change_theme("Light"))
        theme_menu.add_command(label="Dark Mode", command=lambda: self.change_theme("Dark"))
        theme_menu.add_command(label="System Default", command=lambda: self.change_theme("System"))
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # Establecer el menú
        self.master.config(menu=menubar)
        
    def on_tab_change(self, event):
        """
        Manejar el evento de cambio de pestaña.
        
        Args:
            event: Evento de cambio de pestaña
        """
        # Obtener índice de pestaña seleccionada
        tab_id = self.notebook.select()
        tab_name = self.notebook.tab(tab_id, "text").strip()
        
        # Actualizar barra de estado
        self.status_bar.config(text=f"Current view: {tab_name}")
        
        # Actualizar interfaz según pestaña seleccionada
        if tab_name == "Generator":
            self.generator_tab.on_select()
        elif tab_name == "Results":
            self.results_tab.on_select()
        elif tab_name == "Comparison":
            self.comparison_tab.on_select()
        elif tab_name == "Visualization":
            self.visualization_tab.on_select()
        elif tab_name == "Component Browser":
            self.browser_tab.on_select()
    
    def load_settings(self):
        """Cargar configuraciones de la aplicación"""
        # Cargar configuraciones desde el modelo
        settings = self.settings_model.get_settings()
        
        # Aplicar tema
        theme = settings.get("theme", "System")
        self.theme_manager.apply_theme(theme)
        
        self.logger.info(f"Configuraciones cargadas: Tema={theme}")
    
    def save_settings(self):
        """Guardar configuraciones de la aplicación"""
        # Obtener configuraciones actuales
        settings = {
            "theme": self.theme_manager.current_theme,
            "window_size": f"{self.master.winfo_width()}x{self.master.winfo_height()}"
        }
        
        # Guardar configuraciones en el modelo
        self.settings_model.save_settings(settings)
        
        self.logger.info("Configuraciones guardadas")
    
    def new_configuration(self):
        """Iniciar una nueva configuración"""
        # Confirmar si hay una configuración existente
        if self.generator_model.current_computer:
            confirm = messagebox.askyesno("Confirmar nueva configuración", 
                                      "Esto borrará la configuración actual. ¿Continuar?")
            if not confirm:
                return
        
        # Reiniciar el modelo y actualizar la interfaz
        self.generator_model.reset()
        self.generator_tab.reset_form()
        self.results_tab.clear_results()
        self.visualization_tab.clear_visualization()
        
        # Actualizar estado
        self.status_bar.config(text="Nueva configuración iniciada")
        self.logger.info("Nueva configuración iniciada")
    
    def open_configuration(self):
        """Abrir una configuración guardada"""
        # Delegar al controlador del generador
        self.generator_controller.open_configuration()
        
    def save_configuration(self):
        """Guardar la configuración actual"""
        # Delegar al controlador del generador
        self.generator_controller.save_configuration()
    
    def export_results(self):
        """Exportar los resultados actuales"""
        # Delegar al controlador de resultados
        self.results_controller.export_results()
    
    def change_theme(self, theme):
        """
        Cambiar el tema de la aplicación.
        
        Args:
            theme: Nombre del tema a aplicar
        """
        # Aplicar tema
        self.theme_manager.apply_theme(theme)
        
        # Actualizar configuraciones
        self.settings_model.update_setting("theme", theme)
        
        # Actualizar estado
        self.status_bar.config(text=f"Tema cambiado a {theme}")
        self.logger.info(f"Tema cambiado a {theme}")
    
    def show_preferences(self):
        """Mostrar diálogo de preferencias"""
        PreferencesDialog(self.master, self.settings_model, self.theme_manager)
    
    def show_documentation(self):
        """Mostrar documentación"""
        messagebox.showinfo("Documentación", 
                         "Esto abriría la documentación de la aplicación.\n\n"
                         "En una implementación completa, esto abriría una ventana de ayuda "
                         "o dirigiría al usuario a la documentación en línea.")
    
    def show_about(self):
        """Mostrar diálogo de acerca de"""
        AboutDialog(self.master)