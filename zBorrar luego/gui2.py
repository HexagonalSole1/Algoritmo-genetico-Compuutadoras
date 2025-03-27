
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