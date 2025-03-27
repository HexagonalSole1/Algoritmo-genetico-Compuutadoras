
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
        