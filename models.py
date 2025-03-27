from copy import deepcopy
from typing import List, Dict, Any, Optional, Union

class CPU:
    """Enhanced CPU model with additional attributes"""
    def __init__(
        self,
        maker: str,
        model: str,
        performance: int,
        price: float,
        power_consumption: int,
        has_integrated_graphics: bool = False,
        integrated_graphics_power: int = 0,
        socket_type: str = "LGA1700",  # Added socket type
        cores: int = 4,                # Added core count
        threads: int = 8,              # Added thread count
        base_clock: float = 3.0,       # Added base clock speed
        boost_clock: float = 4.0,      # Added boost clock speed
        tdp: int = 65                  # Added TDP
    ) -> None:
        self.maker: str = maker
        self.model: str = model
        self.performance: int = performance
        self.price: float = price
        self.power_consumption: int = power_consumption
        self.has_integrated_graphics: bool = has_integrated_graphics
        self.integrated_graphics_power: int = integrated_graphics_power
        self.socket_type: str = socket_type
        self.cores: int = cores
        self.threads: int = threads
        self.base_clock: float = base_clock
        self.boost_clock: float = boost_clock
        self.tdp: int = tdp

    def __deepcopy__(self, memo):
        return CPU(
            self.maker,
            self.model,
            self.performance,
            self.price,
            self.power_consumption,
            self.has_integrated_graphics,
            self.integrated_graphics_power,
            self.socket_type,
            self.cores,
            self.threads,
            self.base_clock,
            self.boost_clock,
            self.tdp
        )

    def __str__(self):
        igpu_info = f", iGPU: {self.integrated_graphics_power}" if self.has_integrated_graphics else ""
        return f"CPU: {self.maker} {self.model}, {self.cores}C/{self.threads}T, {self.base_clock}-{self.boost_clock}GHz{igpu_info}, ${self.price:.2f}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert CPU to dictionary for serialization"""
        return {
            "maker": self.maker,
            "model": self.model,
            "performance": self.performance,
            "price": self.price,
            "power_consumption": self.power_consumption,
            "has_integrated_graphics": self.has_integrated_graphics,
            "integrated_graphics_power": self.integrated_graphics_power,
            "socket_type": self.socket_type,
            "cores": self.cores,
            "threads": self.threads,
            "base_clock": self.base_clock,
            "boost_clock": self.boost_clock,
            "tdp": self.tdp
        }


class GPU:
    """Enhanced GPU model with additional attributes"""
    def __init__(
        self, 
        maker: str, 
        price: float, 
        power_consumption: int,
        power: int,
        vram: int = 8,                  # Added VRAM amount
        vram_type: str = "GDDR6",       # Added VRAM type
        bus_width: int = 256,           # Added memory bus width
        ray_tracing: bool = False,      # Added ray tracing support
        length_mm: int = 250            # Added physical length
    ) -> None:
        self.maker: str = maker
        self.price: float = price
        self.power_consumption: int = power_consumption
        self.power: int = power
        self.vram: int = vram
        self.vram_type: str = vram_type
        self.bus_width: int = bus_width
        self.ray_tracing: bool = ray_tracing
        self.length_mm: int = length_mm

    def __deepcopy__(self, memo):
        return GPU(
            self.maker,
            self.price, 
            self.power_consumption,
            self.power,
            self.vram,
            self.vram_type,
            self.bus_width,
            self.ray_tracing,
            self.length_mm
        )

    def __str__(self):
        rt_support = ", Ray Tracing" if self.ray_tracing else ""
        return f"GPU: {self.maker}, {self.vram}GB {self.vram_type}{rt_support}, ${self.price:.2f}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert GPU to dictionary for serialization"""
        return {
            "maker": self.maker,
            "price": self.price,
            "power_consumption": self.power_consumption,
            "power": self.power,
            "vram": self.vram,
            "vram_type": self.vram_type,
            "bus_width": self.bus_width,
            "ray_tracing": self.ray_tracing,
            "length_mm": self.length_mm
        }


