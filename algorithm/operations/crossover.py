"""
Crossover operations for the genetic algorithm.
"""
import random
from typing import Tuple
from copy import deepcopy
from models import Computer


class UniformCrossover:
    """
    Implements uniform crossover for computer configurations.
    """
    
    def crossover(self, parent1: Computer, parent2: Computer) -> Tuple[Computer, Computer]:
        """
        Perform uniform crossover between two parents
        
        Args:
            parent1: First parent
            parent2: Second parent
            
        Returns:
            Tuple[Computer, Computer]: Two children
        """
        # Decide which components to swap using random binary mask
        mask = [random.random() < 0.5 for _ in range(8)]  # 8 components
        
        # Create child 1
        child1_cpu = parent1.cpu if mask[0] else parent2.cpu
        child1_gpu = parent1.gpu if mask[1] else parent2.gpu
        child1_ram = parent1.ram if mask[2] else parent2.ram
        child1_storage = parent1.storage if mask[3] else parent2.storage
        child1_motherboard = parent1.motherboard if mask[4] else parent2.motherboard
        child1_psu = parent1.psu if mask[5] else parent2.psu
        child1_cooling = parent1.cooling if mask[6] else parent2.cooling
        child1_case = parent1.case if mask[7] else parent2.case
        
        # Create child 2 with opposite mask
        child2_cpu = parent2.cpu if mask[0] else parent1.cpu
        child2_gpu = parent2.gpu if mask[1] else parent1.gpu
        child2_ram = parent2.ram if mask[2] else parent1.ram
        child2_storage = parent2.storage if mask[3] else parent1.storage
        child2_motherboard = parent2.motherboard if mask[4] else parent1.motherboard
        child2_psu = parent2.psu if mask[5] else parent1.psu
        child2_cooling = parent2.cooling if mask[6] else parent1.cooling
        child2_case = parent2.case if mask[7] else parent1.case
        
        # Create new computer configurations
        child1 = Computer(
            cpu=child1_cpu,
            gpu=child1_gpu,
            ram=child1_ram,
            storage=child1_storage,
            motherboard=child1_motherboard,
            psu=child1_psu,
            cooling=child1_cooling,
            case=child1_case
        )
        
        child2 = Computer(
            cpu=child2_cpu,
            gpu=child2_gpu,
            ram=child2_ram,
            storage=child2_storage,
            motherboard=child2_motherboard,
            psu=child2_psu,
            cooling=child2_cooling,
            case=child2_case
        )
        
        return child1, child2