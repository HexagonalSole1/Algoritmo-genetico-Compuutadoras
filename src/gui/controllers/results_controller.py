"""
Pestaña de resultados para mostrar detalles de la configuración generada.
"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter.scrolledtext import ScrolledText
import logging


class ResultsTab:
    """Pestaña para mostrar resultados detallados"""
    
    def __init__(self, parent, controller):
        """
        Inicializar pestaña de resultados.
        
        Args:
            parent: Widget padre (notebook)
            controller: Controlador de resultados
        """
        self.parent = parent
        self.controller = controller
        self.logger = logging.getLogger("ComputerGenerator.ResultsTab")
        
        # Crear frame principal
        self.frame = ttk.Frame(parent)
        
        # Configurar grid
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=3)
        self.frame.grid_rowconfigure(0, weight=1)
        
        # Crear paneles izquierdo y derecho
        self.create_left_pane()
        self.create_right_pane()
        
        # Registrar como observador del modelo
        self.controller.generator_model.add_observer(self)
        
        self.logger.info("Pestaña de resultados inicializada")
    
    def create_left_pane(self):
        """Crear panel izquierdo con lista de componentes"""
        left_pane = ttk.Frame(self.frame)
        left_pane.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Título
        ttk.Label(left_pane, text="Components", font=("TkDefaultFont", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Árbol de componentes
        columns = ('component', 'details', 'price')
        self.components_tree = ttk.Treeview(left_pane, columns=columns, show='headings', height=20)
        
        # Definir encabezados y columnas
        self.components_tree.heading('component', text='Component')
        self.components_tree.heading('details', text='Details')
        self.components_tree.heading('price', text='Price')
        
        self.components_tree.column('component', width=120, anchor='w')
        self.components_tree.column('details', width=300, anchor='w')
        self.components_tree.column('price', width=80, anchor='e')
        
        # Agregar barra de desplazamiento
        scrollbar = ttk.Scrollbar(left_pane, orient=tk.VERTICAL, command=self.components_tree.yview)
        self.components_tree.configure(yscroll=scrollbar.set)
        
        # Empaquetar componentes
        self.components_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=5)
        
        # Vincular evento de selección
        self.components_tree.bind('<<TreeviewSelect>>', self.on_component_selected)
    
    def create_right_pane(self):
        """Crear panel derecho con detalles de componente"""
        right_pane = ttk.Frame(self.frame)
        right_pane.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Frame de detalles
        self.details_frame = ttk.LabelFrame(right_pane, text="Component Details")
        self.details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Imagen de componente (placeholder)
        self.component_image_label = tk.Label(self.details_frame, text="[Component Image]",
                                           borderwidth=2, relief="solid", width=30, height=10)
        self.component_image_label.pack(padx=20, pady=20)
        
        # Texto de detalles del componente
        self.component_details_text = ScrolledText(self.details_frame, wrap=tk.WORD, height=15, width=50)
        self.component_details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.component_details_text.insert(tk.END, "Select a component to view details...")
        self.component_details_text.config(state=tk.DISABLED)
        
        # Frame de botones
        buttons_frame = ttk.Frame(right_pane)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Botón de reemplazar componente
        replace_button = ctk.CTkButton(buttons_frame, text="Replace Component", 
                                    command=self.show_replace_component)
        replace_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botón de ver alternativas
        alternatives_button = ctk.CTkButton(buttons_frame, text="View Alternatives", 
                                        command=self.show_alternatives)
        alternatives_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botón de agregar a comparación
        add_to_comparison_button = ctk.CTkButton(buttons_frame, text="Add to Comparison", 
                                             command=self.add_to_comparison)
        add_to_comparison_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botón de guardar configuración
        save_button = ctk.CTkButton(buttons_frame, text="Save Configuration", 
                                 command=self.save_configuration)
        save_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Frame de resumen de rendimiento
        performance_frame = ttk.LabelFrame(right_pane, text="Performance Summary")
        performance_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Grid para métricas de rendimiento
        for i in range(4):
            performance_frame.grid_columnconfigure(i, weight=1)
        
        # Métricas de rendimiento
        metrics = ["Gaming", "Productivity", "Content Creation", "Development"]
        self.performance_vars = {}
        
        for i, metric in enumerate(metrics):
            ttk.Label(performance_frame, text=metric).grid(row=0, column=i, padx=5, pady=5)
            self.performance_vars[metric.lower()] = tk.DoubleVar(value=0)
            
            performance_bar = ttk.Progressbar(performance_frame, orient="horizontal", 
                                          length=100, mode="determinate", 
                                          variable=self.performance_vars[metric.lower()])
            performance_bar.grid(row=1, column=i, padx=5, pady=5, sticky="ew")
            
            score_label = ttk.Label(performance_frame, text="0/100")
            score_label.grid(row=2, column=i, padx=5, pady=5)
            self.performance_vars[f"{metric.lower()}_label"] = score_label
    
    def on_component_selected(self, event):
        """
        Manejar selección de componente en el árbol.
        
        Args:
            event: Evento de selección
        """
        selection = self.components_tree.selection()
        if not selection:
            return
            
        # Obtener ítem seleccionado
        item = self.components_tree.item(selection[0])
        component_type = item['values'][0]
        
        # Actualizar detalles del componente
        self.controller.show_component_details(component_type)
    
    def show_component_details(self, component_type, details_text):
        """
        Mostrar detalles de un componente.
        
        Args:
            component_type: Tipo de componente
            details_text: Texto de detalles a mostrar
        """
        # Habilitar edición del texto de detalles
        self.component_details_text.config(state=tk.NORMAL)
        
        # Limpiar texto existente
        self.component_details_text.delete(1.0, tk.END)
        
        # Insertar detalles
        self.component_details_text.insert(tk.END, details_text)
        
        # Configurar etiquetas para estilos
        self.component_details_text.tag_configure("title", font=("TkDefaultFont", 12, "bold"))
        self.component_details_text.tag_configure("heading", font=("TkDefaultFont", 10, "bold"))
        
        # Deshabilitar edición
        self.component_details_text.config(state=tk.DISABLED)
    
    def show_replace_component(self):
        """Mostrar diálogo para reemplazar componente"""
        # Verificar si hay una selección
        selection = self.components_tree.selection()
        if not selection:
            self.controller.show_info("No Selection", "Please select a component to replace.")
            return
            
        # Obtener ítem seleccionado
        item = self.components_tree.item(selection[0])
        component_type = item['values'][0]
        
        # Delegar al controlador
        self.controller.show_replace_component(component_type)
    
    def show_alternatives(self):
        """Mostrar alternativas para el componente seleccionado"""
        # Verificar si hay una selección
        selection = self.components_tree.selection()
        if not selection:
            self.controller.show_info("No Selection", "Please select a component to view alternatives.")
            return
            
        # Obtener ítem seleccionado
        item = self.components_tree.item(selection[0])
        component_type = item['values'][0]
        
        # Delegar al controlador
        self.controller.show_alternatives(component_type)
    
    def add_to_comparison(self):
        """Agregar configuración actual a comparación"""
        # Delegar al controlador
        self.controller.add_to_comparison()
    
    def save_configuration(self):
        """Guardar configuración actual"""
        # Delegar al controlador
        self.controller.save_configuration()
    
    def update_components_tree(self, computer):
        """
        Actualizar el árbol de componentes con la computadora actual.
        
        Args:
            computer: Computadora a mostrar
        """
        # Limpiar ítems existentes
        for item in self.components_tree.get_children():
            self.components_tree.delete(item)
        
        if not computer:
            self.logger.warning("No hay computadora para mostrar")
            return
        
        # Agregar componentes al árbol
        self.components_tree.insert('', 'end', values=('CPU', str(computer.cpu), f"${computer.cpu.price:.2f}"))
        
        if computer.gpu:
            self.components_tree.insert('', 'end', values=('GPU', str(computer.gpu), f"${computer.gpu.price:.2f}"))
        else:
            self.components_tree.insert('', 'end', values=('GPU', 'None (Using Integrated Graphics)', '$0.00'))
        
        self.components_tree.insert('', 'end', values=('RAM', str(computer.ram), f"${computer.ram.price:.2f}"))
        self.components_tree.insert('', 'end', values=('Storage', str(computer.storage), f"${computer.storage.price:.2f}"))
        
        # Agregar almacenamientos adicionales si hay
        for i, storage in enumerate(computer.additional_storages):
            self.components_tree.insert('', 'end', values=(f'Storage {i+2}', str(storage), f"${storage.price:.2f}"))
        
        self.components_tree.insert('', 'end', values=('Motherboard', str(computer.motherboard), f"${computer.motherboard.price:.2f}"))
        self.components_tree.insert('', 'end', values=('PSU', str(computer.psu), f"${computer.psu.price:.2f}"))
        self.components_tree.insert('', 'end', values=('Cooling', str(computer.cooling), f"${computer.cooling.price:.2f}"))
        self.components_tree.insert('', 'end', values=('Case', str(computer.case), f"${computer.case.price:.2f}"))
        
        # Agregar precio total
        self.components_tree.insert('', 'end', values=('Total', '', f"${computer.price:.2f}"))
    
    def update_performance_display(self, computer):
        """
        Actualizar barras de rendimiento.
        
        Args:
            computer: Computadora a mostrar
        """
        if not computer:
            self.logger.warning("No hay computadora para actualizar rendimiento")
            return
        
        # Obtener métricas de rendimiento
        performance = computer.estimated_performance
        
        # Actualizar barras de progreso y etiquetas
        for metric in ['gaming', 'productivity', 'content_creation', 'development']:
            if metric in performance and metric in self.performance_vars:
                # Actualizar barra de progreso
                self.performance_vars[metric].set(performance[metric])
                
                # Actualizar etiqueta
                if f"{metric}_label" in self.performance_vars:
                    self.performance_vars[f"{metric}_label"].config(text=f"{performance[metric]:.1f}/100")
            else:
                # Métrica no disponible, establecer a 0
                if metric in self.performance_vars:
                    self.performance_vars[metric].set(0)
                    
                if f"{metric}_label" in self.performance_vars:
                    self.performance_vars[f"{metric}_label"].config(text="N/A")
    
    def clear_results(self):
        """Limpiar resultados mostrados"""
        # Limpiar árbol de componentes
        for item in self.components_tree.get_children():
            self.components_tree.delete(item)
        
        # Limpiar detalles
        self.component_details_text.config(state=tk.NORMAL)
        self.component_details_text.delete(1.0, tk.END)
        self.component_details_text.insert(tk.END, "Select a component to view details...")
        self.component_details_text.config(state=tk.DISABLED)
        
        # Limpiar métricas de rendimiento
        for metric in ['gaming', 'productivity', 'content_creation', 'development']:
            if metric in self.performance_vars:
                self.performance_vars[metric].set(0)
                
            if f"{metric}_label" in self.performance_vars:
                self.performance_vars[f"{metric}_label"].config(text="0/100")
    
    def on_generation_complete(self, results_text):
        """
        Método llamado cuando se completa la generación.
        Implementado para el patrón Observer.
        
        Args:
            results_text: Texto de resultados
        """
        computer = self.controller.generator_model.get_current_computer()
        self.update_components_tree(computer)
        self.update_performance_display(computer)
    
    def on_select(self):
        """Método llamado cuando se selecciona esta pestaña"""
        # Actualizar interfaz si es necesario
        computer = self.controller.generator_model.get_current_computer()
        if computer:
            self.update_components_tree(computer)
            self.update_performance_display(computer)