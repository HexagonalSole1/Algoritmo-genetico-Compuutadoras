"""
Gestor de temas para la aplicación.
"""
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import matplotlib.pyplot as plt
import logging


class ThemeManager:
    """Gestor de temas para la aplicación"""
    
    def __init__(self):
        """Inicializar el gestor de temas"""
        self.logger = logging.getLogger("ComputerGenerator.ThemeManager")
        
        # Tema actual
        self.current_theme = "System"
        
        # Colores para tema claro
        self.light_colors = {
            "bg_color": "#f0f0f0",
            "fg_color": "#202020",
            "accent_color": "#3a7ebf",
            "subtle_color": "#e0e0e0",
            "error_color": "#e05c5c",
            "success_color": "#5ce05c",
            "warning_color": "#e5c07b",
            "header_color": "#333333",
            "button_color": "#3a7ebf",
            "button_hover_color": "#2a6eaf",
            "disabled_color": "#cccccc",
            "border_color": "#d0d0d0",
            "highlight_color": "#b3d9ff"
        }
        
        # Colores para tema oscuro
        self.dark_colors = {
            "bg_color": "#2b2b2b",
            "fg_color": "#e0e0e0",
            "accent_color": "#3a7ebf",
            "subtle_color": "#3c3c3c",
            "error_color": "#e05c5c",
            "success_color": "#5ce05c",
            "warning_color": "#e5c07b",
            "header_color": "#eeeeee",
            "button_color": "#4a8ecf",
            "button_hover_color": "#5a9edf",
            "disabled_color": "#555555",
            "border_color": "#555555",
            "highlight_color": "#264462"
        }
        
        # Observadores (patrón Observer)
        self.observers = []
    
    def add_observer(self, observer):
        """
        Agregar un observador para notificaciones.
        
        Args:
            observer: Objeto observador que implementa los métodos de notificación
        """
        if observer not in self.observers:
            self.observers.append(observer)
    
    def remove_observer(self, observer):
        """
        Eliminar un observador.
        
        Args:
            observer: Observador a eliminar
        """
        if observer in self.observers:
            self.observers.remove(observer)
    
    def notify_theme_changed(self, theme):
        """
        Notificar a los observadores que el tema ha cambiado.
        
        Args:
            theme: Nombre del nuevo tema
        """
        for observer in self.observers:
            if hasattr(observer, 'on_theme_changed'):
                observer.on_theme_changed(theme)
    
    def apply_theme(self, theme):
        """
        Aplicar un tema a la aplicación.
        
        Args:
            theme: Nombre del tema a aplicar (Light, Dark, System)
        """
        if theme not in ["Light", "Dark", "System"]:
            self.logger.warning(f"Tema desconocido: {theme}, usando System")
            theme = "System"
        
        # Actualizar tema actual
        self.current_theme = theme
        
        # Establecer tema en customtkinter
        ctk.set_appearance_mode(theme)
        
        # Configurar estilo ttk según el tema
        self._update_ttk_style(theme)
        
        # Configurar estilo matplotlib según el tema
        self._update_matplotlib_style(theme)
        
        # Notificar a los observadores
        self.notify_theme_changed(theme)
        
        self.logger.info(f"Tema cambiado a {theme}")
    
    def _update_ttk_style(self, theme):
        """
        Actualizar estilos ttk según el tema.
        
        Args:
            theme: Nombre del tema
        """
        # Obtener colores según el tema
        colors = self.get_colors(theme)
        
        # Inicializar estilo ttk
        style = ttk.Style()
        
        # Configurar estilos
        style.configure('TFrame', background=colors["bg_color"])
        style.configure('TLabel', background=colors["bg_color"], foreground=colors["fg_color"])
        style.configure('TButton', background=colors["button_color"], foreground=colors["fg_color"])
        style.configure('TCheckbutton', background=colors["bg_color"], foreground=colors["fg_color"])
        style.configure('TRadiobutton', background=colors["bg_color"], foreground=colors["fg_color"])
        style.configure('TEntry', background=colors["bg_color"], foreground=colors["fg_color"])
        style.configure('TCombobox', background=colors["bg_color"], foreground=colors["fg_color"])
        style.configure('TNotebook', background=colors["bg_color"], foreground=colors["fg_color"])
        style.configure('TNotebook.Tab', background=colors["subtle_color"], foreground=colors["fg_color"])
        
        # Configurar mapeo de estados
        style.map('TButton',
                background=[('active', colors["button_hover_color"]), ('disabled', colors["disabled_color"])],
                foreground=[('disabled', '#888888')])
        
        style.map('TCheckbutton',
                background=[('active', colors["bg_color"])],
                foreground=[('disabled', '#888888')])
        
        style.map('TRadiobutton',
                background=[('active', colors["bg_color"])],
                foreground=[('disabled', '#888888')])
        
        style.map('TNotebook.Tab',
                background=[('selected', colors["accent_color"])],
                foreground=[('selected', '#ffffff')])
    
    def _update_matplotlib_style(self, theme):
        """
        Actualizar estilo matplotlib según el tema.
        
        Args:
            theme: Nombre del tema
        """
        # Establecer estilo matplotlib según el tema
        if theme == "Dark" or (theme == "System" and self._is_system_dark_mode()):
            plt.style.use('dark_background')
        else:
            plt.style.use('default')
    
    def _is_system_dark_mode(self):
        """
        Determinar si el sistema está en modo oscuro.
        
        Returns:
            bool: True si el sistema está en modo oscuro, False en caso contrario
        """
        # En realidad, esto debería detectar el tema del sistema operativo
        # Como es complicado hacerlo de manera portable, simplemente devolvemos
        # el resultado de ctk.get_appearance_mode() == "Dark" cuando el tema es "System"
        return ctk.get_appearance_mode() == "Dark"
    
    def get_colors(self, theme=None):
        """
        Obtener diccionario de colores según el tema.
        
        Args:
            theme: Nombre del tema (opcional, usa el actual si no se especifica)
            
        Returns:
            Dict: Diccionario con colores del tema
        """
        if theme is None:
            theme = self.current_theme
        
        # Si es tema del sistema, determinar si es claro u oscuro
        if theme == "System":
            if self._is_system_dark_mode():
                return self.dark_colors
            else:
                return self.light_colors
        elif theme == "Dark":
            return self.dark_colors
        else:  # Light
            return self.light_colors
    
    def get_current_theme(self):
        """
        Obtener el tema actual.
        
        Returns:
            str: Nombre del tema actual
        """
        return self.current_theme
    
    def is_dark_mode(self):
        """
        Verificar si está activo el modo oscuro.
        
        Returns:
            bool: True si está activo el modo oscuro, False en caso contrario
        """
        if self.current_theme == "Dark":
            return True
        elif self.current_theme == "System":
            return self._is_system_dark_mode()
        else:
            return False