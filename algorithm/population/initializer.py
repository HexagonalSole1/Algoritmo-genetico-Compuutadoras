"""
Population initialization for the genetic algorithm.
"""
import random
from typing import List
from models import Computer, CPU, GPU, RAM, Storage, Motherboard, PSU, Cooling, Case, UserPreferences


class PopulationInitializer:
    """
    Initializes the population for the genetic algorithm.
    """
    
    def __init__(
        self,
        cpus: List[CPU],
        gpus: List[GPU],
        rams: List[RAM],
        storages: List[Storage],
        motherboards: List[Motherboard],
        psus: List[PSU],
        coolings: List[Cooling],
        cases: List[Case],
        user_preferences: UserPreferences
    ):
        """
        Initialize the population initializer with component lists and user preferences.
        
        Args:
            cpus: List of available CPUs
            gpus: List of available GPUs
            rams: List of available RAMs
            storages: List of available storages
            motherboards: List of available motherboards
            psus: List of available PSUs
            coolings: List of available cooling solutions
            cases: List of available cases
            user_preferences: User preferences for computer configuration
        """
        self.cpus = cpus
        self.gpus = gpus
        self.rams = rams
        self.storages = storages
        self.motherboards = motherboards
        self.psus = psus
        self.coolings = coolings
        self.cases = cases
        self.user_preferences = user_preferences
    
    def initialize(self, population_size: int, fitness_calculator) -> List[Computer]:
        """
        Generate initial population with smart seeding and heuristics
        
        Args:
            population_size: Number of individuals in the population
            fitness_calculator: Calculator for evaluating fitness
            
        Returns:
            List[Computer]: Initial population
        """
        population = []
        
        # Create a portion of population using heuristic-guided initialization
        heuristic_count = population_size // 3
        for _ in range(heuristic_count):
            computer = self.create_heuristic_individual()
            fitness = fitness_calculator.calculate_fitness(computer)
            computer.fitness = fitness
            population.append(computer)
        
        # Fill the rest with random configurations
        for _ in range(population_size - heuristic_count):
            computer = self.create_random_individual()
            fitness = fitness_calculator.calculate_fitness(computer)
            computer.fitness = fitness
            population.append(computer)
            
        return population
    
    def create_random_individual(self) -> Computer:
        """Create a completely random computer configuration"""
        cpu: CPU = random.choice(self.cpus)
        gpu: GPU = random.choice(self.gpus)
        ram: RAM = random.choice(self.rams)
        storage: Storage = random.choice(self.storages)
        motherboard: Motherboard = random.choice(self.motherboards)
        psu: PSU = random.choice(self.psus)
        cooling: Cooling = random.choice(self.coolings)
        case: Case = random.choice(self.cases)
        
        return Computer(cpu, gpu, ram, storage, motherboard, psu, cooling, case)
    
    def create_heuristic_individual(self) -> Computer:
        """
        Create an individual using heuristics based on user preferences
        to increase chances of having viable individuals in initial population
        """
        # First select a compatible motherboard and CPU pair
        motherboard = random.choice(self.motherboards)
        compatible_cpus = [cpu for cpu in self.cpus 
                          if motherboard.is_cpu_compatible(cpu)]
        
        if not compatible_cpus:
            # Fallback to random if no compatible found
            cpu = random.choice(self.cpus)
        else:
            cpu = random.choice(compatible_cpus)
        
        # Match RAM to motherboard
        compatible_rams = [ram for ram in self.rams 
                          if motherboard.is_ram_compatible(ram)]
        ram = random.choice(compatible_rams) if compatible_rams else random.choice(self.rams)
        
        # Select appropriate GPU based on usage
        gpu = None
        if self.user_preferences.usage in ["juegos", "diseño gráfico", "edición de video", "arquitectura"]:
            # Filter for more powerful GPUs for demanding tasks
            powerful_gpus = [g for g in self.gpus if g is not None and g.power >= 40]
            if powerful_gpus:
                gpu = random.choice(powerful_gpus)
            else:
                gpu = random.choice([g for g in self.gpus if g is not None])
        else:
            # For less demanding tasks, integrated graphics might be enough
            if cpu.has_integrated_graphics and random.random() < 0.5:
                gpu = None
            else:
                basic_gpus = [g for g in self.gpus if g is not None and g.power < 40]
                gpu = random.choice(basic_gpus) if basic_gpus else random.choice(self.gpus)
        
        # Select storage based on usage
        if self.user_preferences.usage in ["edición de video", "arquitectura"]:
            large_storages = [s for s in self.storages if s.capacity >= 1000 and s.type == "SSD"]
            storage = random.choice(large_storages) if large_storages else random.choice(self.storages)
        else:
            storage = random.choice(self.storages)
        
        # Calculate power requirements for appropriate PSU
        total_power = cpu.power_consumption + (gpu.power_consumption if gpu else 0) + 150  # Base + buffer
        
        # Find a PSU with enough capacity but not excessive
        suitable_psus = [p for p in self.psus if p.capacity >= total_power and p.capacity <= total_power * 1.5]
        psu = random.choice(suitable_psus) if suitable_psus else random.choice(self.psus)
        
        # Select appropriate cooling
        cooling = random.choice(self.coolings)
        
        # Select a case that can fit the motherboard
        compatible_cases = [c for c in self.cases if c.is_compatible_with_motherboard(motherboard)]
        case = random.choice(compatible_cases) if compatible_cases else random.choice(self.cases)
        
        return Computer(cpu, gpu, ram, storage, motherboard, psu, cooling, case)