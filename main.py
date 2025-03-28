"""
Punto de entrada principal para la aplicación Computer Generator.
"""
import os
import sys
import logging
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

# Añadir la ruta raíz para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar modelos
from src.gui.models.settings_model import SettingsModel
from src.gui.models.component_model import ComponentModel
from algorithm.utils.custom_data_manager import CustomDataManager

# Inicialización básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('ComputerGenerator')

def main():
    """Función principal con integración de modelos básicos"""
    try:
        logger.info("Iniciando aplicación")
        
        # Inicializar data manager y modelos
        data_manager = CustomDataManager()
        settings_model = SettingsModel()
        component_model = ComponentModel(data_manager)
        
        # Inicializar customtkinter
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Crear ventana principal
        root = ctk.CTk()
        root.title("Computer Generator Pro - Modular Demo")
        root.geometry("900x700")
        
        # Frame principal
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Título
        title = ctk.CTkLabel(main_frame, text="Computer Generator Pro", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Crear un notebook para pestañas
        tab_view = ctk.CTkTabview(main_frame)
        tab_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña de Configuraciones
        settings_tab = tab_view.add("Settings")
        
        # Mostrar configuraciones
        settings = settings_model.get_settings()
        settings_frame = ctk.CTkFrame(settings_tab)
        settings_frame.pack(pady=10, fill="x", padx=10)
        
        ctk.CTkLabel(settings_frame, text="Current Settings:", font=("Arial", 16, "bold")).pack(anchor="w", padx=10, pady=5)
        
        for key, value in settings.items():
            setting_text = f"{key}: {value}"
            ctk.CTkLabel(settings_frame, text=setting_text).pack(anchor="w", padx=20, pady=2)
        
        # Pestaña de Componentes
        components_tab = tab_view.add("Components")
        
        # Frame para tipo de componente
        type_frame = ctk.CTkFrame(components_tab)
        type_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(type_frame, text="Component Type:").pack(side="left", padx=10)
        
        # Variable para tipo de componente
        component_type_var = tk.StringVar(value="cpu")
        
        # Combobox para seleccionar tipo de componente
        types = ["cpu", "gpu", "ram", "storage", "motherboard", "psu", "cooling", "case"]
        type_combo = ttk.Combobox(type_frame, textvariable=component_type_var, values=types, state="readonly")
        type_combo.pack(side="left", padx=10)
        
        # Frame para lista de componentes
        list_frame = ctk.CTkFrame(components_tab)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # TreeView para mostrar componentes
        columns = ('name', 'details', 'price')
        component_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        component_tree.heading('name', text='Name')
        component_tree.heading('details', text='Details')
        component_tree.heading('price', text='Price')
        
        component_tree.column('name', width=200)
        component_tree.column('details', width=400)
        component_tree.column('price', width=100)
        
        # Scrollbar para el TreeView
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=component_tree.yview)
        component_tree.configure(yscrollcommand=scrollbar.set)
        
        component_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Función para actualizar lista de componentes
        def update_component_list(*args):
            # Limpiar lista actual
            for item in component_tree.get_children():
                component_tree.delete(item)
                
            # Obtener componentes según tipo seleccionado
            comp_type = component_type_var.get()
            components = []
            
            if comp_type == "cpu":
                components = component_model.get_cpu_list()
            elif comp_type == "gpu":
                components = component_model.get_gpu_list()
            elif comp_type == "ram":
                components = component_model.get_ram_list()
            elif comp_type == "storage":
                components = component_model.get_storage_list()
            elif comp_type == "motherboard":
                components = component_model.get_motherboard_list()
            elif comp_type == "psu":
                components = component_model.get_psu_list()
            elif comp_type == "cooling":
                components = component_model.get_cooling_list()
            elif comp_type == "case":
                components = component_model.get_case_list()
            
            # Actualizar status
            status_label.configure(text=f"Loaded {len(components)} {comp_type.upper()} components")
            
            # Agregar componentes a la lista
            for component in components:
                if component is None:  # Manejar caso especial de GPU None
                    component_tree.insert('', 'end', values=('Integrated Graphics', 'Using CPU integrated graphics', '$0.00'))
                    continue
                
                # Obtener detalles según tipo de componente
                try:
                    name = component.maker if hasattr(component, 'maker') else component.model
                    details = str(component).split(': ')[1] if ': ' in str(component) else str(component)
                    price = f"${component.price:.2f}" if hasattr(component, 'price') else "N/A"
                    
                    component_tree.insert('', 'end', values=(name, details, price))
                except Exception as e:
                    logger.error(f"Error adding component to list: {str(e)}")
        
        # Vincular cambio de tipo de componente a actualización de lista
        type_combo.bind("<<ComboboxSelected>>", update_component_list)
        
        # Frame para botones
        buttons_frame = ctk.CTkFrame(components_tab)
        buttons_frame.pack(fill="x", padx=10, pady=10)
        
        # Botón para refrescar la lista
        refresh_button = ctk.CTkButton(buttons_frame, text="Refresh List", 
                                     command=update_component_list)
        refresh_button.pack(side="left", padx=10)
        
        # Status label
        status_label = ctk.CTkLabel(components_tab, text="Select a component type")
        status_label.pack(padx=10, pady=5, anchor="w")
        
        # Cargar componentes iniciales
        update_component_list()
        
        # Botón para cerrar
        exit_button = ctk.CTkButton(main_frame, text="Close Application", command=root.destroy)
        exit_button.pack(pady=10)
        
        # Ejecutar la aplicación
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Error crítico: {str(e)}", exc_info=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        logger.info("Aplicación cerrada")

if __name__ == '__main__':
    main()