# A spacecraft

from finkchlib.vector import radial_to_cartesian2, Vector2
from finkchlib.constants import vacuum_H_mass_density
from spacetime import Spacetime
import numpy as np

# A ramjet is our basic spacecraft.
# This class will act like an interface for our proper crafts
class Ramjet:
    def __init__(self, name: str, mass: float, fuel_capacity: float, battery_capacity: float, thrust: float, v_e: float, engine_power: float, scoop_power: float, scoop_radius: float, power: float) -> None:
        
        self.name: str = name
        self.spacetime: Spacetime = Spacetime()

        self.mass: float = 0
        self.core_mass: float = mass

        # Fuel storage of this craft
        self.tank: Tank = Tank('tank', fuel_capacity)
        self.battery: Tank = Tank('battery', battery_capacity)

        # Ramjet components
        self.thruster = Thruster('thruster', thrust, v_e, engine_power)
        self.scooper = Scoop('scoop', scoop_power, scoop_radius, 1)
        self.generator = Generator('generator', power)

        self.update_mass()

    def __str__(self) -> str:
        return f'{self.name}, {self.mass} kg\n\
            fuel:\t{self.tank} kg\n\
            battery:\t{self.battery} J\n\
            pos:\t{self.spacetime.position} m\n\
            vel:\t{self.spacetime.velocity} m/s\n\
            acc:\t{self.spacetime.acceleration_preview} m/s^2'

    # One step of simulation for the craft
    def __call__(self, step):

        # Generates power
        self.generator(self, step)

        # Scoops up hydrogen
        self.scooper(self, step)

        # Creates thrust
        thrust = self.thruster(self, step)
        
        # Updates mass
        self.update_mass()

        # Applies thrust
        self.spacetime.force(self.mass, thrust)

        # Steps the craft forward
        self.spacetime(step)

    # Craft mass is craft of the parts plus fuel in tank
    def update_mass(self) -> None:
        self.mass = self.core_mass + self.tank.fuel

    # Applies a force to the craft
    def force(self, amount) -> None:
        self.spacetime.force(self.mass, amount)
    
    # Refunds when one throttle is lower than the other
    def refund(self, fuel: float, fuel_throttle: float, power: float, power_throttle: float) -> tuple[float, float]:
        if fuel_throttle < power_throttle:
            return fuel, self.refund_individual(power, power_throttle, self.battery, fuel_throttle)
        elif power_throttle < fuel_throttle:
            return self.refund_individual(fuel, fuel_throttle, self.tank, power_throttle), power

        return fuel, power
    
    # Refunds an individual tank
    def refund_individual(self, fuel: float, fuel_throttle: float, tank, limiting_throttle: float) -> float:
        fuel_effective = fuel * limiting_throttle / fuel_throttle
        tank.pipe_in(fuel - fuel_effective)
        return fuel_effective
    
    def get_previews(self):
        return {
            self.tank.name:         self.tank.get_preview(),
            self.battery.name:      self.battery.get_preview(),
            self.thruster.name:     self.thruster.get_preview(),
            self.scooper.name:      self.scooper.get_preview(),
            self.generator.name:    self.generator.get_preview()
        }



# A Part is any component of a spacecraft
class Part:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.preview = {}

    def get_preview(self):
        return self.preview

# A Tank holds fuel or battery charge
class Tank(Part):
    def __init__(self, name: str, capacity: float) -> None:
        super().__init__(name)
        
        self.capacity: float = capacity
        self.fuel: float = self.capacity
    
    def __str__(self):
        return f'{self.name}: {self.fuel:.2e} / {self.capacity:.2e} kg'

    # Pipes fuel into the tank
    def pipe_in(self, amount: float) -> float:
        
        # Performs a safety check
        assert amount >= 0, f'Cannot pipe-in negative quantities ({amount})'
        
        # Adds fuel to the tank
        self.fuel += amount

        # Excess fuel is returned
        if self.fuel > self.capacity:
            overflow: float = self.fuel - self.capacity
            self.fuel = self.capacity
            return overflow
        
        return 0

    # Pipes fuel out of the tank
    # Second item returned is the throttle, a ratio of supply to request
    def pipe_out(self, amount: float) -> tuple[float, float]:
        
        # Performs a safety check
        assert amount >= 0, f'Cannot pipe-out negative quantities ({amount})'

        # If the request cannot be fulfilled
        if amount > self.fuel:
            outflow = self.fuel # Outputs all remaining fuel
            self.fuel = 0
            return outflow, outflow / amount
        
        # If the request can be fulfilled
        else:
            self.fuel -= amount
            return amount, 1
    
    # Checks if the tank is empty
    def is_empty(self) -> bool:
        return self.fuel == 0
    
    def get_preview(self):
        return {
            'fuel': self.fuel,
            'capacity': self.capacity
        }