class RAM:
    """Enhanced RAM model with additional attributes"""
    def __init__(
        self,
        maker: str,
        model: str,
        capacity: int,
        frequency: int,
        type: str,
        price: float,
        latency: str = "CL16",      # Added latency
        voltage: float = 1.35,      # Added voltage
        rgb: bool = False,          # Added RGB lighting
        heat_spreader: bool = True  # Added heat spreader
    ) -> None:
        self.maker: str = maker
        self.model: str = model
        self.capacity: int = capacity
        self.frequency: int = frequency
        self.type: str = type
        self.price: float = price
        self.latency: str = latency
        self.voltage: float = voltage
        self.rgb: bool = rgb
        self.heat_spreader: bool = heat_spreader

    def __str__(self):
        rgb_info = ", RGB" if self.rgb else ""
        return f"RAM: {self.maker} {self.model}, {self.capacity}GB {self.type}-{self.frequency}MHz {self.latency}{rgb_info}, ${self.price:.2f}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert RAM to dictionary for serialization"""
        return {
            "maker": self.maker,
            "model": self.model,
            "capacity": self.capacity,
            "frequency": self.frequency,
            "type": self.type,
            "price": self.price,
            "latency": self.latency,
            "voltage": self.voltage,
            "rgb": self.rgb,
            "heat_spreader": self.heat_spreader
        }


class Storage:
    """Enhanced Storage model with additional attributes"""
    def __init__(
        self, 
        maker: str, 
        model: str, 
        type: str, 
        capacity: float,
        price: float,
        interface: str = "NVMe",     # Added interface type
        read_speed: int = 3500,      # Added read speed in MB/s
        write_speed: int = 3000,     # Added write speed in MB/s
        tbw: int = 600,              # Added terabytes written endurance
        form_factor: str = "M.2"     # Added form factor
    ) -> None:
        self.maker: str = maker
        self.model: str = model
        self.type: str = type
        self.capacity: float = capacity
        self.price: float = price
        self.interface: str = interface
        self.read_speed: int = read_speed
        self.write_speed: int = write_speed
        self.tbw: int = tbw
        self.form_factor: str = form_factor

    def __str__(self):
        capacity_str = f"{int(self.capacity)}GB" if self.capacity < 1000 else f"{self.capacity/1000:.1f}TB"
        return f"Storage: {self.maker} {self.model} {self.type} {capacity_str} ({self.interface}, {self.form_factor}), ${self.price:.2f}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert Storage to dictionary for serialization"""
        return {
            "maker": self.maker,
            "model": self.model,
            "type": self.type,
            "capacity": self.capacity,
            "price": self.price,
            "interface": self.interface,
            "read_speed": self.read_speed,
            "write_speed": self.write_speed,
            "tbw": self.tbw,
            "form_factor": self.form_factor
        }


