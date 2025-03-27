"""
Statistics tracking for the genetic algorithm.
"""
from typing import List, Dict, Any
from models import Computer


class StatisticsTracker:
    """
    Tracks statistics during the genetic algorithm execution.
    """
    
    def __init__(self):
        """Initialize the statistics tracker."""
        # Statistics tracking
        self.best_cases: List[Computer] = []
        self.avg_cases: List[float] = []
        self.worst_cases: List[Computer] = []
        self.diversity_history: List[float] = []
    
    def update_generation_stats(self, population: List[Computer]) -> None:
        """
        Update statistics for the current generation.
        
        Args:
            population: Current population of computer configurations
        """
        if not population:
            return
            
        # Calculate statistics
        fitness_values = [computer.fitness for computer in population]
        best_fitness_idx = fitness_values.index(max(fitness_values))
        worst_fitness_idx = fitness_values.index(min(fitness_values))
        avg_fitness = sum(fitness_values) / len(fitness_values)
        
        # Store best, worst, and average cases
        self.best_cases.append(population[best_fitness_idx])
        self.worst_cases.append(population[worst_fitness_idx])
        self.avg_cases.append(avg_fitness)
    
    def update_diversity(self, diversity: float) -> None:
        """
        Update diversity history.
        
        Args:
            diversity: Current population diversity
        """
        self.diversity_history.append(diversity)
    
    def get_best_cases(self) -> List[Computer]:
        """
        Get the history of best cases.
        
        Returns:
            List[Computer]: History of best computer configurations
        """
        return self.best_cases
    
    def get_final_stats(self) -> Dict[str, Any]:
        """
        Get final statistics.
        
        Returns:
            Dict[str, Any]: Dictionary of statistics
        """
        stats = {
            'best_fitness_history': [computer.fitness for computer in self.best_cases],
            'worst_fitness_history': [computer.fitness for computer in self.worst_cases],
            'avg_fitness_history': self.avg_cases,
            'diversity_history': self.diversity_history,
            'final_diversity': self.diversity_history[-1] if self.diversity_history else 0,
        }
        
        return stats