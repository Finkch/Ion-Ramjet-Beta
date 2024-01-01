# A spacecraft

from finkchlib.vector import radial_to_cartesian2, Vector2
from finkchlib.constants import vacuum_H_mass_density
import numpy as np

# A ramjet is our basic spacecraft.
# This class will act like an interface for our proper crafts
class Ramjet:
    def __init__(self, name: str, mass: float, step: int, fuel_capacity: float, battery_capacity: float, thrust: float, v_e: float, engine_power: float, scoop_power: float, scoop_radius: float, power: float) -> None:
        
        self.name: str = name
        self.step = step
        self.spacetime: Spacetime = Spacetime(step)

        self.mass = 0
        self.core_mass: float = mass

        # Fuel storage of this craft
        self.tank = Tank('tank', fuel_capacity)
        self.battery = Tank('battery', battery_capacity)

        # Thruster parameters
        self.thrust = thrust
        self.v_e = v_e
        self.m_d = self.thrust / self.v_e
        self.engine_power = engine_power

        # Scoop parameters
        self.scoop_power = scoop_power
        self.scoop_radius = scoop_radius

        # Generator parameters
        self.power = power

        # Used to preview force
        self.thrust_preview = Vector2()

        self.update_mass()

    def __str__(self) -> str:
        return f'{self.name}, {self.mass} kg, {self.spacetime.time:.2e} s\n\
            fuel:\t{self.tank} kg\n\
            battery:\t{self.battery} J\n\
            pos:\t{self.spacetime.position} m\n\
            vel:\t{self.spacetime.velocity} m/s\n\
            acc:\t{self.spacetime.acceleration_preview} m/s^2\n\
            thr:\t{self.thrust_preview} N'

    # One step of simulation for the craft
    def __call__(self):

        # Resets force preview
        self.thrust_preview = Vector2()

        # Generates power
        self.generate()

        # Scoops up hydrogen
        self.scoop()

        # Creates thrust
        thrust = self.fire()
        
        # Updates mass
        self.update_mass()

        # Applies thrust
        self.force(thrust)

        # Steps the craft forward
        self.spacetime()

    # Craft mass is craft of the parts plus fuel in tank
    def update_mass(self) -> None:
        self.mass = self.core_mass + self.tank.fuel

    # Applies a force to the craft
    def force(self, amount: Vector2) -> None:
        self.spacetime.acceleration += amount / self.mass
        self.thrust_preview += amount / self.mass

    # Fires the engine
    def fire(self) -> Vector2:
        
        # If the tank is emtpy, return a 0 vector
        if self.tank.is_empty():
            return Vector2(0, 0)

        # Obtains some fuel and power
        fuel, fuel_throttle = self.tank.pipe_out(self.m_d * self.step)
        power, power_throttle = self.battery.pipe_out(self.engine_power * self.step)

        # Safety check
        assert fuel_throttle >= 0 and fuel_throttle <= 1, f'Fuel throttle is not within range ({fuel_throttle})'
        assert power_throttle >= 0 and power_throttle <= 1, f'Fuel throttle is not within range ({power_throttle})'

        # Refunds spare fuel when throttles don't match.
        # If the throttles match, these values don't change
        fuel, power = self.refund(fuel, fuel_throttle, power, power_throttle)

        # The thrust generated
        thrust = fuel * self.v_e

        # Converts the thrust to a vector oriented backwards from the craft
        return radial_to_cartesian2(thrust, self.spacetime.position.phi())
    
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


    # Scoops up hydrogen from the ISM
    def scoop(self) -> None:
        
        # Allignment of scoop to ISM
        # Cannot be negative; negative corresponds to the craft facing backwards
        allignment = max(self.spacetime.position.normal() ^ self.spacetime.velocity.normal(), 0)
        if allignment != allignment: # Check for nan
            allignment = 0

        # Power available to the scoop
        power, throttle = self.battery.pipe_out(self.scoop_power)

        # Area of scoop
        area = np.pi * (self.scoop_radius * throttle) ** 2

        # Effective volume swept
        V_eff = area * allignment * self.spacetime.velocity.hypo() * self.step

        # Efficiency of the scoop
        # The percent of hydrogen the scoop fails to pick up
        efficiency = 1

        # Mass of hydrogen scooped up
        m_H = efficiency * V_eff * vacuum_H_mass_density

        # Adds the mass scooped up to the tank
        self.tank.pipe_in(m_H)


    # Generates power
    def generate(self) -> None:
        self.battery.pipe_in(self.power)



# A Tank holds fuel or battery charge
class Tank:
    def __init__(self, name: str, capacity: float) -> None:
        self.name: str = name
        
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


# Oversees the space and time of a thing
class Spacetime:
    def __init__(self, step, position: Vector2 = Vector2(), velocity: Vector2 = Vector2(), acceleration: Vector2 = Vector2()) -> None:
        self.time: float = 0
        self.steps: float = 0
        self.step: int = step

        self.position: Vector2 = position
        self.velocity: Vector2 = velocity
        self.acceleration: Vector2 = acceleration

        self.acceleration_preview: Vector2 = Vector2()
    
    # Updates the space and time
    def __call__(self):

        # Increments time
        self.time += self.step
        self.steps += 1

        # Updates postion and velocity
        self.velocity += self.acceleration * self.step
        self.position += self.velocity * self.step

        # Resets acceleration
        self.acceleration_preview: Vector2 = self.acceleration
        self.acceleration: Vector2 = Vector2()