class Motherboard:
    """Enhanced Motherboard model with additional attributes"""
    def __init__(
        self,
        maker: str,
        model: str,
        price: float,
        power_consumption: int,
        max_ram_capacity: int,
        max_ram_frequency: int,
        ram_socket_type: str,
        compatible_cpus: list,
        form_factor: str = "ATX",            # Added form factor
        socket_type: str = "LGA1700",        # Added socket type
        pcie_slots: int = 3,                 # Added PCIe slots
        m2_slots: int = 2,                   # Added M.2 slots
        sata_ports: int = 6,                 # Added SATA ports
        wifi: bool = False,                  # Added WiFi support
        bluetooth: bool = False,             # Added Bluetooth support
        usb_ports: Dict[str, int] = None     # Added USB ports configuration
    ) -> None:
        self.maker: str = maker
        self.model: str = model
        self.price: float = price
        self.power_consumption: int = power_consumption
        self.max_ram_capacity: int = max_ram_capacity
        self.max_ram_frequency: int = max_ram_frequency
        self.ram_socket_type: str = ram_socket_type
        self.compatible_cpus: list = compatible_cpus
        self.form_factor: str = form_factor
        self.socket_type: str = socket_type
        self.pcie_slots: int = pcie_slots
        self.m2_slots: int = m2_slots
        self.sata_ports: int = sata_ports
        self.wifi: bool = wifi
        self.bluetooth: bool = bluetooth
        self.usb_ports: Dict[str, int] = usb_ports or {"USB 3.0": 4, "USB 2.0": 2}

    def is_cpu_compatible(self, cpu: CPU) -> bool:
        """
        Check if CPU is compatible with the motherboard.
        Now also checks socket compatibility.
        """
        model_compatible = cpu.model in self.compatible_cpus
        socket_compatible = cpu.socket_type == self.socket_type
        return model_compatible and socket_compatible

    def is_ram_compatible(self, ram: RAM) -> bool:
        """Check if RAM is compatible with motherboard"""
        return (
            ram.type == self.ram_socket_type
            and ram.frequency <= self.max_ram_frequency
            and ram.capacity <= self.max_ram_capacity
        )

    def __deepcopy__(self, memo):
        return Motherboard(
            self.maker,
            self.model,
            self.price,
            self.power_consumption,
            self.max_ram_capacity,
            self.max_ram_frequency,
            self.ram_socket_type,
            deepcopy(self.compatible_cpus),
            self.form_factor,
            self.socket_type,
            self.pcie_slots,
            self.m2_slots,
            self.sata_ports,
            self.wifi,
            self.bluetooth,
            deepcopy(self.usb_ports)
        )

    def __str__(self):
        connectivity = []
        if self.wifi:
            connectivity.append("WiFi")
        if self.bluetooth:
            connectivity.append("BT")
        connectivity_str = f", {'+'.join(connectivity)}" if connectivity else ""
        
        return f"Motherboard: {self.maker} {self.model}"
    def __str__(self):
        connectivity = []
        if self.wifi:
            connectivity.append("WiFi")
        if self.bluetooth:
            connectivity.append("BT")
        connectivity_str = f", {'+'.join(connectivity)}" if connectivity else ""
        
        return f"Motherboard: {self.maker} {self.model} {self.form_factor}, {self.socket_type}, {self.ram_socket_type}{connectivity_str}, ${self.price:.2f}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert Motherboard to dictionary for serialization"""
        return {
            "maker": self.maker,
            "model": self.model,
            "price": self.price,
            "power_consumption": self.power_consumption,
            "max_ram_capacity": self.max_ram_capacity,
            "max_ram_frequency": self.max_ram_frequency,
            "ram_socket_type": self.ram_socket_type,
            "compatible_cpus": self.compatible_cpus,
            "form_factor": self.form_factor,
            "socket_type": self.socket_type,
            "pcie_slots": self.pcie_slots,
            "m2_slots": self.m2_slots,
            "sata_ports": self.sata_ports,
            "wifi": self.wifi,
            "bluetooth": self.bluetooth,
            "usb_ports": self.usb_ports
        }


class PSU:
    """Enhanced PSU model with additional attributes"""
    def __init__(
        self, 
        maker: str, 
        model: str, 
        capacity: int, 
        price: float,
        efficiency: str = "80+ Gold",    # Added efficiency rating
        modular: str = "Semi",           # Added modularity (Full, Semi, None)
        fan_size: int = 120,             # Added fan size in mm
        length_mm: int = 150,            # Added physical length
        atx_version: str = "ATX 3.0"     # Added ATX version
    ) -> None:
        self.maker: str = maker
        self.model: str = model
        self.capacity: int = capacity
        self.price: float = price
        self.efficiency: str = efficiency
        self.modular: str = modular
        self.fan_size: int = fan_size
        self.length_mm: int = length_mm
        self.atx_version: str = atx_version

    def __deepcopy__(self, memo):
        return PSU(
            self.maker, 
            self.model, 
            self.capacity, 
            self.price,
            self.efficiency,
            self.modular,
            self.fan_size,
            self.length_mm,
            self.atx_version
        )

    def __str__(self) -> str:
        return f"PSU: {self.maker} {self.model}, {self.capacity}W, {self.efficiency}, {self.modular}-Modular, ${self.price:.2f}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert PSU to dictionary for serialization"""
        return {
            "maker": self.maker,
            "model": self.model,
            "capacity": self.capacity,
            "price": self.price,
            "efficiency": self.efficiency,
            "modular": self.modular,
            "fan_size": self.fan_size,
            "length_mm": self.length_mm,
            "atx_version": self.atx_version
        }


