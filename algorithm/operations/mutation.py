"""
Mutation operations for the genetic algorithm.
"""
import random
from copy import deepcopy
from typing import List
from models import Computer, CPU, GPU, RAM, Storage, Motherboard, PSU, Cooling, Case


class Mutator:
    """
    Implements mutation operations for computer configurations.
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
        mutation_rate: float = 0.1
    ):
        """
        Initialize the mutator with component lists and mutation rate.
        
        Args:
            cpus: List of available CPUs
            gpus: List of available GPUs
            rams: List of available RAMs
            storages: List of available storages
            motherboards: List of available motherboards
            psus: List of available PSUs
            coolings: List of available cooling solutions
            cases: List of available cases
            mutation_rate: Probability of mutation for each component
        """
        self.cpus = cpus
        self.gpus = gpus
        self.rams = rams
        self.storages = storages
        self.motherboards = motherboards
        self.psus = psus
        self.coolings = coolings
        self.cases = cases
        self.mutation_rate = mutation_rate
    
    def mutate(self, computer: Computer) -> Computer:
        """
        Mutate a computer configuration by randomly changing components
        
        Args:
            computer: Computer to mutate
            
        Returns:
            Computer: Mutated computer
        """
        mutated_computer = deepcopy(computer)
        
        # Apply mutation to each component based on mutation rate
        if random.random() < self.mutation_rate:
            mutated_computer.cpu = random.choice(self.cpus)
            
        if random.random() < self.mutation_rate:
            mutated_computer.gpu = random.choice(self.gpus)
            
        if random.random() < self.mutation_rate:
            mutated_computer.ram = random.choice(self.rams)
            
        if random.random() < self.mutation_rate:
            mutated_computer.storage = random.choice(self.storages)
            
        if random.random() < self.mutation_rate:
            mutated_computer.motherboard = random.choice(self.motherboards)
            
        if random.random() < self.mutation_rate:
            mutated_computer.psu = random.choice(self.psus)
            
        if random.random() < self.mutation_rate:
            mutated_computer.cooling = random.choice(self.coolings)
            
        if random.random() < self.mutation_rate:
            mutated_computer.case = random.choice(self.cases)
            
        return mutated_computer