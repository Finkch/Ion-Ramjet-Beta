from finkchlib.vector import Vector2
from finkchlib.constants import c

# Oversees the space and time of a thing.
# From an observer aboard the craft
class Spacetime:
    def __init__(self, position: Vector2 = Vector2(), velocity: Vector2 = Vector2(), acceleration: Vector2 = Vector2()) -> None:
        self.time = 0

        self.position: Vector2 = position
        self.velocity: Vector2 = velocity
        self.acceleration: Vector2 = acceleration

        self.acceleration_preview: Vector2 = Vector2()
    
    # Updates the space and time
    def __call__(self, step: float) -> None:

        # Increases the amount of time experienced
        self.time += step

        # Updates postion and velocity
        self.velocity += self.acceleration * step
        self.position += self.velocity * step

        # Resets acceleration
        self.acceleration_preview: Vector2 = self.acceleration
        self.acceleration: Vector2 = Vector2()

    # Applies a force to the craft
    def force(self, mass, amount: Vector2) -> None:
        self.acceleration += amount / mass

    def get_preview(self):
        return {
            'time': self.time,
            'pos_x': self.position.x,
            'pos_y': self.position.y,
            'vel_x': self.velocity.x,
            'vel_y': self.velocity.y,
            'acc_x': self.acceleration_preview.x,
            'acc_y': self.acceleration_preview.y
        }


# A spacetime that incorporates special relativity.
# Same as spacetime, but from an observer on the ground
class RelativisticSpacetime(Spacetime):
    def __init__(self, position: Vector2 = Vector2(), velocity: Vector2 = Vector2(), acceleration: Vector2 = Vector2()) -> None:
        super().__init__(position, velocity, acceleration)

    def __call__(self, step: float) -> None:
        gamma = self.gamma(self.velocity)

        # Increases time experienced
        step_size = step / gamma
        
        # Steps forward in time'
        super().__call__(step_size)


    # Returns some useful factors
    def gamma(self, velocity: Vector2) -> float:
        return 1 / (1 - self.beta(velocity) ** 2)
    
    def beta(self, velocity: Vector2) -> float:
        return velocity.hypo() / c