class Cooling:
    """New Cooling model for CPU cooling solutions"""
    def __init__(
        self,
        maker: str,
        model: str,
        type: str,                    # Air or Liquid
        cooling_capacity: int,        # In TDP watts
        price: float,
        noise_level: int = 30,        # In dB
        fan_count: int = 1,           # Number of fans
        fan_size: int = 120,          # Fan size in mm
        rgb: bool = False,            # RGB lighting
        height_mm: int = 150          # Height for air coolers or radiator size for liquid
    ) -> None:
        self.maker: str = maker
        self.model: str = model
        self.type: str = type
        self.cooling_capacity: int = cooling_capacity
        self.price: float = price
        self.noise_level: int = noise_level
        self.fan_count: int = fan_count
        self.fan_size: int = fan_size
        self.rgb: bool = rgb
        self.height_mm: int = height_mm

    def __deepcopy__(self, memo):
        return Cooling(
            self.maker,
            self.model,
            self.type,
            self.cooling_capacity,
            self.price,
            self.noise_level,
            self.fan_count,
            self.fan_size,
            self.rgb,
            self.height_mm
        )

    def __str__(self) -> str:
        rgb_info = ", RGB" if self.rgb else ""
        size_info = f", {self.height_mm}mm"
        if self.type == "Liquid":
            size_info = f", {self.height_mm}mm Radiator"
        return f"Cooling: {self.maker} {self.model} {self.type}, {self.fan_count}x{self.fan_size}mm{rgb_info}{size_info}, ${self.price:.2f}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert Cooling to dictionary for serialization"""
        return {
            "maker": self.maker,
            "model": self.model,
            "type": self.type,
            "cooling_capacity": self.cooling_capacity,
            "price": self.price,
            "noise_level": self.noise_level,
            "fan_count": self.fan_count,
            "fan_size": self.fan_size,
            "rgb": self.rgb,
            "height_mm": self.height_mm
        }


