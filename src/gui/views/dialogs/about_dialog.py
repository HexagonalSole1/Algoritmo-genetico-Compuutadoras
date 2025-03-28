"""
Diálogo de acerca de.
"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import webbrowser
import logging


class AboutDialog:
    """Diálogo que muestra información acerca de la aplicación"""
    
    def __init__(self, parent):
        """
        Inicializar diálogo acerca de.
        
        Args:
            parent: Widget padre
        """
        self.parent = parent
        self.logger = logging.getLogger("ComputerGenerator.AboutDialog")
        
        # Crear diálogo
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("About Computer Generator Pro")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Crear contenido
        self.create_content()
        
        # Configurar cierre del diálogo
        self.dialog.protocol("WM_DELETE_WINDOW", self.dialog.destroy)
        
        self.logger.debug("Diálogo acerca de inicializado")
    
    def create_content(self):
        """Crear contenido del diálogo"""
        # Icono/logo de la aplicación (placeholder)
        logo_label = ttk.Label(self.dialog, text="[APP LOGO]", 
                            borderwidth=2, relief="solid", width=10, height=5)
        logo_label.pack(pady=10)
        
        # Nombre y versión de la aplicación
        name_label = ttk.Label(self.dialog, text="Computer Generator Pro", 
                             font=("TkDefaultFont", 14, "bold"))
        name_label.pack(pady=5)
        
        version_label = ttk.Label(self.dialog, text="Version 2.0")
        version_label.pack()
        
        # Descripción
        description = "An advanced tool for generating optimal computer configurations using genetic algorithms."
        description_label = ttk.Label(self.dialog, text=description, wraplength=350)
        description_label.pack(pady=10)
        
        # Copyright
        copyright_label = ttk.Label(self.dialog, text="© 2025 Your Company")
        copyright_label.pack(pady=5)
        
        # Enlace a sitio web
        website_frame = ttk.Frame(self.dialog)
        website_frame.pack(pady=5)
        
        ttk.Label(website_frame, text="Website:").pack(side=tk.LEFT)
        website_link = ttk.Label(website_frame, text="www.yourcompany.com", 
                              foreground="blue", cursor="hand2")
        website_link.pack(side=tk.LEFT, padx=5)
        website_link.bind("<Button-1>", lambda e: webbrowser.open("http://www.yourcompany.com"))
        
        # Botón de cerrar
        close_button = ctk.CTkButton(self.dialog, text="Close", 
                                  command=self.dialog.destroy)
        close_button.pack(pady=10)