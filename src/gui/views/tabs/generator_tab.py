"""
Pestaña de generador de configuraciones de computadoras.
"""
import tkinter as tk
from tkinter import ttk, colorchooser
import customtkinter as ctk
from tkinter.scrolledtext import ScrolledText
import logging


class GeneratorTab:
    """Pestaña de generador de configuraciones"""
    
    def __init__(self, parent, controller):
        """
        Inicializar pestaña del generador.
        
        Args:
            parent: Widget padre (notebook)
            controller: Controlador del generador
        """
        self.parent = parent
        self.controller = controller
        self.logger = logging.getLogger("ComputerGenerator.GeneratorTab")
        
        # Crear frame principal
        self.frame = ttk.Frame(parent)
        
        # Configurar grid
        for i in range(12):
            self.frame.grid_columnconfigure(i, weight=1)
        self.frame.grid_rowconfigure(10, weight=1)  # Hacer que la fila inferior sea expandible
        
        # Inicializar variables
        self.initialize_variables()
        
        # Crear interfaz
        self.create_user_requirements_section()
        self.create_algorithm_parameters_section()
        self.create_component_preferences_section()
        self.create_actions_section()
        self.create_results_preview_section()
        
        self.logger.info("Pestaña de generador inicializada")
    
    def initialize_variables(self):
        """Inicializar variables de la interfaz"""
        # Variables de requisitos del usuario
        self.usage_var = tk.StringVar(value="gaming")
        self.computer_usages = {
            'gaming': 'Gaming',
            'office': 'Office Work',
            'graphics': 'Graphic Design',
            'video': 'Video Editing',
            'web': 'Web Browsing',
            'education': 'Education',
            'architecture': 'Architecture/CAD'
        }
        
        # Variables de rango de precio
        self.price_min_var = tk.StringVar(value="8000")
        self.price_max_var = tk.StringVar(value="15000")
        
        # Variables de prioridad
        self.priority_var = tk.StringVar(value="balanced")
        
        # Variables de factor de forma
        self.form_factor_var = tk.StringVar(value="ATX")
        
        # Variables de prueba de futuro
        self.future_proof_var = tk.BooleanVar(value=False)
        
        # Variables de parámetros del algoritmo
        self.population_size_var = tk.StringVar(value="50")
        self.generations_var = tk.StringVar(value="100")
        self.crossover_rate_var = tk.StringVar(value="0.8")
        self.mutation_rate_var = tk.StringVar(value="0.1")
        self.elitism_var = tk.StringVar(value="10")
        self.advanced_options_var = tk.BooleanVar(value=False)
        self.tournament_size_var = tk.StringVar(value="3")
        self.adaptive_mutation_var = tk.BooleanVar(value=True)
        
        # Variables de preferencias de marca
        self.brand_preferences = {}
        for comp_type in ["cpu", "gpu", "ram", "storage", "motherboard"]:
            self.brand_preferences[comp_type] = tk.StringVar(value="No Preference")
        
        # Variables de preferencias estéticas
        self.rgb_lighting_var = tk.BooleanVar(value=False)
        self.case_color_var = tk.StringVar(value="Black")
        self.custom_color = "#000000"  # Color personalizado predeterminado
        
        # Variables de progreso
        self.progress_var = tk.DoubleVar(value=0)
    
    def create_user_requirements_section(self):
        """Crear sección de requisitos del usuario"""
        # Crear frame para la sección
        requirements_frame = ctk.CTkFrame(self.frame)
        requirements_frame.grid(row=0, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
        
        # Título de la sección
        ttk.Label(requirements_frame, text="User Requirements", font=("TkDefaultFont", 14, "bold")).grid(
            row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Selección de uso
        ttk.Label(requirements_frame, text="Primary Usage:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # Frame para opciones de uso
        usage_frame = ttk.Frame(requirements_frame)
        usage_frame.grid(row=1, column=1, columnspan=3, sticky="w", padx=10, pady=5)
        
        # Crear radiobuttons para cada uso
        for i, (key, value) in enumerate(self.computer_usages.items()):
            col = i % 4
            row = i // 4 + 1
            ttk.Radiobutton(usage_frame, text=value, variable=self.usage_var, value=key, 
                           command=self.on_usage_changed).grid(row=row, column=col, sticky="w", padx=10, pady=2)
        
        # Rango de precio
        ttk.Label(requirements_frame, text="Price Range:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        price_frame = ttk.Frame(requirements_frame)
        price_frame.grid(row=3, column=1, columnspan=3, sticky="w", padx=10, pady=5)
        
        ttk.Label(price_frame, text="Min:").grid(row=0, column=0, sticky="w")
        self.price_min_entry = ttk.Entry(price_frame, textvariable=self.price_min_var, width=10)
        self.price_min_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(price_frame, text="Max:").grid(row=0, column=2, sticky="w")
        self.price_max_entry = ttk.Entry(price_frame, textvariable=self.price_max_var, width=10)
        self.price_max_entry.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
        # Slider de rango de precio
        self.price_range_slider = ctk.CTkSlider(requirements_frame, from_=0, to=50000,
                                              number_of_steps=50, width=400)
        self.price_range_slider.grid(row=3, column=4, columnspan=4, sticky="ew", padx=10, pady=5)
        self.price_range_slider.set(15000)  # Valor predeterminado
        
        # Selección de prioridad
        ttk.Label(requirements_frame, text="Priority:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        priority_frame = ttk.Frame(requirements_frame)
        priority_frame.grid(row=4, column=1, columnspan=3, sticky="w", padx=10, pady=5)
        
        ttk.Radiobutton(priority_frame, text="Performance", variable=self.priority_var, value="performance").grid(
            row=0, column=0, sticky="w", padx=10)
        ttk.Radiobutton(priority_frame, text="Value", variable=self.priority_var, value="value").grid(
            row=0, column=1, sticky="w", padx=10)
        ttk.Radiobutton(priority_frame, text="Balanced", variable=self.priority_var, value="balanced").grid(
            row=0, column=2, sticky="w", padx=10)
        
        # Factor de forma
        ttk.Label(requirements_frame, text="Form Factor:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        form_factor_frame = ttk.Frame(requirements_frame)
        form_factor_frame.grid(row=5, column=1, columnspan=3, sticky="w", padx=10, pady=5)
        
        ttk.Radiobutton(form_factor_frame, text="ATX", variable=self.form_factor_var, value="ATX").grid(
            row=0, column=0, sticky="w", padx=10)
        ttk.Radiobutton(form_factor_frame, text="Micro-ATX", variable=self.form_factor_var, value="Micro-ATX").grid(
            row=0, column=1, sticky="w", padx=10)
        ttk.Radiobutton(form_factor_frame, text="Mini-ITX", variable=self.form_factor_var, value="Mini-ITX").grid(
            row=0, column=2, sticky="w", padx=10)
        
        # Prueba de futuro
        future_proof_check = ttk.Checkbutton(requirements_frame, text="Prioritize Future-Proofing", 
                                          variable=self.future_proof_var)
        future_proof_check.grid(row=5, column=4, sticky="w", padx=10, pady=5)
    
    def create_algorithm_parameters_section(self):
        """Crear sección de parámetros del algoritmo"""
        # Crear frame para la sección
        algo_frame = ctk.CTkFrame(self.frame)
        algo_frame.grid(row=1, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
        
        # Título de la sección
        ttk.Label(algo_frame, text="Algorithm Parameters", font=("TkDefaultFont", 14, "bold")).grid(
            row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Tamaño de población
        ttk.Label(algo_frame, text="Population Size:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        population_size_entry = ttk.Entry(algo_frame, textvariable=self.population_size_var, width=10)
        population_size_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Generaciones
        ttk.Label(algo_frame, text="Generations:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        generations_entry = ttk.Entry(algo_frame, textvariable=self.generations_var, width=10)
        generations_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        # Tasa de cruce
        ttk.Label(algo_frame, text="Crossover Rate:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        crossover_rate_entry = ttk.Entry(algo_frame, textvariable=self.crossover_rate_var, width=10)
        crossover_rate_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Tasa de mutación
        ttk.Label(algo_frame, text="Mutation Rate:").grid(row=2, column=2, sticky="w", padx=10, pady=5)
        mutation_rate_entry = ttk.Entry(algo_frame, textvariable=self.mutation_rate_var, width=10)
        mutation_rate_entry.grid(row=2, column=3, sticky="w", padx=5, pady=5)
        
        # Elitismo
        ttk.Label(algo_frame, text="Elitism %:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        elitism_entry = ttk.Entry(algo_frame, textvariable=self.elitism_var, width=10)
        elitism_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Opciones avanzadas
        advanced_options_check = ttk.Checkbutton(algo_frame, text="Show Advanced Options", 
                                              variable=self.advanced_options_var,
                                              command=self.toggle_advanced_options)
        advanced_options_check.grid(row=3, column=2, columnspan=2, sticky="w", padx=10, pady=5)
        
        # Frame de opciones avanzadas
        self.advanced_frame = ttk.Frame(algo_frame)
        self.advanced_frame.grid(row=4, column=0, columnspan=6, sticky="ew", padx=10, pady=5)
        self.advanced_frame.grid_remove()  # Ocultar inicialmente
        
        # Tamaño de torneo
        ttk.Label(self.advanced_frame, text="Tournament Size:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tournament_size_entry = ttk.Entry(self.advanced_frame, textvariable=self.tournament_size_var, width=10)
        tournament_size_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        # Mutación adaptativa
        adaptive_mutation_check = ttk.Checkbutton(self.advanced_frame, text="Adaptive Mutation", 
                                               variable=self.adaptive_mutation_var)
        adaptive_mutation_check.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        
        # Botón de pesos de fitness
        fitness_weights_button = ctk.CTkButton(self.advanced_frame, text="Fitness Weights", 
                                             command=self.show_fitness_weights)
        fitness_weights_button.grid(row=0, column=3, sticky="w", padx=10, pady=5)
    
    def create_component_preferences_section(self):
        """Crear sección de preferencias de componentes"""
        # Crear frame para la sección
        components_frame = ctk.CTkFrame(self.frame)
        components_frame.grid(row=2, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
        
        # Título de la sección
        ttk.Label(components_frame, text="Component Preferences", font=("TkDefaultFont", 14, "bold")).grid(
            row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Preferencias de marca
        ttk.Label(components_frame, text="Brand Preferences:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # Frame para preferencias de marca
        brands_frame = ttk.Frame(components_frame)
        brands_frame.grid(row=1, column=1, columnspan=5, sticky="w", padx=10, pady=5)
        
        # Etiquetas de tipo de componente
        component_types = ["CPU", "GPU", "Motherboard", "RAM", "Storage"]
        for i, comp_type in enumerate(component_types):
            ttk.Label(brands_frame, text=comp_type + ":").grid(row=0, column=i, sticky="w", padx=5, pady=2)
        
        # Listas desplegables de preferencia de marca
        for i, comp_type in enumerate(component_types):
            brands = ["No Preference", "Intel", "AMD"] if comp_type == "CPU" else ["No Preference", "ASUS", "MSI", "Gigabyte", "EVGA"]
            brand_dropdown = ttk.Combobox(brands_frame, textvariable=self.brand_preferences[comp_type.lower()], values=brands, width=12)
            brand_dropdown.grid(row=1, column=i, sticky="w", padx=5, pady=2)
        
        # Botón de incluir/excluir componentes
        include_exclude_button = ctk.CTkButton(components_frame, text="Include/Exclude Components", 
                                            command=self.show_include_exclude)
        include_exclude_button.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        # Preferencias estéticas
        ttk.Label(components_frame, text="Aesthetics:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        
        # Frame para estética
        aesthetics_frame = ttk.Frame(components_frame)
        aesthetics_frame.grid(row=3, column=1, columnspan=5, sticky="w", padx=10, pady=5)
        
        # Preferencia de iluminación RGB
        rgb_check = ttk.Checkbutton(aesthetics_frame, text="RGB Lighting", variable=self.rgb_lighting_var)
        rgb_check.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        
        # Preferencia de color de caja
        ttk.Label(aesthetics_frame, text="Color:").grid(row=0, column=1, sticky="w", padx=10, pady=2)
        case_colors = ["Black", "White", "Red", "Blue", "Green", "Custom"]
        case_color_dropdown = ttk.Combobox(aesthetics_frame, textvariable=self.case_color_var, values=case_colors, width=10)
        case_color_dropdown.grid(row=0, column=2, sticky="w", padx=5, pady=2)
        
        # Botón de color personalizado
        color_button = ctk.CTkButton(aesthetics_frame, text="Choose Color", command=self.choose_custom_color, width=20)
        color_button.grid(row=0, column=3, sticky="w", padx=5, pady=2)
    
    def create_actions_section(self):
        """Crear sección de acciones"""
        # Crear frame para la sección
        actions_frame = ctk.CTkFrame(self.frame)
        actions_frame.grid(row=3, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
        
        # Botón de generación
        self.generate_button = ctk.CTkButton(actions_frame, text="Generate Computer", 
                                         command=self.generate_computer,
                                         height=40, width=200,
                                         font=("TkDefaultFont", 14))
        self.generate_button.grid(row=0, column=0, padx=10, pady=10)
        
        # Botón de detención
        self.stop_button = ctk.CTkButton(actions_frame, text="Stop", 
                                     command=self.stop_generation,
                                     height=40, width=100,
                                     state="disabled",
                                     font=("TkDefaultFont", 14))
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        
        # Botón de reinicio
        reset_button = ctk.CTkButton(actions_frame, text="Reset", 
                                  command=self.reset_form,
                                  height=40, width=100)
        reset_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(actions_frame, orient="horizontal", 
                                         length=400, mode="determinate", 
                                         variable=self.progress_var)
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.progress_bar.grid_remove()  # Ocultar inicialmente
        
        # Etiqueta de estado
        self.status_label = ttk.Label(actions_frame, text="")
        self.status_label.grid(row=2, column=0, columnspan=3, sticky="w", padx=10, pady=5)
    
    def create_results_preview_section(self):
        """Crear sección de vista previa de resultados"""
        # Crear frame para la sección
        results_preview_frame = ctk.CTkFrame(self.frame)
        results_preview_frame.grid(row=4, column=0, columnspan=12, sticky="nsew", padx=10, pady=10)
        results_preview_frame.grid_rowconfigure(1, weight=1)
        results_preview_frame.grid_columnconfigure(0, weight=1)
        
        # Título de la sección
        ttk.Label(results_preview_frame, text="Results Preview", font=("TkDefaultFont", 14, "bold")).grid(
            row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Área de texto de resultados
        self.results_text = ScrolledText(results_preview_frame, wrap=tk.WORD, height=15, width=80)
        self.results_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.results_text.insert(tk.END, "Generate a computer to see results here...")
        self.results_text.config(state=tk.DISABLED)
    
    # Métodos de manejo de eventos
    def on_usage_changed(self):
        """Manejar cambio en la selección de uso"""
        usage = self.usage_var.get()
        # Actualizar rango de precio basado en el uso
        price_ranges = {
            'gaming': (10000, 30000),
            'office': (8000, 15000),
            'graphics': (15000, 40000),
            'video': (20000, 50000),
            'web': (5000, 10000),
            'education': (8000, 20000),
            'architecture': (20000, 50000)
        }
        
        if usage in price_ranges:
            min_price, max_price = price_ranges[usage]
            self.price_min_var.set(str(min_price))
            self.price_max_var.set(str(max_price))
            self.price_range_slider.set(max_price)
    
    def toggle_advanced_options(self):
        """Mostrar u ocultar opciones avanzadas"""
        if self.advanced_options_var.get():
            self.advanced_frame.grid()
        else:
            self.advanced_frame.grid_remove()
    
    def show_fitness_weights(self):
        """Mostrar diálogo para ajustar pesos de fitness"""
        self.controller.show_fitness_weights(self.frame)
    
    def show_include_exclude(self):
        """Mostrar diálogo para especificar componentes a incluir o excluir"""
        self.controller.show_include_exclude(self.frame)
    
    def choose_custom_color(self):
        """Mostrar selector de color para color de caja personalizado"""
        color = colorchooser.askcolor(title="Choose Case Color")
        if color[1]:  # Si se seleccionó un color
            self.case_color_var.set("Custom")
            self.custom_color = color[1]
    
    def generate_computer(self):
        """Iniciar el proceso de generación de computadora"""
        # Obtener datos del formulario
        try:
            min_price = int(self.price_min_var.get())
            max_price = int(self.price_max_var.get())
            usage = self.usage_var.get()
            priority = self.priority_var.get()
            form_factor = self.form_factor_var.get()
            future_proof = self.future_proof_var.get()
            
            # Parámetros del algoritmo
            population_size = int(self.population_size_var.get())
            generations = int(self.generations_var.get())
            crossover_rate = float(self.crossover_rate_var.get())
            mutation_rate = float(self.mutation_rate_var.get())
            elitism = float(self.elitism_var.get()) / 100.0
            tournament_size = int(self.tournament_size_var.get()) if self.advanced_options_var.get() else 3
            adaptive_mutation = self.adaptive_mutation_var.get() if self.advanced_options_var.get() else True
            
            # Preferencias de marca
            brand_prefs = {}
            for comp_type, var in self.brand_preferences.items():
                if var.get() != "No Preference":
                    brand_prefs[comp_type] = [var.get()]
            
            # Preferencias estéticas
            aesthetic = {
                "rgb": self.rgb_lighting_var.get(),
                "color": self.case_color_var.get()
            }
            if self.case_color_var.get() == "Custom":
                aesthetic["custom_color"] = self.custom_color
            
            # Preparar UI para generación
            self.generate_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.progress_bar.grid()
            self.progress_var.set(0)
            self.status_label.config(text="Generating computer configuration...")
            
            # Delegar al controlador
            self.controller.generate_computer(
                min_price=min_price,
                max_price=max_price,
                usage=usage,
                priority=priority,
                form_factor=form_factor,
                future_proof=future_proof,
                brand_preferences=brand_prefs,
                aesthetic=aesthetic,
                population_size=population_size,
                generations=generations,
                crossover_rate=crossover_rate,
                mutation_rate=mutation_rate,
                elitism=elitism,
                tournament_size=tournament_size,
                adaptive_mutation=adaptive_mutation,
                update_callback=self.update_progress
            )
            
        except ValueError as e:
            self.status_label.config(text=f"Error: {str(e)}")
            self.logger.error(f"Error en la generación: {str(e)}")
    
    def update_progress(self, progress, status_text=None):
        """
        Actualizar la barra de progreso.
        
        Args:
            progress: Valor de progreso (0-100)
            status_text: Texto de estado opcional
        """
        self.progress_var.set(progress)
        
        if status_text:
            self.status_label.config(text=status_text)
    
    def stop_generation(self):
        """Detener el proceso de generación"""
        self.controller.stop_generation()
        self.reset_ui_after_generation()
        self.status_label.config(text="Generation stopped by user")
    
    def reset_ui_after_generation(self):
        """Reiniciar UI después de la generación"""
        self.generate_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.progress_bar.grid_remove()
    
    def reset_form(self):
        """Reiniciar todos los campos del formulario a valores predeterminados"""
        # Reiniciar variables de uso
        self.usage_var.set('gaming')
        
        # Reiniciar rango de precio
        self.price_min_var.set('8000')
        self.price_max_var.set('15000')
        self.price_range_slider.set(15000)
        
        # Reiniciar prioridad
        self.priority_var.set('balanced')
        
        # Reiniciar factor de forma
        self.form_factor_var.set('ATX')
        
        # Reiniciar prueba de futuro
        self.future_proof_var.set(False)
        
        # Reiniciar parámetros del algoritmo
        self.population_size_var.set('50')
        self.generations_var.set('100')
        self.crossover_rate_var.set('0.8')
        self.mutation_rate_var.set('0.1')
        self.elitism_var.set('10')
        
        # Reiniciar opciones avanzadas
        self.advanced_options_var.set(False)
        self.advanced_frame.grid_remove()
        self.tournament_size_var.set('3')
        self.adaptive_mutation_var.set(True)
        
        # Reiniciar preferencias de marca
        for comp_type in self.brand_preferences:
            self.brand_preferences[comp_type].set("No Preference")
        
        # Reiniciar estética
        self.rgb_lighting_var.set(False)
        self.case_color_var.set("Black")
        
        # Reiniciar estado
        self.status_label.config(text="Form reset to default values")
        
        # Reiniciar vista previa de resultados
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Generate a computer to see results here...")
        self.results_text.config(state=tk.DISABLED)
    
    def update_results_text(self, text):
        """
        Actualizar el texto de resultados.
        
        Args:
            text: Texto a mostrar en el área de resultados
        """
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, text)
        self.results_text.config(state=tk.DISABLED)
    
    def on_select(self):
        """Método llamado cuando se selecciona esta pestaña"""
        # Actualizar UI si es necesario cuando se selecciona esta pestaña
        pass