class Case:
    """New Case model for computer chassis"""
    def __init__(
        self,
        maker: str,
        model: str,
        form_factors: List[str],        # Supported motherboard form factors
        max_gpu_length: int,            # Maximum GPU length in mm
        cooling_support: Dict[str, Any], # Dict of cooling support details
        price: float,
        dimensions: Dict[str, int] = None,  # Width, height, depth in mm
        included_fans: int = 2,           # Number of included fans
        drive_bays: Dict[str, int] = None, # Number of each type of drive bay
        psu_mount: str = "Bottom",        # PSU mount location
        front_io: Dict[str, int] = None,  # Front I/O ports
        side_panel: str = "Glass"          # Side panel type
    ) -> None:
        self.maker: str = maker
        self.model: str = model
        self.form_factors: List[str] = form_factors
        self.max_gpu_length: int = max_gpu_length
        self.cooling_support: Dict[str, Any] = cooling_support
        self.price: float = price
        self.dimensions: Dict[str, int] = dimensions or {"width": 210, "height": 450, "depth": 400}
        self.included_fans: int = included_fans
        self.drive_bays: Dict[str, int] = drive_bays or {"3.5": 2, "2.5": 2}
        self.psu_mount: str = psu_mount
        self.front_io: Dict[str, int] = front_io or {"USB 3.0": 2, "USB-C": 1, "Audio": 1}
        self.side_panel: str = side_panel

    def __deepcopy__(self, memo):
        return Case(
            self.maker,
            self.model,
            deepcopy(self.form_factors),
            self.max_gpu_length,
            deepcopy(self.cooling_support),
            self.price,
            deepcopy(self.dimensions),
            self.included_fans,
            deepcopy(self.drive_bays),
            self.psu_mount,
            deepcopy(self.front_io),
            self.side_panel
        )

    def __str__(self) -> str:
        form_factors_str = "/".join(self.form_factors)
        dimensions_str = f"{self.dimensions['width']}×{self.dimensions['height']}×{self.dimensions['depth']}mm"
        return f"Case: {self.maker} {self.model}, {form_factors_str}, {dimensions_str}, {self.side_panel} Panel, ${self.price:.2f}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert Case to dictionary for serialization"""
        return {
            "maker": self.maker,
            "model": self.model,
            "form_factors": self.form_factors,
            "max_gpu_length": self.max_gpu_length,
            "cooling_support": self.cooling_support,
            "price": self.price,
            "dimensions": self.dimensions,
            "included_fans": self.included_fans,
            "drive_bays": self.drive_bays,
            "psu_mount": self.psu_mount,
            "front_io": self.front_io,
            "side_panel": self.side_panel
        }

    def supports_motherboard_form_factor(self, form_factor: str) -> bool:
        """Check if case supports the given motherboard form factor"""
        return form_factor in self.form_factors

    def can_fit_gpu(self, gpu: GPU) -> bool:
        """Check if case can fit the given GPU"""
        return gpu.length_mm <= self.max_gpu_length

    def supports_cooling_type(self, cooling_type: str) -> bool:
        """Check if case supports the given cooling type"""
        if cooling_type == "Air":
            return "max_air_cooler_height" in self.cooling_support
        elif cooling_type == "Liquid":
            return "radiator_support" in self.cooling_support
        return False

    def can_fit_all_components(self, computer) -> bool:
        """Check if case can fit all components in the computer"""
        # Check motherboard compatibility
        if not self.supports_motherboard_form_factor(computer.motherboard.form_factor):
            return False
        
        # Check GPU compatibility if present
        if computer.gpu and not self.can_fit_gpu(computer.gpu):
            return False
        
        # Check cooling compatibility
        if not self.supports_cooling_type(computer.cooling.type):
            return False
        
        # For air cooling, check height clearance
        if computer.cooling.type == "Air" and computer.cooling.height_mm > self.cooling_support.get("max_air_cooler_height", 0):
            return False
        
        # For liquid cooling, check radiator support
        if computer.cooling.type == "Liquid":
            radiator_size = computer.cooling.height_mm
            supported_sizes = self.cooling_support.get("radiator_support", [])
            if radiator_size not in supported_sizes:
                return False
        
        return True
    def is_compatible_with_motherboard(self, motherboard):
        """Check if case is compatible with the given motherboard"""
        return self.supports_motherboard_form_factor(motherboard.form_factor)


