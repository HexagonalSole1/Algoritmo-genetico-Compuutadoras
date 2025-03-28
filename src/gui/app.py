"""
Punto de entrada principal para la aplicación GUI del Generador de Computadoras.
"""
import os
import sys
import logging
import tkinter as tk
import customtkinter as ctk

# Agregar el directorio raíz al PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.views.main_window import MainWindow
from gui.themes.theme_manager import ThemeManager
from algorithm.utils.custom_data_manager import CustomDataManager


def setup_logging():
    """Configurar el sistema de logging"""
    # Crear directorio de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # Configurar logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Crear logger de la aplicación
    logger = logging.getLogger('ComputerGenerator')
    return logger


class ComputerGeneratorApp:
    """Aplicación principal del Generador de Computadoras"""
    
    def __init__(self):
        """Inicializar la aplicación"""
        # Configurar logging
        self.logger = setup_logging()
        self.logger.info("Iniciando aplicación")
        
        # Inicializar customtkinter
        ctk.set_appearance_mode("System")  # Usar tema del sistema por defecto
        ctk.set_default_color_theme("blue")  # Usar tema azul
        
        # Inicializar gestor de temas
        self.theme_manager = ThemeManager()
        
        # Inicializar gestor de datos
        self.data_manager = CustomDataManager()
        
        # Crear ventana principal
        self.root = ctk.CTk()
        self.root.title("Computer Generator Pro")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Inicializar ventana principal
        self.main_window = MainWindow(self.root, self.data_manager, self.theme_manager)
        
    def run(self):
        """Ejecutar la aplicación"""
        try:
            self.logger.info("Ejecutando aplicación")
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Error en la aplicación: {str(e)}", exc_info=True)
        finally:
            self.logger.info("Cerrando aplicación")


def main():
    """Función principal para ejecutar la aplicación"""
    try:
        app = ComputerGeneratorApp()
        app.run()
    except Exception as e:
        print(f"Error crítico: {str(e)}")
        logging.error(f"Error crítico: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()