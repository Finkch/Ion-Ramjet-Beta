# A spacecraft

# A ramjet is our basic spacecraft.
# This class will act like an interface for our proper crafts
class Ramjet:
    def __init__(self, step, fuel, battery, thrust, v_e, scoop_r, scoop_p, power) -> None:
        
        self.step = step

        # Amount that can be stored on the craft
        self.tank = Tank(self.step, fuel)
        self.battery = Tank(self.step, fuel)

        # Thrust parameters
        self.thrust = thrust
        self.v_e = v_e

        # Scoop parameters
        self.scoop_r = scoop_r
        self.scoop_p = scoop_p

        # Reactor parameters
        self.power = power

    def __call__(self) -> None:
        pass

    def fire(self) -> float:
        pass

    def scoop(self) -> None:
        pass

    def power(self) -> None:
        pass




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
            return self.fuel
        else:
            self.fuel -= fuel
            return fuel