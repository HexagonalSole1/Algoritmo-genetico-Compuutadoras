"""
Compatibility repair operations for the genetic algorithm.
"""
import random
from copy import deepcopy
from typing import List
from models import Computer, CPU, GPU, RAM, Storage, Motherboard, PSU, Cooling, Case


class CompatibilityRepairer:
    """
    Repairs compatibility issues in computer configurations.
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
        cases: List[Case]
    ):
        """
        Initialize the repairer with component lists.
        
        Args:
            cpus: List of available CPUs
            gpus: List of available GPUs
            rams: List of available RAMs
            storages: List of available storages
            motherboards: List of available motherboards
            psus: List of available PSUs
            coolings: List of available cooling solutions
            cases: List of available cases
        """
        self.cpus = cpus
        self.gpus = gpus
        self.rams = rams
        self.storages = storages
        self.motherboards = motherboards
        self.psus = psus
        self.coolings = coolings
        self.cases = cases
    
    def repair_compatibility(self, computer: Computer) -> Computer:
        """
        Try to repair incompatibilities in a computer configuration
        
        Args:
            computer: Computer to repair
            
        Returns:
            Computer: Repaired computer
        """
        repaired = deepcopy(computer)
        
        # Fix CPU-Motherboard incompatibility
        if not repaired.motherboard.is_cpu_compatible(repaired.cpu):
            # Either find compatible motherboard or compatible CPU
            if random.random() < 0.5:
                compatible_mobos = [mobo for mobo in self.motherboards 
                                   if mobo.is_cpu_compatible(repaired.cpu)]
                if compatible_mobos:
                    repaired.motherboard = random.choice(compatible_mobos)
            else:
                compatible_cpus = [cpu for cpu in self.cpus 
                                  if repaired.motherboard.is_cpu_compatible(cpu)]
                if compatible_cpus:
                    repaired.cpu = random.choice(compatible_cpus)
                    
        # Fix RAM-Motherboard incompatibility
        if not repaired.motherboard.is_ram_compatible(repaired.ram):
            compatible_rams = [ram for ram in self.rams 
                              if repaired.motherboard.is_ram_compatible(ram)]
            if compatible_rams:
                repaired.ram = random.choice(compatible_rams)
                
        # Fix PSU inadequacy
        total_power = (
            repaired.cpu.power_consumption + 
            (repaired.gpu.power_consumption if repaired.gpu else 0) + 
            repaired.motherboard.power_consumption + 
            50  # Base for other components
        )
        
        if repaired.psu.capacity < total_power:
            adequate_psus = [psu for psu in self.psus if psu.capacity >= total_power]
            if adequate_psus:
                repaired.psu = random.choice(adequate_psus)
                
        # Fix case compatibility
        if not repaired.case.can_fit_all_components(repaired):
            compatible_cases = [case for case in self.cases if case.can_fit_all_components(repaired)]
            if compatible_cases:
                repaired.case = random.choice(compatible_cases)
                
        return repaired