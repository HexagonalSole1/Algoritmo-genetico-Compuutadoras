"""
Script para verificar el acceso a los datos en data.py y comprobar la integración.
"""
import sys
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("VerifyData")

# Añadir el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
logger.info(f"Directorio actual: {current_dir}")
logger.info(f"Python path: {sys.path}")

# Mostrar archivos en el directorio actual
logger.info("Archivos en el directorio actual:")
for file in os.listdir(current_dir):
    if file.endswith('.py'):
        logger.info(f" - {file}")

try:
    # Intentar importar data.py
    logger.info("Intentando importar data.py directamente")
    try:
        import data
        logger.info("✅ data.py importado exitosamente")
        logger.info(f"Número de CPUs en data.py: {len(data.cpus)}")
        logger.info(f"Número de GPUs en data.py: {len(data.gpus)}")
    except ImportError as e:
        logger.error(f"❌ Error al importar data.py directamente: {e}")

    # Intentar usar el puente de datos
    logger.info("\nIntentando usar data_bridge.py")
    try:
        from algorithm.utils.data_bridge import load_data_components
        cpus, gpus, rams, storages, motherboards, psus = load_data_components()
        logger.info("✅ Datos cargados exitosamente usando data_bridge")
        logger.info(f"Número de CPUs: {len(cpus)}")
        logger.info(f"Número de GPUs: {len(gpus)}")
    except Exception as e:
        logger.error(f"❌ Error al usar data_bridge: {e}")

    # Intentar usar el CustomDataManager
    logger.info("\nIntentando usar CustomDataManager")
    try:
        from algorithm.utils.custom_data_manager import CustomDataManager
        custom_manager = CustomDataManager()
        cpus = custom_manager.get_cpus()
        gpus = custom_manager.get_gpus()
        logger.info("✅ Datos cargados exitosamente usando CustomDataManager")
        logger.info(f"Número de CPUs: {len(cpus)}")
        logger.info(f"Número de GPUs: {len(gpus)}")
    except Exception as e:
        logger.error(f"❌ Error al usar CustomDataManager: {e}")

    # Intentar usar el ComputerGenerator
    logger.info("\nIntentando usar ComputerGenerator con CustomDataManager")
    try:
        from algorithm import ComputerGenerator
        from models import UserPreferences
        
        user_prefs = UserPreferences(
            min_price=5000,
            max_price=15000,
            usage="juegos",
            priority="balanced"
        )
        
        generator = ComputerGenerator(
            population_size=10,  # Pequeño para prueba
            crossover_rate=0.8,
            mutation_rate=0.1,
            generations=5,  # Pequeño para prueba
            user_preferences=user_prefs
        )
        
        logger.info("✅ ComputerGenerator inicializado correctamente")
        logger.info(f"Número de CPUs en el generador: {len(generator.cpus)}")
        logger.info(f"Número de GPUs en el generador: {len(generator.gpus)}")
        
        # Intentar una pequeña ejecución
        logger.info("Ejecutando generación inicial de población")
        generator.generate_initial_population()
        logger.info(f"Tamaño de la población generada: {len(generator.population)}")
        
    except Exception as e:
        logger.error(f"❌ Error al usar ComputerGenerator: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    logger.error(f"Error general: {e}")
    import traceback
    traceback.print_exc()

logger.info("\nVerificación completada")