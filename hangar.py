# Used to store Ramjets

from finkchlib.vector import Vector2
from ramjet import Ramjet

# Calling this function returns a Ramjet
def get_ramjet(name: str) -> Ramjet:
    
    # Ramjet {
    #   name:               str
    #   mass:               float
    #   fuel_capacity:      float
    #   battery_capacity:   float
    #   thrust:             float
    #   v_e:                float
    #   engine_power:       float
    #   scoop_power:        float
    #   scoop_radius:       float
    #   power:              float
    # }
    ramjet = None
    
    # Selects the Ramjet
    match name:

        # The classic test
        case 'ioRam-Beta':
            
            # Update thrust:
            # X_e   = 131.293 u
            # H     = 1.00784 u
            ramjet: Ramjet = Ramjet(name, 100, 10, 1e7, 26, 4.9e4, 1.5e6, 1e6, 1e2, 1e8)

        
        # A repurposed Dawn spacecraft
        case 'Dawn':

            RTG_mass = 57
            RTG_power = 300
            RTG_count = 10

            engine_power = 2.3e3

            scoop_power = RTG_power * RTG_count - engine_power
            scoop_radius = (scoop_power / 10) ** (1 / 2)

            # GPHS-RTG
            #   mass:   55.9-57.8   kg
            #   power:  300         W
            #
            # Let's include 10!

            # Dry mass of 747.1 kg, including solar panels
            # Each dawn solar panel is 63 kg; replacing them with RTGs
            ramjet: Ramjet = Ramjet(name, 621.1 + RTG_mass * RTG_count, 470.6, 4233600, 0.092, 30500, engine_power, scoop_power, scoop_radius, RTG_power * RTG_count)
            

        # Crashes if supplied name does not match any entries
        case _:
            assert False, f'No such ramjet \'{name}\'.'


    # Offsets from centre to prevent double div-by-zero
    ramjet.spacetime.position = Vector2(1, 0)

    # Returns the Ramjet
    return ramjet
