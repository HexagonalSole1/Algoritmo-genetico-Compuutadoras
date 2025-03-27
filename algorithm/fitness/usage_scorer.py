"""
Scores computers based on their suitability for different usage types.
"""
from typing import Dict
from models import Computer


class UsageScorer:
    """
    Calculates scores for how well a computer configuration
    matches different usage types.
    """
    
    def score_for_usage(self, computer: Computer, usage: str) -> float:
        """
        Score a computer for a specific usage type.
        
        Args:
            computer: The computer to score
            usage: The usage type (e.g., 'gaming', 'office')
            
        Returns:
            float: Score for how well the computer matches the usage type
        """
        usage_scores = {
            "ofimática": self.get_ofimatica_score(computer),
            "juegos": self.get_gaming_score(computer),
            "diseño gráfico": self.get_graphics_design_score(computer),
            "edición de video": self.get_video_editing_score(computer),
            "navegación web": self.get_web_navigation_score(computer),
            "educación": self.get_education_score(computer),
            "arquitectura": self.get_architecture_score(computer),
        }
        
        return usage_scores.get(usage, 0.0)

    def get_education_score(self, computer: Computer) -> float:
        """Score computer for educational use"""
        score = 0.0
        
        # CPU performance requirements
        if 30 <= computer.cpu.performance <= 60:
            score += 10.0
        elif computer.cpu.performance > 60:
            score += 5.0  # Overkill but works
            
        # RAM requirements
        if 8 < computer.ram.capacity <= 16:
            score += 8.0
        elif computer.ram.capacity > 16:
            score += 5.0  # More than needed
            
        # Storage requirements
        if computer.storage.type == "SSD" and 128 < computer.storage.capacity <= 500:
            score += 7.0
        elif computer.storage.type == "SSD" and computer.storage.capacity > 500:
            score += 5.0
            
        # Graphics requirements
        if ((computer.gpu and computer.gpu.power < 40) or 
            (computer.cpu.has_integrated_graphics and computer.cpu.integrated_graphics_power < 60)):
            score += 5.0
            
        return score

    def get_web_navigation_score(self, computer: Computer) -> float:
        """Score computer for web browsing"""
        score = 0.0
        
        # CPU performance for web browsing
        if 10 <= computer.cpu.performance <= 30:
            score += 8.0
        elif computer.cpu.performance > 30:
            score += 4.0  # Overkill
            
        # RAM requirements
        if computer.ram.capacity == 8:
            score += 8.0
        elif computer.ram.capacity > 8:
            score += 4.0  # More than needed
            
        # Storage requirements
        if computer.storage.type == "SSD" and computer.storage.capacity < 500:
            score += 7.0
        elif computer.storage.type == "SSD":
            score += 5.0
            
        # Graphics requirements
        if computer.gpu is None and computer.cpu.integrated_graphics_power < 20:
            score += 7.0  # Integrated graphics are sufficient
        elif computer.gpu is None:
            score += 5.0
        else:
            score += 2.0  # Dedicated GPU unnecessary
            
        return score

    def get_video_editing_score(self, computer: Computer) -> float:
        """Score computer for video editing"""
        score = 0.0
        
        # GPU requirements
        if computer.gpu and computer.gpu.power >= 60:
            score += 10.0
        elif computer.gpu and computer.gpu.power >= 30:
            score += 7.0
        elif computer.gpu:
            score += 3.0
            
        # CPU performance
        if computer.cpu.performance >= 70:
            score += 8.0
        elif computer.cpu.performance >= 50:
            score += 5.0
            
        # RAM requirements
        if computer.ram.capacity >= 32:
            score += 7.0
        elif computer.ram.capacity >= 16:
            score += 3.0
            
        # Storage requirements
        if computer.storage.type == "SSD" and computer.storage.capacity > 1000:
            score += 5.0
        elif computer.storage.type == "SSD":
            score += 2.0
            
        return score

    def get_graphics_design_score(self, computer: Computer) -> float:
        """Score computer for graphic design use"""
        score = 0.0
        
        # GPU requirements
        if computer.gpu and computer.gpu.power >= 50:
            score += 10.0
        elif computer.gpu and computer.gpu.power >= 30:
            score += 8.0
        elif computer.gpu:
            score += 4.0
            
        # CPU performance
        if computer.cpu.performance >= 60:
            score += 7.0
        elif computer.cpu.performance >= 40:
            score += 5.0
            
        # RAM requirements
        if computer.ram.capacity >= 32:
            score += 7.0
        elif computer.ram.capacity >= 16:
            score += 5.0
            
        # Storage requirements
        if computer.storage.type == "SSD" and computer.storage.capacity > 1000:
            score += 6.0
        elif computer.storage.type == "SSD" and computer.storage.capacity > 500:
            score += 4.0
            
        return score

    def get_gaming_score(self, computer: Computer) -> float:
        """Score computer for gaming use"""
        score = 0.0
        
        # GPU is critical for gaming
        if computer.gpu and computer.gpu.power >= 70:
            score += 12.0
        elif computer.gpu and computer.gpu.power >= 50:
            score += 8.0
        elif computer.gpu:
            score += 4.0
            
        # CPU performance
        if computer.cpu.performance >= 70:
            score += 7.0
        elif computer.cpu.performance >= 60:
            score += 5.0
            
        # RAM requirements
        if computer.ram.capacity >= 32:
            score += 5.0
        elif computer.ram.capacity >= 16:
            score += 4.0
            
        # Storage requirements
        if computer.storage.type == "SSD" and computer.storage.capacity >= 1000:
            score += 6.0
        elif computer.storage.type == "SSD":
            score += 4.0
            
        return score

    def get_ofimatica_score(self, computer: Computer) -> float:
        """Score computer for office work"""
        score = 0.0
        
        # CPU performance
        if computer.cpu.performance >= 20:
            score += 7.0
        elif computer.cpu.performance >= 10:
            score += 5.0
            
        # RAM requirements
        if computer.ram.capacity >= 16:
            score += 7.0
        elif computer.ram.capacity >= 8:
            score += 5.0
            
        # Storage requirements
        if computer.storage.capacity > 1000:
            score += 7.0
        elif computer.storage.capacity > 500:
            score += 5.0
            
        # Graphics requirements
        if computer.gpu is None:
            score += 5.0  # Integrated graphics are sufficient
        elif computer.gpu and computer.gpu.power < 30:
            score += 4.0  # Low-end dedicated GPU
        else:
            score += 2.0  # High-end GPU is unnecessary
            
        return score

    def get_architecture_score(self, computer: Computer) -> float:
        """Score computer for architectural design software"""
        score = 0.0
        
        # GPU requirements
        if computer.gpu and computer.gpu.power >= 80:
            score += 10.0
        elif computer.gpu and computer.gpu.power >= 60:
            score += 7.0
        elif computer.gpu:
            score += 3.0
            
        # CPU performance
        if computer.cpu.performance >= 75:
            score += 8.0
        elif computer.cpu.performance >= 60:
            score += 5.0
            
        # RAM requirements
        if computer.ram.capacity >= 64:
            score += 7.0
        elif computer.ram.capacity >= 32:
            score += 5.0
            
        # Storage requirements
        if computer.storage.type == "SSD" and computer.storage.capacity > 2000:
            score += 5.0
        elif computer.storage.type == "SSD" and computer.storage.capacity > 1000:
            score += 3.0
            
        return score