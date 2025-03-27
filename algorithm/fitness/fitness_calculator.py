"""
Fitness calculation for computer configurations.
"""
from typing import Dict, Any, Optional
from models import Computer, UserPreferences
from algorithm.fitness.usage_scorer import UsageScorer


class FitnessCalculator:
    """
    Calculates fitness scores for computer configurations
    based on user preferences and various metrics.
    """
    def __init__(
        self, 
        user_preferences: UserPreferences,
        fitness_weights: Optional[Dict[str, float]] = None
    ):
        """
        Initialize the fitness calculator.
        
        Args:
            user_preferences: User preferences for computer configuration
            fitness_weights: Weights for different components of fitness function
        """
        self.user_preferences = user_preferences
        
        # Default weights for fitness function
        self.fitness_weights = {
            'price_range': 20,
            'compatibility': 25,
            'usage_match': 30,
            'power_balance': 5,
            'bottleneck': 10,
            'value_cpu': 5,
            'value_gpu': 5,
        }
        
        # Override with user-provided weights if provided
        if fitness_weights:
            self.fitness_weights.update(fitness_weights)
            
        # Initialize usage scorer
        self.usage_scorer = UsageScorer()

    def calculate_fitness(self, computer: Computer) -> float:
        """
        Enhanced fitness function with weighted components based on user preferences
        
        Args:
            computer: Computer configuration to evaluate
            
        Returns:
            float: Fitness score of the computer configuration
        """
        fitness_score: float = 0.0

        # Price range factor - more points for being closer to middle of range
        price_range_score = self.calculate_price_range_score(computer)
        fitness_score += self.fitness_weights['price_range'] * price_range_score
        
        # Compatibility between components
        compatibility_score = self.calculate_compatibility_score(computer)
        fitness_score += self.fitness_weights['compatibility'] * compatibility_score
        
        # Score for matching the intended usage
        usage_score = self.get_usage_score(computer)
        fitness_score += self.fitness_weights['usage_match'] * usage_score
        
        # Power balance - PSU should be adequate but not overpowered
        power_balance_score = self.calculate_power_balance(computer)
        fitness_score += self.fitness_weights['power_balance'] * power_balance_score
        
        # Bottleneck analysis
        bottleneck_score = 1.0 if computer.is_bottleneck() else 0.0
        fitness_score += self.fitness_weights['bottleneck'] * bottleneck_score
        
        # Value for money - CPU
        cpu_value_score = min(1.0, computer.points_for_relation_quality_cpu() / 100.0)
        fitness_score += self.fitness_weights['value_cpu'] * cpu_value_score
        
        # Value for money - GPU
        gpu_value_score = min(1.0, computer.points_for_relation_quality_gpu() / 100.0)
        fitness_score += self.fitness_weights['value_gpu'] * gpu_value_score
        
        # Cooling adequacy for CPU thermal output
        cooling_score = self.calculate_cooling_score(computer)
        fitness_score += 5 * cooling_score
        
        # Physical compatibility (case fits all components)
        case_score = self.calculate_case_compatibility(computer)
        fitness_score += 5 * case_score

        return fitness_score

    def calculate_price_range_score(self, computer: Computer) -> float:
        """Calculate how well the computer fits in the desired price range"""
        if not self.is_within_price_range(computer):
            return 0.0
            
        # Calculate distance from middle of price range
        price_range_mid = (self.user_preferences.min_price + self.user_preferences.max_price) / 2
        max_distance = (self.user_preferences.max_price - self.user_preferences.min_price) / 2
        
        # Normalize to 0-1 range where 1 is being at middle of range
        distance = abs(computer.price - price_range_mid)
        normalized_score = 1.0 - min(1.0, distance / max_distance)
        
        return normalized_score

    def calculate_compatibility_score(self, computer: Computer) -> float:
        """Check compatibility between all components"""
        score = 0.0
        
        # CPU-Motherboard compatibility
        if computer.motherboard.is_cpu_compatible(computer.cpu):
            score += 0.4
            
        # RAM-Motherboard compatibility
        if computer.motherboard.is_ram_compatible(computer.ram):
            score += 0.3
            
        # GPU-PSU compatibility (power requirements)
        if computer.gpu:
            gpu_power_ok = computer.gpu.power_consumption <= computer.psu.capacity * 0.7
            score += 0.3 if gpu_power_ok else 0
            
        # Cooling compatibility with CPU
        cooling_adequate = computer.cooling.cooling_capacity >= computer.cpu.power_consumption
        score += 0.2 if cooling_adequate else 0
        
        # Case compatibility with components
        if computer.case.can_fit_all_components(computer):
            score += 0.2
            
        return min(1.0, score)  # Cap at 1.0

    def calculate_power_balance(self, computer: Computer) -> float:
        """Calculate how well-balanced the power supply is"""
        # Calculate total power consumption
        total_power = (
            computer.cpu.power_consumption + 
            (computer.gpu.power_consumption if computer.gpu else 0) + 
            computer.motherboard.power_consumption + 
            50  # Base power for other components
        )
        
        # Calculate PSU capacity ratio (how much headroom)
        capacity_ratio = computer.psu.capacity / total_power if total_power > 0 else 0
        
        # Ideal ratio is between 1.2 and 1.5
        if capacity_ratio < 1.0:
            return 0.0  # Underpowered
        elif 1.2 <= capacity_ratio <= 1.5:
            return 1.0  # Optimal
        else:
            # Penalize for overpowered PSU
            return max(0.0, 1.0 - (capacity_ratio - 1.5) / 0.5)

    def calculate_cooling_score(self, computer: Computer) -> float:
        """Calculate adequacy of cooling solution"""
        cpu_tdp = computer.cpu.power_consumption
        cooling_capacity = computer.cooling.cooling_capacity
        
        # Calculate cooling adequacy ratio
        cooling_ratio = cooling_capacity / cpu_tdp if cpu_tdp > 0 else 0
        
        # Score based on how well cooling matches CPU needs
        if cooling_ratio < 1.0:
            return 0.0  # Inadequate cooling
        elif 1.0 <= cooling_ratio <= 1.5:
            return 1.0  # Optimal cooling
        else:
            # Slightly penalize excessive cooling (costs more)
            return max(0.7, 1.0 - (cooling_ratio - 1.5) / 2.0)

    def calculate_case_compatibility(self, computer: Computer) -> float:
        """Check if case can fit all components properly"""
        # Check if case supports motherboard form factor
        if not computer.case.supports_motherboard_form_factor(computer.motherboard.form_factor):
            return 0.0
            
        # Check if case has enough space for GPU
        if computer.gpu and not computer.case.can_fit_gpu(computer.gpu):
            return 0.0
            
        # Check cooling compatibility with case
        if not computer.case.supports_cooling_type(computer.cooling.type):
            return 0.0
            
        return 1.0

    def is_within_price_range(self, computer: Computer) -> bool:
        """Check if computer price is within user's specified range"""
        return (
            self.user_preferences.min_price <= computer.price <= self.user_preferences.max_price
        )

    def get_usage_score(self, computer: Computer) -> float:
        """
        Calculate how well the computer matches the intended usage
        Returns a normalized score between 0 and 1
        """
        # Get the raw score from usage scorer
        raw_score = self.usage_scorer.score_for_usage(
            computer=computer,
            usage=self.user_preferences.usage
        )
        
        # Normalize to 0-1 range
        return raw_score / 30.0  # Normalize by max score