# A Thruster provides thrust
class Thruster(Part):
    def __init__(self, name: str, thrust: float, v_e: float, power: float) -> None:
        super().__init__(name)

        # Maximum thrust this engine can provide
        self.thrust: float = thrust

        # Exhaust velocity
        self.v_e: float = v_e

        # Mass flow rate
        self.m_d: float = self.thrust / self.v_e

        # Power consumed by the thruster
        self.power: float = power

    # Call a Thruster converts fuel and power to thrust; it fires the engines
    def __call__(self, ramjet: Ramjet, step: float) -> Vector2:
        
        # If the tank is emtpy, return a 0 vector
        if ramjet.tank.is_empty():
            return Vector2(0, 0)

        # Obtains some fuel and power
        fuel, fuel_throttle = ramjet.tank.pipe_out(self.m_d * step)
        power, power_throttle = ramjet.battery.pipe_out(self.power * step)

        # Safety check
        assert fuel_throttle >= 0 and fuel_throttle <= 1, f'Fuel throttle is not within range ({fuel_throttle})'
        assert power_throttle >= 0 and power_throttle <= 1, f'Fuel throttle is not within range ({power_throttle})'

        # Refunds spare fuel when throttles don't match.
        # If the throttles match, these values don't change
        fuel, power = ramjet.refund(fuel, fuel_throttle, power, power_throttle)

        # The thrust generated
        thrust = fuel * self.v_e

        # Updates the part's preview
        self.preview = {
            'thrust': thrust,
            'fuel': fuel,
            'fuel_throttle': fuel_throttle,
            'power': power,
            'power_throttle': power_throttle
            }

        # Converts the thrust to a vector oriented backwards from the craft
        return radial_to_cartesian2(thrust, ramjet.spacetime.position.phi())



# A Scoop provides fuel
class Scoop(Part):
    def __init__(self, name: str, power: float, max_radius: float, efficiency: float) -> None:
        super().__init__(name)
        self.power = power
        self.radius = max_radius

        self.efficiency = efficiency # Scalar E [0, 1]

    # Calling a Scoop scoops up H from the ISM
    def __call__(self, ramjet: Ramjet, step: float) -> float:
        
        # Allignment of scoop to ISM
        # Cannot be negative; negative corresponds to the craft facing backwards
        allignment = max(ramjet.spacetime.position.normal() ^ ramjet.spacetime.velocity.normal(), 0)
        if allignment != allignment: # Check for nan
            allignment = 0

        # Power available to the scoop
        power, throttle = ramjet.battery.pipe_out(self.power)

        # Area of scoop
        area = np.pi * (self.radius * throttle) ** 2

        # Effective volume swept
        V_eff = area * allignment * ramjet.spacetime.velocity.hypo() * step

        # Mass of hydrogen scooped up
        m_H = self.efficiency * V_eff * vacuum_H_mass_density

        # Adds the mass scooped up to the tank
        ramjet.tank.pipe_in(m_H)

        # Updates the part's preview
        self.preview = {
            'm_H': m_H,
            'power': power,
            'power_throttle': throttle,
            'allignment': allignment,
            'area': area,
            'volume': V_eff
        }



# A Generator provides power
class Generator(Part):
    def __init__(self, name, power) -> None:
        super().__init__(name)
        self.power = power

    # Calling a Generator provides power to the battery
    def __call__(self, ramjet: Ramjet, step: float) -> float:
        ramjet.battery.pipe_in(self.power * step)
        
        # Updates the part's preview
        self.preview = {
            'power': self.power
        }