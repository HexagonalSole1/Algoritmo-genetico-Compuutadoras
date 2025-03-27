import tkinter as tk
import customtkinter as ctk
from gui import ComputerGeneratorGUI
import logging
import sys
import os

def setup_logging():
    """Set up logging configuration"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    # Configure logging
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create application logger
    logger = logging.getLogger('ComputerGenerator')
    return logger

def main():
    """Main entry point for the application"""
    # Set up logging
    logger = setup_logging()
    logger.info("Application starting")
    
    try:
        # Initialize customtkinter
        ctk.set_appearance_mode("System")  # Use system theme
        ctk.set_default_color_theme("blue")  # Use blue theme
        
        # Create main window
        window = ctk.CTk()
        
        # Create and run the GUI
        computer_generator_ui = ComputerGeneratorGUI(window)
        computer_generator_ui.run()
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Application closing")
    
if __name__ == '__main__':
    main()