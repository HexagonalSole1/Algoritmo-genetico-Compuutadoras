import os
import json
import threading
import webbrowser
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple

# GUI imports
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from tkinter.scrolledtext import ScrolledText
import customtkinter as ctk  # Third-party modern UI toolkit for tkinter

# Data visualization
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import seaborn as sns

# Import the algorithm and models
from algorithm import ComputerGenerator
from models import Computer, UserPreferences
from algorithm.utils.custom_data_manager import CustomDataManager


class ComputerGeneratorGUI:
    """
    Modern GUI for the Computer Generator application with dark mode support,
    tabs, advanced visualization, and enhanced user experience.
    """
    def __init__(self, master):
        """Initialize the GUI"""
        self.master = master
        self.data_manager = CustomDataManager()
        
        # Set up style
        self.setup_style()
        
        # Set up main GUI structure
        self.setup_main_window()
        
        # Initialize state variables
        self.current_computer = None
        self.generated_computers = []
        self.optimization_running = False
        self.result_history = []
        
        # Set up the tabs and their content
        self.setup_tabs()
        
        # Load settings and themes
        self.load_application_settings()

    def setup_style(self):
        """Set up the styling for the application"""
        # Initialize customtkinter
        ctk.set_appearance_mode("System")  # Default to system theme
        ctk.set_default_color_theme("blue")
        
        # Configure ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a modern theme
        
        # Configure colors based on theme
        self.update_colors()

    def update_colors(self):
        """Update colors based on current theme"""
        # Get current theme mode
        mode = ctk.get_appearance_mode()
        
        if mode == "Dark":
            self.bg_color = "#2b2b2b"
            self.fg_color = "#e0e0e0"
            self.accent_color = "#3a7ebf"
            self.subtle_color = "#3c3c3c"
            self.error_color = "#e05c5c"
            self.success_color = "#5ce05c"
            
            # Update ttk styles
            self.style.configure('TFrame', background=self.bg_color)
            self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
            self.style.configure('TButton', background=self.accent_color, foreground=self.fg_color)
            self.style.configure('TNotebook', background=self.bg_color, foreground=self.fg_color)
            self.style.configure('TNotebook.Tab', background=self.subtle_color, foreground=self.fg_color)
            
            # Update matplotlib style
            plt.style.use('dark_background')
        else:
            self.bg_color = "#f0f0f0"
            self.fg_color = "#202020"
            self.accent_color = "#3a7ebf"
            self.subtle_color = "#e0e0e0"
            self.error_color = "#e05c5c"
            self.success_color = "#5ce05c"
            
            # Update ttk styles
            self.style.configure('TFrame', background=self.bg_color)
            self.style.configure('TLabel', background=self.bg_color, foreground=self.fg_color)
            self.style.configure('TButton', background=self.accent_color, foreground=self.fg_color)
            self.style.configure('TNotebook', background=self.bg_color, foreground=self.fg_color)
            self.style.configure('TNotebook.Tab', background=self.subtle_color, foreground=self.fg_color)
            
            # Update matplotlib style
            plt.style.use('default')
    
    def setup_main_window(self):
        """Set up the main window"""
        self.master.title("Computer Generator Pro")
        self.master.geometry("1200x800")
        self.master.minsize(1000, 700)
        
        # Configure grid layout with weight to make it expandable
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        
        # Create menu
        self.create_menu()
        
        # Create status bar
        self.status_bar = ttk.Label(self.master, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky="ew")
    
    def create_menu(self):
        """Create the application menu"""
        menubar = tk.Menu(self.master)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Configuration", command=self.new_configuration)
        file_menu.add_command(label="Open Configuration", command=self.open_configuration)
        file_menu.add_command(label="Save Configuration", command=self.save_configuration)
        file_menu.add_separator()
        file_menu.add_command(label="Export Results", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Preferences", command=self.show_preferences)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        
        # Theme submenu
        theme_menu = tk.Menu(view_menu, tearoff=0)
        theme_menu.add_command(label="Light Mode", command=lambda: self.change_theme("Light"))
        theme_menu.add_command(label="Dark Mode", command=lambda: self.change_theme("Dark"))
        theme_menu.add_command(label="System Default", command=lambda: self.change_theme("System"))
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        
        menubar.add_cascade(label="View", menu=view_menu)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        # Set the menu
        self.master.config(menu=menubar)
    
    def setup_tabs(self):
        """Set up the tab structure"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create tabs
        self.setup_generator_tab()
        self.setup_results_tab()
        self.setup_comparison_tab()
        self.setup_visualization_tab()
        self.setup_component_browser_tab()
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def setup_generator_tab(self):
        """Set up the generator tab with all user inputs"""
        # Create the tab
        generator_frame = ttk.Frame(self.notebook)
        self.notebook.add(generator_frame, text=" Generator ")
        
        # Configure the grid
        for i in range(12):
            generator_frame.grid_columnconfigure(i, weight=1)
        generator_frame.grid_rowconfigure(10, weight=1)  # Make bottom row expandable
# Create sections with frames
        # 1. User Requirements Section
        requirements_frame = ctk.CTkFrame(generator_frame)
        requirements_frame.grid(row=0, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
        
        ttk.Label(requirements_frame, text="User Requirements", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Usage selection
        ttk.Label(requirements_frame, text="Primary Usage:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
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
        
        usage_frame = ttk.Frame(requirements_frame)
        usage_frame.grid(row=1, column=1, columnspan=3, sticky="w", padx=10, pady=5)
        
        for i, (key, value) in enumerate(self.computer_usages.items()):
            col = i % 4
            row = i // 4 + 1
            ttk.Radiobutton(usage_frame, text=value, variable=self.usage_var, value=key, 
                            command=self.on_usage_changed).grid(row=row, column=col, sticky="w", padx=10, pady=2)
        
        # Price range
        ttk.Label(requirements_frame, text="Price Range:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        price_frame = ttk.Frame(requirements_frame)
        price_frame.grid(row=3, column=1, columnspan=3, sticky="w", padx=10, pady=5)
        
        ttk.Label(price_frame, text="Min:").grid(row=0, column=0, sticky="w")
        self.price_min_var = tk.StringVar(value="8000")
        self.price_min_entry = ttk.Entry(price_frame, textvariable=self.price_min_var, width=10)
        self.price_min_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(price_frame, text="Max:").grid(row=0, column=2, sticky="w")
        self.price_max_var = tk.StringVar(value="15000")
        self.price_max_entry = ttk.Entry(price_frame, textvariable=self.price_max_var, width=10)
        self.price_max_entry.grid(row=0, column=3, sticky="w", padx=5, pady=5)
        
        # Price slider
        self.price_range_slider = ctk.CTkSlider(requirements_frame, from_=0, to=50000,
                                               number_of_steps=50, width=400)
        self.price_range_slider.grid(row=3, column=4, columnspan=4, sticky="ew", padx=10, pady=5)
        self.price_range_slider.set(15000)  # Default value
        
        # Priority selection
        ttk.Label(requirements_frame, text="Priority:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.priority_var = tk.StringVar(value="balanced")
        priority_frame = ttk.Frame(requirements_frame)
        priority_frame.grid(row=4, column=1, columnspan=3, sticky="w", padx=10, pady=5)
        
        ttk.Radiobutton(priority_frame, text="Performance", variable=self.priority_var, value="performance").grid(row=0, column=0, sticky="w", padx=10)
        ttk.Radiobutton(priority_frame, text="Value", variable=self.priority_var, value="value").grid(row=0, column=1, sticky="w", padx=10)
        ttk.Radiobutton(priority_frame, text="Balanced", variable=self.priority_var, value="balanced").grid(row=0, column=2, sticky="w", padx=10)
        
        # Form factor
        ttk.Label(requirements_frame, text="Form Factor:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.form_factor_var = tk.StringVar(value="ATX")
        form_factor_frame = ttk.Frame(requirements_frame)
        form_factor_frame.grid(row=5, column=1, columnspan=3, sticky="w", padx=10, pady=5)
        
        ttk.Radiobutton(form_factor_frame, text="ATX", variable=self.form_factor_var, value="ATX").grid(row=0, column=0, sticky="w", padx=10)
        ttk.Radiobutton(form_factor_frame, text="Micro-ATX", variable=self.form_factor_var, value="Micro-ATX").grid(row=0, column=1, sticky="w", padx=10)
        ttk.Radiobutton(form_factor_frame, text="Mini-ITX", variable=self.form_factor_var, value="Mini-ITX").grid(row=0, column=2, sticky="w", padx=10)
        
        # Future-proofing
        self.future_proof_var = tk.BooleanVar(value=False)
        future_proof_check = ttk.Checkbutton(requirements_frame, text="Prioritize Future-Proofing", 
                                           variable=self.future_proof_var)
        future_proof_check.grid(row=5, column=4, sticky="w", padx=10, pady=5)
        
        # 2. Algorithm Parameters Section
        algo_frame = ctk.CTkFrame(generator_frame)
        algo_frame.grid(row=1, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
        
        ttk.Label(algo_frame, text="Algorithm Parameters", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Population size
        ttk.Label(algo_frame, text="Population Size:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.population_size_var = tk.StringVar(value="50")
        population_size_entry = ttk.Entry(algo_frame, textvariable=self.population_size_var, width=10)
        population_size_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(algo_frame, text="Generations:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
        self.generations_var = tk.StringVar(value="100")
        generations_entry = ttk.Entry(algo_frame, textvariable=self.generations_var, width=10)
        generations_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)
        
        ttk.Label(algo_frame, text="Crossover Rate:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.crossover_rate_var = tk.StringVar(value="0.8")
        crossover_rate_entry = ttk.Entry(algo_frame, textvariable=self.crossover_rate_var, width=10)
        crossover_rate_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(algo_frame, text="Mutation Rate:").grid(row=2, column=2, sticky="w", padx=10, pady=5)
        self.mutation_rate_var = tk.StringVar(value="0.1")
        mutation_rate_entry = ttk.Entry(algo_frame, textvariable=self.mutation_rate_var, width=10)
        mutation_rate_entry.grid(row=2, column=3, sticky="w", padx=5, pady=5)
        
        ttk.Label(algo_frame, text="Elitism %:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.elitism_var = tk.StringVar(value="10")
        elitism_entry = ttk.Entry(algo_frame, textvariable=self.elitism_var, width=10)
        elitism_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Advanced options toggle
        self.advanced_options_var = tk.BooleanVar(value=False)
        advanced_options_check = ttk.Checkbutton(algo_frame, text="Show Advanced Options", 
                                               variable=self.advanced_options_var,
                                               command=self.toggle_advanced_options)
        advanced_options_check.grid(row=3, column=2, columnspan=2, sticky="w", padx=10, pady=5)
        
        # Advanced options frame (initially hidden)
        self.advanced_frame = ttk.Frame(algo_frame)
        self.advanced_frame.grid(row=4, column=0, columnspan=6, sticky="ew", padx=10, pady=5)
        self.advanced_frame.grid_remove()  # Hide initially
        
        ttk.Label(self.advanced_frame, text="Tournament Size:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.tournament_size_var = tk.StringVar(value="3")
        tournament_size_entry = ttk.Entry(self.advanced_frame, textvariable=self.tournament_size_var, width=10)
        tournament_size_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        self.adaptive_mutation_var = tk.BooleanVar(value=True)
        adaptive_mutation_check = ttk.Checkbutton(self.advanced_frame, text="Adaptive Mutation", 
                                                variable=self.adaptive_mutation_var)
        adaptive_mutation_check.grid(row=0, column=2, sticky="w", padx=10, pady=5)
        
        # Fitness weights button
        fitness_weights_button = ctk.CTkButton(self.advanced_frame, text="Fitness Weights", 
                                              command=self.show_fitness_weights)
        fitness_weights_button.grid(row=0, column=3, sticky="w", padx=10, pady=5)
        
        # 3. Component Preferences Section
        components_frame = ctk.CTkFrame(generator_frame)
        components_frame.grid(row=2, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
        
        ttk.Label(components_frame, text="Component Preferences", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Brand preferences
        ttk.Label(components_frame, text="Brand Preferences:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        # Create a frame for brand preferences
        brands_frame = ttk.Frame(components_frame)
        brands_frame.grid(row=1, column=1, columnspan=5, sticky="w", padx=10, pady=5)
        
        # Component type labels
        component_types = ["CPU", "GPU", "Motherboard", "RAM", "Storage"]
        for i, comp_type in enumerate(component_types):
            ttk.Label(brands_frame, text=comp_type + ":").grid(row=0, column=i, sticky="w", padx=5, pady=2)
        
        # Brand preference dropdown lists
        self.brand_preferences = {}
        for i, comp_type in enumerate(component_types):
            self.brand_preferences[comp_type.lower()] = tk.StringVar(value="No Preference")
            brands = ["No Preference", "Intel", "AMD"] if comp_type == "CPU" else ["No Preference", "ASUS", "MSI", "Gigabyte", "EVGA"]
            brand_dropdown = ttk.Combobox(brands_frame, textvariable=self.brand_preferences[comp_type.lower()], values=brands, width=12)
            brand_dropdown.grid(row=1, column=i, sticky="w", padx=5, pady=2)
        
        # Must include/exclude components button
        include_exclude_button = ctk.CTkButton(components_frame, text="Include/Exclude Components", 
                                             command=self.show_include_exclude)
        include_exclude_button.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        
        # Aesthetic preferences
        ttk.Label(components_frame, text="Aesthetics:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        
        # Aesthetics frame
        aesthetics_frame = ttk.Frame(components_frame)
        aesthetics_frame.grid(row=3, column=1, columnspan=5, sticky="w", padx=10, pady=5)
        
        # RGB lighting preference
        self.rgb_lighting_var = tk.BooleanVar(value=False)
        rgb_check = ttk.Checkbutton(aesthetics_frame, text="RGB Lighting", variable=self.rgb_lighting_var)
        rgb_check.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        
        # Case color preference
        ttk.Label(aesthetics_frame, text="Color:").grid(row=0, column=1, sticky="w", padx=10, pady=2)
        self.case_color_var = tk.StringVar(value="Black")
        case_colors = ["Black", "White", "Red", "Blue", "Green", "Custom"]
        case_color_dropdown = ttk.Combobox(aesthetics_frame, textvariable=self.case_color_var, values=case_colors, width=10)
        case_color_dropdown.grid(row=0, column=2, sticky="w", padx=5, pady=2)
        
        # Custom color button
        color_button = ctk.CTkButton(aesthetics_frame, text="Choose Color", command=self.choose_custom_color, width=20)
        color_button.grid(row=0, column=3, sticky="w", padx=5, pady=2)
        
        # 4. Action Buttons
        actions_frame = ctk.CTkFrame(generator_frame)
        actions_frame.grid(row=3, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
        
        # Generate button
        self.generate_button = ctk.CTkButton(actions_frame, text="Generate Computer", 
                                          command=self.generate_computer,
                                          height=40, width=200,
                                          font=("TkDefaultFont", 14))
        self.generate_button.grid(row=0, column=0, padx=10, pady=10)
        
        # Stop button (initially disabled)
        self.stop_button = ctk.CTkButton(actions_frame, text="Stop", 
                                      command=self.stop_generation,
                                      height=40, width=100,
                                      state="disabled",
                                      font=("TkDefaultFont", 14))
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)
        
        # Reset button
        reset_button = ctk.CTkButton(actions_frame, text="Reset", 
                                   command=self.reset_form,
                                   height=40, width=100)
        reset_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Progress bar (initially hidden)
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(actions_frame, orient="horizontal", 
                                          length=400, mode="determinate", 
                                          variable=self.progress_var)
        self.progress_bar.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.progress_bar.grid_remove()  # Hide initially
        
        # Status label
        self.status_label = ttk.Label(actions_frame, text="")
        self.status_label.grid(row=2, column=0, columnspan=3, sticky="w", padx=10, pady=5)
        
        # 5. Results Preview
        results_preview_frame = ctk.CTkFrame(generator_frame)
        results_preview_frame.grid(row=4, column=0, columnspan=12, sticky="nsew", padx=10, pady=10)
        results_preview_frame.grid_rowconfigure(1, weight=1)
        results_preview_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(results_preview_frame, text="Results Preview", font=("TkDefaultFont", 14, "bold")).grid(
            row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Results text area
        self.results_text = ScrolledText(results_preview_frame, wrap=tk.WORD, height=15, width=80)
        self.results_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.results_text.insert(tk.END, "Generate a computer to see results here...")
        self.results_text.config(state=tk.DISABLED)
    
    def setup_results_tab(self):
        """Set up the results tab for detailed view of generated computer"""
        # Create the tab
        results_frame = ttk.Frame(self.notebook)
        self.notebook.add(results_frame, text=" Results ")
        
        # Configure the grid
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_columnconfigure(1, weight=3)
        results_frame.grid_rowconfigure(0, weight=1)
        
        # Create left and right panes
        left_pane = ttk.Frame(results_frame)
        left_pane.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        right_pane = ttk.Frame(results_frame)
        right_pane.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Left pane - Component list
        ttk.Label(left_pane, text="Components", font=("TkDefaultFont", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Components tree view
        columns = ('component', 'details', 'price')
        self.components_tree = ttk.Treeview(left_pane, columns=columns, show='headings', height=20)
        
        # Define headings and columns
        self.components_tree.heading('component', text='Component')
        self.components_tree.heading('details', text='Details')
        self.components_tree.heading('price', text='Price')
        
        self.components_tree.column('component', width=120, anchor='w')
        self.components_tree.column('details', width=300, anchor='w')
        self.components_tree.column('price', width=80, anchor='e')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(left_pane, orient=tk.VERTICAL, command=self.components_tree.yview)
        self.components_tree.configure(yscroll=scrollbar.set)
        
        # Pack components
        self.components_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=5)
        
        # Bind selection event
        self.components_tree.bind('<<TreeviewSelect>>', self.on_component_selected)
        
        # Right pane - Component details
        self.details_frame = ttk.LabelFrame(right_pane, text="Component Details")
        self.details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Component image placeholder
        self.component_image_label = tk.Label(self.details_frame, text="[Component Image]",
                                            borderwidth=2, relief="solid", width=30, height=10)
        self.component_image_label.pack(padx=20, pady=20)
        
        # Component details text
        self.component_details_text = ScrolledText(self.details_frame, wrap=tk.WORD, height=15, width=50)
        self.component_details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.component_details_text.insert(tk.END, "Select a component to view details...")
        self.component_details_text.config(state=tk.DISABLED)
        
        # Buttons frame
        buttons_frame = ttk.Frame(right_pane)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Replace component button
        replace_button = ctk.CTkButton(buttons_frame, text="Replace Component", 
                                     command=self.show_replace_component)
        replace_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # View alternatives button
        alternatives_button = ctk.CTkButton(buttons_frame, text="View Alternatives", 
                                         command=self.show_alternatives)
        alternatives_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Add to comparison button
        add_to_comparison_button = ctk.CTkButton(buttons_frame, text="Add to Comparison", 
                                              command=self.add_to_comparison)
        add_to_comparison_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Save configuration button
        save_button = ctk.CTkButton(buttons_frame, text="Save Configuration", 
                                  command=self.save_configuration)
        save_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Performance summary frame
        performance_frame = ttk.LabelFrame(right_pane, text="Performance Summary")
        performance_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Grid for performance metrics
        for i in range(4):
            performance_frame.grid_columnconfigure(i, weight=1)
        
        # Performance metrics
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
    
    def setup_comparison_tab(self):
        """Set up the comparison tab for comparing multiple configurations"""
        # Create the tab
        comparison_frame = ttk.Frame(self.notebook)
        self.notebook.add(comparison_frame, text=" Comparison ")
        
        # Configure the grid
        comparison_frame.grid_columnconfigure(0, weight=1)
        comparison_frame.grid_rowconfigure(1, weight=1)
        
        # Top controls frame
        controls_frame = ttk.Frame(comparison_frame)
        controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ttk.Label(controls_frame, text="Compare Configurations", font=("TkDefaultFont", 14, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Add buttons
        clear_button = ctk.CTkButton(controls_frame, text="Clear All", 
                                   command=self.clear_comparison)
        clear_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        export_button = ctk.CTkButton(controls_frame, text="Export Comparison", 
                                    command=self.export_comparison)
        export_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Main comparison area
        comparison_area = ttk.Frame(comparison_frame)
        comparison_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Setup scrollable canvas for comparison
        canvas = tk.Canvas(comparison_area, borderwidth=0)
        scrollbar = ttk.Scrollbar(comparison_area, orient=tk.VERTICAL, command=canvas.yview)
        self.comparison_container = ttk.Frame(canvas)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas_window = canvas.create_window((0, 0), window=self.comparison_container, anchor=tk.NW)
        
        # Configure scrolling
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas_width(event):
            canvas.itemconfig(canvas_window, width=event.width)
        
        self.comparison_container.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas_width)
        
        # Add some placeholder text
        ttk.Label(self.comparison_container, text="Add configurations to compare them side by side...").pack(padx=20, pady=20)
    
    def setup_visualization_tab(self):
        """Set up the visualization tab for displaying charts and graphs"""
        # Create the tab
        visualization_frame = ttk.Frame(self.notebook)
        self.notebook.add(visualization_frame, text=" Visualization ")
        
        # Configure the grid
        visualization_frame.grid_columnconfigure(0, weight=1)
        visualization_frame.grid_rowconfigure(1, weight=1)
        
        # Top controls frame
        controls_frame = ttk.Frame(visualization_frame)
        controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ttk.Label(controls_frame, text="Performance Visualization", font=("TkDefaultFont", 14, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Chart type selection
        ttk.Label(controls_frame, text="Chart Type:").pack(side=tk.LEFT, padx=10, pady=5)
        self.chart_type_var = tk.StringVar(value="radar")
        chart_types = ["radar", "bar", "heatmap", "evolution"]
        chart_type_dropdown = ttk.Combobox(controls_frame, textvariable=self.chart_type_var, 
                                         values=chart_types, width=10,
                                         state="readonly")
        chart_type_dropdown.pack(side=tk.LEFT, padx=5, pady=5)
        chart_type_dropdown.bind("<<ComboboxSelected>>", self.update_visualization)
        
        # Export button
        export_button = ctk.CTkButton(controls_frame, text="Export Chart", 
                                    command=self.export_chart)
        export_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Main visualization area
        self.visualization_area = ttk.Frame(visualization_frame)
        self.visualization_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Create a figure for matplotlib
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.plot = self.figure.add_subplot(111)
        
        # Create canvas for matplotlib figure
        self.chart_canvas = FigureCanvasTkAgg(self.figure, self.visualization_area)
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add placeholder text on the plot
        self.plot.text(0.5, 0.5, "Generate a computer to visualize performance data", 
                     horizontalalignment='center', verticalalignment='center',
                     transform=self.plot.transAxes, fontsize=14)
        self.plot.axis('off')
        self.chart_canvas.draw()
    
    def setup_component_browser_tab(self):
        """Set up the component browser tab for exploring available components"""
        # Create the tab
        browser_frame = ttk.Frame(self.notebook)
        self.notebook.add(browser_frame, text=" Component Browser ")
        
        # Configure the grid
        browser_frame.grid_columnconfigure(1, weight=1)
        browser_frame.grid_rowconfigure(1, weight=1)
        
        # Top controls frame
        controls_frame = ttk.Frame(browser_frame)
        controls_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        ttk.Label(controls_frame, text="Component Browser", font=("TkDefaultFont", 14, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Component type selection
        ttk.Label(controls_frame, text="Component Type:").pack(side=tk.LEFT, padx=10, pady=5)
        self.component_type_var = tk.StringVar(value="cpu")
        component_types = ["cpu", "gpu", "ram", "storage", "motherboard", "psu", "cooling", "case"]
        component_type_dropdown = ttk.Combobox(controls_frame, textvariable=self.component_type_var, 
                                             values=component_types, width=12,
                                             state="readonly")
        component_type_dropdown.pack(side=tk.LEFT, padx=5, pady=5)
        component_type_dropdown.bind("<<ComboboxSelected>>", self.update_component_browser)
        
        # Search bar
        ttk.Label(controls_frame, text="Search:").pack(side=tk.LEFT, padx=10, pady=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(controls_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        search_button = ctk.CTkButton(controls_frame, text="Search", 
                                    command=self.search_components)
        search_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Reset filters button
        reset_button = ctk.CTkButton(controls_frame, text="Reset Filters", 
                                   command=self.reset_component_filters)
        reset_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Left pane - filters
        filters_frame = ttk.LabelFrame(browser_frame, text="Filters")
        filters_frame.grid(row=1, column=0, sticky="ns", padx=10, pady=10)
        
        # Price range filter
        ttk.Label(filters_frame, text="Price Range:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        price_filter_frame = ttk.Frame(filters_frame)
        price_filter_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)
        
        ttk.Label(price_filter_frame, text="Min:").grid(row=0, column=0, sticky="w")
        self.price_filter_min_var = tk.StringVar(value="0")
        price_filter_min_entry = ttk.Entry(price_filter_frame, textvariable=self.price_filter_min_var, width=8)
        price_filter_min_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(price_filter_frame, text="Max:").grid(row=0, column=2, sticky="w")
        self.price_filter_max_var = tk.StringVar(value="50000")
        price_filter_max_entry = ttk.Entry(price_filter_frame, textvariable=self.price_filter_max_var, width=8)
        price_filter_max_entry.grid(row=0, column=3, sticky="w", padx=5, pady=2)
        
        # Apply price filter button
        apply_price_button = ctk.CTkButton(price_filter_frame, text="Apply", 
                                         command=self.apply_price_filter,
                                         width=20)
        apply_price_button.grid(row=0, column=4, padx=5, pady=2)
        
        # Brand filter
        ttk.Label(filters_frame, text="Brand:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        
        self.brand_filter_var = tk.StringVar(value="All")
        self.brand_filter_list = ttk.Combobox(filters_frame, textvariable=self.brand_filter_var, 
                                            values=["All"], width=15)
        self.brand_filter_list.grid(row=3, column=0, sticky="w", padx=10, pady=2)
        self.brand_filter_list.bind("<<ComboboxSelected>>", self.apply_brand_filter)
        
        # Component-specific filters frame
        self.specific_filters_frame = ttk.LabelFrame(filters_frame, text="Specific Filters")
        self.specific_filters_frame.grid(row=4, column=0, sticky="ew", padx=5, pady=10)
        
        # Right pane - component list
        list_frame = ttk.Frame(browser_frame)
        list_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        
        # Component list with details
        columns = ('name', 'details', 'performance', 'price')
        self.components_browser = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Define headings and columns
        self.components_browser.heading('name', text='Name')
        self.components_browser.heading('details', text='Details')
        self.components_browser.heading('performance', text='Performance')
        self.components_browser.heading('price', text='Price')
        
        self.components_browser.column('name', width=200, anchor='w')
        self.components_browser.column('details', width=300, anchor='w')
        self.components_browser.column('performance', width=100, anchor='center')
        self.components_browser.column('price', width=100, anchor='e')
        
        # Scrollbars
        vscrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.components_browser.yview)
        hscrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.components_browser.xview)
        self.components_browser.configure(yscroll=vscrollbar.set, xscroll=hscrollbar.set)
        
        # Pack components
        self.components_browser.grid(row=0, column=0, sticky="nsew")
        vscrollbar.grid(row=0, column=1, sticky="ns")
        hscrollbar.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        # Context menu for component browser
        self.component_context_menu = tk.Menu(self.components_browser, tearoff=0)
        self.component_context_menu.add_command(label="View Details", command=self.view_component_details)
        self.component_context_menu.add_command(label="Add to Current Build", command=self.add_component_to_build)
        self.component_context_menu.add_command(label="Compare with Current", command=self.compare_with_current)
        
        # Bind context menu
        self.components_browser.bind("<Button-3>", self.show_component_context_menu)
        self.components_browser.bind("<Double-1>", lambda e: self.view_component_details())
        
        # Initialize the browser with CPUs
        self.update_component_browser()
    
    # Event handlers and utility methods
    def on_usage_changed(self):
        """Handle change in usage selection"""
        usage = self.usage_var.get()
        # Update price range based on usage
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
        """Show or hide advanced options"""
        if self.advanced_options_var.get():
            self.advanced_frame.grid()
        else:
            self.advanced_frame.grid_remove()
    
    def show_fitness_weights(self):
        """Show dialog to adjust fitness weights"""
        weights_dialog = ctk.CTkToplevel(self.master)
        weights_dialog.title("Fitness Function Weights")
        weights_dialog.geometry("400x350")
        weights_dialog.transient(self.master)
        weights_dialog.grab_set()
        
        # Create sliders for each weight
        weight_names = {
            'price_range': 'Price Range',
            'compatibility': 'Compatibility',
            'usage_match': 'Usage Match',
            'power_balance': 'Power Balance',
            'bottleneck': 'Bottleneck Prevention',
            'value_cpu': 'CPU Value',
            'value_gpu': 'GPU Value'
        }
        
        # Default weights
        default_weights = {
            'price_range': 20,
            'compatibility': 25,
            'usage_match': 30,
            'power_balance': 5,
            'bottleneck': 10,
            'value_cpu': 5,
            'value_gpu': 5
        }
        
        # Create and store variables
        self.weight_vars = {}
        
        # Create frame for weights
        weights_frame = ttk.Frame(weights_dialog)
        weights_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Add description
        ttk.Label(weights_frame, text="Adjust the importance of each factor in the fitness function:",
                wraplength=350).grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Add sliders for each weight
        for i, (key, name) in enumerate(weight_names.items()):
            ttk.Label(weights_frame, text=name).grid(row=i+1, column=0, sticky="w", padx=5, pady=5)
            self.weight_vars[key] = tk.IntVar(value=default_weights.get(key, 10))
            slider = ttk.Scale(weights_frame, from_=0, to=50, variable=self.weight_vars[key], 
                             orient=tk.HORIZONTAL, length=200)
            slider.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)
            ttk.Label(weights_frame, textvariable=self.weight_vars[key], width=3).grid(row=i+1, column=2, padx=5, pady=5)
        
        # Buttons
        buttons_frame = ttk.Frame(weights_dialog)
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        
        apply_button = ctk.CTkButton(buttons_frame, text="Apply", 
                                   command=lambda: self.apply_fitness_weights(weights_dialog))
        apply_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        reset_button = ctk.CTkButton(buttons_frame, text="Reset to Default", 
                                   command=self.reset_fitness_weights)
        reset_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def apply_fitness_weights(self, dialog):
        """Apply the selected fitness weights"""
        # Get all weight values from the dialog
        weights = {key: var.get() for key, var in self.weight_vars.items()}
        
        # Store for later use
        self.fitness_weights = weights
        
        # Close the dialog
        dialog.destroy()
        
        # Update status
        self.status_label.config(text="Fitness weights updated")
    
    def reset_fitness_weights(self):
        """Reset fitness weights to default values"""
        default_weights = {
            'price_range': 20,
            'compatibility': 25,
            'usage_match': 30,
            'power_balance': 5,
            'bottleneck': 10,
            'value_cpu': 5,
            'value_gpu': 5
        }
        
        for key, value in default_weights.items():
            if key in self.weight_vars:
                self.weight_vars[key].set(value)
    
    def show_include_exclude(self):
        """Show dialog to specify components to include or exclude"""
        include_dialog = ctk.CTkToplevel(self.master)
        include_dialog.title("Include/Exclude Components")
        include_dialog.geometry("600x500")
        include_dialog.transient(self.master)
        include_dialog.grab_set()
        
        # Create notebook for component types
        component_notebook = ttk.Notebook(include_dialog)
        component_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Component types
        component_types = ["CPU", "GPU", "RAM", "Storage", "Motherboard", "PSU", "Cooling", "Case"]
        
        # Create a tab for each component type
        self.include_exclude_vars = {}
        
        for comp_type in component_types:
            # Create frame for this component type
            comp_frame = ttk.Frame(component_notebook)
            component_notebook.add(comp_frame, text=comp_type)
            
            # Configure grid
            comp_frame.grid_columnconfigure(0, weight=1)
            comp_frame.grid_columnconfigure(1, weight=1)
            comp_frame.grid_rowconfigure(1, weight=1)
            
            # Add "Must Include" and "Must Exclude" sections
            ttk.Label(comp_frame, text="Must Include:", font=("TkDefaultFont", 11, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
            ttk.Label(comp_frame, text="Must Exclude:", font=("TkDefaultFont", 11, "bold")).grid(row=0, column=1, sticky="w", padx=10, pady=5)
            
            # Get components of this type
            components = self.get_components_list(comp_type.lower())
            
            # Create listboxes
            include_frame = ttk.Frame(comp_frame)
            include_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
            
            exclude_frame = ttk.Frame(comp_frame)
            exclude_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=5)
            
            # Include listbox with scrollbar
            include_listbox = tk.Listbox(include_frame, selectmode=tk.MULTIPLE, height=15)
            include_scrollbar = ttk.Scrollbar(include_frame, orient=tk.VERTICAL, command=include_listbox.yview)
            include_listbox.configure(yscrollcommand=include_scrollbar.set)
            
            include_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            include_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Exclude listbox with scrollbar
            exclude_listbox = tk.Listbox(exclude_frame, selectmode=tk.MULTIPLE, height=15)
            exclude_scrollbar = ttk.Scrollbar(exclude_frame, orient=tk.VERTICAL, command=exclude_listbox.yview)
            exclude_listbox.configure(yscrollcommand=exclude_scrollbar.set)
            
            exclude_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            exclude_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Populate listboxes
            for comp in components:
                include_listbox.insert(tk.END, comp)
                exclude_listbox.insert(tk.END, comp)
            
            # Store variables for later retrieval
            self.include_exclude_vars[comp_type.lower()] = {
                'include': include_listbox,
                'exclude': exclude_listbox
            }
        
        # Buttons
        buttons_frame = ttk.Frame(include_dialog)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        apply_button = ctk.CTkButton(buttons_frame, text="Apply", 
                                   command=lambda: self.apply_include_exclude(include_dialog))
        apply_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        clear_button = ctk.CTkButton(buttons_frame, text="Clear All", 
                                   command=self.clear_include_exclude)
        clear_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def get_components_list(self, component_type):
        """Get list of components of the specified type"""
        # This would normally come from your data manager
        # For now, return some dummy data
        components = {
            'cpu': ["Intel Core i9-14900K", "AMD Ryzen 9 7950X", "Intel Core i7-14700K", 
                  "AMD Ryzen 7 7800X3D", "Intel Core i5-14600K"],
            'gpu': ["NVIDIA RTX 4090", "AMD Radeon RX 7900 XTX", "NVIDIA RTX 4080 Super",
                  "AMD Radeon RX 7800 XT", "NVIDIA RTX 4070 Ti Super"],
            'ram': ["G.Skill Trident Z5 RGB 32GB DDR5-6000", "Corsair Vengeance 32GB DDR5-5600",
                  "Kingston Fury Beast 32GB DDR4-3600", "Crucial Ballistix 16GB DDR4-3200"],
            'storage': ["Samsung 990 Pro 2TB", "WD Black SN850X 1TB", "Crucial T700 2TB",
                       "Sabrent Rocket 4 Plus 2TB", "Samsung 870 EVO 1TB SATA SSD"],
            'motherboard': ["ASUS ROG Maximus Z790 Hero", "Gigabyte X670E Aorus Master",
                          "MSI MPG Z790 Carbon WiFi", "ASRock B650E Steel Legend"],
            'psu': ["Corsair RM850x", "Seasonic Prime TX-1000", "EVGA SuperNOVA 750 G5",
                  "be quiet! Dark Power Pro 12 1500W"],
            'cooling': ["Noctua NH-D15", "ARCTIC Liquid Freezer II 360", "Corsair iCUE H150i Elite",
                       "be quiet! Dark Rock Pro 4"],
            'case': ["Lian Li O11 Dynamic EVO", "Corsair 5000D Airflow", "Fractal Design Meshify 2",
                    "NZXT H510 Flow"]
        }
        
        return components.get(component_type, [])
    
    def apply_include_exclude(self, dialog):
        """Apply the include/exclude component selections"""
        include_components = {}
        exclude_components = {}
        
        for comp_type, listboxes in self.include_exclude_vars.items():
            include_listbox = listboxes['include']
            exclude_listbox = listboxes['exclude']
            
            # Get selected items
            include_selected = [include_listbox.get(idx) for idx in include_listbox.curselection()]
            exclude_selected = [exclude_listbox.get(idx) for idx in exclude_listbox.curselection()]
            
            if include_selected:
                include_components[comp_type] = include_selected
            
            if exclude_selected:
                exclude_components[comp_type] = exclude_selected
        
        # Store for later use
        self.must_include = include_components
        self.must_exclude = exclude_components
        
        # Close dialog
        dialog.destroy()
        
        # Update status
        self.status_label.config(text=f"Include/exclude preferences updated: {len(include_components)} inclusions, {len(exclude_components)} exclusions")
    
    def clear_include_exclude(self):
        """Clear all selections in include/exclude dialog"""
        for comp_type, listboxes in self.include_exclude_vars.items():
            include_listbox = listboxes['include']
            exclude_listbox = listboxes['exclude']
            
            include_listbox.selection_clear(0, tk.END)
            exclude_listbox.selection_clear(0, tk.END)
    
    def choose_custom_color(self):
        """Show color picker for custom case color"""
        color = colorchooser.askcolor(title="Choose Case Color")
        if color[1]:  # If a color was selected
            self.case_color_var.set("Custom")
            self.custom_color = color[1]
    
    def generate_computer(self):
        """Start the computer generation process"""
        try:
            # Validate inputs
            min_price = int(self.price_min_var.get())
            max_price = int(self.price_max_var.get())
            population_size = int(self.population_size_var.get())
            generations = int(self.generations_var.get())
            crossover_rate = float(self.crossover_rate_var.get())
            mutation_rate = float(self.mutation_rate_var.get())
            elitism = float(self.elitism_var.get()) / 100.0
            
            # Additional parameters
            tournament_size = int(self.tournament_size_var.get()) if self.advanced_options_var.get() else 3
            adaptive_mutation = self.adaptive_mutation_var.get() if self.advanced_options_var.get() else True
            
            # Get fitness weights if set
            fitness_weights = getattr(self, 'fitness_weights', None)
            
            # Create user preferences
            usage_mapping = {
                'gaming': 'juegos',
                'office': 'ofimática',
                'graphics': 'diseño gráfico',
                'video': 'edición de video',
                'web': 'navegación web',
                'education': 'educación',
                'architecture': 'arquitectura'
            }
            
            usage = usage_mapping.get(self.usage_var.get(), 'gaming')
            
            # Brand preferences
            brand_prefs = {}
            for comp_type, var in self.brand_preferences.items():
                if var.get() != "No Preference":
                    brand_prefs[comp_type] = [var.get()]
            
            # Aesthetic preferences
            aesthetic = {
                "rgb": self.rgb_lighting_var.get(),
                "color": self.case_color_var.get()
            }
            if hasattr(self, 'custom_color') and self.case_color_var.get() == "Custom":
                aesthetic["custom_color"] = self.custom_color
            
            # Must include/exclude components
            must_include = getattr(self, 'must_include', {})
            must_exclude = getattr(self, 'must_exclude', {})
            
            # Create user preferences object
            user_prefs = UserPreferences(
                min_price=min_price,
                max_price=max_price,
                usage=usage,
                priority=self.priority_var.get(),
                brand_preferences=brand_prefs,
                form_factor=self.form_factor_var.get(),
                aesthetic=aesthetic,
                must_include=must_include,
                must_exclude=must_exclude,
                future_proof=self.future_proof_var.get()
            )
            
            # Update UI state
            self.generate_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.progress_bar.grid()
            self.progress_var.set(0)
            self.status_label.config(text="Generating computer configuration...")
            
            # Create and start the generator in a separate thread
            self.generator = ComputerGenerator(
                population_size=population_size,
                crossover_rate=crossover_rate,
                mutation_rate=mutation_rate,
                generations=generations,
                user_preferences=user_prefs,
                elitism_percentage=elitism,
                tournament_size=tournament_size,
                adaptive_mutation=adaptive_mutation,
                fitness_weights=fitness_weights
            )
            
            # Set flag for the running state
            self.optimization_running = True
            
            # Start the generation thread
            self.generation_thread = threading.Thread(target=self.run_generation)
            self.generation_thread.daemon = True
            self.generation_thread.start()
            
            # Start progress update
            self.master.after(100, self.update_progress)
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
    
    def run_generation(self):
        """Run the genetic algorithm in a separate thread"""
        try:
            # Run the generator and get the best computer
            self.current_computer, self.stats = self.generator.run()
            
            # Add to history
            self.result_history.append({
                "computer": self.current_computer,
                "stats": self.stats,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "preferences": self.generator.user_preferences
            })
            
            # Update UI in the main thread
            self.master.after(0, self.update_results_ui)
        
        except Exception as e:
            # Handle errors
            self.master.after(0, lambda: messagebox.showerror("Generation Error", f"Error during generation: {str(e)}"))
            self.master.after(0, self.reset_ui_after_generation)
    
    def update_progress(self):
        """Update the progress bar during generation"""
        if not hasattr(self, 'generator') or not self.optimization_running:
            return
        
        # Calculate progress
        if hasattr(self.generator, 'best_cases'):
            progress = min(100, len(self.generator.best_cases) / self.generator.generations * 100)
            self.progress_var.set(progress)
            
            # Update status text
            if len(self.generator.best_cases) > 0:
                best_fitness = self.generator.best_cases[-1].fitness
                self.status_label.config(text=f"Generation {len(self.generator.best_cases)}/{self.generator.generations} - Best fitness: {best_fitness:.2f}")
        
        # Continue updating if still running
        if self.optimization_running:
            self.master.after(100, self.update_progress)
    
    def update_results_ui(self):
        """Update UI with generation results"""
        if not hasattr(self, 'current_computer'):
            return
        
        # Update results text
        self.update_results_text()
        
        # Update components tree
        self.update_components_tree()
        
        # Update performance bars
        self.update_performance_display()
        
        # Update visualization
        self.update_visualization()
        
        # Reset UI state
        self.reset_ui_after_generation()
        
        # Show success message
        messagebox.showinfo("Generation Complete", "Computer configuration generated successfully!")
        
        # Switch to results tab
        self.notebook.select(1)  # Index of the Results tab
    
    def update_results_text(self):
        """Update the results text with computer details"""
        if not hasattr(self, 'current_computer'):
            return
        
        # Enable editing
        self.results_text.config(state=tk.NORMAL)
        
        # Clear existing text
        self.results_text.delete(1.0, tk.END)
        
        # Add computer details
        self.results_text.insert(tk.END, str(self.current_computer))
        
        # Add additional stats
        self.results_text.insert(tk.END, "\n\nGeneration Stats:\n")
        self.results_text.insert(tk.END, f"Execution Time: {self.stats['execution_time']:.2f} seconds\n")
        self.results_text.insert(tk.END, f"Generations Completed: {self.stats['generations_completed']}\n")
        self.results_text.insert(tk.END, f"Final Population Size: {self.stats['final_population_size']}\n")
        self.results_text.insert(tk.END, f"Final Diversity: {self.stats['final_diversity']:.2f}\n")
        
        # Disable editing
        self.results_text.config(state=tk.DISABLED)
    
    def update_components_tree(self):
        """Update the components tree with the current computer configuration"""
        if not hasattr(self, 'current_computer') or self.current_computer is None:
            # No hay computadora para mostrar
            return
        
        # Clear existing items
        for item in self.components_tree.get_children():
            self.components_tree.delete(item)
        
        # Add components to tree
        self.components_tree.insert('', 'end', values=('CPU', str(self.current_computer.cpu), f"${self.current_computer.cpu.price:.2f}"))
        
        if self.current_computer.gpu:
            self.components_tree.insert('', 'end', values=('GPU', str(self.current_computer.gpu), f"${self.current_computer.gpu.price:.2f}"))
        else:
            self.components_tree.insert('', 'end', values=('GPU', 'None (Using Integrated Graphics)', '$0.00'))
        
        self.components_tree.insert('', 'end', values=('RAM', str(self.current_computer.ram), f"${self.current_computer.ram.price:.2f}"))
        self.components_tree.insert('', 'end', values=('Storage', str(self.current_computer.storage), f"${self.current_computer.storage.price:.2f}"))
        
        # Add additional storages if any
        for i, storage in enumerate(self.current_computer.additional_storages):
            self.components_tree.insert('', 'end', values=(f'Storage {i+2}', str(storage), f"${storage.price:.2f}"))
        
        self.components_tree.insert('', 'end', values=('Motherboard', str(self.current_computer.motherboard), f"${self.current_computer.motherboard.price:.2f}"))
        self.components_tree.insert('', 'end', values=('PSU', str(self.current_computer.psu), f"${self.current_computer.psu.price:.2f}"))
        self.components_tree.insert('', 'end', values=('Cooling', str(self.current_computer.cooling), f"${self.current_computer.cooling.price:.2f}"))
        self.components_tree.insert('', 'end', values=('Case', str(self.current_computer.case), f"${self.current_computer.case.price:.2f}"))
        
        # Add total price
        self.components_tree.insert('', 'end', values=('Total', '', f"${self.current_computer.price:.2f}"))
    
    def update_performance_display(self):
        """Update the performance display bars"""
        if not hasattr(self, 'current_computer'):
            return
        
        # Get performance metrics
        performance = self.current_computer.estimated_performance
        
        # Update progress bars and labels
        for metric in ['gaming', 'productivity', 'content_creation', 'development']:
            if metric in performance and metric in self.performance_vars:
                # Update progress bar
                self.performance_vars[metric].set(performance[metric])
                
                # Update label
                if f"{metric}_label" in self.performance_vars:
                    self.performance_vars[f"{metric}_label"].config(text=f"{performance[metric]:.1f}/100")
            else:
                # Metric not available, set to 0
                if metric in self.performance_vars:
                    self.performance_vars[metric].set(0)
                    
                if f"{metric}_label" in self.performance_vars:
                    self.performance_vars[f"{metric}_label"].config(text="N/A")
    
    def update_visualization(self, event=None):
        """Update the visualization based on selected chart type"""
        if not hasattr(self, 'current_computer') or not hasattr(self, 'stats'):
            return
        
        # Clear the figure
        self.plot.clear()
        
        # Get selected chart type
        chart_type = self.chart_type_var.get()
        
        if chart_type == "radar":
            self.create_radar_chart()
        elif chart_type == "bar":
            self.create_bar_chart()
        elif chart_type == "heatmap":
            self.create_heatmap_chart()
        elif chart_type == "evolution":
            self.create_evolution_chart()
        
        # Redraw the canvas
        self.chart_canvas.draw()
    
    def create_radar_chart(self):
        """Create a radar chart of performance metrics"""
        # Get performance metrics
        if not hasattr(self, 'current_computer'):
            return
                
        performance = self.current_computer.estimated_performance
        
        # Categories for radar chart
        categories = ['Gaming', 'Productivity', 'Content Creation', 'Development']
        
        # Values for each category
        values = [
            performance.get('gaming', 0),
            performance.get('productivity', 0),
            performance.get('content_creation', 0),
            performance.get('development', 0)
        ]
        
        # Add the first value to close the circular graph
        categories.append(categories[0])
        values.append(values[0])
        
        # Convert to radians for plot
        angles = np.linspace(0, 2*np.pi, len(categories)-1, endpoint=False).tolist()
        angles.append(angles[0])
        
        # Clear previous plot and create a new polar subplot
        self.plot.clear()
        self.plot = self.figure.add_subplot(111, polar=True)
        
        # Create radar chart
        self.plot.plot(angles, values, marker='o', linestyle='-', linewidth=2)
        
        # Fill area
        self.plot.fill(angles, values, alpha=0.25)
        
        # Set category labels
        self.plot.set_xticks(angles[:-1])
        self.plot.set_xticklabels(categories[:-1])
        
        # Set y-axis limits
        self.plot.set_ylim(0, 100)
        
        # Add title
        self.plot.set_title("Performance Radar Chart")
    
    def create_bar_chart(self):
        """Create a bar chart of performance metrics"""
        # Get performance metrics
        if not hasattr(self, 'current_computer'):
            return
            
        performance = self.current_computer.estimated_performance
        
        # Categories and values
        categories = ['Gaming', 'Productivity', 'Content Creation', 'Development']
        values = [
            performance.get('gaming', 0),
            performance.get('productivity', 0),
            performance.get('content_creation', 0),
            performance.get('development', 0)
        ]
        
        # Create bar chart
        bars = self.plot.bar(categories, values, color='skyblue')
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            self.plot.text(bar.get_x() + bar.get_width()/2., height + 1,
                         f'{height:.1f}', ha='center', va='bottom')
        
        # Add labels and title
        self.plot.set_xlabel('Performance Category')
        self.plot.set_ylabel('Score (0-100)')
        self.plot.set_title('Performance by Category')
        self.plot.set_ylim(0, 110)  # Allow space for labels
    
    def create_heatmap_chart(self):
        """Create a heatmap comparing component quality"""
        # Define components and quality scores
        if not hasattr(self, 'current_computer'):
            return
            
        # Define components and their quality scores (0-10)
        components = ['CPU', 'GPU', 'RAM', 'Storage', 'Motherboard', 'PSU', 'Cooling', 'Case']
        
        # Calculate quality scores based on price and performance
        quality_scores = [
            min(10, self.current_computer.cpu.performance / 10),
            min(10, (self.current_computer.gpu.power / 10) if self.current_computer.gpu else self.current_computer.cpu.integrated_graphics_power / 10),
            min(10, self.current_computer.ram.capacity / 8 + self.current_computer.ram.frequency / 1000),
            min(10, self.current_computer.storage.capacity / 500 + (5 if self.current_computer.storage.type == "SSD" else 0)),
            min(10, self.current_computer.motherboard.price / 1000 * 5),
            min(10, self.current_computer.psu.capacity / 100),
            min(10, self.current_computer.cooling.cooling_capacity / 100),
            min(10, self.current_computer.case.price / 500 * 5)
        ]
        
        # Create heatmap data
        heatmap_data = np.array(quality_scores).reshape(1, -1)
        
        # Create heatmap
        im = self.plot.imshow(heatmap_data, cmap='viridis', aspect='auto')
        
        # Add colorbar
        cbar = self.figure.colorbar(im, ax=self.plot, orientation='vertical', pad=0.01)
        cbar.set_label('Quality Score (0-10)')
        
        # Configure axes
        self.plot.set_yticks([])
        self.plot.set_xticks(np.arange(len(components)))
        self.plot.set_xticklabels(components, rotation=45, ha='right')
        
        # Add value labels
        for i, score in enumerate(quality_scores):
            self.plot.text(i, 0, f'{score:.1f}', ha='center', va='center', color='white', fontweight='bold')
        
        # Add title
        self.plot.set_title('Component Quality Heatmap')
    
    def create_evolution_chart(self):
        """Create a chart showing the evolution of fitness during optimization"""
        if not hasattr(self, 'stats'):
            return
            
        # Get evolution data
        generations = range(len(self.stats['best_fitness_history']))
        best_fitness = self.stats['best_fitness_history']
        avg_fitness = self.stats['avg_fitness_history']
        worst_fitness = self.stats['worst_fitness_history']
        
        # Plot data
        self.plot.plot(generations, best_fitness, 'g-', label='Best Fitness')
        self.plot.plot(generations, avg_fitness, 'b-', label='Average Fitness')
        self.plot.plot(generations, worst_fitness, 'r-', label='Worst Fitness')
        
        # Add labels and title
        self.plot.set_xlabel('Generation')
        self.plot.set_ylabel('Fitness Score')
        self.plot.set_title('Fitness Evolution Over Generations')
        self.plot.legend()
        self.plot.grid(True)
    
    def stop_generation(self):
        """Stop the ongoing generation process"""
        if self.optimization_running:
            self.optimization_running = False
            
            # Reset UI state
            self.reset_ui_after_generation()
            
            # Update status
            self.status_label.config(text="Generation stopped by user")
    
    def reset_ui_after_generation(self):
        """Reset UI elements after generation completes or is stopped"""
        self.generate_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.progress_bar.grid_remove()
        self.optimization_running = False
    
    def reset_form(self):
        """Reset all form fields to default values"""
        # Reset usage
        self.usage_var.set('gaming')
        
        # Reset price range
        self.price_min_var.set('8000')
        self.price_max_var.set('15000')
        self.price_range_slider.set(15000)
        
        # Reset priority
        self.priority_var.set('balanced')
        
        # Reset form factor
        self.form_factor_var.set('ATX')
        
        # Reset future-proofing
        self.future_proof_var.set(False)
        
        # Reset algorithm parameters
        self.population_size_var.set('50')
        self.generations_var.set('100')
        self.crossover_rate_var.set('0.8')
        self.mutation_rate_var.set('0.1')
        self.elitism_var.set('10')
        
        # Reset advanced options
        self.advanced_options_var.set(False)
        self.advanced_frame.grid_remove()
        self.tournament_size_var.set('3')
        self.adaptive_mutation_var.set(True)
        
        # Reset brand preferences
        for comp_type in self.brand_preferences:
            self.brand_preferences[comp_type].set("No Preference")
        
        # Reset aesthetics
        self.rgb_lighting_var.set(False)
        self.case_color_var.set("Black")
        
        # Clear must include/exclude
        if hasattr(self, 'must_include'):
            self.must_include = {}
        if hasattr(self, 'must_exclude'):
            self.must_exclude = {}
        
        # Reset fitness weights
        self.reset_fitness_weights()
        
        # Update status
        self.status_label.config(text="Form reset to default values")
    
    def on_component_selected(self, event):
        """Handle component selection in the components tree"""
        selection = self.components_tree.selection()
        if not selection:
            return
            
        # Get selected item
        item = self.components_tree.item(selection[0])
        component_type = item['values'][0]
        
        # Update component details
        self.show_component_details(component_type)
    
    def show_component_details(self, component_type):
        """Show details for the selected component"""
        if not hasattr(self, 'current_computer'):
            return
            
        # Enable editing of details text
        self.component_details_text.config(state=tk.NORMAL)
        
        # Clear existing text
        self.component_details_text.delete(1.0, tk.END)
        
        # Get component details based on type
        component = None
        if component_type == 'CPU':
            component = self.current_computer.cpu
        elif component_type == 'GPU':
            component = self.current_computer.gpu
        elif component_type == 'RAM':
            component = self.current_computer.ram
        elif component_type == 'Storage':
            component = self.current_computer.storage
        elif component_type.startswith('Storage '):
            index = int(component_type.split(' ')[1]) - 2
            if index < len(self.current_computer.additional_storages):
                component = self.current_computer.additional_storages[index]
        elif component_type == 'Motherboard':
            component = self.current_computer.motherboard
        elif component_type == 'PSU':
            component = self.current_computer.psu
        elif component_type == 'Cooling':
            component = self.current_computer.cooling
        elif component_type == 'Case':
            component = self.current_computer.case
        elif component_type == 'Total':
            # Show summary for total
            self.component_details_text.insert(tk.END, f"Total System Price: ${self.current_computer.price:.2f}\n\n")
            self.component_details_text.insert(tk.END, "Performance Summary:\n")
            for metric, value in self.current_computer.estimated_performance.items():
                self.component_details_text.insert(tk.END, f"{metric.replace('_', ' ').title()}: {value:.1f}/100\n")
            
            # Disable editing and return
            self.component_details_text.config(state=tk.DISABLED)
            return
        
        # If component found, display details
        if component:
            # Get all attributes
            attributes = vars(component)
            
            # Insert title
            self.component_details_text.insert(tk.END, f"{component_type} Details:\n", "title")
            self.component_details_text.insert(tk.END, f"{str(component)}\n\n")
            
            # Insert all attributes
            self.component_details_text.insert(tk.END, "Specifications:\n", "heading")
            for key, value in attributes.items():
                # Skip certain attributes for readability
                if key in ['fitness']:
                    continue
                
                # Format the key name
                formatted_key = key.replace('_', ' ').title()
                
                # Format the value based on type
                if isinstance(value, float):
                    formatted_value = f"{value:.2f}"
                elif isinstance(value, bool):
                    formatted_value = "Yes" if value else "No"
                else:
                    formatted_value = str(value)
                
                self.component_details_text.insert(tk.END, f"{formatted_key}: {formatted_value}\n")
        
        # Add tags for styling
        self.component_details_text.tag_configure("title", font=("TkDefaultFont", 12, "bold"))
        self.component_details_text.tag_configure("heading", font=("TkDefaultFont", 10, "bold"))
        
        # Disable editing
        self.component_details_text.config(state=tk.DISABLED)
    
    def show_replace_component(self):
        """Show dialog to replace a component"""
        # First check if a computer exists and a component is selected
        if not hasattr(self, 'current_computer'):
            messagebox.showinfo("No Computer", "Please generate a computer first.")
            return
            
        selection = self.components_tree.selection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a component to replace.")
            return
            
        # Get selected component type
        item = self.components_tree.item(selection[0])
        component_type = item['values'][0]
        
        # Check if it's a replaceable component
        if component_type == 'Total':
            messagebox.showinfo("Cannot Replace", "Cannot replace the total price entry.")
            return
            
        # Create replacement dialog
        replace_dialog = ctk.CTkToplevel(self.master)
        replace_dialog.title(f"Replace {component_type}")
        replace_dialog.geometry("600x500")
        replace_dialog.transient(self.master)
        replace_dialog.grab_set()
        
        # Create search frame
        search_frame = ttk.Frame(replace_dialog)
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5, pady=5)
        replace_search_var = tk.StringVar()
        replace_search_entry = ttk.Entry(search_frame, textvariable=replace_search_var, width=30)
        replace_search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        search_button = ctk.CTkButton(search_frame, text="Search", 
                                   command=lambda: self.search_replacement_components(replace_list, component_type, replace_search_var.get()))
        search_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Create list of alternative components
        list_frame = ttk.Frame(replace_dialog)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ('name', 'details', 'performance', 'price')
        replace_list = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Define headings and columns
        replace_list.heading('name', text='Name')
        replace_list.heading('details', text='Details')
        replace_list.heading('performance', text='Performance')
        replace_list.heading('price', text='Price')
        
        replace_list.column('name', width=150, anchor='w')
        replace_list.column('details', width=250, anchor='w')
        replace_list.column('performance', width=80, anchor='center')
        replace_list.column('price', width=80, anchor='e')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=replace_list.yview)
        replace_list.configure(yscroll=scrollbar.set)
        
        replace_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Populate the list with alternative components
        self.populate_replacement_components(replace_list, component_type)
        
        # Add buttons
        buttons_frame = ttk.Frame(replace_dialog)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        replace_button = ctk.CTkButton(buttons_frame, text="Replace Component", 
                                     command=lambda: self.replace_component(replace_dialog, replace_list, component_type))
        replace_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        cancel_button = ctk.CTkButton(buttons_frame, text="Cancel", 
                                    command=replace_dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def populate_replacement_components(self, tree_view, component_type):
        """Populate the replacement dialog with alternative components"""
        # Clear existing items
        for item in tree_view.get_children():
            tree_view.delete(item)
            
        # Get components based on type
        components = []
        
        # This would normally come from your data manager
        # For now, add some dummy data
        if component_type == 'CPU':
            components = [
                {"name": "Intel Core i9-14900K", "details": "24 cores, 5.6GHz", "performance": 95, "price": 599.99},
                {"name": "AMD Ryzen 9 7950X", "details": "16 cores, 5.7GHz", "performance": 93, "price": 549.99},
                {"name": "Intel Core i7-14700K", "details": "20 cores, 5.5GHz", "performance": 87, "price": 419.99},
                {"name": "AMD Ryzen 7 7800X3D", "details": "8 cores, 5.0GHz", "performance": 85, "price": 399.99},
                {"name": "Intel Core i5-14600K", "details": "14 cores, 5.3GHz", "performance": 80, "price": 319.99}
            ]
        elif component_type == 'GPU':
            components = [
                {"name": "NVIDIA RTX 4090", "details": "24GB GDDR6X", "performance": 100, "price": 1599.99},
                {"name": "AMD Radeon RX 7900 XTX", "details": "24GB GDDR6", "performance": 90, "price": 999.99},
                {"name": "NVIDIA RTX 4080 Super", "details": "16GB GDDR6X", "performance": 85, "price": 999.99},
                {"name": "AMD Radeon RX 7800 XT", "details": "16GB GDDR6", "performance": 75, "price": 499.99},
                {"name": "NVIDIA RTX 4070 Ti Super", "details": "16GB GDDR6X", "performance": 78, "price": 799.99}
            ]
        elif component_type == 'RAM':
            components = [
                {"name": "G.Skill Trident Z5 RGB", "details": "32GB DDR5-6000", "performance": 95, "price": 229.99},
                {"name": "Corsair Vengeance", "details": "32GB DDR5-5600", "performance": 90, "price": 189.99},
                {"name": "Kingston Fury Beast", "details": "32GB DDR4-3600", "performance": 75, "price": 129.99},
                {"name": "Crucial Ballistix", "details": "16GB DDR4-3200", "performance": 60, "price": 79.99}
            ]
            
        # Add components to tree view
        for component in components:
            tree_view.insert('', 'end', values=(
                component["name"],
                component["details"],
                component["performance"],
                f"${component['price']:.2f}"
            ))
    
    def search_replacement_components(self, tree_view, component_type, search_term):
        """Search for replacements matching the search term"""
        # First repopulate with all components
        self.populate_replacement_components(tree_view, component_type)
        
        # If search term is empty, return
        if not search_term.strip():
            return
            
        # Case-insensitive search through tree items
        search_term = search_term.lower()
        items_to_remove = []
        
        for item_id in tree_view.get_children():
            item = tree_view.item(item_id)
            values = item['values']
            
            # Check if search term is in name or details
            name = str(values[0]).lower()
            details = str(values[1]).lower()
            
            if search_term not in name and search_term not in details:
                items_to_remove.append(item_id)
        
        # Remove non-matching items
        for item_id in items_to_remove:
            tree_view.delete(item_id)
    
    def replace_component(self, dialog, tree_view, component_type):
        """Replace the selected component"""
        # Check if a replacement is selected
        selection = tree_view.selection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a replacement component.")
            return
            
        # Get selected replacement
        item = tree_view.item(selection[0])
        values = item['values']
        
        # Confirm replacement
        confirm = messagebox.askyesno("Confirm Replacement", 
                                     f"Are you sure you want to replace the current {component_type} with {values[0]}?")
        
        if confirm:
            # This would normally update the computer object
            # For now, just show a message
            messagebox.showinfo("Component Replaced", 
                              f"The {component_type} has been replaced with {values[0]} (${float(values[3].replace('$', '')):.2f}).\n\n"
                              "Note: In a complete implementation, this would update the computer configuration.")
            
            # Close the dialog
            dialog.destroy()
    
    def show_alternatives(self):
        """Show alternative components for the selected component"""
        # Similar to show_replace_component but without the replace functionality
        messagebox.showinfo("Show Alternatives", 
                          "This would show alternatives for the selected component.\n\n"
                          "This feature would be similar to the replace component dialog, "
                          "but would focus on showing comparable alternatives with different "
                          "price/performance characteristics.")
    
    def add_to_comparison(self):
        """Add the current computer to the comparison tab"""
        if not hasattr(self, 'current_computer'):
            messagebox.showinfo("No Computer", "Please generate a computer first.")
            return
            
        # Create a name for this configuration
        timestamp = datetime.now().strftime("%H:%M:%S")
        config_name = f"Config {len(self.generated_computers) + 1} ({timestamp})"
        
        # Add to generated computers list
        self.generated_computers.append({
            "name": config_name,
            "computer": self.current_computer,
            "stats": getattr(self, 'stats', {})
        })
        
        # Update comparison tab
        self.update_comparison_tab()
        
        # Switch to comparison tab
        self.notebook.select(2)  # Index of the Comparison tab
        
        # Show confirmation
        messagebox.showinfo("Added to Comparison", 
                          f"Computer configuration '{config_name}' has been added to the comparison tab.")
    
    def update_comparison_tab(self):
        """Update the comparison tab with all generated computers"""
        # Clear existing comparison
        for widget in self.comparison_container.winfo_children():
            widget.destroy()
            
        # If no computers to compare, show message
        if not self.generated_computers:
            ttk.Label(self.comparison_container, text="Add configurations to compare them side by side...").pack(padx=20, pady=20)
            return
            
        # Create comparison table
        table_frame = ttk.Frame(self.comparison_container)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create headers
        ttk.Label(table_frame, text="Component", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Add computer names as column headers
        for i, config in enumerate(self.generated_computers):
            ttk.Label(table_frame, text=config["name"], font=("TkDefaultFont", 10, "bold")).grid(row=0, column=i+1, sticky="w", padx=5, pady=5)
            
            # Add remove button
            remove_button = ttk.Button(table_frame, text="X", width=2,
                                     command=lambda idx=i: self.remove_from_comparison(idx))
            remove_button.grid(row=0, column=i+1, sticky="e", padx=5, pady=5)
        
        # Add component rows
        component_types = [
            "CPU", "GPU", "RAM", "Storage", "Motherboard", 
            "PSU", "Cooling", "Case", "Price", "Performance"
        ]
        
        for row, comp_type in enumerate(component_types):
            # Add row header
            ttk.Label(table_frame, text=comp_type).grid(row=row+1, column=0, sticky="w", padx=5, pady=5)
            
            # Add component details for each configuration
            for col, config in enumerate(self.generated_computers):
                computer = config["computer"]
                
                # Get component details based on type
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
                
                # Add to table
                ttk.Label(table_frame, text=value, wraplength=200).grid(row=row+1, column=col+1, sticky="w", padx=5, pady=5)
        
        # Add performance comparison chart
        self.add_comparison_chart()
    
    def add_comparison_chart(self):
        """Add a chart comparing performance of all configurations"""
        if not self.generated_computers:
            return
            
        # Create frame for chart
        chart_frame = ttk.LabelFrame(self.comparison_container, text="Performance Comparison")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create figure for matplotlib
        figure = Figure(figsize=(10, 6), dpi=100)
        plot = figure.add_subplot(111)
        
        # Prepare data
        config_names = []
        gaming_scores = []
        productivity_scores = []
        content_creation_scores = []
        development_scores = []
        
        for config in self.generated_computers:
            computer = config["computer"]
            config_names.append(config["name"])
            gaming_scores.append(computer.estimated_performance.get('gaming', 0))
            productivity_scores.append(computer.estimated_performance.get('productivity', 0))
            content_creation_scores.append(computer.estimated_performance.get('content_creation', 0))
            development_scores.append(computer.estimated_performance.get('development', 0))
        
        # Set up positions for bars
        x = np.arange(len(config_names))
        width = 0.2
        
        # Create bars
        plot.bar(x - 1.5*width, gaming_scores, width, label='Gaming')
        plot.bar(x - 0.5*width, productivity_scores, width, label='Productivity')
        plot.bar(x + 0.5*width, content_creation_scores, width, label='Content Creation')
        plot.bar(x + 1.5*width, development_scores, width, label='Development')
        
        # Add labels and legend
        plot.set_xlabel('Configuration')
        plot.set_ylabel('Performance Score')
        plot.set_title('Performance Comparison')
        plot.set_xticks(x)
        plot.set_xticklabels(config_names, rotation=45, ha='right')
        plot.legend()
        plot.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Adjust layout
        figure.tight_layout()
        
        # Create canvas for matplotlib figure
        canvas = FigureCanvasTkAgg(figure, chart_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def remove_from_comparison(self, index):
        """Remove a configuration from the comparison"""
        if 0 <= index < len(self.generated_computers):
            # Get config name for message
            config_name = self.generated_computers[index]["name"]
            
            # Remove from list
            self.generated_computers.pop(index)
            
            # Update comparison tab
            self.update_comparison_tab()
            
            # Show confirmation
            self.status_label.config(text=f"Removed '{config_name}' from comparison")
    
    def clear_comparison(self):
        """Clear all configurations from comparison"""
        if not self.generated_computers:
            return
            
        # Confirm clearing
        confirm = messagebox.askyesno("Confirm Clear", 
                                    "Are you sure you want to clear all configurations from comparison?")
        
        if confirm:
            # Clear the list
            self.generated_computers = []
            
            # Update comparison tab
            self.update_comparison_tab()
            
            # Show confirmation
            self.status_label.config(text="Cleared all configurations from comparison")
    
    def export_comparison(self):
        """Export comparison to a file"""
        if not self.generated_computers:
            messagebox.showinfo("No Configurations", "No configurations to export.")
            return
            
        # Ask for file name
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("HTML files", "*.html"), ("CSV files", "*.csv")])
        
        if not file_path:
            return
            
        # Determine export format based on extension
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            # Export as PDF
            messagebox.showinfo("Export", f"Exporting comparison to PDF: {file_path}\n\n"
                              "This would generate a PDF report of the comparison.")
        elif file_ext == '.html':
            # Export as HTML
            messagebox.showinfo("Export", f"Exporting comparison to HTML: {file_path}\n\n"
                              "This would generate an HTML report of the comparison.")
        elif file_ext == '.csv':
            # Export as CSV
            messagebox.showinfo("Export", f"Exporting comparison to CSV: {file_path}\n\n"
                              "This would generate a CSV file with the comparison data.")
        else:
            messagebox.showinfo("Unknown Format", f"Unknown export format: {file_ext}")
    
    def export_chart(self):
        """Export the current visualization chart to a file"""
        if not hasattr(self, 'figure'):
            messagebox.showinfo("No Chart", "No chart to export.")
            return
            
        # Ask for file name
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")])
        
        if not file_path:
            return
            
        # Save the figure
        try:
            self.figure.savefig(file_path, dpi=300, bbox_inches='tight')
            messagebox.showinfo("Export Successful", f"Chart exported to: {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Error exporting chart: {str(e)}")
    
    def update_component_browser(self, event=None):
        """Update the component browser with components of the selected type"""
        # Get selected component type
        component_type = self.component_type_var.get()
        
        # Clear existing components
        for item in self.components_browser.get_children():
            self.components_browser.delete(item)
        
        # Update component-specific filters
        self.update_specific_filters(component_type)
        
        # Get components from data manager
        components = self.get_component_browser_data(component_type)
        
        # Add components to browser
        for component in components:
            self.components_browser.insert('', 'end', values=(
                component["name"],
                component["details"],
                component["performance"],
                component["price"]
            ))
        
        # Update brand filter dropdown
        self.update_brand_filter_list(component_type, components)
    
    def update_specific_filters(self, component_type):
        """Update the component-specific filter options"""
        # Clear existing filters
        for widget in self.specific_filters_frame.winfo_children():
            widget.destroy()
        
        # Add filters based on component type
        if component_type == 'cpu':
            # Add CPU-specific filters
            ttk.Label(self.specific_filters_frame, text="Min Cores:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            self.cpu_cores_var = tk.StringVar(value="0")
            cpu_cores_entry = ttk.Entry(self.specific_filters_frame, textvariable=self.cpu_cores_var, width=5)
            cpu_cores_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Label(self.specific_filters_frame, text="Integrated Graphics:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            self.cpu_igpu_var = tk.BooleanVar(value=False)
            cpu_igpu_check = ttk.Checkbutton(self.specific_filters_frame, variable=self.cpu_igpu_var)
            cpu_igpu_check.grid(row=1, column=1, sticky="w", padx=5, pady=2)
            
        elif component_type == 'gpu':
            # Add GPU-specific filters
            ttk.Label(self.specific_filters_frame, text="Min VRAM (GB):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            self.gpu_vram_var = tk.StringVar(value="0")
            gpu_vram_entry = ttk.Entry(self.specific_filters_frame, textvariable=self.gpu_vram_var, width=5)
            gpu_vram_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Label(self.specific_filters_frame, text="Ray Tracing:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            self.gpu_rt_var = tk.BooleanVar(value=False)
            gpu_rt_check = ttk.Checkbutton(self.specific_filters_frame, variable=self.gpu_rt_var)
            gpu_rt_check.grid(row=1, column=1, sticky="w", padx=5, pady=2)
            
        elif component_type == 'ram':
            # Add RAM-specific filters
            ttk.Label(self.specific_filters_frame, text="Min Capacity (GB):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            self.ram_capacity_var = tk.StringVar(value="0")
            ram_capacity_entry = ttk.Entry(self.specific_filters_frame, textvariable=self.ram_capacity_var, width=5)
            ram_capacity_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Label(self.specific_filters_frame, text="Type:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            self.ram_type_var = tk.StringVar(value="Any")
            ram_type_combo = ttk.Combobox(self.specific_filters_frame, textvariable=self.ram_type_var, 
                                        values=["Any", "DDR4", "DDR5"], width=10, state="readonly")
            ram_type_combo.grid(row=1, column=1, sticky="w", padx=5, pady=2)
            
        elif component_type == 'storage':
            # Add Storage-specific filters
            ttk.Label(self.specific_filters_frame, text="Min Capacity (GB):").grid(row=0, column=0, sticky="w", padx=5, pady=2)
            self.storage_capacity_var = tk.StringVar(value="0")
            storage_capacity_entry = ttk.Entry(self.specific_filters_frame, textvariable=self.storage_capacity_var, width=5)
            storage_capacity_entry.grid(row=0, column=1, sticky="w", padx=5, pady=2)
            
            ttk.Label(self.specific_filters_frame, text="Type:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
            self.storage_type_var = tk.StringVar(value="Any")
            storage_type_combo = ttk.Combobox(self.specific_filters_frame, textvariable=self.storage_type_var, 
                                            values=["Any", "SSD", "HDD"], width=10, state="readonly")
            storage_type_combo.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # Add apply filters button
        apply_button = ctk.CTkButton(self.specific_filters_frame, text="Apply Filters", 
                                   command=self.apply_specific_filters,
                                   width=20)
        apply_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    
    def update_brand_filter_list(self, component_type, components):
        """Update the brand filter dropdown based on available components"""
        # Extract all unique brands
        brands = set()
        for component in components:
            # Extract brand from name (usually the first word)
            name_parts = component["name"].split()
            if name_parts:
                brands.add(name_parts[0])
        
        # Update dropdown values
        brands_list = ["All"] + sorted(list(brands))
        self.brand_filter_list.configure(values=brands_list)
        self.brand_filter_var.set("All")
    
    def get_component_browser_data(self, component_type):
        """Get component data for the browser"""
        # This would normally come from your data manager
        # For now, return some dummy data based on the component type
        dummy_data = {
            'cpu': [
                {"name": "Intel Core i9-14900K", "details": "24 cores, 5.6GHz", "performance": "95/100", "price": "$599.99"},
                {"name": "AMD Ryzen 9 7950X", "details": "16 cores, 5.7GHz", "performance": "93/100", "price": "$549.99"},
                {"name": "Intel Core i7-14700K", "details": "20 cores, 5.5GHz", "performance": "87/100", "price": "$419.99"},
                {"name": "AMD Ryzen 7 7800X3D", "details": "8 cores, 5.0GHz", "performance": "85/100", "price": "$399.99"},
                {"name": "Intel Core i5-14600K", "details": "14 cores, 5.3GHz", "performance": "80/100", "price": "$319.99"}
            ],
            'gpu': [
                {"name": "NVIDIA RTX 4090", "details": "24GB GDDR6X", "performance": "100/100", "price": "$1599.99"},
                {"name": "AMD Radeon RX 7900 XTX", "details": "24GB GDDR6", "performance": "90/100", "price": "$999.99"},
                {"name": "NVIDIA RTX 4080 Super", "details": "16GB GDDR6X", "performance": "85/100", "price": "$999.99"},
                {"name": "AMD Radeon RX 7800 XT", "details": "16GB GDDR6", "performance": "75/100", "price": "$499.99"},
                {"name": "NVIDIA RTX 4070 Ti Super", "details": "16GB GDDR6X", "performance": "78/100", "price": "$799.99"}
            ],
            'ram': [
                {"name": "G.Skill Trident Z5 RGB", "details": "32GB DDR5-6000", "performance": "95/100", "price": "$229.99"},
                {"name": "Corsair Vengeance", "details": "32GB DDR5-5600", "performance": "90/100", "price": "$189.99"},
                {"name": "Kingston Fury Beast", "details": "32GB DDR4-3600", "performance": "75/100", "price": "$129.99"},
                {"name": "Crucial Ballistix", "details": "16GB DDR4-3200", "performance": "60/100", "price": "$79.99"}
            ],
            'storage': [
                {"name": "Samsung 990 Pro", "details": "2TB NVMe SSD", "performance": "95/100", "price": "$229.99"},
                {"name": "WD Black SN850X", "details": "1TB NVMe SSD", "performance": "92/100", "price": "$149.99"},
                {"name": "Crucial T700", "details": "2TB NVMe SSD", "performance": "90/100", "price": "$199.99"},
                {"name": "Samsung 870 EVO", "details": "1TB SATA SSD", "performance": "70/100", "price": "$89.99"},
                {"name": "Seagate Barracuda", "details": "2TB 7200RPM HDD", "performance": "40/100", "price": "$54.99"}
            ],
            'motherboard': [
                {"name": "ASUS ROG Maximus Z790 Hero", "details": "Intel Z790, DDR5", "performance": "95/100", "price": "$629.99"},
                {"name": "Gigabyte X670E Aorus Master", "details": "AMD X670E, DDR5", "performance": "93/100", "price": "$499.99"},
                {"name": "MSI MPG Z790 Carbon WiFi", "details": "Intel Z790, DDR5", "performance": "90/100", "price": "$399.99"},
                {"name": "ASRock B650E Steel Legend", "details": "AMD B650E, DDR5", "performance": "85/100", "price": "$249.99"},
                {"name": "ASUS TUF Gaming B760M-PLUS", "details": "Intel B760, DDR5", "performance": "80/100", "price": "$179.99"}
            ],
            'psu': [
                {"name": "Corsair RM850x", "details": "850W, 80+ Gold", "performance": "90/100", "price": "$139.99"},
                {"name": "Seasonic Prime TX-1000", "details": "1000W, 80+ Titanium", "performance": "95/100", "price": "$279.99"},
                {"name": "EVGA SuperNOVA 750 G5", "details": "750W, 80+ Gold", "performance": "88/100", "price": "$119.99"},
                {"name": "be quiet! Dark Power Pro 12", "details": "1500W, 80+ Titanium", "performance": "98/100", "price": "$449.99"},
                {"name": "Thermaltake Toughpower GF3", "details": "850W, 80+ Gold", "performance": "87/100", "price": "$129.99"}
            ],
            'cooling': [
                {"name": "Noctua NH-D15", "details": "Air Cooler, Dual Fan", "performance": "90/100", "price": "$99.99"},
                {"name": "ARCTIC Liquid Freezer II 360", "details": "360mm AIO", "performance": "95/100", "price": "$129.99"},
                {"name": "Corsair iCUE H150i Elite", "details": "360mm AIO, RGB", "performance": "93/100", "price": "$169.99"},
                {"name": "be quiet! Dark Rock Pro 4", "details": "Air Cooler", "performance": "88/100", "price": "$89.99"},
                {"name": "Lian Li Galahad 240", "details": "240mm AIO, RGB", "performance": "85/100", "price": "$109.99"}
            ],
            'case': [
                {"name": "Lian Li O11 Dynamic EVO", "details": "Mid Tower, Tempered Glass", "performance": "95/100", "price": "$179.99"},
                {"name": "Corsair 5000D Airflow", "details": "Mid Tower, Mesh", "performance": "93/100", "price": "$149.99"},
                {"name": "Fractal Design Meshify 2", "details": "Mid Tower, Mesh", "performance": "90/100", "price": "$159.99"},
                {"name": "NZXT H510 Flow", "details": "Mid Tower, Mesh", "performance": "85/100", "price": "$89.99"},
                {"name": "Phanteks Eclipse P500A", "details": "Mid Tower, Mesh", "performance": "92/100", "price": "$139.99"}
            ]
        }
        
        return dummy_data.get(component_type, [])
    
    def search_components(self):
        """Search for components matching the search term"""
        # Get selected component type
        component_type = self.component_type_var.get()
        
        # Get search term
        search_term = self.search_var.get().lower()
        
        # Clear existing components
        for item in self.components_browser.get_children():
            self.components_browser.delete(item)
        
        # Get all components of this type
        components = self.get_component_browser_data(component_type)
        
        # Filter by search term if provided
        if search_term:
            filtered_components = []
            for component in components:
                if (search_term in component["name"].lower() or 
                    search_term in component["details"].lower()):
                    filtered_components.append(component)
            components = filtered_components
        
        # Add filtered components to browser
        for component in components:
            self.components_browser.insert('', 'end', values=(
                component["name"],
                component["details"],
                component["performance"],
                component["price"]
            ))
    
    def apply_price_filter(self):
        """Apply price filter to component browser"""
        # Get selected component type
        component_type = self.component_type_var.get()
        
        # Get price range
        try:
            min_price = float(self.price_filter_min_var.get())
            max_price = float(self.price_filter_max_var.get())
        except ValueError:
            messagebox.showinfo("Invalid Price", "Please enter valid numbers for price range.")
            return
        
        # Clear existing components
        for item in self.components_browser.get_children():
            self.components_browser.delete(item)
        
        # Get all components of this type
        components = self.get_component_browser_data(component_type)
        
        # Filter by price range
        filtered_components = []
        for component in components:
            # Parse price string (remove $ and convert to float)
            price = float(component["price"].replace('$', ''))
            if min_price <= price <= max_price:
                filtered_components.append(component)
        
        # Add filtered components to browser
        for component in filtered_components:
            self.components_browser.insert('', 'end', values=(
                component["name"],
                component["details"],
                component["performance"],
                component["price"]
            ))
    
    def apply_brand_filter(self, event=None):
        """Apply brand filter to component browser"""
        # Get selected component type
        component_type = self.component_type_var.get()
        
        # Get selected brand
        brand = self.brand_filter_var.get()
        
        # If "All" selected, reset to show all brands
        if brand == "All":
            self.update_component_browser()
            return
        
        # Clear existing components
        for item in self.components_browser.get_children():
            self.components_browser.delete(item)
        
        # Get all components of this type
        components = self.get_component_browser_data(component_type)
        
        # Filter by brand
        filtered_components = []
        for component in components:
            # Extract brand from name (usually the first word)
            name_parts = component["name"].split()
            if name_parts and name_parts[0] == brand:
                filtered_components.append(component)
        
        # Add filtered components to browser
        for component in filtered_components:
            self.components_browser.insert('', 'end', values=(
                component["name"],
                component["details"],
                component["performance"],
                component["price"]
            ))
    
    def apply_specific_filters(self):
        """Apply component-specific filters"""
        # Get selected component type
        component_type = self.component_type_var.get()
        
        # Clear existing components
        for item in self.components_browser.get_children():
            self.components_browser.delete(item)
        
        # Get all components of this type
        components = self.get_component_browser_data(component_type)
        
        # Apply filters based on component type
        filtered_components = components
        
        if component_type == 'cpu':
            # Filter by cores
            try:
                min_cores = int(self.cpu_cores_var.get())
                filtered_components = []
                for component in components:
                    # Extract cores from details (e.g., "24 cores, 5.6GHz")
                    cores_text = component["details"].split(',')[0].strip()
                    cores = int(cores_text.split()[0])
                    if cores >= min_cores:
                        filtered_components.append(component)
            except (ValueError, IndexError):
                pass
            
            # Filter by integrated graphics if needed
            if self.cpu_igpu_var.get():
                filtered_components = [c for c in filtered_components if "iGPU" in c["details"]]
                
        elif component_type == 'gpu':
            # Filter by VRAM
            try:
                min_vram = int(self.gpu_vram_var.get())
                filtered_components = []
                for component in components:
                    # Extract VRAM from details (e.g., "24GB GDDR6X")
                    vram_text = component["details"].split()[0].strip()
                    vram = int(vram_text.replace('GB', ''))
                    if vram >= min_vram:
                        filtered_components.append(component)
            except (ValueError, IndexError):
                pass
            
            # Filter by ray tracing if needed
            if self.gpu_rt_var.get():
                filtered_components = [c for c in filtered_components if "RTX" in c["name"]]
                
        elif component_type == 'ram':
            # Filter by capacity
            try:
                min_capacity = int(self.ram_capacity_var.get())
                filtered_components = []
                for component in components:
                    # Extract capacity from details (e.g., "32GB DDR5-6000")
                    capacity_text = component["details"].split()[0].strip()
                    capacity = int(capacity_text.replace('GB', ''))
                    if capacity >= min_capacity:
                        filtered_components.append(component)
            except (ValueError, IndexError):
                pass
            
            # Filter by RAM type if not "Any"
            ram_type = self.ram_type_var.get()
            if ram_type != "Any":
                filtered_components = [c for c in filtered_components if ram_type in c["details"]]
                
        elif component_type == 'storage':
            # Filter by capacity
            try:
                min_capacity = int(self.storage_capacity_var.get())
                filtered_components = []
                for component in components:
                    # Extract capacity from details (e.g., "2TB NVMe SSD")
                    capacity_text = component["details"].split()[0].strip()
                    multiplier = 1
                    if 'TB' in capacity_text:
                        multiplier = 1000
                    capacity = int(float(capacity_text.replace('TB', '').replace('GB', '')) * multiplier)
                    if capacity >= min_capacity:
                        filtered_components.append(component)
            except (ValueError, IndexError):
                pass
            
            # Filter by storage type if not "Any"
            storage_type = self.storage_type_var.get()
            if storage_type != "Any":
                filtered_components = [c for c in filtered_components if storage_type in c["details"]]
        
        # Add filtered components to browser
        for component in filtered_components:
            self.components_browser.insert('', 'end', values=(
                component["name"],
                component["details"],
                component["performance"],
                component["price"]
            ))
    
    def reset_component_filters(self):
        """Reset all component filters to defaults"""
        # Reset price filter
        self.price_filter_min_var.set("0")
        self.price_filter_max_var.set("50000")
        
        # Reset brand filter
        self.brand_filter_var.set("All")
        
        # Reset search field
        self.search_var.set("")
        
        # Reset component-specific filters
        component_type = self.component_type_var.get()
        if component_type == 'cpu':
            self.cpu_cores_var.set("0")
            self.cpu_igpu_var.set(False)
        elif component_type == 'gpu':
            self.gpu_vram_var.set("0")
            self.gpu_rt_var.set(False)
        elif component_type == 'ram':
            self.ram_capacity_var.set("0")
            self.ram_type_var.set("Any")
        elif component_type == 'storage':
            self.storage_capacity_var.set("0")
            self.storage_type_var.set("Any")
        
        # Refresh the component browser
        self.update_component_browser()
    
    def show_component_context_menu(self, event):
        """Show context menu for component browser"""
        # Get selected item
        item = self.components_browser.identify_row(event.y)
        if not item:
            return
            
        # Select the item
        self.components_browser.selection_set(item)
        
        # Show context menu
        self.component_context_menu.post(event.x_root, event.y_root)
    
    def view_component_details(self):
        """View details of selected component in browser"""
        selection = self.components_browser.selection()
        if not selection:
            return
            
        # Get selected item
        item = self.components_browser.item(selection[0])
        values = item['values']
        
        # Create details dialog
        details_dialog = ctk.CTkToplevel(self.master)
        details_dialog.title(f"Component Details: {values[0]}")
        details_dialog.geometry("500x400")
        details_dialog.transient(self.master)
        details_dialog.grab_set()
        
        # Create details text
        details_text = ScrolledText(details_dialog, wrap=tk.WORD, width=60, height=20)
        details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add component details
        details_text.insert(tk.END, f"Name: {values[0]}\n\n", "heading")
        details_text.insert(tk.END, f"Details: {values[1]}\n\n")
        details_text.insert(tk.END, f"Performance: {values[2]}\n\n")
        details_text.insert(tk.END, f"Price: {values[3]}\n\n")
        
        # Add some dummy specifications based on component type
        component_type = self.component_type_var.get()
        details_text.insert(tk.END, "Specifications:\n", "heading")
        
        if component_type == 'cpu':
            details_text.insert(tk.END, "Architecture: Zen 4 / Intel Core\n")
            details_text.insert(tk.END, "Socket: AM5 / LGA1700\n")
            details_text.insert(tk.END, "TDP: 105W / 125W\n")
            details_text.insert(tk.END, "Max Temp: 95°C\n")
            details_text.insert(tk.END, "Manufacturing Process: 5nm / 7nm\n")
            details_text.insert(tk.END, "Release Date: Q3 2023\n")
        elif component_type == 'gpu':
            details_text.insert(tk.END, "Architecture: Ada Lovelace / RDNA 3\n")
            details_text.insert(tk.END, "Boost Clock: 2.5 GHz\n")
            details_text.insert(tk.END, "Memory Bandwidth: 1008 GB/s\n")
            details_text.insert(tk.END, "Power Consumption: 285W - 450W\n")
            details_text.insert(tk.END, "CUDA Cores / Stream Processors: 16384\n")
            details_text.insert(tk.END, "Release Date: Q4 2022\n")
        
        # Add styling
        details_text.tag_configure("heading", font=("TkDefaultFont", 12, "bold"))
        
        # Disable editing
        details_text.config(state=tk.DISABLED)
        
        # Add close button
        close_button = ctk.CTkButton(details_dialog, text="Close", 
                                   command=details_dialog.destroy)
        close_button.pack(pady=10)
    
    def add_component_to_build(self):
        """Add selected component from browser to current build"""
        selection = self.components_browser.selection()
        if not selection:
            return
            
        # Get selected item
        item = self.components_browser.item(selection[0])
        values = item['values']
        
        # Check if we have a current computer
        if not hasattr(self, 'current_computer'):
            messagebox.showinfo("No Computer", "Please generate a computer first.")
            return
            
        # Get component type
        component_type = self.component_type_var.get()
        
        # Confirm replacement
        confirm = messagebox.askyesno("Confirm Addition", 
                                    f"Do you want to replace the current {component_type} with {values[0]}?")
        
        if confirm:
            # This would normally update the computer object
            # For now, just show a message
            messagebox.showinfo("Component Added", 
                              f"The {component_type} has been replaced with {values[0]} (${values[3]}).\n\n"
                              "Note: In a complete implementation, this would update the computer configuration.")
    
    def compare_with_current(self):
        """Compare selected component with current build's component"""
        selection = self.components_browser.selection()
        if not selection:
            return
            
        # Get selected item
        item = self.components_browser.item(selection[0])
        values = item['values']
        
        # Check if we have a current computer
        if not hasattr(self, 'current_computer'):
            messagebox.showinfo("No Computer", "Please generate a computer first.")
            return
            
        # Get component type
        component_type = self.component_type_var.get()
        
        # Create comparison dialog
        compare_dialog = ctk.CTkToplevel(self.master)
        compare_dialog.title(f"Component Comparison: {component_type}")
        compare_dialog.geometry("700x500")
        compare_dialog.transient(self.master)
        compare_dialog.grab_set()
        
        # Create comparison frame
        compare_frame = ttk.Frame(compare_dialog)
        compare_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Configure grid
        compare_frame.grid_columnconfigure(0, weight=1)
        compare_frame.grid_columnconfigure(1, weight=1)
        
        # Add headers
        ttk.Label(compare_frame, text="Current Component", font=("TkDefaultFont", 12, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
        ttk.Label(compare_frame, text="Selected Component", font=("TkDefaultFont", 12, "bold")).grid(row=0, column=1, sticky="w", padx=10, pady=5)
        
        # Get current component details
        current_component = None
        if component_type == 'cpu':
            current_component = self.current_computer.cpu
        elif component_type == 'gpu':
            current_component = self.current_computer.gpu
        elif component_type == 'ram':
            current_component = self.current_computer.ram
        elif component_type == 'storage':
            current_component = self.current_computer.storage
        elif component_type == 'motherboard':
            current_component = self.current_computer.motherboard
        elif component_type == 'psu':
            current_component = self.current_computer.psu
        elif component_type == 'cooling':
            current_component = self.current_computer.cooling
        elif component_type == 'case':
            current_component = self.current_computer.case
        
        # Create component details text areas
        current_text = ScrolledText(compare_frame, wrap=tk.WORD, width=40, height=20)
        current_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        selected_text = ScrolledText(compare_frame, wrap=tk.WORD, width=40, height=20)
        selected_text.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        
        # Add current component details
        if current_component:
            current_text.insert(tk.END, f"Name: {str(current_component)}\n\n", "heading")
            
            # Get all attributes
            attributes = vars(current_component)
            
            # Insert all attributes
            current_text.insert(tk.END, "Specifications:\n", "heading")
            for key, value in attributes.items():
                # Skip certain attributes for readability
                if key in ['fitness']:
                    continue
                
                # Format the key name
                formatted_key = key.replace('_', ' ').title()
                
                # Format the value based on type
                if isinstance(value, float):
                    formatted_value = f"{value:.2f}"
                elif isinstance(value, bool):
                    formatted_value = "Yes" if value else "No"
                else:
                    formatted_value = str(value)
                
                current_text.insert(tk.END, f"{formatted_key}: {formatted_value}\n")
        else:
            current_text.insert(tk.END, "No current component available.")
        
        # Add selected component details
        selected_text.insert(tk.END, f"Name: {values[0]}\n\n", "heading")
        selected_text.insert(tk.END, f"Details: {values[1]}\n\n")
        selected_text.insert(tk.END, f"Performance: {values[2]}\n\n")
        selected_text.insert(tk.END, f"Price: {values[3]}\n\n")
        
        # Add styling
        current_text.tag_configure("heading", font=("TkDefaultFont", 11, "bold"))
        selected_text.tag_configure("heading", font=("TkDefaultFont", 11, "bold"))
        
        # Disable editing
        current_text.config(state=tk.DISABLED)
        selected_text.config(state=tk.DISABLED)
        
        # Add comparison metrics
        metrics_frame = ttk.LabelFrame(compare_dialog, text="Comparison Metrics")
        metrics_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Use a grid for metrics
        metrics_frame.grid_columnconfigure(0, weight=1)
        metrics_frame.grid_columnconfigure(1, weight=1)
        metrics_frame.grid_columnconfigure(2, weight=1)
        
        # Add metric headers
        ttk.Label(metrics_frame, text="Metric", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(metrics_frame, text="Current", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=1, sticky="w", padx=5, pady=2)
        ttk.Label(metrics_frames, text="Selected", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=2, sticky="w", padx=5, pady=2)
        
        # Add dummy comparison metrics based on component type
        if component_type == 'cpu':
            # Add CPU comparison metrics
            metrics = [
                ("Performance Score", "76/100", values[2]),
                ("Price", "$389.99", values[3]),
                ("Price/Performance", "0.19", "0.18"),
                ("Power Consumption", "125W", "105W"),
                ("Cooling Requirements", "High", "Medium")
            ]
        elif component_type == 'gpu':
            # Add GPU comparison metrics
            metrics = [
                ("Performance Score", "82/100", values[2]),
                ("Price", "$699.99", values[3]),
                ("Price/Performance", "0.12", "0.13"),
                ("Power Consumption", "300W", "250W"),
                ("Ray Tracing Performance", "High", "Medium")
            ]
        else:
            # Generic metrics for other components
            metrics = [
                ("Performance Score", "80/100", values[2]),
                ("Price", "$199.99", values[3]),
                ("Value Rating", "Good", "Better"),
                ("Compatibility Score", "Perfect", "Good"),
                ("Future Compatibility", "Good", "Excellent")
            ]
        
        # Add metrics to grid
        for i, (metric, current, selected) in enumerate(metrics):
            ttk.Label(metrics_frame, text=metric).grid(row=i+1, column=0, sticky="w", padx=5, pady=2)
            ttk.Label(metrics_frame, text=current).grid(row=i+1, column=1, sticky="w", padx=5, pady=2)
            ttk.Label(metrics_frame, text=selected).grid(row=i+1, column=2, sticky="w", padx=5, pady=2)
        
        # Add recommendation
        recommendation_frame = ttk.Frame(compare_dialog)
        recommendation_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(recommendation_frame, text="Recommendation:", font=("TkDefaultFont", 11, "bold")).pack(anchor="w")
        ttk.Label(recommendation_frame, text="The selected component offers better value for money with similar performance. Consider upgrading if budget allows.", wraplength=680).pack(anchor="w", pady=5)
        
        # Add buttons
        buttons_frame = ttk.Frame(compare_dialog)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        replace_button = ctk.CTkButton(buttons_frame, text="Replace Component", 
                                     command=lambda: self.replace_from_comparison(compare_dialog, component_type, values))
        replace_button.pack(side=tk.RIGHT, padx=10)
        
        close_button = ctk.CTkButton(buttons_frame, text="Close", 
                                   command=compare_dialog.destroy)
        close_button.pack(side=tk.RIGHT, padx=10)
    
    def replace_from_comparison(self, dialog, component_type, values):
        """Replace component from comparison dialog"""
        # This would normally update the computer object
        # For now, just show a message
        messagebox.showinfo("Component Replaced", 
                          f"The {component_type} has been replaced with {values[0]} ({values[3]}).\n\n"
                          "Note: In a complete implementation, this would update the computer configuration.")
        
        # Close the dialog
        dialog.destroy()
    
    # File and settings operations
    def new_configuration(self):
        """Start a new configuration"""
        # Confirm if there's an existing configuration
        if hasattr(self, 'current_computer'):
            confirm = messagebox.askyesno("Confirm New Configuration", 
                                        "This will clear the current configuration. Continue?")
            if not confirm:
                return
        
        # Reset form
        self.reset_form()
        
        # Clear current computer
        if hasattr(self, 'current_computer'):
            delattr(self, 'current_computer')
        
        # Clear results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Generate a computer to see results here...")
        self.results_text.config(state=tk.DISABLED)
        
        # Clear components tree
        for item in self.components_tree.get_children():
            self.components_tree.delete(item)
        
        # Clear performance bars
        for metric in ['gaming', 'productivity', 'content_creation', 'development']:
            self.performance_vars[metric].set(0)
            if f"{metric}_label" in self.performance_vars:
                self.performance_vars[f"{metric}_label"].config(text="0/100")
        
        # Reset visualization
        self.plot.clear()
        self.plot.text(0.5, 0.5, "Generate a computer to visualize performance data", 
                     horizontalalignment='center', verticalalignment='center',
                     transform=self.plot.transAxes, fontsize=14)
        self.plot.axis('off')
        self.chart_canvas.draw()
        
        # Update status
        self.status_label.config(text="New configuration started")
    
    def open_configuration(self):
        """Open a saved configuration"""
        # Ask for file
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        
        if not file_path:
            return
            
        try:
            # This would normally load the configuration from file
            # For now, just show a message
            messagebox.showinfo("Open Configuration", 
                              f"This would load a configuration from: {file_path}\n\n"
                              "Note: In a complete implementation, this would load a computer configuration "
                              "from the selected file.")
            
            # Update status
            self.status_label.config(text=f"Configuration loaded from {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error Opening Configuration", f"Error: {str(e)}")
    
    def save_configuration(self):
        """Save the current configuration"""
        # Check if there's a configuration to save
        if not hasattr(self, 'current_computer'):
            messagebox.showinfo("No Configuration", "No computer configuration to save.")
            return
            
        # Ask for file name
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")])
        
        if not file_path:
            return
            
        try:
            # This would normally save the configuration to file
            # For now, just show a message
            messagebox.showinfo("Save Configuration", 
                              f"This would save the current configuration to: {file_path}\n\n"
                              "Note: In a complete implementation, this would save the computer configuration "
                              "to the selected file.")
            
            # Update status
            self.status_label.config(text=f"Configuration saved to {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error Saving Configuration", f"Error: {str(e)}")
    
    def export_results(self):
        """Export the current results to a file"""
        # Check if there's a configuration to export
        if not hasattr(self, 'current_computer'):
            messagebox.showinfo("No Configuration", "No computer configuration to export.")
            return
            
        # Ask for file name
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("HTML files", "*.html"), ("Text files", "*.txt")])
        
        if not file_path:
            return
            
        # Determine export format based on extension
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.pdf':
                # Export as PDF
                messagebox.showinfo("Export", f"Exporting configuration to PDF: {file_path}\n\n"
                                 "This would generate a PDF report of the configuration.")
            elif file_ext == '.html':
                # Export as HTML
                messagebox.showinfo("Export", f"Exporting configuration to HTML: {file_path}\n\n"
                                 "This would generate an HTML report of the configuration.")
            elif file_ext == '.txt':
                # Export as text
                messagebox.showinfo("Export", f"Exporting configuration to text: {file_path}\n\n"
                                 "This would generate a text report of the configuration.")
            else:
                messagebox.showinfo("Unknown Format", f"Unknown export format: {file_ext}")
                return
            
            # Update status
            self.status_label.config(text=f"Results exported to {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error Exporting Results", f"Error: {str(e)}")
    
    def show_preferences(self):
        """Show preferences dialog"""
        preferences_dialog = ctk.CTkToplevel(self.master)
        preferences_dialog.title("Preferences")
        preferences_dialog.geometry("500x400")
        preferences_dialog.transient(self.master)
        preferences_dialog.grab_set()
        
        # Create notebook for preference categories
        preferences_notebook = ttk.Notebook(preferences_dialog)
        preferences_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General preferences tab
        general_frame = ttk.Frame(preferences_notebook)
        preferences_notebook.add(general_frame, text="General")
        
        # Theme option
        ttk.Label(general_frame, text="Theme:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        theme_var = tk.StringVar(value=ctk.get_appearance_mode())
        theme_combo = ttk.Combobox(general_frame, textvariable=theme_var, 
                                 values=["Light", "Dark", "System"], 
                                 width=15, state="readonly")
        theme_combo.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        # Default values option
        ttk.Label(general_frame, text="Reset to defaults on startup:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        reset_defaults_var = tk.BooleanVar(value=False)
        reset_defaults_check = ttk.Checkbutton(general_frame, variable=reset_defaults_var)
        reset_defaults_check.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        
        # Save window size option
        ttk.Label(general_frame, text="Remember window size:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        save_size_var = tk.BooleanVar(value=True)
        save_size_check = ttk.Checkbutton(general_frame, variable=save_size_var)
        save_size_check.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        
        # Algorithm preferences tab
        algorithm_frame = ttk.Frame(preferences_notebook)
        preferences_notebook.add(algorithm_frame, text="Algorithm")
        
        # Default population size
        ttk.Label(algorithm_frame, text="Default Population Size:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        default_pop_var = tk.StringVar(value="50")
        default_pop_entry = ttk.Entry(algorithm_frame, textvariable=default_pop_var, width=10)
        default_pop_entry.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        # Default generations
        ttk.Label(algorithm_frame, text="Default Generations:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        default_gen_var = tk.StringVar(value="100")
        default_gen_entry = ttk.Entry(algorithm_frame, textvariable=default_gen_var, width=10)
        default_gen_entry.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        
        # Use adaptive mutation
        ttk.Label(algorithm_frame, text="Use Adaptive Mutation:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        adaptive_mutation_var = tk.BooleanVar(value=True)
        adaptive_mutation_check = ttk.Checkbutton(algorithm_frame, variable=adaptive_mutation_var)
        adaptive_mutation_check.grid(row=2, column=1, sticky="w", padx=10, pady=10)
        
        # Auto-save results option
        ttk.Label(algorithm_frame, text="Auto-save results:").grid(row=3, column=0, sticky="w", padx=10, pady=10)
        autosave_var = tk.BooleanVar(value=False)
        autosave_check = ttk.Checkbutton(algorithm_frame, variable=autosave_var)
        autosave_check.grid(row=3, column=1, sticky="w", padx=10, pady=10)
        
        # Data preferences tab
        data_frame = ttk.Frame(preferences_notebook)
        preferences_notebook.add(data_frame, text="Data")
        
        # Auto-update component data
        ttk.Label(data_frame, text="Auto-update component data:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
        auto_update_var = tk.BooleanVar(value=True)
        auto_update_check = ttk.Checkbutton(data_frame, variable=auto_update_var)
        auto_update_check.grid(row=0, column=1, sticky="w", padx=10, pady=10)
        
        # Update frequency
        ttk.Label(data_frame, text="Update frequency:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
        update_freq_var = tk.StringVar(value="7")
        update_freq_combo = ttk.Combobox(data_frame, textvariable=update_freq_var, 
                                       values=["1", "7", "14", "30"], 
                                       width=10, state="readonly")
        update_freq_combo.grid(row=1, column=1, sticky="w", padx=10, pady=10)
        ttk.Label(data_frame, text="days").grid(row=1, column=2, sticky="w")
        
        # Custom data source
        ttk.Label(data_frame, text="Custom data source:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
        data_source_var = tk.StringVar(value="")
        data_source_entry = ttk.Entry(data_frame, textvariable=data_source_var, width=30)
        data_source_entry.grid(row=2, column=1, columnspan=2, sticky="w", padx=10, pady=10)
        
        # Browse button for data source
        browse_button = ctk.CTkButton(data_frame, text="Browse", 
                                    command=lambda: data_source_var.set(filedialog.askdirectory()),
                                    width=20)
        browse_button.grid(row=2, column=3, padx=5, pady=10)
        
        # Button to check for updates now
        check_updates_button = ctk.CTkButton(data_frame, text="Check for Updates Now", 
                                          command=lambda: messagebox.showinfo("Update Check", 
                                                                         "This would check for component updates."))
        check_updates_button.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=10)
        
        # Buttons
        buttons_frame = ttk.Frame(preferences_dialog)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)
        
        save_button = ctk.CTkButton(buttons_frame, text="Save", 
                                  command=lambda: self.save_preferences(preferences_dialog, theme_var.get()))
        save_button.pack(side=tk.RIGHT, padx=5, pady=5)
        
        cancel_button = ctk.CTkButton(buttons_frame, text="Cancel", 
                                    command=preferences_dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def save_preferences(self, dialog, theme):
        """Save preferences and close dialog"""
        # Change theme if different
        if theme != ctk.get_appearance_mode():
            self.change_theme(theme)
        
        # This would normally save other preferences
        # For now, just close the dialog
        dialog.destroy()
        
        # Update status
        self.status_label.config(text="Preferences saved")
    
    def change_theme(self, theme):
        """Change the application theme"""
        ctk.set_appearance_mode(theme)
        
        # Update colors based on new theme
        self.update_colors()
        
        # Update status
        self.status_label.config(text=f"Theme changed to {theme}")
    
    def show_documentation(self):
        """Show documentation"""
        # This would normally open documentation
        # For now, just show a message
        messagebox.showinfo("Documentation", 
                          "This would open the documentation for the application.\n\n"
                          "In a complete implementation, this would either open a help window "
                          "or direct the user to online documentation.")
    
    def show_about(self):
        """Show about dialog"""
        about_dialog = ctk.CTkToplevel(self.master)
        about_dialog.title("About Computer Generator Pro")
        about_dialog.geometry("400x300")
        about_dialog.transient(self.master)
        about_dialog.grab_set()
        
        # App icon/logo placeholder
        logo_label = ttk.Label(about_dialog, text="[APP LOGO]", 
                             borderwidth=2, relief="solid", width=10, height=5)
        logo_label.pack(pady=10)
        
        # App name and version
        ttk.Label(about_dialog, text="Computer Generator Pro", 
                font=("TkDefaultFont", 14, "bold")).pack(pady=5)
        ttk.Label(about_dialog, text="Version 2.0").pack()
        
        # Description
        description = "An advanced tool for generating optimal computer configurations using genetic algorithms."
        ttk.Label(about_dialog, text=description, wraplength=350).pack(pady=10)
        
        # Copyright
        ttk.Label(about_dialog, text="© 2025 Your Company").pack(pady=5)
        
        # Website link
        website_frame = ttk.Frame(about_dialog)
        website_frame.pack(pady=5)
        
        ttk.Label(website_frame, text="Website:").pack(side=tk.LEFT)
        website_link = ttk.Label(website_frame, text="www.yourcompany.com", 
                               foreground="blue", cursor="hand2")
        website_link.pack(side=tk.LEFT, padx=5)
        website_link.bind("<Button-1>", lambda e: webbrowser.open("http://www.yourcompany.com"))
        
        # Close button
        close_button = ctk.CTkButton(about_dialog, text="Close", 
                                   command=about_dialog.destroy)
        close_button.pack(pady=10)
    
    def on_tab_change(self, event):
        """Handle tab change event"""
        # Get selected tab
        tab_id = self.notebook.select()
        tab_name = self.notebook.tab(tab_id, "text").strip()
        
        # Update status bar
        self.status_bar.config(text=f"Current view: {tab_name}")
        
        # Update UI based on selected tab
        if tab_name == "Generator":
            pass  # Nothing special to do
        elif tab_name == "Results":
            # Refresh results if needed
            if hasattr(self, 'current_computer') and self.current_computer is not None:
                self.update_components_tree()
        elif tab_name == "Comparison":
            # Refresh comparison if needed
            if hasattr(self, 'generated_computers') and self.generated_computers:
                self.update_comparison_tab()
        elif tab_name == "Visualization":
            # Refresh visualization if needed
            if hasattr(self, 'current_computer') and self.current_computer is not None:
                self.update_visualization()
        elif tab_name == "Component Browser":
            # Refresh component browser
            self.update_component_browser()
    
    def load_application_settings(self):
        """Load application settings"""
        # This would normally load settings from a file
        # For now, just use default settings
        ctk.set_appearance_mode("System")  # Use system theme by default
    
    def run(self):
        """Run the application main loop"""
        self.master.resizable(True, True)  # Allow resizing
        self.master.mainloop()
        