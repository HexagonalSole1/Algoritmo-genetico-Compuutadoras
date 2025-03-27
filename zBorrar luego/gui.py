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
from data_manager import DataManager


class ComputerGeneratorGUI:
    """
    Modern GUI for the Computer Generator application with dark mode support,
    tabs, advanced visualization, and enhanced user experience.
    """
    def __init__(self, master):
        """Initialize the GUI"""
        self.master = master
        self.data_manager = DataManager()
        
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