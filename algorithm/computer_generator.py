"""
Main ComputerGenerator class that coordinates the genetic algorithm.
"""
import logging
import time
from typing import List, Dict, Any, Tuple, Optional

from models import Computer, UserPreferences
from data_manager import DataManager
# Importar el gestor de datos personalizado como alternativa
from algorithm.utils.custom_data_manager import CustomDataManager

from algorithm.fitness.fitness_calculator import FitnessCalculator
from algorithm.operations.selection import TournamentSelection
from algorithm.operations.crossover import UniformCrossover
from algorithm.operations.mutation import Mutator
from algorithm.operations.repair import CompatibilityRepairer
from algorithm.population.initializer import PopulationInitializer
from algorithm.population.diversity import DiversityCalculator
from algorithm.utils.statistics import StatisticsTracker


class ComputerGenerator:
    """
    Enhanced Genetic Algorithm for computer configuration generation
    with improved selection, crossover, mutation methods and more detailed
    fitness function.
    """
    def __init__(
        self,
        population_size: int,
        crossover_rate: float,
        mutation_rate: float,
        generations: int,
        user_preferences: UserPreferences,
        elitism_percentage: float = 0.1,
        tournament_size: int = 3,
        adaptive_mutation: bool = True,
        fitness_weights: Dict[str, float] = None,
    ) -> None:
        """
        Initialize the ComputerGenerator with genetic algorithm parameters
        
        Args:
            population_size: Size of the population in each generation
            crossover_rate: Probability of crossover
            mutation_rate: Base probability of mutation
            generations: Number of generations to run
            user_preferences: User preferences for computer configuration
            elitism_percentage: Percentage of top individuals to preserve
            tournament_size: Number of individuals in tournament selection
            adaptive_mutation: Whether to adapt mutation rate based on diversity
            fitness_weights: Weights for different components of fitness function
        """
        self.population_size: int = max(4, population_size)  # Ensure minimum population size
        self.crossover_rate: float = crossover_rate
        self.base_mutation_rate: float = mutation_rate
        self.mutation_rate: float = mutation_rate
        self.generations: int = generations
        self.elitism_percentage: float = elitism_percentage
        self.tournament_size: int = min(tournament_size, population_size // 2)
        self.adaptive_mutation: bool = adaptive_mutation
        self.user_preferences: UserPreferences = user_preferences
        
        # Get component data from manager
        self.data_manager = DataManager()
        self.cpus = self.data_manager.get_cpus()
        self.gpus = self.data_manager.get_gpus()
        self.rams = self.data_manager.get_rams()
        self.storages = self.data_manager.get_storages()
        self.motherboards = self.data_manager.get_motherboards()
        self.psus = self.data_manager.get_psus()
        self.coolings = self.data_manager.get_coolings()
        self.cases = self.data_manager.get_cases()
        
        # Create component classes
        self.fitness_calculator = FitnessCalculator(
            user_preferences=user_preferences,
            fitness_weights=fitness_weights
        )
        
        self.population_initializer = PopulationInitializer(
            cpus=self.cpus,
            gpus=self.gpus,
            rams=self.rams,
            storages=self.storages,
            motherboards=self.motherboards,
            psus=self.psus,
            coolings=self.coolings,
            cases=self.cases,
            user_preferences=user_preferences
        )
        
        self.selector = TournamentSelection(tournament_size=self.tournament_size)
        self.crossover = UniformCrossover()
        self.mutator = Mutator(
            cpus=self.cpus,
            gpus=self.gpus,
            rams=self.rams,
            storages=self.storages,
            motherboards=self.motherboards,
            psus=self.psus,
            coolings=self.coolings,
            cases=self.cases,
            mutation_rate=self.mutation_rate
        )
        
        self.repairer = CompatibilityRepairer(
            cpus=self.cpus,
            gpus=self.gpus,
            rams=self.rams,
            storages=self.storages,
            motherboards=self.motherboards,
            psus=self.psus,
            coolings=self.coolings,
            cases=self.cases
        )
        
        self.diversity_calculator = DiversityCalculator(
            cpus=self.cpus,
            gpus=self.gpus,
            rams=self.rams,
            storages=self.storages,
            motherboards=self.motherboards,
            psus=self.psus
        )
        
        self.stats_tracker = StatisticsTracker()
        
        # Initialize population list
        self.population: List[Computer] = []
        
        # Logger setup
        logging.basicConfig(level=logging.INFO, 
                           format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger("ComputerGenerator")

    def generate_initial_population(self) -> None:
        """
        Generate initial population with smart seeding and heuristics to
        create promising initial configurations.
        """
        self.logger.info("Generating initial population...")
        self.population = self.population_initializer.initialize(
            population_size=self.population_size,
            fitness_calculator=self.fitness_calculator
        )
        self.logger.info(f"Initial population created with {self.population_size} individuals")

    def update_mutation_rate(self, diversity: float) -> None:
        """
        Update mutation rate based on population diversity
        - Increase mutation when diversity is low
        - Decrease mutation when diversity is high
        
        Args:
            diversity: Current population diversity (0-1)
        """
        if not self.adaptive_mutation:
            return
            
        # If diversity is low, increase mutation rate
        if diversity < 0.3:
            self.mutation_rate = min(0.5, self.base_mutation_rate * 2)
        # If diversity is high, decrease mutation rate
        elif diversity > 0.7:
            self.mutation_rate = max(0.001, self.base_mutation_rate / 2)
        # Otherwise, reset to base rate
        else:
            self.mutation_rate = self.base_mutation_rate
        
        # Update mutator mutation rate
        self.mutator.mutation_rate = self.mutation_rate
        
        self.logger.info(f"Mutation rate adjusted to {self.mutation_rate:.4f} based on diversity of {diversity:.4f}")

    def select_elite(self, population: List[Computer], count: int) -> List[Computer]:
        """
        Select elite individuals to preserve across generations
        
        Args:
            population: Current population
            count: Number of elite individuals to select
            
        Returns:
            List[Computer]: Elite individuals
        """
        # Sort population by fitness and select top individuals
        sorted_population = sorted(population, key=lambda x: x.fitness, reverse=True)
        return sorted_population[:count]

    def run(self) -> Tuple[Computer, Dict[str, Any]]:
        """
        Run the genetic algorithm to generate optimal computer configurations
        
        Returns:
            Tuple[Computer, Dict]: Best computer and statistics dictionary
        """
        start_time = time.time()
        self.logger.info(f"Starting genetic algorithm with population size {self.population_size}")
        self.logger.info(f"User preferences: {self.user_preferences.__dict__}")
        
        # Generate initial population
        self.generate_initial_population()
        
        # Number of elite individuals to preserve
        elite_count = max(1, int(self.population_size * self.elitism_percentage))
        
        # Main evolution loop
        for generation in range(self.generations):
            self.logger.info(f"Generation {generation+1}/{self.generations}")
            
            # Calculate population diversity
            diversity = self.diversity_calculator.calculate_diversity(self.population)
            self.stats_tracker.update_diversity(diversity)
            
            # Update mutation rate based on diversity
            self.update_mutation_rate(diversity)
            
            # Select elite individuals
            elites = self.select_elite(self.population, elite_count)
            
            # Create next generation
            next_generation = []
            
            # Add elites to next generation
            next_generation.extend(elites)
            
            # Fill the rest of the population through selection, crossover, and mutation
            while len(next_generation) < self.population_size:
                # Select parents
                parent1 = self.selector.select(self.population)
                parent2 = self.selector.select(self.population)
                
                # Perform crossover
                if random.random() < self.crossover_rate:
                    child1, child2 = self.crossover.crossover(parent1, parent2)
                else:
                    child1, child2 = deepcopy(parent1), deepcopy(parent2)
                
                # Perform mutation
                child1 = self.mutator.mutate(child1)
                child2 = self.mutator.mutate(child2)
                
                # Apply repair if needed
                if random.random() < 0.5:  # 50% chance to apply repair
                    child1 = self.repairer.repair_compatibility(child1)
                if random.random() < 0.5:
                    child2 = self.repairer.repair_compatibility(child2)
                
                # Calculate fitness for children
                child1.fitness = self.fitness_calculator.calculate_fitness(child1)
                child2.fitness = self.fitness_calculator.calculate_fitness(child2)
                
                # Add children to next generation
                next_generation.append(child1)
                if len(next_generation) < self.population_size:
                    next_generation.append(child2)
            
            # Replace current population with next generation
            self.population = next_generation
            
            # Update statistics
            self.stats_tracker.update_generation_stats(self.population)
            
            # Log progress
            best_fitness = max(computer.fitness for computer in self.population)
            avg_fitness = sum(computer.fitness for computer in self.population) / len(self.population)
            self.logger.info(f"Best fitness: {best_fitness:.2f}, Avg fitness: {avg_fitness:.2f}")
            
            # Optional early stopping if converged
            if generation > 20:
                best_cases = self.stats_tracker.get_best_cases()
                if len(best_cases) >= 20 and abs(best_cases[-1].fitness - best_cases[-20].fitness) < 0.001:
                    self.logger.info("Early stopping: Convergence detected")
                    break
        
        # Get final best computer
        best_computer = max(self.population, key=lambda computer: computer.fitness)
        
        # Calculate execution time
        execution_time = time.time() - start_time
        
        # Prepare statistics
        stats = self.stats_tracker.get_final_stats()
        stats['execution_time'] = execution_time
        stats['generations_completed'] = generation + 1
        stats['final_population_size'] = len(self.population)
        
        self.logger.info(f"Genetic algorithm completed in {execution_time:.2f} seconds")
        self.logger.info(f"Best computer fitness: {best_computer.fitness:.2f}")
        
        return best_computer, stats

# Add imported modules to ensure the code will run
import random
from copy import deepcopy