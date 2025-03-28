"""
Pestaña de comparación para el Generador de Computadoras.
"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
import numpy as np


class ComparisonTab:
    """Pestaña para comparar múltiples configuraciones de computadoras"""
    
    def __init__(self, parent, controller):
        """
        Inicializar pestaña de comparación.
        
        Args:
            parent: Widget padre (notebook)
            controller: Controlador de comparación
        """
        self.parent = parent
        self.controller = controller
        self.logger = logging.getLogger("ComputerGenerator.ComparisonTab")
        
        # Crear frame principal
        self.frame = ttk.Frame(parent)
        
        # Configurar grid
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        
        # Crear secciones
        self.create_controls_frame()
        self.create_comparison_area()
        
        # Registrar como observador del modelo
        self.controller.generator_model.add_observer(self)
        
        self.logger.info("Pestaña de comparación inicializada")
    
    def create_controls_frame(self):
        """Crear frame de controles superiores"""
        controls_frame = ttk.Frame(self.frame)
        controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ttk.Label(controls_frame, text="Compare Configurations", font=("TkDefaultFont", 14, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Botones de acción
        clear_button = ctk.CTkButton(controls_frame, text="Clear All", 
                                  command=self.clear_comparison)
        clear_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        export_button = ctk.CTkButton(controls_frame, text="Export Comparison", 
                                   command=self.export_comparison)
        export_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def create_comparison_area(self):
        """Crear área principal de comparación"""
        comparison_area = ttk.Frame(self.frame)
        comparison_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configurar canvas desplazable para comparación
        canvas = tk.Canvas(comparison_area, borderwidth=0)
        scrollbar = ttk.Scrollbar(comparison_area, orient=tk.VERTICAL, command=canvas.yview)
        self.comparison_container = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas_window = canvas.create_window((0, 0), window=self.comparison_container, anchor=tk.NW)
        
        # Configurar desplazamiento
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        self.comparison_container.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)
        
        # Agregar texto de marcador de posición
        ttk.Label(self.comparison_container, text="Add configurations to compare them side by side...").pack(padx=20, pady=20)
    
    def update_comparison_tab(self):
        """Actualizar la pestaña de comparación con todas las computadoras generadas"""
        # Limpiar contenido existente
        for widget in self.comparison_container.winfo_children():
            widget.destroy()
            
        # Obtener computadoras generadas
        generated_computers = self.controller.generator_model.get_generated_computers()
        
        # Si no hay computadoras para comparar, mostrar mensaje
        if not generated_computers:
            ttk.Label(self.comparison_container, text="Add configurations to compare them side by side...").pack(padx=20, pady=20)
            return
            
        # Crear tabla de comparación
        table_frame = ttk.Frame(self.comparison_container)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear encabezados
        ttk.Label(table_frame, text="Component", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Agregar nombres de computadoras como encabezados de columna
        for i, config in enumerate(generated_computers):
            ttk.Label(table_frame, text=config["name"], font=("TkDefaultFont", 10, "bold")).grid(row=0, column=i+1, sticky="w", padx=5, pady=5)
            
            # Botón de eliminar
            remove_button = ttk.Button(table_frame, text="X", width=2,
                                    command=lambda idx=i: self.remove_from_comparison(idx))
            remove_button.grid(row=0, column=i+1, sticky="e", padx=5, pady=5)
        
        # Agregar filas de componentes
        component_types = [
            "CPU", "GPU", "RAM", "Storage", "Motherboard", 
            "PSU", "Cooling", "Case", "Price", "Performance"
        ]
        
        for row, comp_type in enumerate(component_types):
            # Agregar encabezado de fila
            ttk.Label(table_frame, text=comp_type).grid(row=row+1, column=0, sticky="w", padx=5, pady=5)
            
            # Agregar detalles de componentes para cada configuración
            for col, config in enumerate(generated_computers):
                computer = config["computer"]
                
                # Obtener detalles de componente según el tipo
                if comp_type == "CPU":
                    value = str(computer.cpu)
                elif comp_type == "GPU":
                    value = str(computer.gpu) if computer.gpu else "Integrated Graphics"
                elif comp_type == "RAM":
                    value = str(computer.ram)
                elif comp_type == "Storage":
                    value = str(computer.storage)
                elif comp_type == "Motherboard":
                    value = str(computer.motherboard)
                elif comp_type == "PSU":
                    value = str(computer.psu)
                elif comp_type == "Cooling":
                    value = str(computer.cooling)
                elif comp_type == "Case":
                    value = str(computer.case)
                elif comp_type == "Price":
                    value = f"${computer.price:.2f}"
                elif comp_type == "Performance":
                    gaming = computer.estimated_performance.get('gaming', 0)
                    productivity = computer.estimated_performance.get('productivity', 0)
                    avg_perf = (gaming + productivity) / 2
                    value = f"Gaming: {gaming:.1f}, Productivity: {productivity:.1f}, Avg: {avg_perf:.1f}"
                
                # Agregar a tabla
                ttk.Label(table_frame, text=value, wraplength=200).grid(row=row+1, column=col+1, sticky="w", padx=5, pady=5)
        
        # Crear gráfico de comparación
        self.create_comparison_chart()
    
    def create_comparison_chart(self):
        """Crear un gráfico comparando el rendimiento de todas las configuraciones"""
        generated_computers = self.controller.generator_model.get_generated_computers()
        if not generated_computers:
            return
            
        # Crear frame para gráfico
        chart_frame = ttk.LabelFrame(self.comparison_container, text="Performance Comparison")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear figura para matplotlib
        figure = Figure(figsize=(10, 6), dpi=100)
        plot = figure.add_subplot(111)
        
        # Preparar datos
        config_names = []
        gaming_scores = []
        productivity_scores = []
        content_creation_scores = []
        development_scores = []
        
        for config in generated_computers:
            computer = config["computer"]
            config_names.append(config["name"])
            gaming_scores.append(computer.estimated_performance.get('gaming', 0))
            productivity_scores.append(computer.estimated_performance.get('productivity', 0))
            content_creation_scores.append(computer.estimated_performance.get('content_creation', 0))
            development_scores.append(computer.estimated_performance.get('development', 0))
        
        # Configurar posiciones para barras
        x = np.arange(len(config_names))
        width = 0.2
        
        # Crear barras
        plot.bar(x - 1.5*width, gaming_scores, width, label='Gaming')
        plot.bar(x - 0.5*width, productivity_scores, width, label='Productivity')
        plot.bar(x + 0.5*width, content_creation_scores, width, label='Content Creation')
        plot.bar(x + 1.5*width, development_scores, width, label='Development')
        
        # Agregar etiquetas y leyenda
        plot.set_xlabel('Configuration')
        plot.set_ylabel('Performance Score')
        plot.set_title('Performance Comparison')
        plot.set_xticks(x)
        plot.set_xticklabels(config_names, rotation=45, ha='right')
        plot.legend()
        plot.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Ajustar diseño
        figure.tight_layout()
        
        # Crear canvas para figura matplotlib
        canvas = FigureCanvasTkAgg(figure, chart_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def remove_from_comparison(self, index):
        """
        Eliminar una configuración de la comparación.
        
        Args:
            index: Índice de la configuración a eliminar
        """
        self.controller.remove_from_comparison(index)
        self.update_comparison_tab()
    
    def clear_comparison(self):
        """Limpiar todas las configuraciones de comparación"""
        self.controller.clear_comparison()
        self.update_comparison_tab()
    
    def export_comparison(self):
        """Exportar comparación a un archivo"""
        self.controller.export_comparison()
    
    def on_select(self):
        """Método llamado cuando se selecciona esta pestaña"""
        # Actualizar interfaz
        self.update_comparison_tab()