class Computer:
    """Enhanced Computer model with additional components and metrics"""
    def __init__(
        self,
        cpu: CPU,
        gpu: Optional[GPU],
        ram: RAM,
        storage: Storage,
        motherboard: Motherboard,
        psu: PSU,
        cooling: Cooling,          # Added cooling component
        case: Case,                # Added case component
        fitness: float = 0,        # For genetic algorithm
        additional_storages: List[Storage] = None,  # Multiple storage support
        estimated_performance: Dict[str, float] = None  # Performance estimates
    ) -> None:
        self.cpu: CPU = cpu
        self.gpu: Optional[GPU] = gpu
        self.ram: RAM = ram
        self.storage: Storage = storage
        self.motherboard: Motherboard = motherboard
        self.psu: PSU = psu
        self.cooling: Cooling = cooling
        self.case: Case = case
        self.additional_storages: List[Storage] = additional_storages or []
        
        # Calculate total price
        self.price: float = (
            self.cpu.price
            + (self.gpu.price if self.gpu else 0) 
            + self.ram.price
            + self.storage.price
            + self.motherboard.price
            + self.psu.price
            + self.cooling.price
            + self.case.price
            + sum(storage.price for storage in self.additional_storages)
        )
        
        self.fitness = fitness
        
        # Estimated performance metrics for different tasks
        self.estimated_performance = estimated_performance or self._calculate_estimated_performance()

    def _calculate_estimated_performance(self) -> Dict[str, float]:
        """Calculate estimated performance metrics for different tasks"""
        performance = {}
        
        # Gaming performance (heavily GPU dependent)
        if self.gpu:
            gaming_score = (0.7 * self.gpu.power + 0.3 * self.cpu.performance) * (1 + self.ram.capacity / 100)
            performance["gaming"] = min(100, gaming_score)
        else:
            # Fall back to CPU integrated graphics if available
            if self.cpu.has_integrated_graphics:
                gaming_score = (0.7 * self.cpu.integrated_graphics_power + 0.3 * self.cpu.performance) * (1 + self.ram.capacity / 100)
                performance["gaming"] = min(100, gaming_score / 2)  # Reduced score for integrated graphics
            else:
                performance["gaming"] = 0  # No graphics capability
        
        # Productivity (office work, web browsing, etc.)
        productivity_score = (0.6 * self.cpu.performance + 0.3 * self.ram.capacity / 32 + 0.1 * (100 if self.storage.type == "SSD" else 50)) 
        performance["productivity"] = min(100, productivity_score)
        
        # Content creation (video editing, rendering, etc.)
        content_creation_score = (0.4 * self.cpu.performance + 0.3 * (self.gpu.power if self.gpu else 0) + 0.2 * self.ram.capacity / 32 + 0.1 * self.storage.capacity / 1000)
        performance["content_creation"] = min(100, content_creation_score)
        
        # Development (programming, compiling, etc.)
        development_score = (0.5 * self.cpu.performance + 0.4 * self.ram.capacity / 32 + 0.1 * (100 if self.storage.type == "SSD" else 50))
        performance["development"] = min(100, development_score)
        
        return performance

    def __str__(self):
        storages_str = ""
        if self.additional_storages:
            storages_str = "\n".join([f"Additional Storage: {str(storage)}" for storage in self.additional_storages])
            storages_str = "\n" + storages_str
            
        return (
            f"Computer Configuration:\n"
            f"{str(self.cpu)}\n"
            f"{str(self.gpu) if self.gpu else 'GPU: None (Using Integrated Graphics)'}\n"
            f"{str(self.ram)}\n"
            f"{str(self.storage)}{storages_str}\n"
            f"{str(self.motherboard)}\n"
            f"{str(self.psu)}\n"
            f"{str(self.cooling)}\n"
            f"{str(self.case)}\n"
            f"Total Price: ${self.price:.2f}\n"
            f"Estimated Performance:\n"
            f"  Gaming: {self.estimated_performance.get('gaming', 0):.1f}/100\n"
            f"  Productivity: {self.estimated_performance.get('productivity', 0):.1f}/100\n"
            f"  Content Creation: {self.estimated_performance.get('content_creation', 0):.1f}/100\n"
            f"  Development: {self.estimated_performance.get('development', 0):.1f}/100"
        )

    def __deepcopy__(self, memo):
        new_computer = Computer(
            deepcopy(self.cpu),
            deepcopy(self.gpu),
            deepcopy(self.ram),
            deepcopy(self.storage),
            deepcopy(self.motherboard),
            deepcopy(self.psu),
            deepcopy(self.cooling),
            deepcopy(self.case),
            self.fitness,
            [deepcopy(storage) for storage in self.additional_storages],
            deepcopy(self.estimated_performance)
        )
        return new_computer

    def is_psu_capacity_enough(self) -> bool:
        """Check if PSU capacity is sufficient but not excessive"""
        # Calculate total power consumption
        power_needed = (
            self.cpu.power_consumption 
            + (self.gpu.power_consumption if self.gpu else 0) 
            + self.motherboard.power_consumption 
            + 50  # Base for RAM, storage, etc.
        )
        
        # Check if PSU capacity is sufficient but not excessive
        return (power_needed < self.psu.capacity) and (
            self.psu.capacity - power_needed <= self.psu.capacity * 0.4  # Allow up to 40% headroom
        )
        
    def is_bottleneck(self) -> bool:
        """Check for performance bottlenecks between CPU and GPU"""
        if self.gpu is None:
            # No bottleneck if no GPU (using integrated graphics)
            return True
        
        # Calculate difference between CPU and GPU performance
        bottleneck = abs(self.cpu.performance - self.gpu.power)
        
        # Consider balanced if difference is less than 20
        return bottleneck <= 20
    
    def points_for_relation_quality_cpu(self) -> float:
        """Calculate points for CPU price-to-performance ratio"""
        if self.cpu.price <= 0:
            return 0
        relation = (self.cpu.performance / self.cpu.price) * 100
        return min(10, relation)  # Cap at 10 points
    
    def points_for_relation_quality_gpu(self) -> float:
        """Calculate points for GPU price-to-performance ratio"""
        if self.gpu is None:
            return 0  # No GPU means no points
        
        if self.gpu.price <= 0:
            return 0
            
        relation = (self.gpu.power / self.gpu.price) * 650
        return min(10, relation)  # Cap at 10 points
    
    def calculate_cooling_adequacy(self) -> float:
        """Calculate how adequate the cooling solution is for the CPU"""
        if self.cooling.cooling_capacity <= 0 or self.cpu.power_consumption <= 0:
            return 0
            
        # Calculate ratio of cooling capacity to CPU TDP
        ratio = self.cooling.cooling_capacity / self.cpu.power_consumption
        
        if ratio < 1.0:
            return 0  # Inadequate cooling
        elif ratio > 2.0:
            return 0.7  # Excessive cooling (wastes money)
        else:
            # Optimal range is between 1.0 and 2.0
            return 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Computer to dictionary for serialization"""
        return {
            "cpu": self.cpu.to_dict(),
            "gpu": self.gpu.to_dict() if self.gpu else None,
            "ram": self.ram.to_dict(),
            "storage": self.storage.to_dict(),
            "motherboard": self.motherboard.to_dict(),
            "psu": self.psu.to_dict(),
            "cooling": self.cooling.to_dict(),
            "case": self.case.to_dict(),
            "additional_storages": [storage.to_dict() for storage in self.additional_storages],
            "price": self.price,
            "fitness": self.fitness,
            "estimated_performance": self.estimated_performance
        }


class UserPreferences:
    """Enhanced UserPreferences model with more detailed options"""
    def __init__(
        self, 
        min_price: int, 
        max_price: int, 
        usage: str,
        priority: str = "performance",  # performance, value, or balance
        brand_preferences: Dict[str, List[str]] = None,  # Preferred brands for each component
        form_factor: str = "ATX",       # Preferred form factor
        aesthetic: Dict[str, Any] = None,  # Aesthetic preferences
        must_include: Dict[str, Any] = None,  # Components that must be included
        must_exclude: Dict[str, Any] = None,  # Components that must be excluded
        future_proof: bool = False      # Prioritize future-proofing
    ) -> None:
        self.min_price: int = min_price
        self.max_price: int = max_price
        self.usage: str = usage
        self.priority: str = priority
        self.brand_preferences: Dict[str, List[str]] = brand_preferences or {}
        self.form_factor: str = form_factor
        self.aesthetic: Dict[str, Any] = aesthetic or {"rgb": False, "color": "black"}
        self.must_include: Dict[str, Any] = must_include or {}
        self.must_exclude: Dict[str, Any] = must_exclude or {}
        self.future_proof: bool = future_proof

    def __str__(self) -> str:
        return (
            f"User Preferences:\n"
            f"  Price Range: ${self.min_price} - ${self.max_price}\n"
            f"  Primary Usage: {self.usage}\n"
            f"  Priority: {self.priority}\n"
            f"  Form Factor: {self.form_factor}\n"
            f"  Future-proof: {'Yes' if self.future_proof else 'No'}"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert UserPreferences to dictionary for serialization"""
        return {
            "min_price": self.min_price,
            "max_price": self.max_price,
            "usage": self.usage,
            "priority": self.priority,
            "brand_preferences": self.brand_preferences,
            "form_factor": self.form_factor,
            "aesthetic": self.aesthetic,
            "must_include": self.must_include,
            "must_exclude": self.must_exclude,
            "future_proof": self.future_proof
        }