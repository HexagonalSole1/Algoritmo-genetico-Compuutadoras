"""
Selection operations for the genetic algorithm.
"""
import random
from typing import List
from models import Computer


class TournamentSelection:
    """
    Implements tournament selection for the genetic algorithm.
    """
    
    def __init__(self, tournament_size: int = 3):
        """
        Initialize the tournament selection.
        
        Args:
            tournament_size: Number of individuals to include in each tournament
        """
        self.tournament_size = tournament_size
    
    def select(self, population: List[Computer]) -> Computer:
        """
        Select an individual using tournament selection
        
        Args:
            population: List of computer configurations to select from
            
        Returns:
            Computer: Selected individual
        """
        # Randomly select individuals for tournament
        tournament = random.sample(population, min(self.tournament_size, len(population)))
        
        # Select the best individual from tournament
        return max(tournament, key=lambda computer: computer.fitness)