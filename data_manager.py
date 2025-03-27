import sqlite3
import json
import os
import logging
from typing import List, Dict, Any, Optional
import requests
from datetime import datetime

from models import CPU, GPU, RAM, Storage, Motherboard, PSU, Cooling, Case

class DataManager:
    """
    Handles data persistence, loading, and updating for computer components.
    Supports both local database and optional API integration for price updates.
    """
    
    def __init__(self, db_path: str = "components.db", enable_api_updates: bool = False, 
                api_key: str = None, update_interval_days: int = 7):
        """
        Initialize the DataManager
        
        Args:
            db_path: Path to SQLite database file
            enable_api_updates: Whether to enable API updates for prices
            api_key: API key for price updates service
            update_interval_days: How often to check for price updates
        """
        self.db_path = db_path
        self.enable_api_updates = enable_api_updates
        self.api_key = api_key
        self.update_interval_days = update_interval_days
        
        # Setup logging
        self.logger = logging.getLogger("DataManager")
        
        # Initialize database if it doesn't exist
        self._init_database()
        
        # Check if it's time to update prices from API
        if enable_api_updates and api_key:
            self._check_for_updates()
    
    def _init_database(self) -> None:
        """
        Initialize the database and create tables if they don't exist
        """
        # Tomar solo el directorio si existe en la ruta
        dir_name = os.path.dirname(self.db_path)
        if dir_name:  # Solo crear directorios si hay un directorio en la ruta
            os.makedirs(dir_name, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Resto del código para crear tablas
        # ...
        
        # Create tables if they don't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cpus (
            id INTEGER PRIMARY KEY,
            maker TEXT,
            model TEXT,
            performance INTEGER,
            price REAL,
            power_consumption INTEGER,
            has_integrated_graphics INTEGER,
            integrated_graphics_power INTEGER,
            last_updated TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS gpus (
            id INTEGER PRIMARY KEY,
            maker TEXT,
            price REAL,
            power_consumption INTEGER,
            power INTEGER,
            last_updated TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS rams (
            id INTEGER PRIMARY KEY,
            maker TEXT,
            model TEXT,
            capacity INTEGER,
            frequency INTEGER,
            type TEXT,
            price REAL,
            last_updated TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS storages (
            id INTEGER PRIMARY KEY,
            maker TEXT,
            model TEXT,
            type TEXT,
            capacity REAL,
            price REAL,
            last_updated TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS motherboards (
            id INTEGER PRIMARY KEY,
            maker TEXT,
            model TEXT,
            price REAL,
            power_consumption INTEGER,
            max_ram_capacity INTEGER,
            max_ram_frequency INTEGER,
            ram_socket_type TEXT,
            form_factor TEXT,
            compatible_cpus TEXT,
            last_updated TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS psus (
            id INTEGER PRIMARY KEY,
            maker TEXT,
            model TEXT,
            capacity INTEGER,
            price REAL,
            last_updated TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS coolings (
            id INTEGER PRIMARY KEY,
            maker TEXT,
            model TEXT,
            type TEXT,
            cooling_capacity INTEGER,
            price REAL,
            last_updated TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY,
            maker TEXT,
            model TEXT,
            form_factors TEXT,
            max_gpu_length INTEGER,
            cooling_support TEXT,
            price REAL,
            last_updated TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        ''')
        
        # Check if database is empty and needs initial data
        cursor.execute("SELECT COUNT(*) FROM cpus")
        count = cursor.fetchone()[0]
        
        if count == 0:
            self.logger.info("Database is empty, loading initial data")
            self._load_initial_data()
        
        conn.commit()
        conn.close()
    
    def _load_initial_data(self) -> None:
        """
        Load initial component data into the database from default data files
        """
        try:
            # Intenta cargar datos desde data.py del proyecto original
            self.logger.info("Loading data from data.py")
            # Importa los datos desde data.py
            from data import cpus, gpus, rams, storages, motherboards, psus
            
            # Conviértelos al formato necesario y cárgalos
            cpus_data = [cpu.__dict__ for cpu in cpus]
            gpus_data = [gpu.__dict__ if gpu is not None else None for gpu in gpus]
            rams_data = [ram.__dict__ for ram in rams]
            storages_data = [storage.__dict__ for storage in storages]
            motherboards_data = [mb.__dict__ for mb in motherboards]
            psus_data = [psu.__dict__ for psu in psus]
            
            # Crea datos de muestra para coolings y cases que no existen en data.py
            coolings_data = [
                {
                    "maker": "Noctua",
                    "model": "NH-D15",
                    "type": "Air",
                    "cooling_capacity": 180,
                    "price": 99.99,
                    "noise_level": 30,
                    "fan_count": 2,
                    "fan_size": 140,
                    "rgb": False,
                    "height_mm": 165
                },
                {
                    "maker": "ARCTIC",
                    "model": "Liquid Freezer II 240",
                    "type": "Liquid",
                    "cooling_capacity": 250,
                    "price": 119.99,
                    "noise_level": 25,
                    "fan_count": 2,
                    "fan_size": 120,
                    "rgb": False,
                    "height_mm": 240
                }
            ]
            
            cases_data = [
                {
                    "maker": "Lian Li",
                    "model": "O11 Dynamic",
                    "form_factors": ["ATX", "Micro-ATX", "Mini-ITX"],
                    "max_gpu_length": 420,
                    "cooling_support": {"max_air_cooler_height": 155, "radiator_support": [240, 360]},
                    "price": 149.99
                },
                {
                    "maker": "Fractal Design",
                    "model": "Meshify 2",
                    "form_factors": ["ATX", "Micro-ATX", "Mini-ITX"],
                    "max_gpu_length": 460,
                    "cooling_support": {"max_air_cooler_height": 185, "radiator_support": [240, 280, 360]},
                    "price": 139.99
                }
            ]
            
            # Insertar datos en la base de datos
            self._insert_cpus(cpus_data)
            self._insert_gpus(gpus_data)
            self._insert_rams(rams_data)
            self._insert_storages(storages_data)
            self._insert_motherboards(motherboards_data)
            self._insert_psus(psus_data)
            self._insert_coolings(coolings_data)
            self._insert_cases(cases_data)
            
        except Exception as e:
            self.logger.error(f"Error loading initial data: {e}")
            # En caso de error, carga unos pocos datos de demostración para que la aplicación funcione
            self._load_minimal_demo_data()
    def _load_minimal_demo_data(self) -> None:
        """
        Load minimal demo data in case of emergency
        """
        self.logger.info("Loading minimal demo data")
        
        # Datos mínimos para cada tipo de componente
        cpus_data = [
            {
                "maker": "Intel Core i7",
                "model": "14700K",
                "performance": 78,
                "price": 419.99,
                "power_consumption": 125,
                "has_integrated_graphics": True,
                "integrated_graphics_power": 15
            }
        ]
        
        gpus_data = [
            None,
            {
                "maker": "NVIDIA RTX 4070",
                "price": 599.99,
                "power_consumption": 200,
                "power": 70
            }
        ]
        
        # Y así con todos los componentes...
        
        # Insertar datos mínimos en la base de datos
        self._insert_cpus(cpus_data)
        self._insert_gpus(gpus_data)
        # Insertar el resto de componentes...       
    
    def _load_from_json(self) -> None:
        """
        Load component data from JSON files
        """
        data_dir = "data"
        os.makedirs(data_dir, exist_ok=True)
        
        # Load CPUs
        with open(os.path.join(data_dir, "cpus.json"), "r") as f:
            cpus_data = json.load(f)
            self._insert_cpus(cpus_data)
        
        # Load GPUs
        with open(os.path.join(data_dir, "gpus.json"), "r") as f:
            gpus_data = json.load(f)
            self._insert_gpus(gpus_data)
        
        # Load RAMs
        with open(os.path.join(data_dir, "rams.json"), "r") as f:
            rams_data = json.load(f)
            self._insert_rams(rams_data)
        
        # Load Storages
        with open(os.path.join(data_dir, "storages.json"), "r") as f:
            storages_data = json.load(f)
            self._insert_storages(storages_data)
        
        # Load Motherboards
        with open(os.path.join(data_dir, "motherboards.json"), "r") as f:
            motherboards_data = json.load(f)
            self._insert_motherboards(motherboards_data)
        
        # Load PSUs
        with open(os.path.join(data_dir, "psus.json"), "r") as f:
            psus_data = json.load(f)
            self._insert_psus(psus_data)
        
        # Load Coolings
        with open(os.path.join(data_dir, "coolings.json"), "r") as f:
            coolings_data = json.load(f)
            self._insert_coolings(coolings_data)
        
        # Load Cases
        with open(os.path.join(data_dir, "cases.json"), "r") as f:
            cases_data = json.load(f)
            self._insert_cases(cases_data)
    
    def _load_hardcoded_data(self) -> None:
        """
        Load hardcoded component data as a fallback
        """
        # Import hardcoded data from a backup module
        from data_backup import (cpus_data, gpus_data, rams_data, storages_data, 
                               motherboards_data, psus_data, coolings_data, cases_data)
        
        self._insert_cpus(cpus_data)
        self._insert_gpus(gpus_data)
        self._insert_rams(rams_data)
        self._insert_storages(storages_data)
        self._insert_motherboards(motherboards_data)
        self._insert_psus(psus_data)
        self._insert_coolings(coolings_data)
        self._insert_cases(cases_data)
    
    def _insert_cpus(self, cpus_data: List[Dict[str, Any]]) -> None:
        """Insert CPU data into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for cpu in cpus_data:
            cursor.execute('''
            INSERT INTO cpus (maker, model, performance, price, power_consumption,
                            has_integrated_graphics, integrated_graphics_power, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cpu['maker'],
                cpu['model'],
                cpu['performance'],
                cpu['price'],
                cpu['power_consumption'],
                1 if cpu['has_integrated_graphics'] else 0,
                cpu['integrated_graphics_power'],
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def _insert_gpus(self, gpus_data: List[Dict[str, Any]]) -> None:
        """Insert GPU data into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for gpu in gpus_data:
            # Handle None entries in GPUs list
            if gpu is None:
                cursor.execute('''
                INSERT INTO gpus (maker, price, power_consumption, power, last_updated)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    "None",
                    0,
                    0,
                    0,
                    datetime.now().isoformat()
                ))
            else:
                cursor.execute('''
                INSERT INTO gpus (maker, price, power_consumption, power, last_updated)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    gpu['maker'],
                    gpu['price'],
                    gpu['power_consumption'],
                    gpu['power'],
                    datetime.now().isoformat()
                ))
        
        conn.commit()
        conn.close()
    
    def _insert_rams(self, rams_data: List[Dict[str, Any]]) -> None:
        """Insert RAM data into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for ram in rams_data:
            cursor.execute('''
            INSERT INTO rams (maker, model, capacity, frequency, type, price, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                ram['maker'],
                ram['model'],
                ram['capacity'],
                ram['frequency'],
                ram['type'],
                ram['price'],
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def _insert_storages(self, storages_data: List[Dict[str, Any]]) -> None:
        """Insert Storage data into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for storage in storages_data:
            cursor.execute('''
            INSERT INTO storages (maker, model, type, capacity, price, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                storage['maker'],
                storage['model'],
                storage['type'],
                storage['capacity'],
                storage['price'],
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def _insert_motherboards(self, motherboards_data: List[Dict[str, Any]]) -> None:
        """Insert Motherboard data into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for motherboard in motherboards_data:
            # Convert compatible CPUs list to JSON string
            compatible_cpus_json = json.dumps(motherboard['compatible_cpus'])
            
            cursor.execute('''
            INSERT INTO motherboards (maker, model, price, power_consumption, max_ram_capacity,
                                    max_ram_frequency, ram_socket_type, form_factor, compatible_cpus, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                motherboard['maker'],
                motherboard['model'],
                motherboard['price'],
                motherboard['power_consumption'],
                motherboard['max_ram_capacity'],
                motherboard['max_ram_frequency'],
                motherboard['ram_socket_type'],
                motherboard.get('form_factor', 'ATX'),  # Default to ATX if not specified
                compatible_cpus_json,
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def _insert_psus(self, psus_data: List[Dict[str, Any]]) -> None:
        """Insert PSU data into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for psu in psus_data:
            cursor.execute('''
            INSERT INTO psus (maker, model, capacity, price, last_updated)
            VALUES (?, ?, ?, ?, ?)
            ''', (
                psu['maker'],
                psu['model'],
                psu['capacity'],
                psu['price'],
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def _insert_coolings(self, coolings_data: List[Dict[str, Any]]) -> None:
        """Insert Cooling data into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for cooling in coolings_data:
            cursor.execute('''
            INSERT INTO coolings (maker, model, type, cooling_capacity, price, last_updated)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                cooling['maker'],
                cooling['model'],
                cooling['type'],
                cooling['cooling_capacity'],
                cooling['price'],
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def _insert_cases(self, cases_data: List[Dict[str, Any]]) -> None:
        """Insert Case data into database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for case in cases_data:
            # Convert form factors and cooling support lists to JSON strings
            form_factors_json = json.dumps(case['form_factors'])
            cooling_support_json = json.dumps(case['cooling_support'])
            
            cursor.execute('''
            INSERT INTO cases (maker, model, form_factors, max_gpu_length, cooling_support, price, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                case['maker'],
                case['model'],
                form_factors_json,
                case['max_gpu_length'],
                cooling_support_json,
                case['price'],
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
    
    def _check_for_updates(self) -> None:
        """
        Check if it's time to update prices from external API
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get last update timestamp
        cursor.execute("SELECT value FROM metadata WHERE key = 'last_price_update'")
        result = cursor.fetchone()
        
        update_needed = True
        if result:
            last_update = datetime.fromisoformat(result[0])
            days_since_update = (datetime.now() - last_update).days
            update_needed = days_since_update >= self.update_interval_days
        
        if update_needed:
            self.logger.info("Updating prices from API")
            self._update_prices_from_api()
            
            # Update last update timestamp
            cursor.execute("INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)",
                          ('last_price_update', datetime.now().isoformat()))
            conn.commit()
        
        conn.close()
    
    def _update_prices_from_api(self) -> None:
        """
        Update component prices from external API
        """
        try:
            # Example API calls - replace with actual implementation
            api_base_url = "https://example-hardware-api.com/prices"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Update CPU prices
            cpu_response = requests.get(f"{api_base_url}/cpus", headers=headers)
            if cpu_response.status_code == 200:
                cpu_prices = cpu_response.json()
                self._update_cpu_prices(cpu_prices)
            
            # Update GPU prices
            gpu_response = requests.get(f"{api_base_url}/gpus", headers=headers)
            if gpu_response.status_code == 200:
                gpu_prices = gpu_response.json()
                self._update_gpu_prices(gpu_prices)
            
            # Similarly for other components...
            
            self.logger.info("Price updates completed successfully")
        except Exception as e:
            self.logger.error(f"Error updating prices from API: {e}")
    
    def _update_cpu_prices(self, cpu_prices: List[Dict[str, Any]]) -> None:
        """
        Update CPU prices in database from API data
        
        Args:
            cpu_prices: List of CPU price data from API
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for cpu_price in cpu_prices:
            # Match by maker and model
            cursor.execute('''
            UPDATE cpus
            SET price = ?, last_updated = ?
            WHERE maker = ? AND model = ?
            ''', (
                cpu_price['price'],
                datetime.now().isoformat(),
                cpu_price['maker'],
                cpu_price['model']
            ))
        
        conn.commit()
        conn.close()
    
    def _update_gpu_prices(self, gpu_prices: List[Dict[str, Any]]) -> None:
        """
        Update GPU prices in database from API data
        
        Args:
            gpu_prices: List of GPU price data from API
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for gpu_price in gpu_prices:
            # Match by maker
            cursor.execute('''
            UPDATE gpus
            SET price = ?, last_updated = ?
            WHERE maker = ?
            ''', (
                gpu_price['price'],
                datetime.now().isoformat(),
                gpu_price['maker']
            ))
        
        conn.commit()
        conn.close()
    
    def get_cpus(self) -> List[CPU]:
        """
        Get all CPUs from database
        
        Returns:
            List[CPU]: List of CPU objects
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM cpus")
        rows = cursor.fetchall()
        
        cpus = []
        for row in rows:
            cpu = CPU(
                maker=row['maker'],
                model=row['model'],
                performance=row['performance'],
                price=row['price'],
                power_consumption=row['power_consumption'],
                has_integrated_graphics=bool(row['has_integrated_graphics']),
                integrated_graphics_power=row['integrated_graphics_power']
            )
            cpus.append(cpu)
        
        conn.close()
        return cpus
    
    def get_gpus(self) -> List[Optional[GPU]]:
        """
        Get all GPUs from database
        
        Returns:
            List[Optional[GPU]]: List of GPU objects (including None for integrated graphics option)
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM gpus")
        rows = cursor.fetchall()
        
        gpus = []
        for row in rows:
            if row['maker'] == "None":
                gpus.append(None)
            else:
                gpu = GPU(
                    maker=row['maker'],
                    price=row['price'],
                    power_consumption=row['power_consumption'],
                    power=row['power']
                )
                gpus.append(gpu)
        
        conn.close()
        return gpus
    
    def get_rams(self) -> List[RAM]:
        """
        Get all RAMs from database
        
        Returns:
            List[RAM]: List of RAM objects
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM rams")
        rows = cursor.fetchall()
        
        rams = []
        for row in rows:
            ram = RAM(
                maker=row['maker'],
                model=row['model'],
                capacity=row['capacity'],
                frequency=row['frequency'],
                type=row['type'],
                price=row['price']
            )
            rams.append(ram)
        
        conn.close()
        return rams
    
    def get_storages(self) -> List[Storage]:
        """
        Get all Storages from database
        
        Returns:
            List[Storage]: List of Storage objects
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM storages")
        rows = cursor.fetchall()
        
        storages = []
        for row in rows:
            storage = Storage(
                maker=row['maker'],
                model=row['model'],
                type=row['type'],
                capacity=row['capacity'],
                price=row['price']
            )
            storages.append(storage)
        
        conn.close()
        return storages
    
    def get_motherboards(self) -> List[Motherboard]:
        """
        Get all Motherboards from database
        
        Returns:
            List[Motherboard]: List of Motherboard objects
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM motherboards")
        rows = cursor.fetchall()
        
        motherboards = []
        for row in rows:
            # Parse JSON string back to list
            compatible_cpus = json.loads(row['compatible_cpus'])
            
            motherboard = Motherboard(
                maker=row['maker'],
                model=row['model'],
                price=row['price'],
                power_consumption=row['power_consumption'],
                max_ram_capacity=row['max_ram_capacity'],
                max_ram_frequency=row['max_ram_frequency'],
                ram_socket_type=row['ram_socket_type'],
                form_factor=row['form_factor'],
                compatible_cpus=compatible_cpus
            )
            motherboards.append(motherboard)
        
        conn.close()
        return motherboards
    
    def get_psus(self) -> List[PSU]:
        """
        Get all PSUs from database
        
        Returns:
            List[PSU]: List of PSU objects
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM psus")
        rows = cursor.fetchall()
        
        psus = []
        for row in rows:
            psu = PSU(
                maker=row['maker'],
                model=row['model'],
                capacity=row['capacity'],
                price=row['price']
            )
            psus.append(psu)
        
        conn.close()
        return psus
    
    def get_coolings(self) -> List[Cooling]:
        """
        Get all Cooling solutions from database
        
        Returns:
            List[Cooling]: List of Cooling objects
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM coolings")
        rows = cursor.fetchall()
        
        coolings = []
        for row in rows:
            cooling = Cooling(
                maker=row['maker'],
                model=row['model'],
                type=row['type'],
                cooling_capacity=row['cooling_capacity'],
                price=row['price']
            )
            coolings.append(cooling)
        
        conn.close()
        return coolings
    
    def get_cases(self) -> List[Case]:
        """
        Get all Cases from database
        
        Returns:
            List[Case]: List of Case objects
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM cases")
        rows = cursor.fetchall()
        
        cases = []
        for row in rows:
            # Parse JSON strings back to lists
            form_factors = json.loads(row['form_factors'])
            cooling_support = json.loads(row['cooling_support'])
            
            case = Case(
                maker=row['maker'],
                model=row['model'],
                form_factors=form_factors,
                max_gpu_length=row['max_gpu_length'],
                cooling_support=cooling_support,
                price=row['price']
            )
            cases.append(case)
        
        conn.close()
        return cases
    
    def export_data_to_json(self, export_dir: str = "data_export") -> None:
        """
        Export all component data to JSON files
        
        Args:
            export_dir: Directory to export JSON files to
        """
        os.makedirs(export_dir, exist_ok=True)
        
        # Export CPUs
        cpus = self.get_cpus()
        with open(os.path.join(export_dir, "cpus.json"), "w") as f:
            json.dump([cpu.__dict__ for cpu in cpus], f, indent=2)
        
        # Export GPUs
        gpus = self.get_gpus()
        # Handle None values in GPU list
        gpu_data = []
        for gpu in gpus:
            if gpu is None:
                gpu_data.append(None)
            else:
                gpu_data.append(gpu.__dict__)
        with open(os.path.join(export_dir, "gpus.json"), "w") as f:
            json.dump(gpu_data, f, indent=2)
        
        # Export RAMs
        rams = self.get_rams()
        with open(os.path.join(export_dir, "rams.json"), "w") as f:
            json.dump([ram.__dict__ for ram in rams], f, indent=2)
        
        # Export Storages
        storages = self.get_storages()
        with open(os.path.join(export_dir, "storages.json"), "w") as f:
            json.dump([storage.__dict__ for storage in storages], f, indent=2)
        
        # Export Motherboards
        motherboards = self.get_motherboards()
        with open(os.path.join(export_dir, "motherboards.json"), "w") as f:
            json.dump([motherboard.__dict__ for motherboard in motherboards], f, indent=2)
        
        # Export PSUs
        psus = self.get_psus()
        with open(os.path.join(export_dir, "psus.json"), "w") as f:
            json.dump([psu.__dict__ for psu in psus], f, indent=2)
        
        # Export Coolings
        coolings = self.get_coolings()
        with open(os.path.join(export_dir, "coolings.json"), "w") as f:
            json.dump([cooling.__dict__ for cooling in coolings], f, indent=2)
        
        # Export Cases
        cases = self.get_cases()
        with open(os.path.join(export_dir, "cases.json"), "w") as f:
            json.dump([case.__dict__ for case in cases], f, indent=2)
        
        self.logger.info(f"Data exported to {export_dir}")
    
    def add_component(self, component_type: str, component_data: Dict[str, Any]) -> bool:
        """
        Add a new component to the database
        
        Args:
            component_type: Type of component to add ('cpu', 'gpu', etc.)
            component_data: Dictionary of component data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if component_type == 'cpu':
                cursor.execute('''
                INSERT INTO cpus (maker, model, performance, price, power_consumption,
                               has_integrated_graphics, integrated_graphics_power, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    component_data['maker'],
                    component_data['model'],
                    component_data['performance'],
                    component_data['price'],
                    component_data['power_consumption'],
                    1 if component_data['has_integrated_graphics'] else 0,
                    component_data['integrated_graphics_power'],
                    datetime.now().isoformat()
                ))
            
            elif component_type == 'gpu':
                if component_data is None:
                    cursor.execute('''
                    INSERT INTO gpus (maker, price, power_consumption, power, last_updated)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                        "None",
                        0,
                        0,
                        0,
                        datetime.now().isoformat()
                    ))
                else:
                    cursor.execute('''
                    INSERT INTO gpus (maker, price, power_consumption, power, last_updated)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (
                        component_data['maker'],
                        component_data['price'],
                        component_data['power_consumption'],
                        component_data['power'],
                        datetime.now().isoformat()
                    ))
            
            elif component_type == 'ram':
                cursor.execute('''
                INSERT INTO rams (maker, model, capacity, frequency, type, price, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    component_data['maker'],
                    component_data['model'],
                    component_data['capacity'],
                    component_data['frequency'],
                    component_data['type'],
                    component_data['price'],
                    datetime.now().isoformat()
                ))
            
            elif component_type == 'storage':
                cursor.execute('''
                INSERT INTO storages (maker, model, type, capacity, price, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    component_data['maker'],
                    component_data['model'],
                    component_data['type'],
                    component_data['capacity'],
                    component_data['price'],
                    datetime.now().isoformat()
                ))
            
            elif component_type == 'motherboard':
                # Convert compatible_cpus list to JSON string
                compatible_cpus_json = json.dumps(component_data['compatible_cpus'])
                
                cursor.execute('''
                INSERT INTO motherboards (maker, model, price, power_consumption, max_ram_capacity,
                                      max_ram_frequency, ram_socket_type, form_factor, compatible_cpus, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    component_data['maker'],
                    component_data['model'],
                    component_data['price'],
                    component_data['power_consumption'],
                    component_data['max_ram_capacity'],
                    component_data['max_ram_frequency'],
                    component_data['ram_socket_type'],
                    component_data.get('form_factor', 'ATX'),  # Default to ATX if not specified
                    compatible_cpus_json,
                    datetime.now().isoformat()
                ))
            
            elif component_type == 'psu':
                cursor.execute('''
                INSERT INTO psus (maker, model, capacity, price, last_updated)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    component_data['maker'],
                    component_data['model'],
                    component_data['capacity'],
                    component_data['price'],
                    datetime.now().isoformat()
                ))
            
            elif component_type == 'cooling':
                cursor.execute('''
                INSERT INTO coolings (maker, model, type, cooling_capacity, price, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    component_data['maker'],
                    component_data['model'],
                    component_data['type'],
                    component_data['cooling_capacity'],
                    component_data['price'],
                    datetime.now().isoformat()
                ))
            
            elif component_type == 'case':
                # Convert form_factors and cooling_support lists to JSON strings
                form_factors_json = json.dumps(component_data['form_factors'])
                cooling_support_json = json.dumps(component_data['cooling_support'])
                
                cursor.execute('''
                INSERT INTO cases (maker, model, form_factors, max_gpu_length, cooling_support, price, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    component_data['maker'],
                    component_data['model'],
                    form_factors_json,
                    component_data['max_gpu_length'],
                    cooling_support_json,
                    component_data['price'],
                    datetime.now().isoformat()
                ))
            
            else:
                self.logger.error(f"Unknown component type: {component_type}")
                conn.close()
                return False
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            self.logger.error(f"Error adding component: {e}")
            return False
    
    def update_component(self, component_type: str, component_id: int, 
                       updates: Dict[str, Any]) -> bool:
        """
        Update an existing component in the database
        
        Args:
            component_type: Type of component to update ('cpu', 'gpu', etc.)
            component_id: ID of component to update
            updates: Dictionary of updates to apply
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build SET clause dynamically based on updates
            set_clauses = []
            params = []
            
            for key, value in updates.items():
                # Handle special cases for JSON fields
                if component_type == 'motherboard' and key == 'compatible_cpus':
                    set_clauses.append(f"{key} = ?")
                    params.append(json.dumps(value))
                elif component_type == 'case' and key in ['form_factors', 'cooling_support']:
                    set_clauses.append(f"{key} = ?")
                    params.append(json.dumps(value))
                else:
                    set_clauses.append(f"{key} = ?")
                    params.append(value)
            
            # Add last_updated timestamp
            set_clauses.append("last_updated = ?")
            params.append(datetime.now().isoformat())
            
            # Add component_id for WHERE clause
            params.append(component_id)
            
            # Build and execute SQL query
            query = f"UPDATE {component_type}s SET {', '.join(set_clauses)} WHERE id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        
        except Exception as e:
            self.logger.error(f"Error updating component: {e}")
            return False
    
    def delete_component(self, component_type: str, component_id: int) -> bool:
        """
        Delete a component from the database
        
        Args:
            component_type: Type of component to delete ('cpu', 'gpu', etc.)
            component_id: ID of component to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"DELETE FROM {component_type}s WHERE id = ?", (component_id,))
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        
        except Exception as e:
            self.logger.error(f"Error deleting component: {e}")
            return False
    
    def search_components(self, component_type: str, query: str) -> List[Dict[str, Any]]:
        """
        Search for components in the database
        
        Args:
            component_type: Type of component to search for ('cpu', 'gpu', etc.)
            query: Search query
            
        Returns:
            List[Dict[str, Any]]: List of matching components
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Search for components matching the query in maker or model
            cursor.execute(f"SELECT * FROM {component_type}s WHERE maker LIKE ? OR model LIKE ?",
                         (f"%{query}%", f"%{query}%"))
            
            rows = cursor.fetchall()
            
            # Convert rows to dictionaries
            results = []
            for row in rows:
                result = dict(row)
                
                # Handle special cases for JSON fields
                if component_type == 'motherboard' and 'compatible_cpus' in result:
                    result['compatible_cpus'] = json.loads(result['compatible_cpus'])
                elif component_type == 'case':
                    if 'form_factors' in result:
                        result['form_factors'] = json.loads(result['form_factors'])
                    if 'cooling_support' in result:
                        result['cooling_support'] = json.loads(result['cooling_support'])
                
                results.append(result)
            
            conn.close()
            return results
        
        except Exception as e:
            self.logger.error(f"Error searching components: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the component database
        
        Returns:
            Dict[str, Any]: Dictionary of statistics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats = {}
            
            # Get counts for each component type
            for component_type in ['cpu', 'gpu', 'ram', 'storage', 'motherboard', 'psu', 'cooling', 'case']:
                cursor.execute(f"SELECT COUNT(*) FROM {component_type}s")
                count = cursor.fetchone()[0]
                stats[f"{component_type}_count"] = count
            
            # Get price ranges for each component type
            for component_type in ['cpu', 'gpu', 'ram', 'storage', 'motherboard', 'psu', 'cooling', 'case']:
                cursor.execute(f"SELECT MIN(price), MAX(price), AVG(price) FROM {component_type}s")
                min_price, max_price, avg_price = cursor.fetchone()
                stats[f"{component_type}_price_range"] = {
                    "min": min_price,
                    "max": max_price,
                    "avg": avg_price
                }
            
            # Get database size
            stats["database_size_bytes"] = os.path.getsize(self.db_path)
            
            # Get last update timestamp
            cursor.execute("SELECT value FROM metadata WHERE key = 'last_price_update'")
            result = cursor.fetchone()
            if result:
                stats["last_price_update"] = result[0]
            else:
                stats["last_price_update"] = None
            
            conn.close()
            return stats
        
        except Exception as e:
            self.logger.error(f"Error getting database stats: {e}")
            return {}