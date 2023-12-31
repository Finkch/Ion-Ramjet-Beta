# A spacecraft

from finkchlib.actor import Actor2
import numpy as np

# A ramjet is our basic spacecraft.
# This class will act like an interface for our proper crafts
class Ramjet(Actor2):
    def __init__(self, name, mass, radius, step, fuel, battery, thrust, v_e, engine_power, scoop_r, scoop_p, power) -> None:
        super().__init__(name, mass, radius)
        
        self.step = step

        # Amount that can be stored on the craft
        self.tank = Tank(self.step, fuel)
        self.battery = Tank(self.step, battery)

        # Thrust parameters
        self.thrust = thrust
        self.v_e = v_e
        self.m_d = self.thrust / self.v_e
        self.engine_power = engine_power

        # Scoop parameters
        self.scoop_r = scoop_r
        self.scoop_p = scoop_p

        # Reactor parameters
        self.power = power

    # Does one step of simulation
    def __call__(self) -> None:
        super().__call__(self.step)



    # Fires the engine, producing thrust
    def fire(self) -> float:
    
        reaction_mass, mass_throttle = self.tank.pipe_out(self.m_d)
        reaction_power, power_throttle = self.battery.pipe_out(self.engine_power)
        
        # If one source doesn't produce enough, then refund the other source
        mass_refund = 0
        power_refund = 0

        self.tank.pipe_in(mass_refund)
        self.battery.pipe_in(power_refund)

        return reaction_mass * self.v_e 



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

        # NOT UP TO DATE
        # Still needs to account for velocity and area
        return np.pi * (self.scoop_r * power_throttle) ** 2


    # Generates power, adding it to the battery
    def generate(self) -> None:
        self.battery.pipe_in(self.power * self.step)




# A tank holds fuel or electricity
class Tank:
    def __init__(self, step, max_fuel) -> None:
        
        self.step = step
        
        self.max_fuel = max_fuel
        self.fuel = self.max_fuel


    # Move fuel into or out of this tank
    def pipe_in(self, fuel) -> None:

        # Adds fuel
        # Fuel cannot go above max capacity; excess is 'jettisoned overvoard'
        self.fuel = min(self.fuel + fuel, self.max_fuel)

    def pipe_out(self, fuel) -> float:
        
        # Pipes out fuel
        if fuel > self.fuel: # Limits fuel output if there isn't enough
            self.fuel = 0
            return self.fuel, 1
        else:
            throttle = self.fuel / fuel
            self.fuel -= fuel
            return fuel, throttle