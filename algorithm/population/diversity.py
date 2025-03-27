"""
Diversity calculation for the genetic algorithm population.
"""
from typing import List, Set
from models import Computer, CPU, GPU, RAM, Storage, Motherboard, PSU


class DiversityCalculator:
    """
    Calculates diversity metrics for a population of computer configurations.
    """
    
    def __init__(
        self,
        cpus: List[CPU],
        gpus: List[GPU],
        rams: List[RAM],
        storages: List[Storage],
        motherboards: List[Motherboard],
        psus: List[PSU]
    ):
        """
        Initialize the diversity calculator with component lists.
        
        Args:
            cpus: List of available CPUs
            gpus: List of available GPUs
            rams: List of available RAMs
            storages: List of available storages
            motherboards: List of available motherboards
            psus: List of available PSUs
        """
        self.cpus = cpus
        self.gpus = gpus
        self.rams = rams
        self.storages = storages
        self.motherboards = motherboards
        self.psus = psus
    
    def calculate_diversity(self, population: List[Computer]) -> float:
        """
        Calculate diversity of the population as a measure of genetic variation
        
        Args:
            population: List of computer configurations
            
        Returns:
            float: Diversity score between 0 and 1
        """
        if not population:
            return 0
            
        # Count unique components across population
        unique_cpus: Set[str] = set()
        unique_gpus: Set[str] = set()
        unique_rams: Set[str] = set()
        unique_storages: Set[str] = set()
        unique_motherboards: Set[str] = set()
        unique_psus: Set[str] = set()
        
        for computer in population:
            unique_cpus.add(computer.cpu.maker)
            if computer.gpu:
                unique_gpus.add(computer.gpu.maker)
            unique_rams.add(computer.ram.maker)
            unique_storages.add(f"{computer.storage.maker}_{computer.storage.type}")
            unique_motherboards.add(computer.motherboard.maker)
            unique_psus.add(computer.psu.maker)
        
        # Calculate diversity as ratio of unique components to total components in population
        total_possible_cpus = len(set(cpu.maker for cpu in self.cpus))
        total_possible_gpus = len(set(gpu.maker for gpu in self.gpus if gpu))
        total_possible_rams = len(set(ram.maker for ram in self.rams))
        total_possible_storages = len(set(f"{s.maker}_{s.type}" for s in self.storages))
        total_possible_motherboards = len(set(mb.maker for mb in self.motherboards))
        total_possible_psus = len(set(psu.maker for psu in self.psus))
        
        # Calculate normalized diversity scores
        cpu_diversity = len(unique_cpus) / total_possible_cpus if total_possible_cpus > 0 else 0
        gpu_diversity = len(unique_gpus) / total_possible_gpus if total_possible_gpus > 0 else 0
        ram_diversity = len(unique_rams) / total_possible_rams if total_possible_rams > 0 else 0
        storage_diversity = len(unique_storages) / total_possible_storages if total_possible_storages > 0 else 0
        mb_diversity = len(unique_motherboards) / total_possible_motherboards if total_possible_motherboards > 0 else 0
        psu_diversity = len(unique_psus) / total_possible_psus if total_possible_psus > 0 else 0
        
        # Overall diversity as weighted average
        overall_diversity = (
            cpu_diversity * 0.2 + 
            gpu_diversity * 0.2 + 
            ram_diversity * 0.15 + 
            storage_diversity * 0.15 + 
            mb_diversity * 0.15 + 
            psu_diversity * 0.15
        )
        
        return overall_diversity