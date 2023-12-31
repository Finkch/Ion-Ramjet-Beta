# A spacecraft

from finkchlib.actor import Actor2
#from finkchlib.vector
import numpy as np

# A ramjet is our basic spacecraft.
# This class will act like an interface for our proper crafts
class Ramjet(Actor2):
    def __init__(self, name: str, mass: float, radius: float, step: float, fuel: float, battery: float, thrust: float, v_e: float, engine_power: float, scoop_r: float, scoop_p: float, power: float) -> None:
        super().__init__(name, mass, radius)
        
        self.step: int = step

        # Amount that can be stored on the craft
        self.tank: Tank = Tank(self.step, fuel)
        self.battery: Tank = Tank(self.step, battery)

        # Thrust parameters
        self.thrust: float = thrust
        self.v_e: float = v_e
        self.m_d: float = self.thrust / self.v_e
        self.engine_power: float = engine_power

        # Scoop parameters
        self.scoop_r: float = scoop_r
        self.scoop_p: float = scoop_p

        # Reactor parameters
        self.power: float = power

    # Does one step of simulation
    def __call__(self) -> None:

        # Generates power
        self.generate()

        # Scoops hydrogen
        self.scoop()

        # Fires engines
        self.force(self.fire())

        # Updates position and velocty
        super().__call__(self.step)

    def __str__(self) -> str:
        f'{self.name}, {self.spacetime.time:.2e}\n\
            fuel:\t{self.tank.fuel:.2e} kg, battery:\t{self.battery.fuel:.2e}\n\
            pos:\t{self.pos()} m\n\
            vel:\t{self.vel()} m/s\n\
            acc:\t{self.acc()} m/s^2'



    # Fires the engine, producing thrust
    def fire(self) -> float:
    
        # Requests fuel and power
        reaction_mass, mass_throttle = self.tank.pipe_out(self.m_d * self.step)
        reaction_power, power_throttle = self.battery.pipe_out(self.engine_power * self.step)

        # Refunds fuel and power if one is less than the other
        reaction_mass, reaction_power = self.refund(reaction_mass, mass_throttle, reaction_power, power_throttle)
        
        # Produces thrust
        return reaction_mass * self.v_e 
    

    # If one source doesn't produce enough, then refund the other source
    def refund(self, fuel: float, fuel_throttle: float, power: float, power_throttle: float):
        
        # Refunds power if there is less fuel
        if fuel_throttle < power_throttle:

            power_refund = power * (1 - fuel_throttle / power_throttle)
            power = power * fuel_throttle / power_throttle

            self.battery.pipe_in(power_refund)

        # Refunds fuel if there is less power
        elif power_throttle < fuel_throttle:
            
            fuel_refund = fuel * (1 - power_throttle / fuel_throttle)
            fuel = fuel * power_throttle / fuel_throttle

            self.tank.pipe_in(fuel_refund)
        
        # Returns the amount of fuel and power
        return fuel, power


    # Scoops up hydrogen from the ISM
    def scoop(self) -> None:
        
        # Mass of hydrogen swept
        hydrogen = self.sweep_hydrogen()

        # Adds hydrogen to the tank
        self.tank.pipe_in(hydrogen * self.step)

    # Returns the mass of hydrogen scooped up 
    def sweep_hydrogen(self):
        
        # Gets the ratio of requested power
        power_throttle = self.battery.pipe_out(self.scoop_p)[1]

        return np.pi * (self.scoop_r * power_throttle) ** 2 * self.pos().normal() ^ self.vel()


    # Generates power, adding it to the battery
    def generate(self) -> None:
        self.battery.pipe_in(self.power * self.step)




# A tank holds fuel or electricity
class Tank:
    def __init__(self, step: int, max_fuel: float) -> None:
        
        self.step: int = step
        
        self.max_fuel: float = max_fuel
        self.fuel: float = self.max_fuel


    # Move fuel into or out of this tank
    def pipe_in(self, fuel: float) -> None:

        # Adds fuel
        # Fuel cannot go above max capacity; excess is 'jettisoned overvoard'
        self.fuel = min(self.fuel + fuel, self.max_fuel)

    def pipe_out(self, fuel: float) -> float:
        
        # Pipes out fuel
        if fuel > self.fuel: # Limits fuel output if there isn't enough
            self.fuel = 0
            return self.fuel, 1
        else:
            throttle = self.fuel / fuel
            self.fuel -= fuel
            return fuel, throttle